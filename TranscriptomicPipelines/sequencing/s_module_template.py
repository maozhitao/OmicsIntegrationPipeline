
class SequencingModule:
    def __init__(self, owner):
        self.owner = owner
        
    def get_s_query_id(self):
        return self.owner.get_s_query_id()
        
    def get_t_metadata(self):
        return self.owner.get_t_metadata()
        
    def set_t_metadata(self,metadata):
        return self.owner.set_t_metadata(metadata)
        
    def get_t_gene_annotation(self):
        return self.owner.get_t_gene_annotation()
        
    def get_general_parameters(self):
        return self.owner.get_general_parameters()
        
    def get_general_constant(self):
        return self.owner.get_general_constant()
        
class SequencingSubModule(SequencingModule):
    def __init__(self, owner):
        self.owner = owner
        
    def get_bowtie2_parameters(self):
        return self.owner.get_bowtie2_parameters()
    
    def get_sratool_parameters(self):
        return self.owner.get_sratool_parameters()
        
    def get_rseqc_parameters(self):
        return self.owner.get_rseqc_parameters()
        
    def get_htseq_parameters(self):
        return self.owner.get_htseq_parameters()