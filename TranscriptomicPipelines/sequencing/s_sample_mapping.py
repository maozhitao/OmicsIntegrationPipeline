from . import s_module_template

class SequencingSampleMapping(s_module_template.SequencingModule):
    def __init__(self, owner):
        self.owner = owner
    
    def merge_different_run(self):
        self.data = None
        
    def merge_sample(self):
        self.data = None