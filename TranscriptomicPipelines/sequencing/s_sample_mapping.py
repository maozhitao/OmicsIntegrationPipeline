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

import pickle
import subprocess

import os



class SequencingSampleMappingConstant(Enum):
    JOB_NAME                    = 's_sample_mapping_'


class DifferentRunMergeMode(Enum):
    DROP_EXPERIMENT = "drop"
    RANDOM_RUN      = "random"
    SPECIFIED_RUN   = "specified"
    AVERAGE         = "average"
    
    
class SequencingSampleMappingParallelParameters:
    def __init__(self, default_parallel_parameters):
        self.parallel_parameters = default_parallel_parameters
        self.pyscripts = 'script_merge_runs.py'


class SequencingSampleMappingParameters:
    def __init__(   self, 
                    different_run_merge_mode = DifferentRunMergeMode.AVERAGE.value,
                    specified_mapping_experiment_runs = None,
                    n_trial = 10):
        self.different_run_merge_mode = different_run_merge_mode
        self.specified_mapping_experiment_runs = specified_mapping_experiment_runs
        self.n_trial = n_trial
        
        self.skip_merge_different_run = True
        
        self.clean_existed_worker_file = True
        self.clean_existed_results = True

class SequencingSampleMappingResults:
    def __init__(self):
        self.merged_count_reads_result = {}
        self.mapping_experiment_runs_after_merge = {}
        self.count_reads_matrix = None
        self.done = False
        self.exception = None
        
        self.worker_file = {} #worker_*
        self.result_file = {} #result_*
        
    def update_mapping_experiment_runs_after_merge(self, exp, runs):
        self.mapping_experiment_runs_after_merge[exp] = runs
        
    def update_merged_count_reads_result(self, exp, merged_count_reads_result):
        self.merged_count_reads_result[exp] = merged_count_reads_result
        
    def update_count_reads_matrix(self, count_reads_matrix):
        self.count_reads_matrix = count_reads_matrix
        
    def update_worker_file(self, exp, worker_file):
        self.worker_file[exp] = worker_file
        
    def update_result_file(self, exp, result_file):
        self.result_file[exp] = result_file
        
        
