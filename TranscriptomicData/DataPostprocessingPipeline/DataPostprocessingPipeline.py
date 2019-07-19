import DataConcatenation
import DataImputation
import DataNormalization

class DataPostprocessingPipeline:
    def __init__(self):
        self.data_concatenation_module = DataConcatenation.DataConcatenationModule()
        self.data_imputation_module = DataImputation.DataImputationModule()
        self.data_normalization_module = DataNormalization.DataNormalizationModule()