from . import s_module_template
from . import s_value_extraction_exceptions

from enum import Enum
import sys
import subprocess
import os
import pandas as pd


class SequencingExtractionConstant(Enum):
    NEWLINE                     = '\n'
    TABSEP                      = '\t'
    SPACE                       = ' '
    PERCENT                     = '%'
    EXT_PAIR_1                  = '_1.fastq.gz'
    EXT_PAIR_2                  = '_2.fastq.gz'
    EXT_SINGLE                  = '.fastq.gz'
    EXT_ALIGN_OUT               = '.sam'
    WRITEMODE                   = 'wb'
    SINGLE_PAIREDTYPE           = 'SingleEnd'
    PAIRED_PAIREDTYPE           = 'PairEnd'
    STRANDEDTYPE                = 'STRANDED'
    UNSTRANDEDTYPE              = 'UNSTRANDED'
    STRANDED_MODE               = 'yes'
    UNSTRANDED_MODE             = 'no'
    COUNT_NO_FEATURE            = '__no_feature'
    COUNT_AMBIGUOUS             = '__ambiguous'
    COUNT_TOO_LOW_AQUAL         = '__too_low_aQual'
    COUNT_NOT_ALIGNED           = '__not_aligned'
    COUNT_ALIGNMENT_NOT_UNIQUE  = '__alignment_not_unique'
    
    
    
