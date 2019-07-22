import t_metadata_def

import datetime

class TranscriptomeMetadata:
    def __init__(   self, 
                    data_type = t_metadata_def.SourceType.ALL : t_metadata_def.SourceType,
                    query_date = datetime.date(1,1,1) : datetime.date,
                    query_string = "" : str,
                    entries = iter([]) : type(iter([]))
                    ):
        self.data_type = data_type #{Microarray, Sequencing, All}
        self.query_date = query_date #A datetime object
        self.query_string = query_string
        self.entries = entries #(A List with entries)
        
    