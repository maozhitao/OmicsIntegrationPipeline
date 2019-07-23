import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline

import t_utilities.t_metadata as t_metadata
import t_utilities.t_gff as t_gff

class TranscriptomicDataPreparationPipeline:
    def __init__(   self,
                    m_query_id : list,
                    s_query_id : list,
                    gff_path : list #GFF3 Table Paths
                    ):
                    
        self.m_query_id = m_query_id
        self.s_query_id = s_query_id
        #Initialize the metadata table:
        #metadata will be initialized here and it will shared by ALL COMPONENT in this pipeline
        self.t_metadata = t_metadata.TranscriptomeMetadata()
        #Initialize the gene annotation table:
        self.t_gene_annotation = t_gff.GeneAnnotation(gff_path)
        self.t_gene_annotation.read_file()
        
        
        self.microarray_pipeline = microarray_pipeline.MicroarrayPipeline()
        self.sequencing_pipeline = sequencing_pipeline.SequencingPipeline(s_query_id,self.t_metadata,self.t_gene_annotation)
        self.postprocessing_pipeline = postprocessing_pipeline.PostprocessingPipeline()
        self.validation_pipeline = validation_pipeline.ValidationPipeline()
        

        
        
        
if __name__ == "__main__":
    #For Testing
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline([],['SRX000001','SRX000010'],['../TestFiles/CT18.gff3','../TestFiles/LT2.gff3'])
    
    #Start Working
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.complete_data_independent_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.filter_entry()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_data()
    
    