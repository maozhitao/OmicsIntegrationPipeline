from Bio import Entrez
from enum import Enum

import pandas as pd
import subprocess

import sys
if (sys.version_info < (3, 0)):
    import s_module_template
    import s_data_retrieval_exceptions
else:
    from . import s_module_template
    from . import s_data_retrieval_exceptions

class SequencingRetrievalConstant(Enum):
    SRADB           = "sra"
    RUNINFO         = "runinfo"
    TEXT            = "text"
    
    NUCLEOTIDEDB    = "nucleotide"
    FASTA           = "fasta"
    
    WRITEMODE       = 'w'
    SPACE           = ' '
    NEWLINE         = '\n'
    
    SRAINFO_COL_RUN = 'Run'
    SRAINFO_COL_EXP = 'Experiment'
    
    SRA_RESULT_OK   = 'consistent'
    

class SequencingRetrievalParameters:
    def __init__(   self, owner,
                    entrez_mail = 'cetan@ucdavis.edu',
                    fasta_path = 'merged.fasta',
                    sra_file_dir = '.'):
        self.owner = owner
        self.entrez_mail = entrez_mail
        self.fasta_path = fasta_path
        self.sra_file_dir = sra_file_dir
        
        general_parameters = self.owner.get_general_parameters()
        
        if self.sra_file_dir == "":
            raise s_data_retrieval_exceptions.InvalidSRAFilePathException('You should provide the directory for saving downloaded sequencing data!')
        if not self.sra_file_dir.endswith(general_parameters.dir_sep):
            self.sra_file_dir = self.sra_file_dir + general_parameters.dir_sep
    
    def get_sratool_prefetch_command(self, sra_run_id = ''):
        sratool_parameters = self.owner.get_sratool_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = sratool_parameters.dir + general_parameters.executive_prefix + sratool_parameters.prefetch_exe_file + general_parameters.executive_surfix
        sra_run_id = sra_run_id
        output_par = sratool_parameters.prefetch_par_output_file
        output_file_name = self.sra_file_dir + sra_run_id
        command = [executive_path, sra_run_id, output_par, output_file_name]
        return(command)
        
    def get_sratool_vdb_validate_command(self, sra_run_id = ''):
        sratool_parameters = self.owner.get_sratool_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = sratool_parameters.dir + general_parameters.executive_prefix + sratool_parameters.validate_exe_file + general_parameters.executive_surfix
        sra_run_id = sra_run_id
        check_file_name = self.sra_file_dir + sra_run_id
        command = [executive_path, check_file_name]
        return(command)
        
        
class SequencingRetrievalResults:
    def __init__(self):
        self.fasta_path = None
        self.sra_file_dir = None
        self.mapping_experiment_runs = None
        
    def update_download_metadata(self, fasta_path):
        self.fasta_path = fasta_path

    def update_complete_data_independent_metadata(self, mapping_experiment_runs = None):
        self.mapping_experiment_runs = mapping_experiment_runs
        
    def update_download_data(self, sra_file_dir = ''):
        self.sra_file_dir = sra_file_dir

