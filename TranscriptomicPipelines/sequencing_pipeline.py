import sequencing.s_data_retrieval as s_data_retrieval
import sequencing.s_value_extraction as s_value_extraction
import sequencing.s_sample_mapping as s_sample_mapping
import sequencing.s_gene_mapping as s_gene_mapping
import sequencing.s_module_template as s_module_template

import pickle
import subprocess

from enum import Enum
class ParallelOptions(Enum):
    NONE = "None"
    LOCAL = "local"
    SLURM = "SLURM"

class Bowtie2Parameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.build_exe_file                 = 'bowtie2-build'
        self.build_nthreads                 = 4
        self.build_par_nthreads             = '--threads'
        self.build_index_name               = 'TestTemplate'
        
        self.align_exe_file                 = 'bowtie2'
        self.align_par_index_name           = '-x'
        self.align_par_paired_1             = '-1'
        self.align_par_paired_2             = '-2'
        self.align_par_unpaired             = '-U'
        self.align_par_sam                  = '-S'
        self.align_par_fastq                = '-q'
        self.align_par_phred33              = '--phred33'
        self.align_par_phred64              = '--phred64'
        
        self.align_par_very_fast            = '--very-fast'
        self.align_par_fast                 = '--fast'
        self.align_par_sensitive            = '--sensitive'
        self.align_par_very_sensitive       = '--very-sensitive'
        self.align_par_very_fast_local      = '--very-fast-local'
        self.align_par_fast_local           = '--fast-local'
        self.align_par_sensitive_local      = '--sensitive-local'
        self.align_par_very_sensitive_local = '-very-sensitive-local'
        self.align_speed                    = self.align_par_sensitive
        
        self.align_par_end_to_end           = '--end-to-end'
        self.align_par_local                = '--local'
        self.align_mode                     = self.align_par_end_to_end
        
        self.align_par_nthreads             = '--threads'
        self.align_nthreads                 = 4
        self.align_par_reorder              = '--reorder'
        self.align_par_mm                   = '--mm'
        
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
        
        
class SRAToolkitParameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.prefetch_exe_file          = 'prefetch'
        self.prefetch_par_output_file   = '-o'
        
        self.validate_exe_file          = 'vdb-validate'
        
        self.fastqdump_exe_file         = 'fastq-dump'
        self.fastqdump_par_gzip         = '--gzip'
        self.fastqdump_par_split3       = '--split-3'
        self.fastqdump_par_output_dir  = '-O'
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
            

class RSeQCParameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.infer_experiment_exe_file = 'infer_experiment.py'
        self.infer_experiment_par_bed = '-r'
        self.infer_experiment_par_input = '-i'
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
            
class HTSeqParameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.htseq_count_exe_file = 'htseq-count'
        self.htseq_count_par_target_type = '-t'
        self.htseq_count_par_used_id = '-i'
        self.htseq_count_par_quiet = '-q'
        self.htseq_count_par_stranded = '-s'
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
            
class SequencingPipelineParallelParameters:
    def __init__(self, owner):
        self.owner = owner
        self.parallel_mode = ParallelOptions.LOCAL.value
        self.n_processes_local = 2
        self.pyscripts_get_read_counts = 'scripts_get_read_counts_run.py'
        self.pyscripts_merge_runs = 'scripts_merge_runs.py'
        self.parameters_SLURM = SequencingPipelineParallelParameters_SLURM()
        
    def prepare_worker_file_s_data_retrieval(self, run, worker):
        pickle.dump(worker, open(self.get_worker_file_s_data_retrieval(run), 'wb'))
    def prepare_worker_file_s_value_extraction(self, run, worker):
        pickle.dump(worker, open(self.get_worker_file_s_value_extraction(run), 'wb'))
    def get_worker_file_s_data_retrieval(self, run):
        return 'worker_s_data_retrieval_' + str(run) + '.dat'
    def get_worker_file_s_value_extraction(self, run):
        return 'worker_s_value_extraction_' + str(run) + 'dat'
    def get_results_file_get_read_counts(self, run):
        return 'results_get_read_counts_' + str(run) + '.dat'
    def get_results_get_read_counts(self, run):
        return pickle.load(open(self.get_results_file_get_read_counts(run), 'rb'))
        
    def prepare_worker_file_s_sample_mapping(self, exp, worker):
        pickle.dump(worker, open(self.get_worker_file_s_sample_mapping(exp), 'wb'))
    def get_worker_file_s_sample_mapping(self, exp):
        return 'worker_s_sample_mapping_' + str(exp) + 'dat'
    def get_results_file_merge_runs(self, exp):
        return 'results_merge_runs_' + str(exp) + '.dat'
    def get_results_merge_runs(self, exp):
        return pickle.load(open(self.get_results_file_merge_runs(exp), 'rb'))
        
    
        
    def get_pyscripts_get_read_counts(self):
        return self.pyscripts_get_read_counts
        
    def get_pyscripts_merge_runs(self):
        return self.pyscripts_merge_runs
        
    def get_read_counts_command(self, run):
        python_path = 'python'
        script_path = self.get_pyscripts_get_read_counts()
        data_retrieval_worker_path = self.get_worker_file_s_data_retrieval(run)
        value_extraction_worker_path = self.get_worker_file_s_value_extraction(run)
        result_path = self.get_results_file_get_read_counts(run)
        
        command = [python_path, script_path, 
                data_retrieval_worker_path, value_extraction_worker_path, 
                result_path]
                
        return command
        
    def get_merge_runs_command(self, exp):
        python_path = 'python'
        script_path = self.get_pyscripts_get_read_counts()
        sample_mapping_worker_path = self.get_worker_file_s_sample_mapping(exp)
        result_path = self.get_results_file_merge_runs(exp)
        
        command = [python_path, script_path, 
                sample_mapping_worker_path, 
                result_path]
                
        return command
        
        
