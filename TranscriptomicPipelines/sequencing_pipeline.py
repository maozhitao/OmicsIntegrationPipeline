import sequencing.s_data_retrieval as s_data_retrieval
import sequencing.s_value_extraction as s_value_extraction
import sequencing.s_sample_mapping as s_sample_mapping
import sequencing.s_gene_mapping as s_gene_mapping
import sequencing.s_module_template as s_module_template

class Bowtie2Parameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.build_exe_file             = 'bowtie2-build'
        self.build_nthreads             = 4
        self.build_par_nthreads         = '--threads'
        self.build_index_name           = 'TestTemplate'
        
        self.align_exe_file             = 'bowtie2'
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
        
        
class SRAToolkitParameters:
    def __init__(self, owner):
        self.owner = owner
        self.dir = ''
        self.prefetch_exe_file          = 'prefetch'
        self.prefetch_par_output_file   = '-o'
        
        self.validate_exe_file          = 'vdb-validate'
        
        self.fastqdump_exe_file         = 'fastq-dump'
        self.fastqdump_par_gzip         = '--gzip'
        self.fastqdump_par_split3       = '--split-3'
        self.fastqdump_par_output_dir  = '-O'
        
        general_constant = self.owner.get_general_constant()
        general_parameters = self.owner.get_general_parameters()
        
        self.dir.replace(general_constant.UNIX_DIR_SEP.value,general_parameters.dir_sep)
        self.dir.replace(general_constant.WINDOWS_DIR_SEP.value,general_parameters.dir_sep)
        
        if not self.dir.endswith(general_parameters.dir_sep) and self.dir != "":
            self.dir = self.dir + general_parameters.dir_sep
        
class SequencingPipeline(s_module_template.SequencingModule):
    def __init__(self, owner):
        self.owner = owner
        
        self.bowtie2_parameters = Bowtie2Parameters(self)
        self.sratool_parameters = SRAToolkitParameters(self)
        
        self.s_data_retrieval = s_data_retrieval.SequencingRetrieval(self)
        self.s_value_extraction = s_value_extraction.SequencingExtraction(self)
        self.s_sample_mapping = s_sample_mapping.SequencingSampleMapping(self)
        self.s_gene_mapping = s_gene_mapping.SequencingGeneMapping(self)
        
        
    def get_s_data_retrieval_results(self):
        return self.s_data_retrieval.get_results()
        
    def get_s_data_retrieval_parameters(self):
        return self.s_data_retrieval.get_parameters()
        
    def get_bowtie2_parameters(self):
        return self.bowtie2_parameters
    
    def get_sratool_parameters(self):
        return self.sratool_parameters
        