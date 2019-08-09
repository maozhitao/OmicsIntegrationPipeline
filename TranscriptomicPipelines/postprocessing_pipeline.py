import postprocessing.concatenation as concatenation
import postprocessing.imputation as imputation
import postprocessing.normalization as normalization
import postprocessing.p_module_template as p_module_template

class PostprocessingPipeline(p_module_template.PostprocessingModule):
    def __init__(self, owner):
        self.owner = owner
        self.data_concatenation = concatenation.Concatenation(self)
        self.data_imputation = imputation.Imputation(self)
        self.data_normalization = normalization.Normalization(self)