class SequencingRetrieval(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = SequencingRetrievalParameters(self)
        self.results = SequencingRetrievalResults()
        
        self.sra_run_info = None
        self.mapping_experiment_runs = None
        
        self.workers = {}
        
        
    def get_parameters(self):
        return self.parameters
        
    def get_results(self):
        return self.results
        
    def download_metadata(self):
        #1. Download run_info table from SRA
        #2. Download fasta files from NCBI genome and merge fasta files
        self.download_srainfo()
        self.download_fasta()
        self.results.update_download_metadata(self.parameters.fasta_path)
        
    def download_srainfo(self):
        Entrez.mail = self.parameters.entrez_mail
        for id in self.get_s_query_id():
            handle = Entrez.efetch( id = id, 
                                    db = SequencingRetrievalConstant.SRADB.value, 
                                    rettype = SequencingRetrievalConstant.RUNINFO.value, 
                                    retmode = SequencingRetrievalConstant.TEXT.value)
            df = pd.read_csv(handle)
            if self.sra_run_info is None:
                self.sra_run_info = df
            else:
                self.sra_run_info = pd.concat([self.sra_run_info, df])
            handle.close()
            
    def download_fasta(self):
        Entrez.mail = self.parameters.entrez_mail
        genome_id = self.get_t_gene_annotation().get_genome_id()
        with open(self.parameters.fasta_path, SequencingRetrievalConstant.WRITEMODE.value) as outfile:
            for id in genome_id:
                print(id)
                handle = Entrez.efetch( id = id,
                                        db = SequencingRetrievalConstant.NUCLEOTIDEDB.value,
                                        rettype = SequencingRetrievalConstant.FASTA.value,
                                        retmode = SequencingRetrievalConstant.TEXT.value)
                outfile.write(handle.read())
                outfile.write(SequencingRetrievalConstant.NEWLINE.value)
                                    
        
    def complete_data_independent_metadata(self):
        #Note: You should manage the experiment - run mapping information
        self.mapping_experiment_runs = {}
        experiments = self.sra_run_info[SequencingRetrievalConstant.SRAINFO_COL_EXP.value].tolist()
        
        metadata = self.get_s_metadata()
        for exp in experiments:
            idx = self.sra_run_info[SequencingRetrievalConstant.SRAINFO_COL_EXP.value] == exp
            self.mapping_experiment_runs[exp] = self.sra_run_info[SequencingRetrievalConstant.SRAINFO_COL_RUN.value][idx].tolist()
        
        self.results.update_complete_data_independent_metadata(self.mapping_experiment_runs)
        self.results.update_download_data(self.parameters.sra_file_dir)
        
    def filter_entry(self):
        self.data = None #Fake
        
    def prepare_workers(self):
        for exp in self.mapping_experiment_runs:
            for run in self.mapping_experiment_runs[exp]:
                self.workers[run] = self.prepare_worker(run)
        
    def prepare_worker(self, run):
        download_data_command = self.parameters.get_sratool_prefetch_command(run)
        check_data_command = self.parameters.get_sratool_vdb_validate_command(run)
        general_parameters = self.get_general_parameters()
        general_constant = self.get_general_constant()
        worker = SequencingRetrievalWorker(run, download_data_command, check_data_command, general_parameters, general_constant)
        return worker
        
    def download_data(self):
        #For each entry in metadata table, download each run
        for exp in self.mapping_experiment_runs:
            for run in self.mapping_experiment_runs[exp]:
                self.workers[run].download_data_run_independent()
                
                        
        #self.results.update_download_data(self.parameters.sra_file_dir)
        
    
        

class SequencingRetrievalWorker:
    def __init__(self, run, download_data_command, check_data_command, general_parameters, general_constant):
        self.run = run
        self.download_data_command = download_data_command
        self.check_data_command = check_data_command
        self.general_parameters = general_parameters
        self.general_constant = general_constant
        
    def do_run(self):
        self.download_data_run_independent()
        
    def download_data_run_independent(self):
        if self.check_data_independent() == False:
            print(self.download_data_command)
            subprocess.call(self.download_data_command, stdout=subprocess.PIPE, shell = self.general_parameters.use_shell)
            if self.check_data_independent() == False:
                raise s_data_retrieval_exceptions.FailedToDownloadSRAFileException('Failed to download this run:' + self.run)
                
    def check_data_independent(self):
        try:
            binary_result = subprocess.check_output(self.check_data_command, stderr=subprocess.STDOUT, shell = self.general_parameters.use_shell)
        except subprocess.CalledProcessError as e:
            return False
        result = binary_result.decode(self.general_constant.CODEC.value)
        result = result.split(SequencingRetrievalConstant.SPACE.value)
        result = result[-1].replace(SequencingRetrievalConstant.NEWLINE.value,"")
        if result == SequencingRetrievalConstant.SRA_RESULT_OK.value:
            return True
        else:
            return False
