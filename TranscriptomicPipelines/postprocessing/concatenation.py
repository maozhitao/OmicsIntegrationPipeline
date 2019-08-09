from . import p_module_template

import pandas as pd

class ConcatenationParameters:
    def __init__(   self, owner, 
                    merged_metadata_table_path = "MergedMetadataTable.csv",
                    merged_data_matrix_path = "MergedDataMatrix.csv"):
        self.owner = owner
        self.merged_metadata_table_path = merged_metadata_table_path
        self.merged_data_matrix_path = merged_data_matrix_path
        
    def get_merged_metadata_table_path(self):
        return self.merged_metadata_table_path
        
    def get_merged_data_matrix_path(self):
        return self.merged_data_matrix_path

class Concatenation(p_module_template.PostprocessingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.parameters = ConcatenationParameters(self)
        
    def concat_compendium_to_t_compendium_collections(self, compendium_list):
        t_compendium_collections = self.get_t_compendium_collections()
        for compendium in compendium_list:
            t_compendium_collections.append_additional_compendium(compendium)
            
    def concat_old_compendium_collections_to_t_compendium_collections(self, old_compendium_collections = None):
        if not old_compendium_collections:
            return
        t_compendium_collections = self.get_t_compendium_collections()
        for compendium_in_old in old_compendium_collections.compendium_list:
            t_compendium_collections.append_additional_compendium(compendium_in_old)
    
    def concat_microarray_sequencing_compendium(self):
        m_compendium = self.get_m_compendium()
        s_compendium = self.get_s_compendium()
        
        self.concat_compendium_to_t_compendium_collections([m_compendium, s_compendium])
        
    def concat_compendium(self):
        t_compendium_collections = self.get_t_compendium_collections()
        t_compendium_collections.reset_compendium_list()
        self.concat_microarray_sequencing_compendium()
        self.concat_old_compendium_collections_to_t_compendium_collections()
        
        metadata_table_list = []
        data_matrix_list = []
        for compendium in t_compendium_collections.compendium_list:
            cur_metadata_table = compendium.get_metadata().metadata_table
            cur_data_matrix = compendium.get_data().ori_data_matrix #Can be changed later :)

            metadata_table_list.append(cur_metadata_table)
            data_matrix_list.append(cur_data_matrix)
            
        merged_metadata_table = pd.concat(metadata_table_list)
        merged_data_matrix = pd.concat(data_matrix_list, axis = 1)
        
        merged_metadata_table_path = self.parameters.get_merged_metadata_table_path()
        merged_data_matrix_path = self.parameters.get_merged_data_matrix_path()
        t_compendium_collections.set_merged_metadata_table(merged_metadata_table, merged_metadata_table_path)
        t_compendium_collections.set_merged_data_matrix(merged_data_matrix, merged_data_matrix_path)
        t_compendium_collections.output_merged_metadata_table()
        t_compendium_collections.output_merged_data_matrix()
        
        
        
        