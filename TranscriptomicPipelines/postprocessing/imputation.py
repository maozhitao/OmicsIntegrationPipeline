import sys
if (sys.version_info < (3, 0)):
    import p_module_template
else:
    from . import p_module_template
    
#RF Impute
#NOTE: Later this part should become a independent package so that we should import it directly
sys.path.insert(0,"../utilities/imputation")
import rfimpute

from enum import Enum
import pandas as pd

import os

class ImputationOptions(Enum):
    AVERAGE = "average"
    ZERO    = "zero"
    KNN     = "knn"
    RF      = "random_forest"


class ImputationParameters:
    def __init__(   self,
                    imputed_data_matrix_path = "ImputedDataMatrix.csv"):
        self.imputation_options = ImputationOptions.RF.value
        self.imputed_data_matrix_path = imputed_data_matrix_path
        
        self.skip_imputation = True
       
        
    def get_imputed_data_matrix_path(self):
        return self.imputed_data_matrix_path

    
class Imputation(p_module_template.PostprocessingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = ImputationParameters()
        self.rfimpute = rfimpute.MissForestImputation()
        
    def impute_data_matrix(self):
        t_compendium_collections = self.get_t_compendium_collections()
        #Parameter configuration:
        self.rfimpute.parameters.parallel_options = rfimpute.ParallelOptions.LOCAL.value #FOR TESTING
        
        merged_data_matrix = t_compendium_collections.get_merged_data_matrix()

        if self.parameters.skip_imputation == False or self.check_existed_imputation_results() == False:
            
            if self.parameters.imputation_options == ImputationOptions.RF.value:
                imputed_data_matrix = self.rfimpute.miss_forest_imputation(merged_data_matrix)
            
            imputed_data_matrix = pd.DataFrame(data = imputed_data_matrix, index = merged_data_matrix.index, columns = merged_data_matrix.columns)
            
        else:
            imputed_data_matrix = pd.read_csv(self.parameters.imputed_data_matrix_path,index_col = 0)

        
        t_compendium_collections.set_imputed_data_matrix(imputed_data_matrix, 
                                                        self.parameters.imputation_options,
                                                        self.parameters.imputed_data_matrix_path)
        
        t_compendium_collections.output_imputed_data_matrix()
    def check_existed_imputation_results(self):
        if not os.path.isfile(self.parameters.imputed_data_matrix_path):
            return False
        else:
            return True
        
        
    
        