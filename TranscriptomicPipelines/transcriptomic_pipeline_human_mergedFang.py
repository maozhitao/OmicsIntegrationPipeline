import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline
import parallel_engine

import subprocess

import sys
if (sys.version_info < (3, 0)):
    sys.path.insert(0, "t_utilities")
    sys.path.insert(0, "metadata")
    sys.path.insert(0, "refgen")
    import r_retrieval
    import extractor
    import t_compendium
    import t_gff
    import t_parameters
else:
    import refgen.r_retrieval as r_retrieval
    import metadata.extractor as extractor
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
        print("read gff")
        self.t_gene_annotation.read_file()
        print("read gff: done")
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
    #python transcriptome_pipeline_human_mergedFang.py <target_studies> <target_species> <validate_corr_input> <validate_knowledge_input_samples> <validate_knowledge_input_genes> <(optional)sample_filter_list>
    import pandas as pd
    
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("You have to provide 5 or 6 input arguments!")
        print("Usage:")
        print("python transcriptome_pipeline_human_mergedFang.py <target_studies> <target_species> <validate_corr_input> <validate_knowledge_capture_input_samples> <validate_knowledge_capture_input_genes> <(optional)sample_filter_list>")
        sys.exit(1)
    
    target_studies = sys.argv[1]
    target_species = sys.argv[2]
    validate_corr_input = sys.argv[3]
    validate_knowledge_capture_input_samples = sys.argv[4]
    validate_knowledge_capture_input_genes = sys.argv[5]
    
    if len(sys.argv) == 7:
        optional_sample_filter_list = sys.argv[6]
    else:
        optional_sample_filter_list = None
    
    
    #Obtain the target sample list
    subprocess.call(['meta-omics',target_studies,"tmp_sample_list.csv"]) #Get the csv table
    metadata_extractor = extractor.Extractor()
    exp_list = metadata_extractor.extract("tmp_sample_list.csv")
    print(exp_list)
    print(len(exp_list))
    
    #Just keep the things we want
    if optional_sample_filter_list is not None:
        tmp = pd.read_csv(optional_sample_filter_list)
        exp_list2 = tmp["Experiment"].tolist()
        print(exp_list2)
        print(len(exp_list2))
        
        
        #exp_list = list(set(exp_list) & set(exp_list2))
        exp_list = exp_list2
        print(exp_list)
        print(len(exp_list))
    
    
    #raise Exception
    
    #Obtain the reference genome
    r_refgen = r_retrieval.RefGenRetriever()
    gff_file = r_refgen.download_refseq(target_species)
    print(gff_file)
    
    #exp_list = ["SRX3266939","SRX5961261"],
    
    transcriptome_pipeline = TranscriptomicDataPreparationPipeline([],exp_list,[gff_file])
    
    tmp_t_parameters = t_parameters.TranscriptomicParameters(transcriptome_pipeline)
    transcriptome_pipeline.configure_parameter_set_all()
    
    
    #Start Working
    s_platform_id_remove = []
    s_series_id_remove = []
    s_experiment_id_remove = []
    s_run_id_remove = []
    
    transcriptome_pipeline.sequencing_pipeline.run_sequencing_pipeline(s_platform_id_remove,s_series_id_remove,s_experiment_id_remove,s_run_id_remove)
    transcriptome_pipeline.postprocessing_pipeline.run_postprocessing_pipeline()
    transcriptome_pipeline.validation_pipeline.run_validation_pipeline( input_corr_path = validate_corr_input, 
                                                                        input_knowledge_capture_groupping_path = validate_knowledge_capture_input_samples, 
                                                                        input_knowledge_capture_gene_list_path = validate_knowledge_capture_input_genes)
    
