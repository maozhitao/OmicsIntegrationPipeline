from . import s_module_template
from enum import Enum, auto

from . import s_sample_mapping_exceptions
import random
import pandas as pd

class DifferentRunMergeMode(Enum):
    DROP_EXPERIMENT = auto()
    RANDOM_RUN      = auto()
    SPECIFIED_RUN   = auto()
    AVERAGE         = auto()


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
        
    def update_mapping_experiment_runs_after_merge(self, exp, runs):
        self.mapping_experiment_runs_after_merge[exp] = runs
        
    def update_merged_count_reads_result(self, exp, merged_count_reads_result):
        self.merged_count_reads_result[exp] = merged_count_reads_result
        
    def update_count_reads_matrix(self, count_reads_matrix):
        self.count_reads_matrix = count_reads_matrix
        print(self.count_reads_matrix)
        
        
class SequencingSampleMapping(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results() #Get Mapping Results
        self.s_value_extraction_results = owner.get_s_value_extraction_results() #Get Read Counts Results
        self.parameters = SequencingSampleMappingParameters(self)
        self.results = SequencingSampleMappingResults()
        
    
    def merge_different_run(self):
        if self.parameters.different_run_merge_mode == DifferentRunMergeMode.DROP_EXPERIMENT.value:
            self.merge_different_run_drop_experiment()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.RANDOM_RUN.value:
            self.merge_different_run_random_run()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.SPECIFIED_RUN.value:
            self.merge_different_run_specified_run()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.AVERAGE.value:
            self.merge_different_run_average()
        else:
            raise s_sample_mapping_exceptions.InvalidDifferentRunMergeMode('Invalid different run merge mode!')
            
    def merge_different_run_drop_experiment(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            if len(self.s_retrieval_results.mapping_experiment_runs[exp]) > 1:
                continue
            else:
                run = self.s_retrieval_results.mapping_experiment_runs[exp][0]
                merged_count_reads_result = self.s_value_extraction_results.count_reads_result[run]
                merged_count_reads_result.columns = [exp]
                self.results.update_mapping_experiment_runs_after_merge(exp, [run])
                self.results.update_merged_count_reads_result(exp, merged_count_reads_result)
                
    def merge_different_run_random_run(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            run = random.choice(self.s_retrieval_results.mapping_experiment_runs[exp])
            merged_count_reads_result = self.s_value_extraction_results.count_reads_result[run]
            merged_count_reads_result.columns = [exp]
            self.results.update_mapping_experiment_runs_after_merge(exp, [run])
            self.results.update_merged_count_reads_result(exp, merged_count_reads_result)
            
    def merge_different_run_specified_run(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            try:
                run = self.parameters.specified_mapping_experiment_runs[exp]
            except Exception as e:
                raise s_sample_mapping_exceptions.InvalidSpecifiedExperimentMapping('Invalid specified run')
                
            merged_count_reads_result = self.s_value_extraction_results.count_reads_result[run]
            merged_count_reads_result.columns = [exp]
            self.results.update_mapping_experiment_runs_after_merge(exp, [run])
            self.results.update_merged_count_reads_result(exp, merged_count_reads_result)
            
    def merge_different_run_average(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            if len(self.s_retrieval_results.mapping_experiment_runs[exp]) == 1:
                run = self.s_retrieval_results.mapping_experiment_runs[exp][0]
                merged_count_reads_result = self.s_value_extraction_results.count_reads_result[run]
                
                self.results.update_mapping_experiment_runs_after_merge(exp, [run])
                self.results.update_merged_count_reads_result(exp, merged_count_reads_result)
            else:
                count_reads_results_exp = []
                for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                    count_reads_results_exp.append(self.s_value_extraction_results.count_reads_result[run])
                
                concat_count_reads_results_exp = pd.concat(count_reads_results_exp, axis = 1)
                mean_concat_count_reads_results_exp = concat_count_reads_results_exp.mean(axis = 0)
                mean_concat_count_reads_results_exp.columns = [exp]
                
                self.results.update_mapping_experiment_runs_after_merge(exp, self.s_retrieval_results.mapping_experiment_runs[exp])
                self.results.update_merged_count_reads_result(exp, merged_count_reads_result)
        
                print(merged_count_reads_result)
                
    def merge_sample(self):
        count_reads_results_exps = []
        exps = []
        for exp in self.results.mapping_experiment_runs_after_merge:
            exps.append(exp)
            count_reads_results_exps.append(self.results.merged_count_reads_result[exp])
            
        count_reads_matrix = pd.concat(count_reads_results_exps, axis = 1)
        count_reads_matrix.columns = exps
        
        self.results.update_count_reads_matrix(count_reads_matrix)
        