class SequencingExtractionParameters:
    def __init__(self, owner, fastq_file_dir : str = ".", 
                    alignment_record_file_ext : str = ".align_out",
                    infer_experiment_record_file_ext : str = ".infer_experiment_out",
                    infer_experiment_threshold : float = 0.9,
                    count_reads_file_ext : str = '.count_reads'):
        self.owner = owner
        self.fastq_file_dir = fastq_file_dir
        self.alignment_record_file_ext = alignment_record_file_ext
        self.infer_experiment_record_file_ext = infer_experiment_record_file_ext
        self.infer_experiment_threshold = infer_experiment_threshold
        self.count_reads_file_ext = count_reads_file_ext
        
        general_parameters = self.owner.get_general_parameters()
        if self.fastq_file_dir == "":
            raise s_value_extraction_exceptions.InvalidFastqFilePathException('You should provide the directory for saving fastq data!')
        if not self.fastq_file_dir.endswith(general_parameters.dir_sep):
            self.fastq_file_dir = self.fastq_file_dir + general_parameters.dir_sep
            
    def get_fastqdump_command(self, input_sra : str = ''):
        sratool_parameters = self.owner.get_sratool_parameters()
        
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = sratool_parameters.dir + general_parameters.executive_prefix + sratool_parameters.fastqdump_exe_file + general_parameters.executive_surfix
        input_sra = input_sra
        fastqdump_par_gzip = sratool_parameters.fastqdump_par_gzip
        fastqdump_par_split3 = sratool_parameters.fastqdump_par_split3
        fastqdump_par_dir = sratool_parameters.fastqdump_par_output_dir
        fastqdump_dir = self.fastq_file_dir
        command = [executive_path, input_sra, fastqdump_par_gzip, fastqdump_par_split3, fastqdump_par_dir, fastqdump_dir]
        return(command)
        
        
    def get_bowtie2_build_command(self, input_fasta : str = ''):
        bowtie2_parameters = self.owner.get_bowtie2_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = bowtie2_parameters.dir + general_parameters.executive_prefix + bowtie2_parameters.build_exe_file + general_parameters.executive_surfix
        thread_par = bowtie2_parameters.build_par_nthreads
        nthread = str(bowtie2_parameters.build_nthreads)
        fasta_path = input_fasta
        bowtie2_index_name = bowtie2_parameters.build_index_name
        command = [executive_path, thread_par, nthread, fasta_path, bowtie2_index_name]
        return(command)
        
    def get_bowtie2_align_command(self, input_sra : str = ''):
        bowtie2_parameters = self.owner.get_bowtie2_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = bowtie2_parameters.dir + general_parameters.executive_prefix + bowtie2_parameters.align_exe_file + general_parameters.executive_surfix
        
        #Performance Parameters
        thread_par = bowtie2_parameters.align_par_nthreads
        nthread = str(bowtie2_parameters.align_nthreads)
        reorder_par = bowtie2_parameters.align_par_reorder
        mm_par = bowtie2_parameters.align_par_mm
        
        align_mode_par = bowtie2_parameters.align_mode
        align_speed_par = bowtie2_parameters.align_speed
        
        #Bowtie2IndexPath
        index_par = bowtie2_parameters.align_par_index_name
        bowtie2_index_name = bowtie2_parameters.build_index_name
        
        #Output
        sam_par = bowtie2_parameters.align_par_sam
        output_path = input_sra + SequencingExtractionConstant.EXT_ALIGN_OUT.value
        #Check Paired or Single
        file_paired_1 = input_sra + SequencingExtractionConstant.EXT_PAIR_1.value
        file_paired_2 = input_sra + SequencingExtractionConstant.EXT_PAIR_2.value
        file_single = input_sra + SequencingExtractionConstant.EXT_SINGLE.value
        
        if os.path.isfile(file_paired_1) and os.path.isfile(file_paired_2):
            paired_1_par = bowtie2_parameters.align_par_paired_1
            paired_2_par = bowtie2_parameters.align_par_paired_2
            command = [executive_path, thread_par, nthread, reorder_par, mm_par, 
                        align_mode_par, align_speed_par,
                        index_par, bowtie2_index_name,
                        paired_1_par, file_paired_1, paired_2_par, file_paired_2,
                        sam_par, output_path]
            return(command)
        elif os.path.isfile(file_single):
            unpaired_par = bowtie2_parameters.align_par_unpaired
            command = [executive_path, thread_par, nthread, reorder_par, mm_par, 
                        align_mode_par, align_speed_par,
                        index_par, bowtie2_index_name,
                        unpaired_par, file_single,
                        sam_par, output_path]
            return(command)
        else:
            raise s_value_extraction_exceptions.FastqFileNotFoundException('Fastq file not fouund!')


    def get_rseqc_infer_experiment_command(self, input_sra : str = ''):
        rseqc_parameters = self.owner.get_rseqc_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = rseqc_parameters.dir + general_parameters.executive_prefix + rseqc_parameters.infer_experiment_exe_file + general_parameters.executive_surfix
        bed_par = rseqc_parameters.infer_experiment_par_bed
        bed_path = self.owner.get_t_gene_annotation().get_bed_file_path()
        input_par = rseqc_parameters.infer_experiment_par_input
        input_path = input_sra + SequencingExtractionConstant.EXT_ALIGN_OUT.value
        
        command = [executive_path, bed_par, bed_path, input_par, input_path]
        return(command)
        
    def get_htseq_count_command(self, input_sra : str = '', stranded = True):
        htseq_parameters = self.owner.get_htseq_parameters()
        general_parameters = self.owner.get_general_parameters()
        
        executive_path = htseq_parameters.dir + general_parameters.executive_prefix + htseq_parameters.htseq_count_exe_file + general_parameters.executive_surfix
        input_path = input_sra + SequencingExtractionConstant.EXT_ALIGN_OUT.value
        gff_path = self.owner.get_t_gene_annotation().get_gff_file_path()
        target_type_par = htseq_parameters.htseq_count_par_target_type
        target_type = self.owner.get_t_gene_annotation().get_target_type()
        used_id_par = htseq_parameters.htseq_count_par_used_id
        used_id = self.owner.get_t_gene_annotation().get_used_id()
        quiet_par = htseq_parameters.htseq_count_par_quiet
        stranded_par = htseq_parameters.htseq_count_par_stranded
        
        if stranded:
            stranded_mode = SequencingExtractionConstant.STRANDED_MODE.value
        else:
            stranded_mode = SequencingExtractionConstant.UNSTRANDED_MODE.value
        
        
        command = [executive_path, input_path, gff_path, target_type_par, target_type, used_id_par, used_id, quiet_par, stranded_par, stranded_mode]
        return(command)
        
        
        
class SequencingExtractionResults:
    def __init__(self):
        self.alignment_rate = {}
        self.infer_experiment_result = {}
        self.count_reads_result = {}
        
    def update_alignment_rate(self, run, alignment_rate_run):
        self.alignment_rate[run] = alignment_rate

    def update_infer_experiment_result(self, run, infer_experiment_result_run):
        self.infer_experiment_result[run] = infer_experiment_result_run
        
    def update_count_reads_result(self, run, count_reads_result_run):
        self.count_reads_result[run] = count_reads_result_run
        
class InferExperimentResults:
    def __init__(self, paired_type, ratio_failed, ratio_direction1, ratio_direction2, stranded_info):
        self.paired_type = paired_type
        self.ratio_failed = ratio_failed
        self.ratio_direction1 = ratio_direction1
        self.ratio_direction2 = ratio_direction2
        self.stranded_info = stranded_info
        
    def check_stranded_info(self):
        if self.stranded_info == SequencingExtractionConstant.STRANDEDTYPE.value:
            return True
        else:
            return False

