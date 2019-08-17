import sys
if (sys.version_info < (3, 0)):
    import t_metadata_def
else:
    from . import t_metadata_def

import datetime
import pandas as pd

class TranscriptomeMetadata:
    def __init__(   self, 
                    data_type = t_metadata_def.SourceType.ALL,
                    query_date = datetime.date(1,1,1),
                    query_string = "",
                    entries = []
                    ):
        self.data_type = data_type #{Microarray, Sequencing, All}
        self.query_date = query_date #A datetime object
        self.query_string = query_string
        self.entries = entries #(A List with entries)
        self.metadata_table = pd.DataFrame() #Should add the column name
        
    def new_entry(self):
        new_entry = t_metadata_def.MetadataEntry()
        return new_entry
        
    def add_entry(self, entry):
        self.entries.append(entry)
        
        
        
        
    