class SequencingPipelineParallelParameters_SLURM:
    def __init__(self, owner):
        self.owner = owner
        self.par_num_node = '-N'
        self.num_node = 1
        self.par_num_core_each_node = '-c'
        self.num_core_each_node = 4
        self.par_time_limit = '--time'
        self.time_limit_hr = 1
        self.time_limit_min = 0
        self.par_job_name = '-J'

        self.par_output = '-o'
        self.output_ext = ".output"
        self.par_error = '-e'
        self.error_ext = ".error"
        
        self.shell_script_path = 'job.sh'
        
    def get_pyscripts_get_read_counts(self):
        return self.owner.pyscripts_get_read_counts
        
    def get_pyscripts_merge_runs(self):
        return self.owner.pyscripts_merge_runs
        
    def get_read_counts_command(self, run):
        return self.owner.get_read_counts_command(run)
        
    def prepare_shell_file_read_counts_command(self, run):
        command = ['srun']
        original_command = self.get_read_counts_command(run)
        command.extend(original_command)
        command_shell =' '.join(command)
        
        with open(self.shell_script_path, 'w') as tmp:
            tmp.writelines('#!/bin/bash\n')
            tmp.writelines(command_shell)
    
    def get_read_counts_command_sbatch(self, run):
        exe_path = 'sbatch'
        
        par_num_node = self.par_num_node
        num_node = str(self.num_node)
        par_num_core_each_node = self.par_num_core_each_node
        num_core_each_node = str(self.num_core_each_node)
        par_time_limit = self.par_time_limit
        time_limit = str(self.time_limit_hr) + ":" + (format(self.time_limit_min,'02')) + ":00"
        par_job_name = self.par_job_name
        job_name = 'get_read_counts' + '_' + str(run)
        par_output = self.par_output
        output_file = job_name + self.output_ext
        par_error = self.par_error
        error_file = job_name + self.error_ext
        
        shell_script_path = self.shell_script_path
        return ([exe_path, par_num_node, num_node, par_num_core_each_node, num_core_each_node, par_time_limit, time_limit, \
                par_job_name, job_name, par_output, output_file, par_error, error_file, shell_script_path])
                
    def get_merge_runs_command(self, exp):
        return self.owner.get_merge_runs_command(exp)
        
    def prepare_shell_file_merge_runs_command(self, exp):
        command = ['srun']
        original_command = self.get_merge_runs_command(exp)
        command.extend(original_command)
        command_shell =' '.join(command)
        
        with open(self.shell_script_path, 'w') as tmp:
            tmp.writelines('#!/bin/bash\n')
            tmp.writelines(command_shell)
            
    def get_merge_runs_command_sbatch(self, exp):
        exe_path = 'sbatch'
        
        par_num_node = self.par_num_node
        num_node = str(self.num_node)
        par_num_core_each_node = self.par_num_core_each_node
        num_core_each_node = str(self.num_core_each_node)
        par_time_limit = self.par_time_limit
        time_limit = str(self.time_limit_hr) + ":" + (format(self.time_limit_min,'02')) + ":00"
        par_job_name = self.par_job_name
        job_name = 'merge_runs' + '_' + str(run)
        par_output = self.par_output
        output_file = job_name + self.output_ext
        par_error = self.par_error
        error_file = job_name + self.error_ext
        
        shell_script_path = self.shell_script_path
        return ([exe_path, par_num_node, num_node, par_num_core_each_node, num_core_each_node, par_time_limit, time_limit, \
                par_job_name, job_name, par_output, output_file, par_error, error_file, shell_script_path])

        
