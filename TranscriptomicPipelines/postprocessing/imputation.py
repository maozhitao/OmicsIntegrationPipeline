from . import p_module_template

class Imputation(p_module_template.PostprocessingSubModule):
    def __init__(self, owner):
        self.owner = owner