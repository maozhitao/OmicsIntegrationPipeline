import pickle
import time
import copy
import subprocess

from enum import Enum

import sequencing_pipeline

class ParallelOptions(Enum):
    NONE = "None"
    LOCAL = "local"
    SLURM = "SLURM"

class ParallelParameters:
    def __init__(self):
        self.parallel_option = ParallelOptions
        self.parallel_mode = self.parallel_option.SLURM.value
        self.n_processes_local = 2
        self.n_jobs_slurm = 8
        self.parameters_SLURM = ParallelParameters_SLURM()

class ParallelParameters_SLURM:
    def __init__(self):
        self.par_num_node = '-N'
        self.num_node = 1
        self.par_num_core_each_node = '-c'
        self.num_core_each_node = 1
        self.par_time_limit = '--time'
        self.time_limit_hr = 1
        self.time_limit_min = 0
        self.par_job_name = '-J'

        self.par_output = '-o'
        self.output_ext = ".output"
        self.par_error = '-e'
        self.error_ext = ".error"
        
        self.shell_script_path = 'job.sh'
        
class ParallelEngine:
    def __init__(self):
        self.parameters = ParallelParameters()
        
    def reset_parameters(self):
        self.parameters = ParallelParameters()
        
    def get_parameters(self):
        return copy.copy(self.parameters)
        
    def set_parameters(self, parameters):
        self.parameters = parameters
        
    def prepare_shell_file(self, local_submit_command):
        command = ['srun']
        command.extend(local_submit_command)
        command_shell =' '.join(command)
        
        shell_script_path = self.parameters.parameters_SLURM.shell_script_path
        
        with open(shell_script_path, 'w') as tmp:
            tmp.writelines('#!/bin/bash\n')
            tmp.writelines(command_shell)
    
    def get_command_sbatch(self, job_name):
        exe_path = 'sbatch'
        
        slurm_parameters = self.parameters.parameters_SLURM
        
        par_num_node = slurm_parameters.par_num_node
        num_node = str(slurm_parameters.num_node)
        par_num_core_each_node = slurm_parameters.par_num_core_each_node
        num_core_each_node = str(slurm_parameters.num_core_each_node)
        par_time_limit = slurm_parameters.par_time_limit
        time_limit = str(slurm_parameters.time_limit_hr) + ":" + (format(slurm_parameters.time_limit_min,'02')) + ":00"
        par_job_name = slurm_parameters.par_job_name
        par_output = slurm_parameters.par_output
        output_file = job_name + slurm_parameters.output_ext
        par_error = slurm_parameters.par_error
        error_file = job_name + slurm_parameters.error_ext
        
        shell_script_path = slurm_parameters.shell_script_path
        return ([exe_path, par_num_node, num_node, par_num_core_each_node, num_core_each_node, par_time_limit, time_limit, \
                par_job_name, job_name, par_output, output_file, par_error, error_file, shell_script_path])
        
    def do_run_local_parallel(self, command_list):
        obj_Popen = [None]*self.parameters.n_processes_local
        next_entry_idx = 0
        while True:
            finish = True
            for i in range(self.parameters.n_processes_local):
                if obj_Popen[i] is not None:
                    if obj_Popen[i].poll() is None:
                        #Working
                        finish = False
                        continue
                    else:
                        #Join the zombie process
                        obj_Popen[i].wait()
                        obj_Popen[i] = None
                        
                if next_entry_idx < len(command_list):
                    #New job has to be assigned
                    obj_Popen[i] = subprocess.Popen(command_list[next_entry_idx])
                    next_entry_idx = next_entry_idx + 1
                    finish = False
                    
            if finish == True:
                break
                
                
    def do_run_slurm_parallel(self, command_list, result_path_list):
        running_idx = [-1]*self.parameters.n_jobs_slurm
        next_entry_idx = 0
        while True:
            finish = True
            time.sleep(1)
            for i in range(self.parameters.n_jobs_slurm):
                if running_idx[i] != -1:
                    #Working ==> Try to read results
                    try:
                        cur_results = pickle.load(open(result_path_list[running_idx[i]],'rb'))
                    except IOError as e:
                        finish = False
                        continue
                        
                    if cur_results.done == False and cur_result.exception is None:
                        finish = False
                        continue
                    else:
                        #Done (or failed)!
                        if cur_results.exception is not None:
                            print(command_list[running_idx[i]])
                            print(cur_results.exception)
                        running_idx[i] = -1
                        
                if next_entry_idx < len(command_list):
                    #New job has to be assigned
                    running_idx[i] = next_entry_idx
                    subprocess.call(command_list[next_entry_idx])
                    next_entry_idx = next_entry_idx + 1
                    finish = False
                    
            if finish == True:
                break
                
                