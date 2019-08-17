import sys
if (sys.version_info < (3, 0)):
    import s_module_template
    import s_sample_mapping_exceptions
else:
    from . import s_module_template
    from . import s_sample_mapping_exceptions

from enum import Enum


import random
import pandas as pd

class DifferentRunMergeMode(Enum):
    DROP_EXPERIMENT = "drop"
    RANDOM_RUN      = "random"
    SPECIFIED_RUN   = "specified"
    AVERAGE         = "average"


class SequencingSampleMappingParameters:
    def __init__(   self, owner, 
                    different_run_merge_mode = DifferentRunMergeMode.AVERAGE.value,
                    specified_mapping_experiment_runs = None):
        self.owner = owner
        self.different_run_merge_mode = different_run_merge_mode
        self.specified_mapping_experiment_runs = specified_mapping_experiment_runs

class SequencingSampleMappingResults:
    def __init__(self):
        self.merged_count_reads_result = {}
        self.mapping_experiment_runs_after_merge = {}
        self.count_reads_matrix = None
        self.done = False
        self.exception = None
        
    def update_mapping_experiment_runs_after_merge(self, exp, runs):
        self.mapping_experiment_runs_after_merge[exp] = runs
        
    def update_merged_count_reads_result(self, exp, merged_count_reads_result):
        self.merged_count_reads_result[exp] = merged_count_reads_result
        
    def update_count_reads_matrix(self, count_reads_matrix):
        self.count_reads_matrix = count_reads_matrix
        
        
class SequencingSampleMapping(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results() #Get Mapping Results
        self.s_value_extraction_results = owner.get_s_value_extraction_results() #Get Read Counts Results
        self.parameters = SequencingSampleMappingParameters(self)
        self.results = SequencingSampleMappingResults()
        
        self.workers = {}
        
    def prepare_workers(self, count_reads_result_2D = None):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            if count_reads_result_2D == None:
                self.workers[exp] = self.prepare_worker(exp)
            else:
                self.workers[exp] = self.prepare_worker(exp, count_reads_result_2D[exp])
            
    def prepare_worker(self, exp, count_reads_result = None):
        different_run_merge_mode = self.parameters.different_run_merge_mode
        mapping_experiment_runs = self.s_retrieval_results.mapping_experiment_runs
        if count_reads_result == None:
            count_reads_result = self.s_value_extraction_results.count_reads_result
        specified_mapping_experiment_runs = self.parameters.specified_mapping_experiment_runs
        worker = SequencingSampleMappingWorker(exp, different_run_merge_mode, mapping_experiment_runs, count_reads_result, 
                                        specified_mapping_experiment_runs)
        
        return worker
    
    def merge_different_run(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            worker[exp].run()
                
    def merge_sample(self):
        count_reads_results_exps = []
        exps = []
        for exp in self.results.mapping_experiment_runs_after_merge:
            exps.append(exp)
            count_reads_results_exps.append(self.results.merged_count_reads_result[exp])
            
        count_reads_matrix = pd.concat(count_reads_results_exps, axis = 1)
        count_reads_matrix.columns = exps
        
        self.results.update_count_reads_matrix(count_reads_matrix)
        
    def get_results(self):
        return self.results
        
    def get_parameters(self):
        return self.parameters
        

class SequencingSampleMappingWorker:
    def __init__(self, exp, different_run_merge_mode, mapping_experiment_runs, count_reads_result,
                    specified_mapping_experiment_runs = None):
        self.exp = exp
        self.different_run_merge_mode = different_run_merge_mode
        self.mapping_experiment_runs = mapping_experiment_runs
        self.count_reads_result = count_reads_result
        self.specified_mapping_experiment_runs = specified_mapping_experiment_runs
        
        self.results = SequencingSampleMappingResults()
        
    def do_run(self):
        self.merge_different_run_exp()
        
    def merge_different_run_exp(self):
        if self.different_run_merge_mode == DifferentRunMergeMode.DROP_EXPERIMENT.value:
            self.merge_different_run_drop_experiment_exp()
        elif self.different_run_merge_mode == DifferentRunMergeMode.RANDOM_RUN.value:
            self.merge_different_run_random_run_exp()
        elif self.different_run_merge_mode == DifferentRunMergeMode.SPECIFIED_RUN.value:
            self.merge_different_run_specified_run_exp()
        elif self.different_run_merge_mode == DifferentRunMergeMode.AVERAGE.value:
            self.merge_different_run_average_exp()
        else:
            raise s_sample_mapping_exceptions.InvalidDifferentRunMergeMode('Invalid different run merge mode!')
            
    def merge_different_run_drop_experiment_exp(self):
        if len(self.mapping_experiment_runs[self.exp]) > 1:
            return
        else:
            run = self.mapping_experiment_runs[self.exp][0]
            merged_count_reads_result = self.count_reads_result[run]
            merged_count_reads_result.columns = [self.exp]
            self.results.update_mapping_experiment_runs_after_merge(self.exp, [run])
            self.results.update_merged_count_reads_result(self.exp, merged_count_reads_result)
                
    def merge_different_run_random_run_exp(self):
        run = random.choice(self.mapping_experiment_runs[self.exp])
        merged_count_reads_result = self.count_reads_result[run]
        merged_count_reads_result.columns = [self.exp]
        self.results.update_mapping_experiment_runs_after_merge(self.exp, [run])
        self.results.update_merged_count_reads_result(self.exp, merged_count_reads_result)
            
    def merge_different_run_specified_run_exp(self):
        try:
            run = self.specified_mapping_experiment_runs[self.exp]
        except Exception as e:
            raise s_sample_mapping_exceptions.InvalidSpecifiedExperimentMapping('Invalid specified run')
            
        merged_count_reads_result = self.count_reads_result[run]
        merged_count_reads_result.columns = [self.exp]
        self.results.update_mapping_experiment_runs_after_merge(self.exp, [run])
        self.results.update_merged_count_reads_result(self.exp, merged_count_reads_result)
            
    def merge_different_run_average_exp(self):
        if len(self.mapping_experiment_runs[self.exp]) == 1:
            run = self.mapping_experiment_runs[self.exp][0]
            merged_count_reads_result = self.count_reads_result[run]
            
            self.results.update_mapping_experiment_runs_after_merge(self.exp, [run])
            self.results.update_merged_count_reads_result(self.exp, merged_count_reads_result)
        else:
            count_reads_results_exp = []
            for run in self.mapping_experiment_runs[self.exp]:
                count_reads_results_exp.append(self.count_reads_result[run])
            
            concat_count_reads_results_exp = pd.concat(count_reads_results_exp, axis = 1)
            mean_concat_count_reads_results_exp = concat_count_reads_results_exp.mean(axis = 0)
            mean_concat_count_reads_results_exp.columns = [self.exp]
            
            self.results.update_mapping_experiment_runs_after_merge(self.exp, self.mapping_experiment_runs[self.exp])
            self.results.update_merged_count_reads_result(self.exp, merged_count_reads_result)
    
            print(merged_count_reads_result)