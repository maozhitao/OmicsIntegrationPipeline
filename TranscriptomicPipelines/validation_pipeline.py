import validation.supervised as supervised
import validation.unsupervised as unsupervised

class DataValidationPipeline:
    def __init__(self):
        self.supervised_validation = supervised.SupervisedValidation()
        self.unsupervised_validation = unsupervised.UnsupervisedValidation()