#Parse GFF3 Files
#Only for valid GFF3 files only (from RefSeq), rejected if the gff3 is invalid
import pandas as pd
from enum import Enum, auto


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
    
class GFF3AttributesHeader(Enum):
    NAME = "Name"
    GENESYNONYM = "gene_synonym"
    LOCUSTAG = "locus_tag"

class GeneAnnotation:
    def __init__(   self, 
                    file_paths : list = []):
        self.file_paths = list(set(file_paths)) #Take the unique file list
        self.gff3_data = None 
        
    def read_file(self):
        #Initialize the gff3_data
        self.parse_refseq()
        self.parse_attributes()

        
    def parse_refseq(self):
        for file_path in self.file_paths:
            if self.gff3_data is None:
                self.gff3_data = pd.read_table(file_path, comment = GFF3Symbol.COMMENT.value, names = [e.name for e in GFF3Header])
            else:
                cur_data = pd.read_table(file_path, comment = GFF3Symbol.COMMENT.value, names = [e.name for e in GFF3Header])
                self.gff3_data = pd.concat([self.gff3_data,cur_data])
        
    def parse_attributes(self):
        attributes = pd.DataFrame("", index = self.gff3_data.index, columns = [e.name for e in GFF3AttributesHeader])
        for index, row in self.gff3_data.iterrows():
            extracted_fields = self.parse_fields(row[GFF3Header.ATTRIBUTES.name],[e.value for e in GFF3AttributesHeader])
            for e in GFF3AttributesHeader:
                attributes[e.name][index] = extracted_fields[e.value]
                
                
        self.gff3_data = pd.concat([self.gff3_data,attributes],axis=1)
                
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
        
    def get_genome_id(self) -> list:
        return list(set(list(self.gff3_data[GFF3Header.SEQID.name])))