class SequencingExtraction(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_retrieval_results = owner.get_s_data_retrieval_results()
        self.parameters = SequencingExtractionParameters(self)
        self.results = SequencingExtractionResults()
        
    def get_parameters(self):
        return self.parameters
        
    def get_results(self):
        return self.results
        
    def prepare_data(self):
        #Prepare bowtie2 index
        self.create_bowtie2_index()
        #self.prepare_fastq_file()
        self.get_t_gene_annotation().output_bed_file() #For infer strand
        self.get_t_gene_annotation().output_gff_file() #For htseq count

    def create_bowtie2_index(self):
        command = self.parameters.get_bowtie2_build_command(self.s_retrieval_results.fasta_path)
        subprocess.run(command, stdout=subprocess.PIPE, shell = self.get_general_parameters().use_shell)
        
    def prepare_fastq_file(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                self.prepare_fastq_file_run(run)
                    
    def prepare_fastq_file_run(self, run):
        command = self.parameters.get_fastqdump_command(self.s_retrieval_results.sra_file_dir + run)
        try:
            binary_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = self.get_general_parameters().use_shell)
        except Exception as e:
            raise s_value_extraction_exceptions.FastqdumpFailedException('Failed to run fastqdump')
        
        try:
            output = binary_output.decode(self.get_general_constant().CODEC.value)
            output = output.split(SequencingExtractionConstant.NEWLINE.value)
            line_n_read = output[-3]
            line_n_write = output[-2]
            
            n_read = int(line_n_read.split(SequencingExtractionConstant.SPACE.value)[1])
            n_write = int(line_n_write.split(SequencingExtractionConstant.SPACE.value)[1])

            if n_read != n_write:
                raise s_value_extraction_exceptions.FastqdumpFailedException('n_read != n_write')
            
        except Exception as e:
            raise s_value_extraction_exceptions.FastqdumpFailedException('Error output from fastqdump')
            
    def align_data(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                self.align_data_run(run)
                
    def align_data_run(self, run):
        command = self.parameters.get_bowtie2_align_command(self.s_retrieval_results.sra_file_dir + run)
        try:
            binary_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = self.get_general_parameters().use_shell)
        except Exception as e:
            raise s_value_extraction_exceptions.Bowtie2AlignmentFailedException('Failed to run Bowtie2 alignment')
            
        try:
            output = binary_output.decode(self.get_general_constant().CODEC.value)
            output = output.split(SequencingExtractionConstant.NEWLINE.value)
            
            line_overall_alignment_rate = output[-2]
            alignment_rate = float(line_overall_alignment_rate.split(SequencingExtractionConstant.PERCENT.value)[0])
            if alignment_rate < 0 or alignment_rate > 100:
                raise s_value_extraction_exceptions.Bowtie2AlignmentFailedException('Invalid Bowtie2 alignment results')
        except Exception as e:
            raise s_value_extraction_exceptions.Bowtie2AlignmentFailedException('Invalid Bowtie2 alignment results')
            
        if not os.path.isfile(self.s_retrieval_results.sra_file_dir + run + SequencingExtractionConstant.EXT_ALIGN_OUT.value):
            raise s_value_extraction_exceptions.Bowtie2AlignmentFailedException('SAM output file not exist!')
            
        with open(self.s_retrieval_results.sra_file_dir + run + self.parameters.alignment_record_file_ext, SequencingExtractionConstant.WRITEMODE.value) as outfile:
            outfile.write(binary_output)
            
        self.results.update_alignment_rate(run, alignment_rate)
            
    def infer_stranded_information(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                self.infer_stranded_information_run(run)
    
    def infer_stranded_information_run(self, run):
        command = self.parameters.get_rseqc_infer_experiment_command(self.s_retrieval_results.sra_file_dir + run)
        try:
            binary_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = self.get_general_parameters().use_shell)
        except Exception as e:
            raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Failed to run RSeQC infer_experiment.py')
        
        try:
            output = binary_output.decode(self.get_general_constant().CODEC.value)
            output = output.split(SequencingExtractionConstant.NEWLINE.value)
            
            paired_type = output[-5].split(SequencingExtractionConstant.SPACE.value)[2]
            if paired_type != SequencingExtractionConstant.SINGLE_PAIREDTYPE.value and paired_type != SequencingExtractionConstant.PAIRED_PAIREDTYPE.value:
                raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Invalid RSeQC infer_experiment results')
            
            ratio_failed = float(output[-4].split(SequencingExtractionConstant.SPACE.value)[-1])
            if ratio_failed < 0 or ratio_failed > 1:
                raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Invalid RSeQC infer_experiment results')
            
            ratio_direction1 = float(output[-3].split(SequencingExtractionConstant.SPACE.value)[-1])
            if ratio_direction1 < 0 or ratio_direction1 > 1:
                raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Invalid RSeQC infer_experiment results')
            
            ratio_direction2 = float(output[-2].split(SequencingExtractionConstant.SPACE.value)[-1])
            if ratio_direction2 < 0 or ratio_direction2 > 1:
                raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Invalid RSeQC infer_experiment results')
            
            if ratio_direction1 > self.parameters.infer_experiment_threshold or ratio_direction2 > self.parameters.infer_experiment_threshold:
                stranded_info = SequencingExtractionConstant.STRANDEDTYPE.value
            else:
                stranded_info = SequencingExtractionConstant.UNSTRANDEDTYPE.value
                
            infer_experiment_result_run = InferExperimentResults(paired_type, ratio_failed, ratio_direction1, ratio_direction2, stranded_info)
            
            
        except Exception as e:
            raise s_value_extraction_exceptions.RSeQCInferExperimentFailedException('Invalid RSeQC infer_experiment results')
            
        
        with open(self.s_retrieval_results.sra_file_dir + run + self.parameters.infer_experiment_record_file_ext, SequencingExtractionConstant.WRITEMODE.value) as outfile:
            outfile.write(binary_output)
        
        self.results.update_infer_experiment_result(run, infer_experiment_result_run)
        
    def check_stranded_info(self, run):
        infer_experiment_result = self.results.infer_experiment_result
        return infer_experiment_result[run].check_stranded_info()
        
    def count_reads(self):
        for exp in self.s_retrieval_results.mapping_experiment_runs:
            for run in self.s_retrieval_results.mapping_experiment_runs[exp]:
                self.count_reads_run(run)
        
    def count_reads_run(self, run):
        stranded = self.check_stranded_info(run)
        command = self.parameters.get_htseq_count_command(self.s_retrieval_results.sra_file_dir + run, stranded)
        print(command)
        
        try:
            binary_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = self.get_general_parameters().use_shell)
        except Exception as e:
            raise s_value_extraction_exceptions.HTSeqCountFailedException('Failed to run htseq-count')
            
        try:
            output = binary_output.decode(self.get_general_constant().CODEC.value)
            count_reads_result_run = pd.DataFrame([x.split(SequencingExtractionConstant.TABSEP.value) for x in output.split(SequencingExtractionConstant.NEWLINE.value)])
            count_reads_result_run = count_reads_result_run.set_index(0)
            count_reads_result_run.rename(columns={1:run})
            
            output = output.split(SequencingExtractionConstant.NEWLINE.value)
            print(output)
            
            no_feature_line = output[-6]
            print(no_feature_line)
            if not no_feature_line.startswith(SequencingExtractionConstant.COUNT_NO_FEATURE.value):
                raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
            
            ambiguous_line = output[-5]
            print(ambiguous_line)
            if not ambiguous_line.startswith(SequencingExtractionConstant.COUNT_AMBIGUOUS.value):
                raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
            
            too_low_aQual_line = output[-4]
            print(too_low_aQual_line)
            if not too_low_aQual_line.startswith(SequencingExtractionConstant.COUNT_TOO_LOW_AQUAL.value):
                raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
                
            not_aligned_line = output[-3]
            print(not_aligned_line)
            if not not_aligned_line.startswith(SequencingExtractionConstant.COUNT_NOT_ALIGNED.value):
                raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
                
            alignment_not_unique_line = output[-2]
            print(alignment_not_unique_line)
            if not alignment_not_unique_line.startswith(SequencingExtractionConstant.COUNT_ALIGNMENT_NOT_UNIQUE.value):
                raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
                
        except Exception as e:
            raise s_value_extraction_exceptions.HTSeqCountFailedException('Invalid htseq-count results')
        
        with open(self.s_retrieval_results.sra_file_dir + run + self.parameters.count_reads_file_ext, SequencingExtractionConstant.WRITEMODE.value) as outfile:
            outfile.write(binary_output)
            
        self.results.update_count_reads_result(run,count_reads_result_run)
            
    def complete_data_dependent_metadata(self):
        self.data = None #Fake
        
