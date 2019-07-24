from . import s_module_template

class SequencingGeneMapping(s_module_template.SequencingModule):
    def __init__(self, owner):
        self.owner = owner
        
    def map_gene(self):
        self.data = None