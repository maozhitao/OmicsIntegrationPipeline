import sys
if (sys.version_info < (3, 0)):
    import p_module_template
else:
    from . import p_module_template

from enum import Enum
import pandas as pd
import numpy as np

class NormalizationOptions(Enum):
    QUANTILE = "quantile"


class NormalizationParameters:
    def __init__(   self,
                    normalized_data_matrix_path = "NormalizedDataMatrix.csv"):
        self.normalization_options = NormalizationOptions.QUANTILE.value
        self.normalized_data_matrix_path = normalized_data_matrix_path
       
        
    def get_normalized_data_matrix_path(self):
        return self.normalized_data_matrix_path

    
class Normalization(p_module_template.PostprocessingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = NormalizationParameters()
        
        self.configure_parameter_set()
        
    def configure_parameter_set(self):
        parameter_set = self.get_parameter_set()
        self.parameters.normalization_options       = parameter_set.p_normalization_parameters_normalization_option
        self.parameters.normalized_data_matrix_path = parameter_set.p_normalization_parameters_normalized_data_matrix_path
        
    def normalize_data_matrix(self):
        if self.parameters.normalization_options == NormalizationOptions.QUANTILE.value:
            self.normalize_data_matrix_quantile()
            
    def normalize_data_matrix_quantile(self):
        #Reference: https://intellipaat.com/community/5641/quantile-normalization-on-pandas-dataframe
        #The direction is the same as preprocessCore in R
        t_compendium_collections = self.get_t_compendium_collections()
        imputed_data_matrix = t_compendium_collections.get_imputed_data_matrix()
        rank_mean = imputed_data_matrix.stack().groupby(imputed_data_matrix.rank(method='first').stack().astype(int)).mean()
        #Update (20191210): take care of tie value, which is necessary when zeros appear:

        normalized_data_matrix = imputed_data_matrix
        for col in list(imputed_data_matrix):
            sorted_rank = imputed_data_matrix.rank()[col].sort_values()
            sorted_rank_unique = imputed_data_matrix.rank()[col].sort_values().unique()
            for cur_rank in sorted_rank_unique:
                idx = np.where(imputed_data_matrix.rank()[col] == cur_rank)[0] #idx to be assinged
                idx2 = np.where(sorted_rank == cur_rank)[0] #idx to be extracted from rank_mean

                new_val = np.mean(rank_mean.iloc[idx2])
                normalized_data_matrix[col].iloc[idx] = new_val

        t_compendium_collections.set_normalized_data_matrix(normalized_data_matrix, 
                                                        self.parameters.normalization_options,
                                                        self.parameters.normalized_data_matrix_path)
        t_compendium_collections.output_normalized_data_matrix()
