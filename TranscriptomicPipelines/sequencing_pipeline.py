import sequencing.s_data_retrieval as s_data_retrieval
import sequencing.s_value_extraction as s_value_extraction
import sequencing.s_sample_mapping as s_sample_mapping
import sequencing.s_gene_mapping as s_gene_mapping

import t_utilities.t_metadata as t_metadata
import t_utilities.t_gff as t_gff

class SequencingPipeline:
    def __init__(   self,
                    query_id : list,
                    metadata : t_metadata.TranscriptomeMetadata,
                    gene_annotation : t_gff.GeneAnnotation):
        self.s_data_retrieval = s_data_retrieval.SequencingRetrieval(query_id,metadata,gene_annotation)
        self.s_value_extraction = s_value_extraction.SequencingExtraction()
        self.s_sample_mapping = s_sample_mapping.SequencingSampleMapping()
        self.s_gene_mapping = s_gene_mapping.SequencingGeneMapping()