import postprocessing.concatenation as concatenation
import postprocessing.imputation as imputation
import postprocessing.normalization as normalization

class DataPostprocessingPipeline:
    def __init__(self):
        self.data_concatenation = concatenation.DataConcatenation()
        self.data_imputation = imputation.DataImputation()
        self.data_normalization = normalization.DataNormalization()