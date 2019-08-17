import sys
if (sys.version_info < (3, 0)):
    import s_module_template
    import s_gene_mapping_exceptions
else:
    from . import s_module_template
    from . import s_gene_mapping_exceptions

class SequencingGeneMappingParameters:
    def __init__(self, owner, 
                    drop_unnamed_genes = False,
                    data_matrix_table_path = 'SequencingDataMatrix.csv',
                    gene_mapping_table_path = 'SequencingGeneMappingTable.csv'
                ):
        self.owner = owner
        self.drop_unnamed_genes = drop_unnamed_genes
        self.data_matrix_table_path = data_matrix_table_path
        self.gene_mapping_table_path = gene_mapping_table_path
        
class SequencingGeneMappingResults:
    def __init__(self):
        self.original_data_matrix = None
        
    def update_original_data_matrix(self, original_data_matrix):
        self.original_data_matrix = original_data_matrix

class SequencingGeneMapping(s_module_template.SequencingSubModule):
    def __init__(self, owner):
        self.owner = owner
        self.s_sample_mapping_results = owner.get_s_sample_mapping_results()
        self.parameters = SequencingGeneMappingParameters(self)
        self.results = SequencingGeneMappingResults()
        
    def map_gene(self):
        gene_mapping_table = self.owner.get_t_gene_annotation().get_gene_mapping_table()
        colname_id = self.owner.get_t_gene_annotation().get_gene_mapping_table_colname_id()
        colname_gene_name = self.owner.get_t_gene_annotation().get_gene_mapping_table_colname_gene_name()
        
        gene_mapping_table_selected = gene_mapping_table[[colname_id,colname_gene_name]]
        try:
            gene_mapping_table_selected.to_csv(self.parameters.gene_mapping_table_path)
        except Exception as e:
            raise s_gene_mapping_exceptions.FailedToWriteGeneMappingTable('Failed to write gene mapping table!')
        
        gene_mapping_table_selected_dict = {}
        for index, row in gene_mapping_table_selected.iterrows():
            gene_mapping_table_selected_dict[row[colname_id]] = row[colname_gene_name]
        
        count_reads_matrix = self.s_sample_mapping_results.count_reads_matrix
        indices = count_reads_matrix.index.tolist()
        for i in range(len(indices)):
            indices[i] = self.find_gene_name(indices[i], gene_mapping_table_selected_dict)
            
        count_reads_matrix.index = indices
        self.results.update_original_data_matrix(count_reads_matrix)
        
        
        #Update the compendium part
        s_data = self.get_s_data()
        s_data.update_ori_data_matrix(count_reads_matrix, self.parameters.data_matrix_table_path)
        s_data.output_ori_data_matrix()

            
    def find_gene_name(self, index, gene_mapping_table_dict):
        if gene_mapping_table_dict[index] != "":
            return gene_mapping_table_dict[index]
        else:
            return index
            
            
        
        