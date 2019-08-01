#Parse GFF3 Files
#Only for valid GFF3 files only (from RefSeq), rejected if the gff3 is invalid
import pandas as pd
from enum import Enum, auto

from . import t_gff_exceptions

class GeneAnnotationConstants(Enum):
    SEP = '\t'
    


class GFF3Symbol(Enum):
    COMMENT = "#"
    EQUAL = "="
    ATTRIBUTESEPERATOR = ";"
    BLANK = " "

class GFF3Header(Enum):
    SEQID = auto()
    SOURCE = auto()
    TYPE = auto()
    START = auto()
    END = auto()
    SCORE = auto()
    STRAND = auto()
    PHASE = auto()
    ATTRIBUTES = auto()
    
class GFF3Type(Enum):
    GENE = "gene"
    CDS = "CDS"
    SEQUENCE = "sequence"
    
class BEDHeader(Enum):
    #UCSC BED6 FORMAT
    CHROMOSOME  = auto() #->SEQID in GFF3
    START       = auto() #->START in GFF3
    STOP        = auto() #->END in GFF3
    ID          = auto() #->ATTRIBUTES.LOCUSTAG in GFF3
    SCORE       = auto() #->SCORE in GFF3
    STRAND      = auto() #->STRAND in GFF3
    #The remaining part is the same as GFF3
    SOURCE      = auto()
    TYPE        = auto()
    PHASE       = auto()
    ATTRIBUTES = auto()
    
    
class GFF3AttributesHeader(Enum):
    NAME = "Name"
    GENESYNONYM = "gene_synonym"
    LOCUSTAG = "locus_tag"

class GeneAnnotation:
    def __init__(   self, 
                    file_paths : list = [],
                    output_bed : str = 'gene_annotation.bed',
                    output_gff : str = 'gene_annotation.gff',
                    target_type = GFF3Type.CDS.value,
                    used_id = GFF3AttributesHeader.LOCUSTAG.value):
        self.file_paths = list(set(file_paths)) #Take the unique file list
        self.gff3_data = None
        self.gff3_data_target_type = None
        self.target_type = target_type
        self.used_id = used_id
        
        self.gene_annotation_bed_file = output_bed
        self.gene_annotation_gff_file = output_gff
        
    def read_file(self):
        #Initialize the gff3_data
        self.parse_refseq()
        self.parse_attributes()
        self.extract_target_type_entries()
        
    def parse_refseq(self):
        for file_path in self.file_paths:
            if self.gff3_data is None:
                self.gff3_data = pd.read_table(file_path, comment = GFF3Symbol.COMMENT.value, names = [e.name for e in GFF3Header])
            else:
                cur_data = pd.read_table(file_path, comment = GFF3Symbol.COMMENT.value, names = [e.name for e in GFF3Header])
                self.gff3_data = pd.concat([self.gff3_data,cur_data])
        
    def parse_attributes(self):
        try:
            attributes = pd.DataFrame("", index = self.gff3_data.index, columns = [e.name for e in GFF3AttributesHeader])
            for index, row in self.gff3_data.iterrows():
                extracted_fields = self.parse_fields(row[GFF3Header.ATTRIBUTES.name],[e.value for e in GFF3AttributesHeader])
                for e in GFF3AttributesHeader:
                    attributes[e.name][index] = extracted_fields[e.value]
                    
                    
            self.gff3_data = pd.concat([self.gff3_data,attributes],axis=1)
            
        except Exception as e:
            raise t_gff_exceptions.FailedToExtractGFF3Attributes('Failed to extract GFF3 attributes.\n \
                Make sure this is the GFF3 file from NCBI genome database and the the genome is from RefSeq database.')
                
    def parse_fields(self, input:str, patterns:list) -> dict:
        result = {}
        for pattern in patterns:
            result[pattern] = ""
            
        for s in input.split(GFF3Symbol.ATTRIBUTESEPERATOR.value):
            s2 = s.split(GFF3Symbol.EQUAL.value)
            for pattern in patterns:
                if s2[0].replace(GFF3Symbol.BLANK.value,"") == pattern: 
                    #A = B: if A is the field we want, return B
                    #No Blank should be left
                    result[pattern] = s2[1].replace(GFF3Symbol.BLANK.value,"")
                
        return result
        
    def extract_target_type_entries(self):
        idx = self.gff3_data[GFF3Header.TYPE.name] == self.target_type
        self.gff3_data_target_type = self.gff3_data.loc[idx]
        
    def output_bed_file(self):
        bed_format_data = pd.DataFrame("", index = self.gff3_data_target_type.index, columns = [e.name for e in BEDHeader])
        for index, row in self.gff3_data_target_type.iterrows():
            #UCSC BED6 Parts
            bed_format_data[BEDHeader.CHROMOSOME.name][index] = row[GFF3Header.SEQID.name]
            bed_format_data[BEDHeader.START.name][index] = row[GFF3Header.START.name]
            bed_format_data[BEDHeader.STOP.name][index] = row[GFF3Header.END.name]
            bed_format_data[BEDHeader.ID.name][index] = row[GFF3AttributesHeader.LOCUSTAG.name]
            bed_format_data[BEDHeader.SCORE.name][index] = row[GFF3Header.SCORE.name]
            bed_format_data[BEDHeader.STRAND.name][index] = row[GFF3Header.STRAND.name]
            #Other fields
            bed_format_data[BEDHeader.SOURCE.name][index] = row[GFF3Header.SOURCE.name]
            bed_format_data[BEDHeader.TYPE.name][index] = row[GFF3Header.TYPE.name]
            bed_format_data[BEDHeader.PHASE.name][index] = row[GFF3Header.PHASE.name]
            bed_format_data[BEDHeader.ATTRIBUTES.name][index] = row[GFF3Header.ATTRIBUTES.name]
        
        #Sort it according to START Column
        bed_format_data = bed_format_data.sort_values(by=[BEDHeader.START.name])
        try:
            #Output:
            bed_format_data.to_csv(self.gene_annotation_bed_file,
                                    sep = GeneAnnotationConstants.SEP.value,
                                    index = False,
                                    header = False)
        except Exception as e:
            raise t_gff_exceptions.FailedToOutputBEDFile('Failed to generate gene annotation file in BED format')
            
    def output_gff_file(self):
        gff_format_data = pd.DataFrame("", index = self.gff3_data_target_type.index, columns = [e.name for e in GFF3Header])
        for index, row in self.gff3_data_target_type.iterrows():
            for e in GFF3Header:
                gff_format_data[e.name][index] = row[e.name]
        
        #Sort it according to START Column
        gff_format_data = gff_format_data.sort_values(by=[GFF3Header.START.name])
        try:
            #Output:
            gff_format_data.to_csv(self.gene_annotation_gff_file,
                                    sep = GeneAnnotationConstants.SEP.value,
                                    index = False,
                                    header = False)
        except Exception as e:
            raise t_gff_exceptions.FailedToOutputGFFFile('Failed to generate gene annotation file in GFF format')
            
            
    def get_genome_id(self) -> list:
        return list(set(list(self.gff3_data[GFF3Header.SEQID.name])))
        
    def get_bed_file_path(self) -> str:
        return self.gene_annotation_bed_file
        
    def get_gff_file_path(self) -> str:
        return self.gene_annotation_gff_file
        
    def get_target_type(self) -> str:
        return self.target_type
        
    def get_used_id(self) -> str:
        return self.used_id
        
        
    