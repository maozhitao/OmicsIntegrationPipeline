import sys
if (sys.version_info < (3, 0)):
    sys.path.insert(0, "validation")
    import supervised
    import unsupervised
    import v_module_template
else:
    import validation.supervised as supervised
    import validation.unsupervised as unsupervised
    import validation.v_module_template as v_module_template

class ValidationPipeline(v_module_template.ValidationModule):
    def __init__(self, owner):
        self.owner = owner
        self.supervised_validation = supervised.SupervisedValidation(self)
        self.unsupervised_validation = unsupervised.UnsupervisedValidation(self)
        
    def run_validation_pipeline(self):
        self.unsupervised_validation.validate_data()