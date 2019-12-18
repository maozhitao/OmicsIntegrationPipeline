from enum import Enum
import copy
import time
import pickle
import subprocess

import sequencing_pipeline

class ParallelOptions(Enum):
    NONE    = "None"
    LOCAL   = "local"
    SLURM   = "SLURM"

class ParallelParameters(object):
    def __init__(self):
        self.parallel_option    = ParallelOptions
        self.parallel_mode      = self.parallel_option.LOCAL.value
        self.n_processes_local  = 2
        self.n_jobs_slurm       = 8
        self.parameters_SLURM   = ParallelParameters_SLURM()

class ParallelParameters_SLURM(object):
    def __init__(self):
        self.par_num_node           = '-N'
        self.par_num_core_each_node = '-c'
        self.par_time_limit         = '--time'
        self.par_job_name           = '-J'
        self.par_output             = '-o'
        self.par_error              = '-e'
        self.num_node               = 1
        self.num_core_each_node     = 1
        self.time_limit_hr          = 10
        self.time_limit_min         = 0
        self.ext_output             = ".output"
        self.ext_error              = ".error"
        self.shell_script_path      = 'job.sh'

class ParallelEngine(object):
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
        command_shell = ' '.join(command)

        with open(self.parameters.parameters_SLURM.shell_script_path, 'w') as tmp:
            tmp.writelines('#!/bin/bash\n')
            tmp.writelines(command_shell)

    def get_command_sbatch(self, job_name):
        exe_path = 'sbatch'
        slurm_parameters        = self.parameters.parameters_SLURM

        par_num_node            = slurm_parameters.par_num_node
        par_num_core_each_node  = slurm_parameters.par_num_core_each_node
        par_time_limit          = slurm_parameters.par_time_limit
        par_job_name            = slurm_parameters.par_job_name
        par_output              = slurm_parameters.par_output
        par_error               = slurm_parameters.par_error
        num_node                = str(slurm_parameters.num_node)
        num_core_each_node      = str(slurm_parameters.num_core_each_node)
        time_limit              = str(slurm_parameters.time_limit_hr) + ":" + \
                                    (format(slurm_parameters.time_limit_min,'02')) + ":00"
        file_output             = job_name + slurm_parameters.ext_output
        file_error              = job_name + slurm_parameters.ext_error

        shell_script_path       = slurm_parameters.shell_script_path
        return ([exe_path, par_num_node, num_node, par_num_core_each_node, num_core_each_node, \
            par_time_limit, time_limit, par_job_name, job_name, par_output, file_output, \
            par_error, file_error, shell_script_path])

    def _do_run_local_parallel_batch(self, command_list, obj_Popen, next_entry_idx):
        """private helper method for do_run_local_parallel in order to eliminate the nested loops
        input
            command_list    : (list) commands executed by subprocess
            obj_Popen       : (list) objects storing executable or None
            next_entry_idx  : (int)  pointer to the next position in obj_Popen
        output
            finish          : (bool) false if tasks are working
            next_entry_idx  : (int)  updated next_entry_idx"""

        finish = True

        # iterate over obj_Popen
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
        return (finish, next_entry_idx)

    def do_run_local_parallel(self, command_list):
        obj_Popen       = [None] * self.parameters.n_processes_local
        next_entry_idx  = 0
        while True:
            finish, next_entry_idx = self._do_run_local_parallel_batch(
                command_list,
                obj_Popen,
                next_entry_idx)
            if finish == True:
                break

    def _do_run_slurm_parallel_batch(
            self, local_command_list, command_list, result_path_list, worker_list,
            time_limit, running_idx, running_time, next_entry_idx):
        """private helper method for do_run_slurm_parallel in order to eliminate the nested loops
        input
            local_command_list  : ()
            command_list        : (list) commands executed by subprocess
            result_path_list    :
            worker_list         :
            time_limit          :
            running_idx         :
            running_time        :
            next_entry_idx      : (int)  pointer to the next position in running
        output
            finish          : (bool) false if tasks are working
            next_entry_idx  : (int)  updated next_entry_idx"""

        finish = True
        time.sleep(1)
        print(running_idx)
        for i in range(self.parameters.n_jobs_slurm):
            if running_idx[i] != -1:

                #Working ==> Try to read results
                try:
                    cur_results = pickle.load(open(result_path_list[running_idx[i]],'rb'))
                except Exception as e:
                    finish = False
                    running_time[i] = running_time[i] + 1
                    if running_time[i] > time_limit:
                        print("TIMEOUT!")
                        worker_list[running_idx[i]].clean_intermediate_files_independent(force = True)
                        running_idx[i] = -1
                    continue

                if cur_results.done == False and cur_result.exception is None:
                    finish = False
                    running_time[i] = running_time[i] + 1
                    if running_time[i] > time_limit:
                        print("TIMEOUT!")
                        worker_list[running_idx[i]].clean_intermediate_files_independent(force = True)
                        running_idx[i] = -1
                    continue
                else:

                    #Done (or failed)!
                    if cur_results.exception is not None:
                        print(command_list[running_idx[i]])
                        print(cur_results.exception)
                    running_time[i] = 0
                    running_idx[i] = -1
            if next_entry_idx < len(command_list):

                #New job has to be assigned
                running_idx[i] = next_entry_idx
                self.prepare_shell_file(local_command_list[next_entry_idx])
                subprocess.call(command_list[next_entry_idx])
                print(command_list[next_entry_idx])
                next_entry_idx = next_entry_idx + 1
                print('New')
                running_time[i] = 0
                finish = False
        return (finish, next_entry_idx)

    def do_run_slurm_parallel(
            self, local_command_list, command_list, result_path_list, worker_list,
            time_limit=None):

        if not time_limit:
            time_limit = self.parameters.parameters_SLURM.time_limit_hr * 3600 + \
                            self.parameters.parameters_SLURM.time_limit_min * 60

        running_idx     = [-1] * self.parameters.n_jobs_slurm
        running_time    = [ 0] * self.parameters.n_jobs_slurm
        next_entry_idx  = 0
        while True:
            finish, next_entry_idx = self._do_run_slurm_parallel_batch(
                local_command_list,
                command_list,
                result_path_list,
                worker_list,
                time_limit,
                running_idx,
                running_time,
                next_entry_idx)
            if finish == True:
                break