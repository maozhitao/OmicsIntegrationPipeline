import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline
import parallel_engine

import pickle

import sys
if (sys.version_info < (3, 0)):
    sys.path.insert(0, "t_utilities")
    import t_compendium
    import t_gff
    import t_parameters
else:
    import t_utilities.t_compendium as t_compendium
    import t_utilities.t_gff as t_gff
    import t_utilities.t_parameters as t_parameters

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
                    m_query_id,
                    s_query_id,
                    gff_path, #GFF3 Table Paths
                    owner = None
                    ):
                    
        #Initialize Parameter Set:
        self.parameter_set = t_parameters.TranscriptomicParameters(self)
                    
        #Initialize Environment:
        self.general_constant = GeneralConstant
        self.general_parameters = GeneralParameters() #Temp arrangement, it should be moved to upper layer (OmicsDataPreparationPipeline)
        self.general_parameters.check_os()
                    
        #Initialize the metadata table:
        #metadata will be initialized here and it will shared by ALL COMPONENT in this pipeline
        #Initialize the gene annotation table:
        self.t_gene_annotation = t_gff.GeneAnnotation(gff_path)
        self.t_gene_annotation.read_file()
        self.t_compendium_collections = t_compendium.TranscriptomeCompendiumCollections()
        
        #Parallel Engine
        self.parallel_engine = parallel_engine.ParallelEngine()
        
        self.microarray_pipeline = microarray_pipeline.MicroarrayPipeline(self, m_query_id, t_compendium.TranscriptomeCompendium())
        self.sequencing_pipeline = sequencing_pipeline.SequencingPipeline(self, s_query_id, t_compendium.TranscriptomeCompendium(query_ids = s_query_id))
        self.postprocessing_pipeline = postprocessing_pipeline.PostprocessingPipeline(self)
        self.validation_pipeline = validation_pipeline.ValidationPipeline(self)
        
        #Configure Parameters
    
    def configure_parameter_set_all(self):
        self.configure_parameter_set()
        self.sequencing_pipeline.configure_parameter_set_all(self.general_constant, self.general_parameters)
        self.postprocessing_pipeline.configure_parameter_set_all()
        self.validation_pipeline.configure_parameter_set_all()
    
    def configure_parameter_set(self):
        self.general_parameters.executive_prefix    = self.parameter_set.general_parameters_executive_prefix
        self.general_parameters.executive_surfix    = self.parameter_set.general_parameters_executive_surfix
        self.general_parameters.dir_sep             = self.parameter_set.general_parameters_dir_sep
        self.general_parameters.check_os()
        
    def get_parameter_set(self):
        return self.parameter_set

    def get_t_compendium_collections(self):
        return self.t_compendium_collections
        
    def get_m_compendium(self):
        return self.microarray_pipeline.m_compendium
        
    def get_s_compendium(self):
        return self.sequencing_pipeline.s_compendium
        
    def get_t_gene_annotation(self):
        return self.t_gene_annotation
        
    def get_general_parameters(self):
        return self.general_parameters
        
    def get_general_constant(self):
        return self.general_constant
        
    def get_parallel_engine(self):
        return self.parallel_engine
        
        
if __name__ == "__main__":
    #For Testing
    import pandas as pd
    tmp = pd.read_csv("../TestFiles/SraRunInfo3.csv")
    exp_list = tmp["Experiment"].tolist()
    print(exp_list)
    #exp_list = ["SRX3266939","SRX5961261"],
    
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline([],exp_list,['../TestFiles/LT2_pSLT.gff3','../TestFiles/LT2.gff3'])
    
    tmp_t_parameters = t_parameters.TranscriptomicParameters(transcriptome_pipeline)
    transcriptome_pipeline.configure_parameter_set_all()
    
    
    #Start Working
    s_platform_id_remove = []
    s_series_id_remove = []
    s_experiment_id_remove = []
    s_run_id_remove = []
    
    transcriptome_pipeline.sequencing_pipeline.run_sequencing_pipeline(s_platform_id_remove,s_series_id_remove,s_experiment_id_remove,s_run_id_remove)
    transcriptome_pipeline.postprocessing_pipeline.run_postprocessing_pipeline()
    transcriptome_pipeline.validation_pipeline.run_validation_pipeline( input_corr_path = "../TestFiles/Input_CorrTest.csv", 
                                                                        input_knowledge_capture_groupping_path = "../TestFiles/Input_KnowledgeCapture_fur.csv", 
                                                                        input_knowledge_capture_gene_list_path = "../TestFiles/Input_KnowledgeCapture_fur_related_genes.csv")
    