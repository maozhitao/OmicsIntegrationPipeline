from . import t_metadata_def

import datetime

class TranscriptomeMetadata:
    def __init__(   self, 
                    data_type : t_metadata_def.SourceType = t_metadata_def.SourceType.ALL,
                    query_date : datetime.date = datetime.date(1,1,1),
                    query_string : str = "",
                    entries: type(iter([]))  = iter([]) 
                    ):
        self.data_type = data_type #{Microarray, Sequencing, All}
        self.query_date = query_date #A datetime object
        self.query_string = query_string
        self.entries = entries #(A List with entries)
        
    