from Bio import Entrez
from enum import Enum

import pandas as pd

#Need to import module in parent folder
import sys
sys.path.append("..")
import t_utilities.t_metadata as t_metadata
import t_utilities.t_metadata_def as t_metadata_def
import t_utilities.t_gff as t_gff


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

        

class SequencingRetrieval:
    def __init__(   self, 
                    query_id : list,
                    metadata : t_metadata.TranscriptomeMetadata,
                    gene_annotation : t_gff.GeneAnnotation,
                    parameters : SequencingRetrievalParameters = SequencingRetrievalParameters()
                    ):
        self.query_id = query_id
        self.metadata = metadata
        self.gene_annotation = gene_annotation
        self.parameters = parameters
        
        self.sra_run_info = None
        
    def download_metadata(self):
        #1. Download run_info table from SRA
        #2. Download fasta files from NCBI genome and merge fasta files
        #3. Creating Bowtie2 Index
        self.download_srainfo()
        self.download_fasta()

        
    def download_srainfo(self):
        Entrez.mail = self.parameters.entrez_mail
        for id in self.query_id:
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
        genome_id = self.gene_annotation.get_genome_id()
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
        self.data = None #Fake
        
    def filter_entry(self):
        self.data = None #Fake
        
    def download_data(self):
        #For each entry in metadata table, download each run
        self.data = None #Fake