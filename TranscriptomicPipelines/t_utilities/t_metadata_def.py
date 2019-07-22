from . import t_metadata_exceptions
#t_metadata_def.py
#Define each field of metadata table
from enum import Enum, auto
import datetime

class Separator(Enum):
    CHANNEL_NUM     = "_"
    SERIES          = "/"

class SourceType(Enum):
    GEO             = auto()
    ARRAYEXPRESS    = auto()
    SRA             = auto()
    MICROARRAY      = auto()
    SEQUENCING      = auto()
    ALL             = auto()
    
class ChannelNum(Enum):
    ONE             = auto()
    TWO             = auto()
    NA              = auto()
    
class Channel(Enum):
    CY3             = "cy3"
    CY5             = "cy5"
    UNKNOWN         = "unknown"
    NA              = "NA"
    

class RemovedIndicator(Enum):
    TRUE            = auto()
    FALSE           = auto()
    
class UsedDataType(Enum):
    GEOSOFT         = auto()
    RAW             = auto()
    SEQUENCING      = auto()
    
class PairedType(Enum):
    PAIRED          = auto()
    UNPAIRED        = auto()
    NA              = auto()
    
class StrandedType(Enum):
    STRANDED        = auto()
    UNSTRANDED      = auto()
    NA              = auto()
    
class BGAvailableIndicator(Enum):
    TRUE            = auto()
    FALSE           = auto()
    NA              = auto()
    
class UsedValueType(Enum):
    MEDIAN          = auto()
    MEAN            = auto()
    UNKNOWN         = auto()
    NA              = auto()
    
class ValueValidIndicator(Enum):
    TRUE            = auto()
    FALSE           = auto()
    


class SampleID:
    #For SRA data, we have to take care of cases with multiple runs...
    def __init__(   self, 
                    source_type : SourceType = SourceType.GEO,
                    channel_num : ChannelNum = ChannelNum.TWO,
                    channel : Channel = Channel.CY3,
                    series_id : str = "", #Only for arrayexpress data
                    experiment_id : str = ""
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
                sample_id : SampleID = SampleID(), #Should be prepared well before you call the constructor
                channel_num : ChannelNum = ChannelNum.TWO,
                first_channel : Channel = Channel.CY3,
                second_channel : Channel = Channel.CY5,
                source_type : SourceType = SourceType.GEO,
                series_id : str = "",
                platform_id : str = "",
                removed : RemovedIndicator = RemovedIndicator.FALSE,
                used_data : UsedDataType = UsedDataType.GEOSOFT,
                paired : PairedType = PairedType.NA,
                stranded : StrandedType = StrandedType.NA,
                bg_available : BGAvailableIndicator = BGAvailableIndicator.TRUE,
                used_value : UsedValueType = UsedValueType.MEDIAN,
                value_valid: ValueValidIndicator = ValueValidIndicator.TRUE,
                pmid : list = [], #Should be prepared well before you call the constructor
                author : str = [], #Should be prepared well before you call the constructor
                date : datetime.date = datetime.date(1,1,1) #Should be prepared well before you call the constructor
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
        
