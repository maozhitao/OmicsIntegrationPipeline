import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline

import t_utilities.t_metadata as t_metadata
import t_utilities.t_gff as t_gff

from enum import Enum 
import sys

class GeneralConstant(Enum):
    WINDOWS                     = "win32"
    WINDOWS_EXECUTIVE_PREFIX    = ""
    WINDOWS_EXECUTIVE_SURFIX    = ""
    WINDOWS_DIR_SEP             = "\\"
    
    UNIX_EXECUTIVE_PREFIX       = ""
    UNIX_EXECUTIVE_SURFIX       = ""
    UNIX_DIR_SEP                = "/"
    
    CODEC                       ="utf-8"
    
class GeneralParameters:
    def __init__(self):
        self.use_shell = False
        self.executive_prefix = ""
        self.executive_surfix = ""
        self.dir_sep = ""
        
    def check_os(self):
        if sys.platform == GeneralConstant.WINDOWS.value:
            self.executive_prefix = GeneralConstant.WINDOWS_EXECUTIVE_PREFIX.value
            self.executive_surfix = GeneralConstant.WINDOWS_EXECUTIVE_SURFIX.value
            self.dir_sep = GeneralConstant.WINDOWS_DIR_SEP.value
            self.use_shell = True
        else:
            self.executive_prefix = GeneralConstant.UNIX_EXECUTIVE_PREFIX.value
            self.executive_surfix = GeneralConstant.UNIX_EXECUTIVE_SURFIX.value
            self.dir_sep = GeneralConstant.UNIX_DIR_SEP.value
            self.use_shell = False


class TranscriptomicDataPreparationPipeline:
    def __init__(   self,
                    m_query_id : list,
                    s_query_id : list,
                    gff_path : list, #GFF3 Table Paths
                    owner = None
                    ):
                    
        #Initialize Environment:
        self.general_constant = GeneralConstant
        self.general_parameters = GeneralParameters() #Temp arrangement, it should be moved to upper layer (OmicsDataPreparationPipeline)
        self.general_parameters.check_os()
                    
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
        
    def get_general_parameters(self):
        return self.general_parameters
        
    def get_general_constant(self):
        return self.general_constant
        
        
if __name__ == "__main__":
    #For Testing
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline([],['SRX5961261','SRX3266939'],['../TestFiles/LT2_pSLT.gff3','../TestFiles/LT2.gff3'])
    
    #Start Working
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.complete_data_independent_metadata()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.filter_entry()
    transcriptome_pipeline.sequencing_pipeline.s_data_retrieval.download_data()
    
    transcriptome_pipeline.sequencing_pipeline.s_value_extraction.prepare_data()
    #transcriptome_pipeline.sequencing_pipeline.s_value_extraction.align_data()
    transcriptome_pipeline.sequencing_pipeline.s_value_extraction.infer_stranded_information()
    transcriptome_pipeline.sequencing_pipeline.s_value_extraction.count_reads()
    
    transcriptome_pipeline.sequencing_pipeline.s_sample_mapping.merge_different_run()
    transcriptome_pipeline.sequencing_pipeline.s_sample_mapping.merge_sample()
    
    