from . import s_module_template
from . import s_value_extraction_exceptions

from enum import Enum
import sys
import subprocess


class SequencingExtractionConstant(Enum):
    NEWLINE         = '\n'
    SPACE           = ' '
    
    
    
class SequencingExtractionParameters:
    def __init__(self, owner, fastq_file_dir : str = "."):
        self.owner = owner
        self.fastq_file_dir = fastq_file_dir
        
        general_parameters = self.owner.get_general_parameters()
        if self.fastq_file_dir == "":
            raise s_value_extraction_exception.InvalidFastqFilePathException('You should provide the directory for saving fastq data!')
        if not self.fastq_file_dir.endswith(general_parameters.dir_sep):
            self.fastq_file_dir = self.fastq_file_dir + general_parameters.dir_sep
        
    def get_bowtie2_build_command(self, input_fasta : str = ''):
        bowtie2_parameters = self.owner.get_bowtie2_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = bowtie2_parameters.dir + general_parameters.executive_prefix + bowtie2_parameters.build_exe_file + general_parameters.executive_surfix
        thread_par = bowtie2_parameters.build_par_nthreads
        nthread = str(bowtie2_parameters.build_nthreads)
        fasta_path = input_fasta
        bowtie2_index_name = bowtie2_parameters.build_index_name
        command = [executive_path, thread_par, nthread, fasta_path, bowtie2_index_name]
        return(command)
        
    def get_fastqdump_command(self, input_sra : str = ''):
        sratool_parameters = self.owner.get_sratool_parameters()
        
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = sratool_parameters.dir + general_parameters.executive_prefix + sratool_parameters.fastqdump_exe_file + general_parameters.executive_surfix
        input_sra = input_sra
        fastqdump_par_gzip = sratool_parameters.fastqdump_par_gzip
        fastqdump_par_split3 = sratool_parameters.fastqdump_par_split3
        fastqdump_par_dir = sratool_parameters.fastqdump_par_output_dir
        fastqdump_dir = self.fastq_file_dir
        command = [executive_path, input_sra, fastqdump_par_gzip, fastqdump_par_split3, fastqdump_par_dir, fastqdump_dir]
        return(command)
        
    def get_bowtie2_align_command(self):
        pass


            
class SequencingExtractionOutputs:
    def __init__(self):
        pass

class SequencingExtraction(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results()
        self.parameters = SequencingExtractionParameters(self)
        self.results = SequencingExtractionOutputs()
        
    def prepare_data(self):
        #Prepare bowtie2 index
        self.create_bowtie2_index()
        self.prepare_fastq_file()

    def create_bowtie2_index(self):
        command = self.parameters.get_bowtie2_build_command(self.s_retrieval_results.fasta_path)
        subprocess.run(command, stdout=subprocess.PIPE, shell = self.get_general_parameters().use_shell)
        
    def prepare_fastq_file(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                command = self.parameters.get_fastqdump_command(self.s_retrieval_results.sra_file_dir + run)
                try:
                    binary_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = self.get_general_parameters().use_shell)
                except Exception as e:
                    raise s_value_extraction_exceptions.FastqdumpFailedException('Failed to run fastqdump')
                
                try:
                    output = binary_output.decode(self.get_general_constant().CODEC.value)
                    output = output.split(SequencingExtractionConstant.NEWLINE.value)
                    line_n_read = output[-3]
                    line_n_write = output[-2]
                    
                    n_read = int(line_n_read.split(SequencingExtractionConstant.SPACE.value)[1])
                    n_write = int(line_n_write.split(SequencingExtractionConstant.SPACE.value)[1])

                    if n_read != n_write:
                        raise s_value_extraction_exceptions.FastqdumpFailedException('n_read != n_write')
                    
                except Exception as e:
                    raise s_value_extraction_exceptions.FastqdumpFailedException('Error output from fastqdump')
        
    def align_data(self):
        self.data = None #Fake
    
    def infer_stranded_information(self):
        self.data = None #Fake
        
    def complete_data_dependent_metadata(self):
        self.data = None #Fake
        
