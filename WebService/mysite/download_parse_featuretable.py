import sys
import json
import subprocess
import pandas as pd
   
if __name__ == "__main__":
    ftpurl = sys.argv[1]
    tag_id = sys.argv[2]
    
    #Download gff first
    try:
        subprocess.check_output(['ref-download-featuretable', ftpurl, tag_id+'.txt',tag_id])
    except:
        raise Exception

    cur_result = json.load(open(tag_id,'r'))   
    data_table = pd.read_csv(tag_id+'.txt',sep="\t",index_col=False,low_memory=False)
    data_table = data_table[data_table['# feature']=='CDS']
    
    def extract_feature_tag(x):
        if pd.isnull(x['locus_tag']):
            return x['symbol']
        else:
            return x['locus_tag']

    new_data_table = data_table[['name','symbol','GeneID','assembly','chromosome','genomic_accession']]
    feature_tag = data_table[['symbol','locus_tag']].apply(lambda x: extract_feature_tag(x), axis=1)
    new_data_table = pd.concat([feature_tag,new_data_table],axis=1)
    new_data_table = new_data_table.rename(columns={0:'feature_tag'})
    new_data_table = new_data_table.drop_duplicates()
    new_data_table.to_csv(tag_id+'_parsed.csv',index=False)
    cur_result['output_parsed_feature_table'] = 1
    json.dump(cur_result,open(tag_id,'w'))

    
