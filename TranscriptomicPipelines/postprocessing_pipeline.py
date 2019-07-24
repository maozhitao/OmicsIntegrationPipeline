import postprocessing.concatenation as concatenation
import postprocessing.imputation as imputation
import postprocessing.normalization as normalization
import postprocessing.postprocessing_module_template as postprocessing_module_template

class PostprocessingPipeline(postprocessing_module_template.PostprocessingModule):
    def __init__(self, owner):
        self.owner = owner
        self.data_concatenation = concatenation.Concatenation()
        self.data_imputation = imputation.Imputation()
        self.data_normalization = normalization.Normalization()