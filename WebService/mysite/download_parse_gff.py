import t_gff
import sys
import json
import subprocess

def parse_gff(gene_annotation, tag_id):
    cur_result = json.load(open(tag_id,'r'))
    gene_annotation.parse_refseq()
    cur_result['parse_gff'] = 1
    json.dump(cur_result,open(tag_id,'w'))

    cur_result = json.load(open(tag_id,'r'))
    gene_annotation.parse_attributes()
    cur_result['parse_attribute'] = 1
    json.dump(cur_result,open(tag_id,'w'))

    cur_result = json.load(open(tag_id,'r'))
    gene_annotation.extract_target_type_entries()
    cur_result['extract_target_type_entries'] = 1
    json.dump(cur_result,open(tag_id,'w'))


   
if __name__ == "__main__":
    ftpurl = sys.argv[1]
    tag_id = sys.argv[2]
    
    #Download gff first
    try:
        subprocess.check_output(['ref-download', ftpurl, tag_id+'.gff',tag_id])
    except:
        raise Exception
   
    try:
        gene_annotation = t_gff.GeneAnnotation(file_paths = [tag_id+'.gff'],
                                            output_bed = tag_id+'_parsed.bed',
                                            output_gff = tag_id+'_parsed.gff')

        parse_gff(gene_annotation, tag_id)       

    except:
        try:
            gene_annotation = t_gff.GeneAnnotation(file_paths = [tag_id+'.gff'],
                                            output_bed = tag_id+'_parsed.bed',
                                            output_gff = tag_id+'_parsed.gff',
                                            target_type = t_gff.GFF3Type.GENE.value,
                                            used_id = t_gff.GFF3AttributesHeader.LOCUSTAG.value)

            parse_gff(gene_annotation, tag_id)
        except:
            raise Exception
    
    cur_result = json.load(open(tag_id,'r'))
    gene_annotation.gff3_data.to_csv(tag_id+'_parsed.csv',index=False)
    cur_result['output_parsed_gff'] = 1
    json.dump(cur_result,open(tag_id,'w'))

    