class SequencingSampleMapping(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results() #Get Mapping Results
        self.s_value_extraction_results = owner.get_s_value_extraction_results() #Get Read Counts Results
        self.parameters = SequencingSampleMappingParameters()
        self.parallel_parameters = SequencingSampleMappingParallelParameters(self.owner.get_parallel_engine().get_parameters())
        self.results = SequencingSampleMappingResults()
        
        self.workers = {}
        
    def prepare_workers(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            self.workers[exp] = self.prepare_worker(exp)
            
    def prepare_worker(self, exp):
        mapping_experiment_runs = self.s_retrieval_results.mapping_experiment_runs
        count_reads_result = self.s_value_extraction_results.count_reads_result
        worker = SequencingSampleMappingWorker(exp, self.parameters, mapping_experiment_runs, count_reads_result)
        
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
        
    def complete_data_dependent_metadata(self):
        metadata = self.get_s_metadata()
        
        for exp in self.results.mapping_experiment_runs_after_merge:
            prev_paired = None
            prev_stranded = None
            for run in self.results.mapping_experiment_runs_after_merge[exp]:
                cur_paired = self.s_value_extraction_results.paired_info[run]
                cur_stranded = self.s_value_extraction_results.infer_experiment_result[run].check_stranded_info()
                if prev_paired is None:
                    prev_paired = cur_paired
                elif prev_paired != cur_paired:
                    prev_paired = cur_paired
                    print("Warning: Exp" + str(exp) + "has multiple runs with different paired info!")
                
                if prev_stranded is None:
                    prev_stranded = cur_stranded
                elif prev_stranded != cur_stranded:
                    prev_stranded = cur_stranded
                    print("Warning: Exp" + str(exp) + "has multiple runs with different stranded info!")
            
            metadata.update_sequencing_entry_data_dependent_info(exp, cur_paired, cur_stranded)
        
        df = metadata.get_table()
        df.to_csv("TestMetadataTable_DataDependent.csv")
        
    def get_results(self):
        return self.results
        
    def get_parameters(self):
        return self.parameters
        
    def prepare_worker_file(self, exp):
        pickle.dump(self.workers[exp], open(self.get_worker_file(exp), 'wb'))
    def get_worker_file(self, exp):
        return 'worker_s_sample_mapping_' + str(exp) + '.dat'
    def get_worker_results_file(self, exp):
        return 'results_s_sample_mapping_' + str(exp) + '.dat'
    def get_worker_results(self, exp):
        return pickle.load(open(self.get_worker_results_file(exp), 'rb'))
        
    def get_local_submit_command(self, exp):
        python_path = 'python'
        script_path = self.parallel_parameters.pyscripts
        worker_path = self.get_worker_file(exp)
        result_path = self.get_worker_results_file(exp)
        
        command = [python_path, script_path, 
                worker_path, 
                result_path]
                
        return command
        
        
    def submit_job(self):
        if self.parallel_parameters.parallel_parameters.parallel_mode == self.parallel_parameters.parallel_parameters.parallel_option.NONE.value:
            for exp in self.s_retrieval_results.mapping_experiment_runs:
                if self.parameters.skip_merge_different_run == False or self.check_existed_results(exp) == False:
                    self.workers[exp].do_run()
                    pickle.dump(self.workers[exp].results, open(self.get_worker_results_file(exp),'rb'))
        elif self.parallel_parameters.parallel_parameters.parallel_mode == self.parallel_parameters.parallel_parameters.parallel_option.LOCAL.value:
            commands = []
            for exp in self.s_retrieval_results.mapping_experiment_runs:
                if self.parameters.skip_merge_different_run == False or self.check_existed_results(exp) == False:
                    self.prepare_worker_file(exp)
                    commands.append(self.get_local_submit_command(exp))
            #Run It !
            parallel_engine = self.get_parallel_engine()
            parallel_engine.do_run_local_parallel(commands)
        elif self.parallel_parameters.parallel_parameters.parallel_mode == self.parallel_parameters.parallel_parameters.parallel_option.SLURM.value:
            local_commands = []
            commands = []
            result_path_list = []
            parallel_engine = self.get_parallel_engine()
            for exp in self.s_retrieval_results.mapping_experiment_runs:
                if self.parameters.skip_merge_different_run == False or self.check_existed_results(exp) == False:
                    self.prepare_worker_file(exp)
                    local_command = self.get_local_submit_command(exp)
                    local_commands.append(local_command)
                    command = parallel_engine.get_command_sbatch(SequencingSampleMappingConstant.JOB_NAME.value + exp)
                    commands.append(command)
                    
                    print(local_command)
                    print(command)
                    
                    result_path_list.append(self.get_worker_results_file(exp))
            #Polling
            parallel_engine = self.get_parallel_engine()
            parallel_engine.do_run_slurm_parallel(local_commands, commands, result_path_list)
            
    def join_results(self):
        mapping_experiment_runs = self.s_retrieval_results.mapping_experiment_runs
        
        exception_occurred = False
        for exp in mapping_experiment_runs:
            cur_exp_results = self.get_worker_results(exp)
            if cur_exp_results.exception is not None:
                print(exp + ": Exception Occurred : " + str(cur_exp_results.exception))
                exception_occurred = True
                continue
            #Update the current results
            if cur_exp_results.mapping_experiment_runs_after_merge != {}:
                self.results.update_mapping_experiment_runs_after_merge(exp, cur_exp_results.mapping_experiment_runs_after_merge[exp])
            if cur_exp_results.merged_count_reads_result != {}:
                self.results.update_merged_count_reads_result(exp, cur_exp_results.merged_count_reads_result[exp])
                
                
            if self.parallel_parameters.parallel_parameters.parallel_mode == self.parallel_parameters.parallel_parameters.parallel_option.NONE.value:
                self.results.update_worker_file(exp, None)
            else:
                self.results.update_worker_file(exp, self.get_worker_file(exp))
            self.results.update_result_file(exp, self.get_worker_results_file(exp))
            
        if exception_occurred == True:
            raise s_sample_mapping_exceptions.JoinResultsException('Some exception occurred!')
        
    def check_existed_results(self, exp):
        try:
            cur_exp_results = self.get_worker_results(exp)
        except Exception as e:
            return False
            
        #We have to check the completeness of the results here!
        if cur_exp_results.exception is not None:
            os.remove(self.get_worker_results_file(exp))
            return False
        return True
        

class SequencingSampleMappingWorker:
    def __init__(self, exp, parameters, 
                    mapping_experiment_runs, count_reads_result):
        self.exp = exp
        self.parameters = parameters
        self.mapping_experiment_runs = mapping_experiment_runs
        self.count_reads_result = count_reads_result
        
        self.results = SequencingSampleMappingResults()
        
    def do_run(self):
        self.merge_different_run_exp()
        
    def merge_different_run_exp(self):
        if self.parameters.different_run_merge_mode == DifferentRunMergeMode.DROP_EXPERIMENT.value:
            self.merge_different_run_drop_experiment_exp()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.RANDOM_RUN.value:
            self.merge_different_run_random_run_exp()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.SPECIFIED_RUN.value:
            self.merge_different_run_specified_run_exp()
        elif self.parameters.different_run_merge_mode == DifferentRunMergeMode.AVERAGE.value:
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
            run = self.parameters.specified_mapping_experiment_runs[self.exp]
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
            