import sys
if (sys.version_info < (3, 0)):
    import v_module_template
else:
    from . import v_module_template
    
import numpy as np
import pandas as pd

import os

#RF Impute
#NOTE: Later this part should become a independent package so that we should import it directly
sys.path.insert(0,"../utilities/imputation")
import rfimpute
    
class UnsupervisedValidationParameters:
    def __init__(   self, n_trial = 10,
                    noise_ratio = np.arange(0,1.1,0.1),
                    missing_value_ratio = np.arange(0.3,0.8,0.1),
                    unsupervised_validation_results_path = "UnsupervisedValidationResults.csv"):
        self.n_trial = n_trial
        self.noise_ratio = noise_ratio
        self.missing_value_ratio = missing_value_ratio
        self.unsupervised_validation_results_path = unsupervised_validation_results_path
        
        self.skip_validate_data = True
       
    def get_unsupervised_validation_results_path(self):
        return self.unsupervised_validation_results_path
    
    
class UnsupervisedValidation(v_module_template.ValidationSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.rfimpute = rfimpute.MissForestImputation()
        self.parameters = UnsupervisedValidationParameters()
        
    def validate_data(self):
        if self.parameters.skip_validate_data == False or self.check_existed_result() == False:
            self.rfimpute.parameters.parallel_options = rfimpute.ParallelOptions.LOCAL.value #FOR TESTING
            
            t_compendium_collections = self.get_t_compendium_collections()
            normalized_data_matrix = t_compendium_collections.get_normalized_data_matrix()
            normalized_data_matrix_nparray = np.array(normalized_data_matrix)
            std = np.std(normalized_data_matrix_nparray)
            mean = np.mean(normalized_data_matrix_nparray)
            
            results = np.zeros((len(self.parameters.noise_ratio), len(self.parameters.missing_value_ratio)))
            
            for i in range(self.parameters.n_trial):
                print("Trial : " + str(i))
                cur_results = np.zeros((len(self.parameters.noise_ratio), len(self.parameters.missing_value_ratio)))
                noise = np.random.normal(mean,std,normalized_data_matrix_nparray.shape)
                
                for j in range(len(self.parameters.noise_ratio)):
                    noise_ratio = self.parameters.noise_ratio[j]
                    cur_matrix = noise*noise_ratio + normalized_data_matrix_nparray*(1-noise_ratio)
                    
                    for k in range(len(self.parameters.missing_value_ratio)):
                        missing_value_ratio = self.parameters.missing_value_ratio[k]
                        missing_value_index = []
                        cur_matrix_missing = np.copy(cur_matrix)
                        n_missing_value_each_col = np.round(missing_value_ratio*cur_matrix.shape[0]).astype(int)
                        for colidx in range(cur_matrix.shape[1]):
                            cur_misi = np.random.choice(cur_matrix.shape[0],n_missing_value_each_col,replace = False)
                            cur_matrix_missing[cur_misi,colidx] = np.nan
                            missing_value_index.append(cur_misi)
                            
                        imputed_cur_matrix = self.rfimpute.miss_forest_imputation(cur_matrix_missing)
                        
                        correct_values = []
                        imputed_values = []
                        for colidx in range(cur_matrix.shape[1]):
                            correct_values.extend(cur_matrix[missing_value_index[colidx],colidx].tolist())
                            imputed_values.extend(imputed_cur_matrix[missing_value_index[colidx],colidx].tolist())
                        
                        cur_results[j,k] = np.mean(np.abs(np.array(imputed_values) - np.array(correct_values)))
                        
                results = results + cur_results
            
            results = results/self.parameters.n_trial
            
            results = pd.DataFrame(results, index = self.parameters.noise_ratio.tolist(), columns = self.parameters.missing_value_ratio.tolist())
            results.to_csv(self.parameters.unsupervised_validation_results_path)
        
    def check_existed_result(self):
        if not os.path.isfile(self.parameters.unsupervised_validation_results_path):
            return False
        else:
            return True
        
                    
                    
                    
                        
                        
                    
            
            