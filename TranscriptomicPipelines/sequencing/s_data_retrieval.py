from Bio import Entrez

#Need to import module in parent folder
import sys
sys.path.append("..")
import t_utilities.t_metadata as t_metadata
import t_utilities.t_metadata_def as t_metadata_def

class SequencingRetrieval:
    def __init__(   self, 
                    query_id : type(iter([])),
                    metadata : t_metadata.TranscriptomeMetadata,
                    ):
        self.query_id = query_id
        
    def download_metadata(self):
        self.data = None #Fake
        
    def complete_data_independent_metadata(self):
        self.data = None #Fake
        
    def filter_entry(self):
        self.data = None #Fake
        
    def download_data(self):
        self.data = None #Fake