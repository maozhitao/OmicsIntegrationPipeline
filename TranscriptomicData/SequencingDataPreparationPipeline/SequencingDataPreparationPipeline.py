import DataRetrieval
import ValueExtraction
import SampleMapping
import GeneMapping

class SequencingDataPreparationPipeline:
    def __init__(self):
        self.data_retrieval_module = DataRetrieval.DataRetrievalModule()
        self.value_extraction_module = ValueExtraction.ValueExtractionModule()
        self.sample_mapping_module = SampleMapping.SampleMappingModule()
        self.gene_mapping_module = GeneMapping.GeneMappingModule()