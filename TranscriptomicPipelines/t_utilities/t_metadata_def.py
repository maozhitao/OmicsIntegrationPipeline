import sys
if (sys.version_info < (3, 0)):
    import t_metadata_exceptions
else:
    from . import t_metadata_exceptions
#t_metadata_def.py
#Define each field of metadata table
from enum import Enum
import datetime

class Separator(Enum):
    CHANNEL_NUM     = "_"
    SERIES          = "/"

class SourceType(Enum):
    GEO             = "GEO"
    ARRAYEXPRESS    = "ARRAYEXPRESS"
    SRA             = "SRA"
    MICROARRAY      = "MICROARRAY"
    SEQUENCING      = "SEQUENCING"
    ALL             = "ALL"
    
class ChannelNum(Enum):
    ONE             = "ONE"
    TWO             = "TWO"
    NA              = "NA"
    
class Channel(Enum):
    CY3             = "cy3"
    CY5             = "cy5"
    UNKNOWN         = "unknown"
    NA              = "NA"
    

class RemovedIndicator(Enum):
    TRUE            = "TRUE"
    FALSE           = "FALSE"
    
class UsedDataType(Enum):
    GEOSOFT         = "GEOSOFT"
    RAW             = "RAW"
    SEQUENCING      = "SEQUENCING"
    
class PairedType(Enum):
    PAIRED          = "PAIRED"
    UNPAIRED        = "UNPAIRED"
    NA              = "NA"
    
class StrandedType(Enum):
    STRANDED        = "STRANDED"
    UNSTRANDED      = "UNSTRANDED"
    NA              = "NA"
    
class BGAvailableIndicator(Enum):
    TRUE            = "TRUE"
    FALSE           = "FALSE"
    NA              = "NA"
    
class UsedValueType(Enum):
    MEDIAN          = "MEDIAN"
    MEAN            = "MEAN"
    UNKNOWN         = "UNKNOWN"
    NA              = "NA"
    
class ValueValidIndicator(Enum):
    TRUE            = "TRUE"
    FALSE           = "FALSE"
    


class SampleID:
    #For SRA data, we have to take care of cases with multiple runs...
    def __init__(   self, 
                    source_type = SourceType.GEO,
                    channel_num  = ChannelNum.TWO,
                    channel = Channel.CY3,
                    series_id = "", #Only for arrayexpress data
                    experiment_id = ""
                    ):
        self.source_type = source_type
        self.channel_num = channel_num
        self.channel = channel
        self.series_id = series_id
        self.experiment_id = experiment_id
        self.id = ""
        
    def create_id(self):
        if self.source_type == SourceType.GEO:
            if series_id:
                raise t_metadata_exceptions.FailedToCreateID("No series id should be provided to create id for a GEO entry")
            self.id = add_channel_surfix(self.experiment_id)
            
        elif self.source_type == SourceType.ARRAYEXPRESS:
            if not series_id:
                raise t_metadata_exceptions.FailedToCreateID("Series id should be provided to create id for a ArrayExpress entry")
            self.id = add_channel_surfix(self.series_id + Separator.SERIES + self.experiment_id)
            
        elif self.source_type == SourceType.SRA:
            #SRA data:
            #NOTE: One experiment should be mapped into only ONE entry even there are more than one runs
            if series_id:
                raise t_metadata_exceptions.FailedToCreateID("No series id should be provided to create id for a SRA entry")
            self.id = self.experiment_id
            
        else:
            raise t_metadata_exceptions.FailedToCreateID("Invalid Source Type")
        
    
    def add_channel_surfix(self, prefix_id):
        if self.channel == Channel.CY3:
            result = prefix_id + Separator.CHANNEL_NUM + Channel.CY3
        elif self.channel == Channel.CY5:
            result = prefix_id + Separator.CHANNEL_NUM + Channel.CY5
        else:
            result = prefix_id
        return(result)
        
        
class MetadataEntry:
    #To create one new entry:
    #1. Initiate the new Sample ID after you got the necessary information
    #2. Fill the necessary elements
    def __init__(self,
                sample_id = SampleID(), #Should be prepared well before you call the constructor
                channel_num = ChannelNum.TWO,
                first_channel = Channel.CY3,
                second_channel = Channel.CY5,
                source_type = SourceType.GEO,
                series_id = "",
                platform_id = "",
                removed = RemovedIndicator.FALSE,
                used_data = UsedDataType.GEOSOFT,
                paired = PairedType.NA,
                stranded = StrandedType.NA,
                bg_available = BGAvailableIndicator.TRUE,
                used_value = UsedValueType.MEDIAN,
                value_valid = ValueValidIndicator.TRUE,
                pmid = [], #Should be prepared well before you call the constructor
                author = [], #Should be prepared well before you call the constructor
                date = datetime.date(1,1,1) #Should be prepared well before you call the constructor
                ):
        
        self.sample_id = sample_id
        self.channel_num = channel_num
        self.first_channel = first_channel
        self.second_channel = second_channel
        self.source_type = source_type
        self.series_id = series_id
        self.platform_id = platform_id
        self.removed = removed
        self.used_data = used_data
        self.paired = paired
        self.stranded = stranded
        self.bg_available = bg_available
        self.used_value = used_value
        self.value_valid = value_valid
        self.pmid = pmid
        self.author = author
        self.date = date
        
    def to_dict(self):
        return vars(self)
        
