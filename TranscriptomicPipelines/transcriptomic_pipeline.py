import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline

import t_utilities.t_metadata as t_metadata
import t_utilities.t_gff as t_gff

import copy

class TranscriptomicDataPreparationPipeline:
    def __init__(   self,
                    m_query_id : list,
                    s_query_id : list,
                    gff_path : list, #GFF3 Table Paths
                    owner = None
                    ):
                    
        self.m_query_id = m_query_id
        self.s_query_id = s_query_id
        #Initialize the metadata table:
        #metadata will be initialized here and it will shared by ALL COMPONENT in this pipeline
        self.t_metadata = t_metadata.TranscriptomeMetadata()
        #Initialize the gene annotation table:
        self.t_gene_annotation = t_gff.GeneAnnotation(gff_path)
        self.t_gene_annotation.read_file()
        
        
        self.microarray_pipeline = microarray_pipeline.MicroarrayPipeline(self)
        self.sequencing_pipeline = sequencing_pipeline.SequencingPipeline(self)
        self.postprocessing_pipeline = postprocessing_pipeline.PostprocessingPipeline(self)
        self.validation_pipeline = validation_pipeline.ValidationPipeline(self)
        
    
    def get_m_query_id(self):
        return self.m_query_id
        
    def get_s_query_id(self):
        return self.s_query_id
        
    def get_t_metadata(self):
        return self.t_metadata
        
    def set_t_metadata(self,metadata):
        self.t_metadata = metadata
        
    def get_t_gene_annotation(self):
        return self.t_gene_annotation
        
        
if __name__ == "__main__":
    #For Testing
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline([],['SRX000001','SRX000010'],['../TestFiles/CT18.gff3','../TestFiles/LT2.gff3'])
    
    #Start Working
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.complete_data_independent_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.filter_entry()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_data()
    
    transcriptome_pipeline.sequencing_pipeline.s_value_extraction.prepare_data()
    
    