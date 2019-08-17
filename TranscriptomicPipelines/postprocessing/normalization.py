import sys
if (sys.version_info < (3, 0)):
    import p_module_template
else:
    from . import p_module_template

class Normalization(p_module_template.PostprocessingSubModule):
    def __init__(self, owner):
        self.owner = owner