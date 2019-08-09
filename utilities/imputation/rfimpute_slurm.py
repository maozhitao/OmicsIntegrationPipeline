#Missing Value Imputation Class
#Each feature should be separated for parallel design
#SLURM Wrapper

#To submit the work, we have to:
#1. Prepare the parameters
#2. Create the input file
#3. Submit the jobs
#4. Collect the jobs results and then remove the intermediate files

#Finally the job submission will be:
#sbatch ...(parameters)... ...(target python script)... ...(input_arguments)...

class SlurmImputationParameters:
    def __init__(self):
        self.par_num_node = '-N'
        self.num_node = 1
        self.par_num_core_each_node = '-n'
        self.num_core_each_node = 1
        self.par_time_limit = '--time'
        self.time_limit_hr = 10
        self.time_limit_min = 0
        self.par_job_name = '-J'
        self.job_name = "Imputation"
        self.par_output = '-o'
        self.output_ext = ".output"
        self.par_error = '-e'
        self.error_ext = ".error"
        
        self.script_path = "imputation_script.py"

class SlurmMissForestImputation:
    def __init__(self):
        self.parameters = SlurmImputationParameters()
        
    def slurm_miss_forest_imputation(self, matrix, missing_ind, num_missing_value_order, convergence_criteria):
        #matrix should be initially imputed!
        
        #Should define the convergence criteria
        while True:
            #Create the work for each feature
            
            #Wait the work for each feature: polling here! (TRICKY)
            
            #update the matrix
            
            #check the criterion, if meet the criteria, exit
            pass
        
        pass
        
    def slurm_miss_forest_imputation_single_feature(self, x_train, y_train, x_pred, feature_idx):
        #prepare x_train, y_train, x_pred as input file
        
        pass
