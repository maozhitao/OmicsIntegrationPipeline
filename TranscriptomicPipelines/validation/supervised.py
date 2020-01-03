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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

    
class SupervisedValidationParameters:
    def __init__(   self, n_trial = 10,
                    noise_ratio = np.arange(0,1.1,0.1),
                    correlation_validation_results_path = "CorrelationValidationResults.csv",
                    correlation_validation_results_figure_path = "CorrelationValidationResults.png",
                    knowledge_capture_validation_results_path = "KnowledgeCaptureValidationResults.csv",
                    knowledge_capture_validation_results_figure_path = "KnowledgeCaptureValidationResults.png"):
        self.n_trial = n_trial
        self.noise_ratio = noise_ratio
        self.correlation_validation_results_path = correlation_validation_results_path
        self.correlation_validation_results_figure_path = correlation_validation_results_figure_path
        self.knowledge_capture_validation_results_path = knowledge_capture_validation_results_path
        self.knowledge_capture_validation_results_figure_path = knowledge_capture_validation_results_figure_path
       
    def get_correlation_validation_results_path(self):
        return self.correlation_validation_results_path
        
    def get_knowledge_capture_validation_results_path(self):
        return self.knowledge_capture_validation_results_path
        
class SupervisedValidation(v_module_template.ValidationSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = SupervisedValidationParameters()
        
        self.configure_parameter_set()
        
    def configure_parameter_set(self):
        parameter_set = self.get_parameter_set()
        self.parameters.n_trial                                     = parameter_set.v_supervised_parameters_n_trial
        self.parameters.noise_ratio                                 = parameter_set.v_supervised_parameters_noise_ratio
        self.parameters.correlation_validation_results_path         = parameter_set.v_supervised_parameters_correlation_validation_results_path
        self.parameters.knowledge_capture_validation_results_path   = parameter_set.v_supervised_parameters_knowledge_capture_validation_results_path
        
    def correlation_validation(self, input_corr_path):
        input_corr = pd.read_csv(input_corr_path)
        t_compendium_collections = self.get_t_compendium_collections()
        normalized_data_matrix = t_compendium_collections.get_normalized_data_matrix()
        normalized_data_matrix_nparray = np.array(normalized_data_matrix)
        std = np.std(normalized_data_matrix_nparray)
        mean = np.mean(normalized_data_matrix_nparray)
        
        
        target_curve_name = ["All","Same project","Same Condition","Across projects","Across conditions"]
        results = np.zeros((len(self.parameters.noise_ratio), len(target_curve_name)))
        
        split_exp_indice_project, split_exp_indice_cond = self.split_exp_indice(normalized_data_matrix.columns.tolist(), 
                                                                                input_corr)
        
        for i in range(self.parameters.n_trial):
            print("Trial : " + str(i))
            cur_results = np.zeros((len(self.parameters.noise_ratio), len(target_curve_name)))
            noise = self.get_noise(normalized_data_matrix_nparray)
            
            for j in range(len(self.parameters.noise_ratio)):
                noise_ratio = self.parameters.noise_ratio[j]
                cur_matrix = noise*noise_ratio + normalized_data_matrix_nparray*(1-noise_ratio)
                
                #Corr: ALL
                corr_all = np.corrcoef(np.transpose(cur_matrix))
                corr_all[np.isnan(corr_all) == True] = 0
                
                avg_corr_all = np.mean(corr_all)
                
                avg_expr_project = np.zeros((cur_matrix.shape[0], len(split_exp_indice_project)))
                sum_corr_project = 0
                n_element_corr_project = 0
                for k in range(len(split_exp_indice_project)):
                    if len(split_exp_indice_project[k]) > 1:
                        corr_this_project = np.corrcoef(np.transpose(cur_matrix[:,split_exp_indice_project[k]]))
                        corr_this_project[np.isnan(corr_this_project) == True] = 0
                        sum_corr_project = sum_corr_project + np.sum(np.sum(corr_this_project))
                        n_element_corr_project = n_element_corr_project + corr_this_project.shape[0]*corr_this_project.shape[1]
                    else:
                        corr_this_project = 1
                        sum_corr_project = sum_corr_project + 1
                        n_element_corr_project = n_element_corr_project + 1
                    avg_expr_project[:,k] = np.mean(cur_matrix[:,split_exp_indice_project[k]],axis=1)
                    
                avg_corr_project = sum_corr_project/n_element_corr_project
                
                corr_cross_project = np.corrcoef(np.transpose(avg_expr_project))
                corr_cross_project[np.isnan(corr_cross_project) == True] = 0
                avg_corr_cross_project = np.mean(corr_cross_project)
                
                avg_expr_cond = np.zeros((cur_matrix.shape[0],len(split_exp_indice_cond)))
                sum_corr_cond = 0
                n_element_corr_cond = 0
                for k in range(len(split_exp_indice_cond)):
                    if len(split_exp_indice_cond[k]) > 1:
                        corr_this_cond = np.corrcoef(np.transpose(cur_matrix[:,split_exp_indice_cond[k]]))
                        corr_this_cond[np.isnan(corr_this_cond) == True] = 0
                        sum_corr_cond = sum_corr_cond + np.sum(np.sum(corr_this_cond))
                        n_element_corr_cond = n_element_corr_cond + corr_this_cond.shape[0]*corr_this_cond.shape[1]
                    else:
                        corr_this_cond = 1
                        sum_corr_cond = sum_corr_cond + 1
                        n_element_corr_cond = n_element_corr_cond + 1
                    avg_expr_cond[:,k] = np.mean(cur_matrix[:,split_exp_indice_cond[k]],axis=1)
                    
                avg_corr_cond = sum_corr_cond/n_element_corr_cond
                
                corr_cross_cond = np.corrcoef(np.transpose(avg_expr_cond))
                corr_cross_cond[np.isnan(corr_cross_cond) == True] = 0
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
        
        fig = plt.figure()
        corr_plot = results.plot(
            title="Correlation validation results",
            xlim = (-0.1,1.5)
        )


        corr_plot.set(xlabel='noise ratio',ylabel='correlation')
        plt.savefig(self.parameters.correlation_validation_results_figure_path)
        plt.close(fig)
        
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
            split_exp_indice_project.append(self.get_indice(data_matrix_exp_name, input_corr_exp_name_this_project))
            
        for cond in input_corr_cond_name_unique:
            input_corr_exp_name_this_cond = input_corr_exp_name[np.where(input_corr_cond_name == cond)]
            split_exp_indice_cond.append(self.get_indice(data_matrix_exp_name, input_corr_exp_name_this_cond))
            
        return split_exp_indice_project, split_exp_indice_cond
            
    def get_indice(self, name, query_names):
        result = []
        for query_name in query_names:
            idx = np.where(name == query_name)[0][0]
            result.append(idx)
        return result
        
        
    def knowledge_capture_validation(self, input_grouping_file_path, input_related_gene_file_path):
        t_compendium_collections = self.get_t_compendium_collections()
        normalized_data_matrix = t_compendium_collections.get_normalized_data_matrix()
        normalized_data_matrix_nparray = np.array(normalized_data_matrix)
        
        data_matrix_exp_name = np.array(normalized_data_matrix.columns.tolist())
        data_matrix_gene_name = np.array(normalized_data_matrix.index.tolist())
        
        input_grouping = pd.read_csv(input_grouping_file_path)
        input_related_gene = pd.read_csv(input_related_gene_file_path)
        
        input_grouping_exp_name = np.array(input_grouping["exp_id"])
        input_grouping_indicator = np.array(input_grouping["indicator"]).astype(int)
        input_related_gene = np.array(input_related_gene["gene_list"])
        
        exp_name_0 = input_grouping_exp_name[np.where(input_grouping_indicator == 0)]
        exp_name_1 = input_grouping_exp_name[np.where(input_grouping_indicator == 1)]
        
        exp_indice_0 = self.get_indice(data_matrix_exp_name, exp_name_0)
        exp_indice_1 = self.get_indice(data_matrix_exp_name, exp_name_1)
        gene_indice = self.get_indice(data_matrix_gene_name, input_related_gene)
        

        
        ranking_dataset = self.knowledge_capture_validation_internal(normalized_data_matrix_nparray, exp_indice_0, exp_indice_1, gene_indice)
        ranking_dataset = np.expand_dims(ranking_dataset,axis=1)
        #Add Noise
        std = np.std(normalized_data_matrix_nparray)
        mean = np.mean(normalized_data_matrix_nparray)
        
        ranking_noise = np.zeros((len(gene_indice)+1, len(self.parameters.noise_ratio)))
        for i in range(self.parameters.n_trial):
            print("Trial : " + str(i))
            cur_ranking_noise = np.zeros((len(gene_indice)+1, len(self.parameters.noise_ratio)))
            noise = self.get_noise(normalized_data_matrix_nparray)
            
            for j in range(len(self.parameters.noise_ratio)):
                noise_ratio = self.parameters.noise_ratio[j]
                cur_matrix = noise*noise_ratio + normalized_data_matrix_nparray*(1-noise_ratio)
                cur_ranking_noise[:,j] = self.knowledge_capture_validation_internal(cur_matrix, exp_indice_0, exp_indice_1, gene_indice)
                
            ranking_noise = ranking_noise + cur_ranking_noise
            
        ranking_noise = ranking_noise/self.parameters.n_trial
        
        
        
        ref = np.expand_dims(np.linspace(0,len(data_matrix_gene_name),len(gene_indice)+1),axis=1)
        final_results = np.concatenate((ranking_noise,ref),axis=1)
        
        
        ratio = np.round((0.0+np.array(range(len(gene_indice)+1)))/len(gene_indice),2)
        final_results_columns = []
        final_results_columns.extend(np.round(self.parameters.noise_ratio,2))
        final_results_columns.extend(["ref"])
        final_results = pd.DataFrame(final_results, index = ratio, columns = final_results_columns)
        final_results.to_csv(self.parameters.knowledge_capture_validation_results_path)

        fig = plt.figure()

        ax = fig.add_axes([0,0,1,1])
        ax.set_title("Knowledge capture validation results")
        ax.set_xlabel('Rank')
        ax.set_ylabel('Ratio of targeted genes')
        for col in list(final_results):
            if col != "ref":
                p_val_kstest = stats.kstest( (final_results[col]+0.0)/len(data_matrix_gene_name), 'uniform', alternative='greater' )[1]
                p_val_kstest = np.format_float_scientific(p_val_kstest,trim='0',exp_digits=2,precision=3)
                ax.plot(final_results[col],final_results.index,linewidth=1,label=str(col) + ", p-val = " + str(p_val_kstest))
                ax.legend(loc='bottom right')
            else:
                ax.plot(final_results[col],final_results.index,'k--',linewidth=3,label="(control)")
                ax.legend(loc='bottom right',title="noise ratio")

        plt.savefig(self.parameters.knowledge_capture_validation_results_figure_path,bbox_inches='tight', pad_inches=0)
        plt.close(fig)



        
    def knowledge_capture_validation_internal(self, matrix, exp_indice_0, exp_indice_1, gene_indice):
        val_0 = np.mean(matrix[:,exp_indice_0],axis=1)
        val_1 = np.mean(matrix[:,exp_indice_1],axis=1)

        print(min(val_1))
        print(min(val_0))
        if (min(val_1) < 0):
            raise("!")
        if (min(val_0) < 0):
            raise("!!")
        
        fc = np.absolute(np.log((val_1+1e-5)/(val_0+1e-5))) #To Avoid nan
        ranking = len(fc) - fc.argsort().argsort()
        
        return np.sort(np.pad(ranking[gene_indice],(1,0),'constant',constant_values=(0)))
        
        
