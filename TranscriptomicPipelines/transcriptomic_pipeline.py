import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline

import t_utilities.t_metadata as t_metadata

class TranscriptomicDataPreparationPipeline:
    def __init__(   self,
                    m_query_id : type(iter([])),
                    s_query_id : type(iter([])),
                    gene_annotation #GFF3 Table
                    ):
                    
        self.m_query_id = m_query_id
        self.s_query_id = s_query_id
        #Initialize the metadata table:
        #metadata will be initialized here and it will shared by ALL COMPONENT in this pipeline
        self.t_metadata = t_metadata.TranscriptomeMetadata()
        
        self.microarray_pipeline = microarray_pipeline.MicroarrayPipeline()
        self.sequencing_pipeline = sequencing_pipeline.SequencingPipeline(s_query_id,self.t_metadata)
        self.postprocessing_pipeline = postprocessing_pipeline.PostprocessingPipeline()
        self.validation_pipeline = validation_pipeline.ValidationPipeline()
        
if __name__ == "__main__":
    #For Testing
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline(iter([]),iter([]),"Test")