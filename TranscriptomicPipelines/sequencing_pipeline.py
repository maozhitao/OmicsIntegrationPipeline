import sequencing.s_data_retrieval as s_data_retrieval
import sequencing.s_value_extraction as s_value_extraction
import sequencing.s_sample_mapping as s_sample_mapping
import sequencing.s_gene_mapping as s_gene_mapping
import sequencing.s_module_template as s_module_template


class SequencingPipeline(s_module_template.SequencingModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_data_retrieval = s_data_retrieval.SequencingRetrieval(self)
        self.s_value_extraction = s_value_extraction.SequencingExtraction(self)
        self.s_sample_mapping = s_sample_mapping.SequencingSampleMapping(self)
        self.s_gene_mapping = s_gene_mapping.SequencingGeneMapping(self)
        
        
    def get_s_data_retrieval_results(self):
        return self.s_data_retrieval.get_results()
        