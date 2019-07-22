import microarray.m_data_retrieval as m_data_retrieval
import microarray.m_value_extraction as m_value_extraction
import microarray.m_sample_mapping as m_sample_mapping
import microarray.m_gene_mapping as m_gene_mapping

class MicroarrayPipeline:
    def __init__(self):
        self.m_data_retrieval = m_data_retrieval.MicroarrayRetrieval()
        self.m_value_extraction = m_value_extraction.MicroarrayExtraction()
        self.m_sample_mapping = m_sample_mapping.MicroarraySampleMapping()
        self.m_gene_mapping = m_gene_mapping.MicroarrayGeneMapping()