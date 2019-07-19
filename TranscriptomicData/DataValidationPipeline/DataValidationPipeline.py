import SupervisedValidation
import UnsupervisedValidation

class DataValidationPipeline:
    def __init__(self):
        self.supervised_validation_module = SupervisedValidation.SupervisedValidationModule()
        self.unsupervised_validation_module = UnsupervisedValidation.UnsupervisedValidationModule()