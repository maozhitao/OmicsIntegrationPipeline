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
    
class SupervisedValidationParameters:
    def __init__(   self, n_trial = 10,
                    noise_ratio = np.arange(0,1.1,0.1),
                    correlation_validation_results_path = "CorrelationValidationResults.csv",
                    knowledge_capture_validation_results_path = "KnowledgeCaptureValidationResults.csv"):
        self.n_trial = n_trial
        self.noise_ratio = noise_ratio
        self.correlation_validation_results_path = correlation_validation_results_path
        self.knowledge_capture_validation_results_path = knowledge_capture_validation_results_path
       
    def get_correlation_validation_results_path(self):
        return self.correlation_validation_results_path
        
    def get_knowledge_capture_validation_results_path(self):
        return self.knowledge_capture_validation_results_path
        
class SupervisedValidation(v_module_template.ValidationSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = SupervisedValidationParameters()
        
    def correlation_validation(self, input_corr_path):
        input_corr = pd.read_csv(input_corr_path)
        t_compendium_collections = self.get_t_compendium_collections()
        normalized_data_matrix = t_compendium_collections.get_normalized_data_matrix()
        normalized_data_matrix_nparray = np.array(normalized_data_matrix)
        std = np.std(normalized_data_matrix_nparray)
        mean = np.mean(normalized_data_matrix_nparray)
        
        
        target_curve_name = ["ALL","PROJECT","COND","CROSS_PROJECT","CROSS_COND"]
        results = np.zeros((len(self.parameters.noise_ratio), len(target_curve_name)))
        
        split_exp_indice_project, split_exp_indice_cond = self.split_exp_indice(normalized_data_matrix.columns.tolist(), 
                                                                                input_corr)
        
        for i in range(self.parameters.n_trial):
            print("Trial : " + str(i))
            cur_results = np.zeros((len(self.parameters.noise_ratio), len(target_curve_name)))
            noise = np.random.normal(mean,std,normalized_data_matrix_nparray.shape)
            
            for j in range(len(self.parameters.noise_ratio)):
                noise_ratio = self.parameters.noise_ratio[j]
                cur_matrix = noise*noise_ratio + normalized_data_matrix_nparray*(1-noise_ratio)
                
                #Corr: ALL
                corr_all = np.corrcoef(np.transpose(cur_matrix))
                corr_all[np.where(corr_all == np.nan)] = 0
                avg_corr_all = np.mean(corr_all)
                
                avg_expr_project = np.zeros((cur_matrix.shape[0], len(split_exp_indice_project)))
                sum_corr_project = 0
                n_element_corr_project = 0
                for k in range(len(split_exp_indice_project)):
                    if len(split_exp_indice_project[k]) > 1:
                        corr_this_project = np.corrcoef(np.transpose(cur_matrix[:,split_exp_indice_project[k]]))
                        corr_this_project[np.where(corr_this_project == np.nan)] = 0
                        sum_corr_project = sum_corr_project + np.sum(np.sum(corr_this_project))
                        n_element_corr_project = n_element_corr_project + corr_this_project.shape[0]*corr_this_project.shape[1]
                    else:
                        corr_this_project = 1
                        sum_corr_project = sum_corr_project + 1
                        n_element_corr_project = n_element_corr_project + 1
                    avg_expr_project[:,k] = np.mean(cur_matrix[:,split_exp_indice_project[k]],axis=1)
                    
                avg_corr_project = sum_corr_project/n_element_corr_project
                
                corr_cross_project = np.corrcoef(np.transpose(avg_expr_project))
                corr_cross_project[np.where(corr_cross_project == np.nan)] = 0
                avg_corr_cross_project = np.mean(corr_cross_project)
                
                avg_expr_cond = np.zeros((cur_matrix.shape[0],len(split_exp_indice_cond)))
                sum_corr_cond = 0
                n_element_corr_cond = 0
                for k in range(len(split_exp_indice_cond)):
                    if len(split_exp_indice_cond[k]) > 1:
                        corr_this_cond = np.corrcoef(np.transpose(cur_matrix[:,split_exp_indice_cond[k]]))
                        corr_this_cond[np.where(corr_this_cond == np.nan)] = 0
                        sum_corr_cond = sum_corr_cond + np.sum(np.sum(corr_this_cond))
                        n_element_corr_cond = n_element_corr_cond + corr_this_cond.shape[0]*corr_this_cond.shape[1]
                    else:
                        corr_this_cond = 1
                        sum_corr_cond = sum_corr_cond + 1
                        n_element_corr_cond = n_element_corr_cond + 1
                    avg_expr_cond[:,k] = np.mean(cur_matrix[:,split_exp_indice_cond[k]],axis=1)
                    
                avg_corr_cond = sum_corr_cond/n_element_corr_cond
                
                corr_cross_cond = np.corrcoef(np.transpose(avg_expr_cond))
                corr_cross_cond[np.where(corr_cross_cond == np.nan)] = 0
                avg_corr_cross_cond = np.mean(corr_cross_cond)
                
                cur_results[j,0] = avg_corr_all
                cur_results[j,1] = avg_corr_project
                cur_results[j,2] = avg_corr_cond
                cur_results[j,3] = avg_corr_cross_project
                cur_results[j,4] = avg_corr_cross_cond
                
            results = results + cur_results
        
        results = results/self.parameters.n_trial
        
        results = pd.DataFrame(results, index = self.parameters.noise_ratio.tolist(), columns = target_curve_name)
        results.to_csv(self.parameters.correlation_validation_results_path)
        
        
    def split_exp_indice(self, col_name, input_corr):
        data_matrix_exp_name = np.array(col_name)
        input_corr_exp_name = np.array(input_corr["exp_id"])
        input_corr_project_name = np.array(input_corr["series_id"])
        input_corr_cond_name = np.array(input_corr["cond_id"])
        
        input_corr_project_name_unique = list(set(input_corr["series_id"].tolist()))
        input_corr_cond_name_unique = list(set(input_corr["cond_id"].tolist()))
        
        split_exp_indice_project = []
        split_exp_indice_cond = []
        
        for project in input_corr_project_name_unique:
            input_corr_exp_name_this_project = input_corr_exp_name[np.where(input_corr_project_name == project)]
            split_exp_indice_project.append(self.get_exp_indice(data_matrix_exp_name, input_corr_exp_name_this_project))
            
        for cond in input_corr_cond_name_unique:
            input_corr_exp_name_this_cond = input_corr_exp_name[np.where(input_corr_cond_name == cond)]
            split_exp_indice_cond.append(self.get_exp_indice(data_matrix_exp_name, input_corr_exp_name_this_cond))
            
        return split_exp_indice_project, split_exp_indice_cond
            
    def get_exp_indice(self, data_matrix_exp_name, query_exp_name):
        result = []
        for exp_name in query_exp_name:
            idx = np.where(data_matrix_exp_name == exp_name)[0][0]
            result.append(idx)
        return result

        
        