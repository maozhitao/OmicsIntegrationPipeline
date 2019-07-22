import microarray_pipeline
import sequencing_pipeline
import postprocessing_pipeline
import validation_pipeline

class TranscriptomicDataPreparationPipeline:
    def __init__(self):
        self.microarray_pipeline = microarray_pipeline.MicroarrayPipeline()
        self.sequencing_pipeline = sequencing_pipeline.SequencingPipeline()
        self.postprocessing_pipeline = postprocessing_pipeline.PostprocessingPipeline()
        self.validation_pipeline = validation_pipeline.ValidationPipeline()