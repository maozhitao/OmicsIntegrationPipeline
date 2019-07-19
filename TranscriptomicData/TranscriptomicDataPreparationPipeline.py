import MicroarrayDataPreparationPipeline.MicroarrayDataPreparationPipeline
import SequencingDataPreparationPipeline.SequencingDataPreparationPipeline
import DataPostprocessingPipeline.DataPostprocessingPipeline
import DataValidationPipeline.DataValidationPipeline

class TranscriptomicDataPreparationPipeline:
    def __init__(self):
        self.microarray_data_preparation_pipeline = MicroarrayDataPreparationPipeline.MicroarrayDataPreparationPipeline.MicroarrayDataPreparationPipeline()
        self.sequencing_data_preparation_pipeline = SequencingDataPreparationPipeline.SequencingDataPreparationPipeline.SequencingDataPreparationPipeline()
        self.data_postprocessing_pipeline = DataPostprocessingPipeline.DataPostprocessingPipeline.DataPostprocessingPipeline()
        self.data_validation_pipeline = DataValidationPipeline.DataValidationPipeline.DataValidationPipeline()