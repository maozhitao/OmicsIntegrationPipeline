from Bio import Entrez
from enum import Enum

import pandas as pd

from . import s_module_template

class SequencingRetrievalConstant(Enum):
    SRADB           = "sra"
    RUNINFO         = "runinfo"
    TEXT            = "text"
    
    NUCLEOTIDEDB    = "nucleotide"
    FASTA           = "fasta"
    
    WRITEMODE       = 'w'
    NEWLINE         = '\n'
    

class SequencingRetrievalParameters:
    def __init__(   self, 
                    entrez_mail : str = 'cetan@ucdavis.edu',
                    fasta_path : str = 'merged.fasta'):
        self.entrez_mail = entrez_mail
        self.fasta_path = fasta_path
        

class SequencingRetrievalResults:
    def __init__(self):
        self.fasta_path = None
        self.mapping_experiment_runs = None
        
    def update_download_metadata(self, fasta_path):
        self.fasta_path = fasta_path

    def update_complete_data_independent_metadata(self, mapping_experiment_runs = None):
        self.mapping_experiment_runs = mapping_experiment_runs

class SequencingRetrieval(s_module_template.SequencingModule):
    def __init__(self, owner, parameters : SequencingRetrievalParameters = SequencingRetrievalParameters()):
        self.owner = owner
        self.parameters = parameters
        self.results = SequencingRetrievalResults()
        
        self.sra_run_info = None
        
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
            
        print(self.sra_run_info)
            
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
        metadata = self.get_t_metadata()
        self.set_t_metadata(metadata)
        self.results.update_complete_data_independent_metadata()
        
    def filter_entry(self):
        self.data = None #Fake
        
    def download_data(self):
        #For each entry in metadata table, download each run
        self.data = None #Fake