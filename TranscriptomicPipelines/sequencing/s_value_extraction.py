from . import s_module_template

from enum import Enum
import sys
import subprocess

class SequencingExtractionConstant(Enum):
    WINDOWS                     = "win32"
    WINDOWS_EXECUTIVE_PREFIX    = ""
    WINDOWS_EXECUTIVE_SURFIX    = ""
    WINDOWS_DIR_SEP             = "\\"
    
    UNIX_EXECUTIVE_PREFIX       = ""
    UNIX_EXECUTIVE_SURFIX       = ""
    UNIX_DIR_SEP                = "/"
    
    BOWTIE2_BUILD               = "bowtie2-build"
    BOWTIE2_ALIGN               = "bowtie2"
    
    BOWTIE2_BUILD_PAR_NTHREAD   = "--threads"
    
    
    
    
class SequencingExtractionParameters:
    def __init__(   self, 
                    bowtie2_dir : str = "",
                    sratools_dir : str = "",
                    bowtie2_index_name : str = "TestTemplate",
                    bowtie2_build_index_thread_num : int = 4):
        self.bowtie2_dir = bowtie2_dir
        self.sratools_dir = sratools_dir
        self.bowtie2_index_name = bowtie2_index_name
        self.bowtie2_build_index_thread_num = bowtie2_build_index_thread_num
        
        self.use_shell = False
        
        self.executive_prefix = ""
        self.executive_surfix = ""
        self.dir_sep = ""
        
    def check_os(self):
        if sys.platform == SequencingExtractionConstant.WINDOWS.value:
            self.executive_prefix = SequencingExtractionConstant.WINDOWS_EXECUTIVE_PREFIX.value
            self.executive_surfix = SequencingExtractionConstant.WINDOWS_EXECUTIVE_SURFIX.value
            self.dir_sep = SequencingExtractionConstant.WINDOWS_DIR_SEP.value
            self.bowtie2_dir.replace(SequencingExtractionConstant.UNIX_DIR_SEP.value,self.dir_sep)
            self.sratools_dir.replace(SequencingExtractionConstant.UNIX_DIR_SEP.value,self.dir_sep)
            self.use_shell = True
        else:
            self.executive_prefix = SequencingExtractionConstant.UNIX_EXECUTIVE_PREFIX.value
            self.executive_surfix = SequencingExtractionConstant.UNIX_EXECUTIVE_SURFIX.value
            self.dir_sep = SequencingExtractionConstant.UNIX_DIR_SEP.value
            self.bowtie2_dir.replace(SequencingExtractionConstant.WINDOWS_DIR_SEP.value,self.dir_sep)
            self.sratools_dir.replace(SequencingExtractionConstant.WINDOWS_DIR_SEP.value,self.dir_sep)
            self.use_shell = False
        
        if not self.bowtie2_dir.endswith(self.dir_sep) and self.bowtie2_dir != "":
            self.bowtie2_dir = self.bowtie2_dir + self.dir_sep
        if not self.sratools_dir.endswith(self.dir_sep) and self.sratools_dir != "":
            self.sratools_dir = self.sratools_dir + self.dir_sep
            
    def get_bowtie2_build_executive_path(self):
        return(self.bowtie2_dir + self.executive_prefix + SequencingExtractionConstant.BOWTIE2_BUILD.value + self.executive_surfix)
    def get_bowtie2_align_executive_path(self):
        return(self.bowtie2_dir + self.executive_prefix + SequencingExtractionConstant.BOWTIE2_ALIGN.value + self.executive_surfix)


            
class SequencingExtractionOutputs:
    def __init__(self):
        pass

class SequencingExtraction(s_module_template.SequencingModule):
    def __init__(self, owner, parameters = SequencingExtractionParameters()):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results()
        self.parameters = parameters
        self.parameters.check_os()
        self.results = SequencingExtractionOutputs()
        
        
    def prepare_data(self):
        #Prepare bowtie2 index
        self.create_bowtie2_index()

        
    def create_bowtie2_index(self):
        executive_path = self.parameters.get_bowtie2_build_executive_path()
        thread_par = SequencingExtractionConstant.BOWTIE2_BUILD_PAR_NTHREAD.value
        nthread = str(self.parameters.bowtie2_build_index_thread_num)
        fasta_path = self.s_retrieval_results.fasta_path
        bowtie2_index_name = self.parameters.bowtie2_index_name
        command = [executive_path, thread_par, nthread, fasta_path, bowtie2_index_name]
        print(command)
        subprocess.run(command, stdout=subprocess.PIPE, shell = self.parameters.use_shell)
        
    def align_data(self):
        self.data = None #Fake
    
    def infer_stranded_information(self):
        self.data = None #Fake
        
    def complete_data_dependent_metadata(self):
        self.data = None #Fake