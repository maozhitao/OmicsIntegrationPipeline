import postprocessing.concatenation as concatenation
import postprocessing.imputation as imputation
import postprocessing.normalization as normalization

class PostprocessingPipeline:
    def __init__(self):
        self.data_concatenation = concatenation.Concatenation()
        self.data_imputation = imputation.Imputation()
        self.data_normalization = normalization.Normalization()