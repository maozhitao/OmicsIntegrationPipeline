import sequencing.s_data_retrieval as s_data_retrieval
import sequencing.s_value_extraction as s_data_extraction
import sequencing.s_sample_mapping as s_sample_mapping
import sequencing.s_gene_mapping as s_gene_mapping

class SequencingPipeline:
    def __init__(self):
        self.s_data_retrieval = s_data_retrieval.SequencingRetrieval()
        self.s_value_extraction = s_value_extraction.SequencingExtraction()
        self.s_sample_mapping = s_sample_mapping.SequencingSampleMapping()
        self.s_gene_mapping = s_gene_mapping.SequencingGeneMapping()