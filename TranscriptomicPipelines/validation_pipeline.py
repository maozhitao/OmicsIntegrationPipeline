import sys
if (sys.version_info < (3, 0)):
    sys.path.insert(0, "validation")
    import supervised
    import unsupervised
    import validation_module_template
else:
    import validation.supervised as supervised
    import validation.unsupervised as unsupervised
    import validation.validation_module_template as validation_module_template

class ValidationPipeline(validation_module_template.ValidationModule):
    def __init__(self, owner):
        self.owner = owner
        self.supervised_validation = supervised.SupervisedValidation()
        self.unsupervised_validation = unsupervised.UnsupervisedValidation()