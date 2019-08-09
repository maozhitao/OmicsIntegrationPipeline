#Missing Value Imputation Class
#Each feature should be separated for parallel design
from enum import Enum, auto
from . import rfimpute_slurm

class InitialGuessOptions(Enum):
    AVERAGE = auto()
    ZERO    = auto()
    
class ParallelOptions(Enum):
    SLURM   = auto()
    LOCAL   = auto()


class MissForestImputationParameters:
    def __init__(self):
        self.initial_guess = InitialGuessOptions.AVERAGE.value
        self.parallel_options = ParallelOptions.LOCAL.value
        self.num_core_local = 1

class MissForestImputation:
    def __init__(self):
        self.parameters = MissForestImputationParameters()
        self.slurm_instance = None

    def miss_forest_imputation(self, matrix_for_impute):
        #matrix_for_impute: a numpy matrix
        
        if self.parameters.parallel_options == ParallelOptions.LOCAL.value:
            self.slurm_instance = rfimpute_slurm.SlurmMissForestImputation()
        
        
    def get_num_missing_value_order(self, matrix_for_impute):
        pass
        
    def initial_guess(self, matrix_for_impute):
        pass