class SequencingPipeline(s_module_template.SequencingModule):
    def __init__(self, owner, s_query_id, s_compendium):
        self.owner = owner
        
        self.s_query_id = s_query_id
        self.s_compendium = s_compendium
        
        self.bowtie2_parameters = Bowtie2Parameters(self)
        self.sratool_parameters = SRAToolkitParameters(self)
        self.rseqc_parameters = RSeQCParameters(self)
        self.htseq_parameters = HTSeqParameters(self)
        self.parallel_parameters = SequencingPipelineParallelParameters(self)
        
        self.s_data_retrieval = s_data_retrieval.SequencingRetrieval(self)
        self.s_value_extraction = s_value_extraction.SequencingExtraction(self)
        self.s_sample_mapping = s_sample_mapping.SequencingSampleMapping(self)
        self.s_gene_mapping = s_gene_mapping.SequencingGeneMapping(self)
        
        
    def run_sequencing_pipeline(self):
        self.s_data_retrieval.download_metadata()
        self.s_data_retrieval.complete_data_independent_metadata()
        self.s_data_retrieval.filter_entry()
        
        self.s_value_extraction.prepare_gene_annotation()
        
        self.s_data_retrieval.prepare_workers()
        self.s_value_extraction.prepare_workers()
        
        #Runs
        self.s_data_retrieval.download_data()
        self.s_value_extraction.prepare_fastq_file()
        self.s_value_extraction.align_data()
        self.s_value_extraction.infer_stranded_information()
        self.s_value_extraction.count_reads()
        
        #Exps
        self.s_sample_mapping.merge_different_run()
        
        #Entire Matrix
        self.s_sample_mapping.merge_sample()
        self.s_gene_mapping.map_gene()
        
    def run_sequencing_pipeline_parallel(self):
        self.s_data_retrieval.download_metadata()
        self.s_data_retrieval.complete_data_independent_metadata()
        self.s_data_retrieval.filter_entry()
        
        self.s_value_extraction.prepare_gene_annotation()
        
        self.s_data_retrieval.prepare_workers()
        self.s_value_extraction.prepare_workers()
        
        mapping_experiment_runs = self.s_data_retrieval.results.mapping_experiment_runs
        if self.parallel_parameters.parallel_mode == ParallelOptions.NONE.value:
            for exp in mapping_experiment_runs:
                for run in mapping_experiment_runs[exp]:
                    self.s_data_retrieval.workers[run].run()
                    self.s_value_extraction.workers[run].run()
            #JOIN
            count_reads_result_2D = {}
            for exp in mapping_experiment_runs:
                for run in mapping_experiment_runs[exp]:
                    cur_run_results = self.s_value_extraction.workers[run].results
                    count_reads_result_2D[exp][run] = cur_run_results.count_reads_result[run]
                    
                    #Update the current results
                    self.s_value_extraction.results.update_alignment_rate(run, cur_run_results.alignment_rate[run])
                    self.s_value_extraction.results.update_infer_experiment_result(run, cur_run_results.infer_experiment_result[run])
                    self.s_value_extraction.results.update_count_reads_result(run, cur_run_results.count_reads_result[run], cur_run_results_exceptions[run])
                    
        elif self.parallel_parameters.parallel_mode == ParallelOptions.LOCAL.value:
            runs = []
            for exp in mapping_experiment_runs:
                for run in mapping_experiment_runs[exp]:
                    runs.append(run)
            
            obj_Popen = [None]*self.parameters.n_processes_local
            next_run_idx = 0
            while next_run_idx < len(runs):
                finish = True
                for i in range(self.parameters.n_processes_local):
                    if obj_Popen[i] is not None:
                        if obj_Popen[i].poll() is None:
                            #Working
                            finish = False
                            continue
                            
                    if next_run_idx < len(runs):
                        run = runs[next_run_idx]
                        self.parameters.prepare_worker_file_s_data_retrieval(run, self.s_data_retrieval.workers[run])
                        self.parameters.prepare_worker_file_s_value_extraction(run, self.s_value_extraction.workers[run])
                        command = self.parameters.get_read_counts_command(run)
                        obj_Popen[i] = subprocess.Popen(command)
                        next_run_idx = next_run_idx + 1
                        finish = False
                        
                if finish == True:
                    break
            #JOIN
            count_reads_result_2D = {}
            for exp in mapping_experiment_runs:
                count_reads_result_2D[exp] = {}
                for run in mapping_experiment_runs[exp]:
                    cur_run_results = self.parallel_parameters.get_results_get_read_counts(run)
                    count_reads_result_2D[exp][run] = cur_run_results.count_reads_result[run]
                    
                    #Update the current results
                    self.s_value_extraction.results.update_alignment_rate(run, cur_run_results.alignment_rate[run])
                    self.s_value_extraction.results.update_infer_experiment_result(run, cur_run_results.infer_experiment_result[run])
                    self.s_value_extraction.results.update_count_reads_result(run, cur_run_results.count_reads_result[run], cur_run_results_exceptions[run])
        
            #Now the s_value_extraction.results is the same as the outcome as in serial mode!
        elif self.parallel_parameters.parallel_mode == ParallelOptions.SLURM.value:
            pass
                
       
        self.s_sample_mapping.prepare_workers(count_reads_result_2D)
        
        
        
        #START PARALLEL
        if self.parallel_parameters.parallel_mode == ParallelOptions.NONE.value:
            for exp in mapping_experiment_runs:
                self.s_sample_mapping.workers[exp].run()
            #JOIN
            for exp in mapping_experiment_runs:
                cur_exp_results = self.s_sample_mapping.workers[run].results
                
                #Update the current results
                if cur_exp_results.mapping_experiment_runs_after_merge != {}:
                    self.s_sample_mapping.results.update_mapping_experiment_runs_after_merge(exp, cur_exp_results.mapping_experiment_runs_after_merge[exp])
                if cur_exp_results.merged_count_reads_result != {}
                    self.s_sample_mapping.results.update_merged_count_reads_result(exp, cur_exp_results.merged_count_reads_result[exp])
                    
        elif self.parallel_parameters.parallel_mode == ParallelOptions.LOCAL.value:
            exps = []
            for exp in mapping_experiment_runs:
                exps.append(exp)
            
            obj_Popen = [None]*self.parameters.n_processes_local
            next_exp_idx = 0
            while next_exp_idx < len(exps):
                finish = True
                for i in range(self.parameters.n_processes_local):
                    if obj_Popen[i] is not None:
                        if obj_Popen[i].poll() is None:
                            #Working
                            finish = False
                            continue
                    
                    if next_exp_idx < len(exps):
                        exp = exps[next_exp_idx]
                        self.parameters.prepare_worker_file_s_sample_mapping(exp, self.s_sample_mapping.workers[exp])
                        command = self.parameters.get_merge_runs_command(run)
                        obj_Popen[i] = subprocess.Popen(command)
                        next_run_idx = next_run_idx + 1
                        finish = False
                    
                if finish == True:
                    break
                    
            #JOIN
            for exp in mapping_experiment_runs:
                cur_exp_results = self.parallel_parameters.get_results_merge_runs(exp)
                #Update the current results
                if cur_exp_results.mapping_experiment_runs_after_merge != {}:
                    self.s_sample_mapping.results.update_mapping_experiment_runs_after_merge(exp, cur_exp_results.mapping_experiment_runs_after_merge[exp])
                if cur_exp_results.merged_count_reads_result != {}
                    self.s_sample_mapping.results.update_merged_count_reads_result(exp, cur_exp_results.merged_count_reads_result[exp])
                    
        elif self.parallel_parameters.parallel_mode == ParallelOptions.SLURM.value:
            pass
        
        
        
        
        #Now the thing are the same as serial now :)
        self.s_sample_mapping.merge_sample()
        self.s_gene_mapping.map_gene()
        
        

        
        
        
        
        
    def get_s_query_id(self):
        return self.s_query_id
        
    def get_s_metadata(self):
        return self.s_compendium.get_metadata()
        
    def get_s_data(self):
        return self.s_compendium.get_data()
        
    def get_s_data_retrieval_results(self):
        return self.s_data_retrieval.get_results()
        
    def get_s_data_retrieval_parameters(self):
        return self.s_data_retrieval.get_parameters()
        
    def get_s_value_extraction_results(self):
        return self.s_value_extraction.get_results()
        
    def get_s_sample_mapping_results(self):
        return self.s_sample_mapping.get_results()
        
    def get_bowtie2_parameters(self):
        return self.bowtie2_parameters
    
    def get_sratool_parameters(self):
        return self.sratool_parameters
        
    def get_rseqc_parameters(self):
        return self.rseqc_parameters
        
    def get_htseq_parameters(self):
        return self.htseq_parameters
        