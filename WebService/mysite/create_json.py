import json
import sys
if __name__=="__main__":
    id_tag = sys.argv[1]
    test_result = {'id_tag': None,
            'pid': 0,
            'curr_size': 0.0,
            'curr_perc': 0.0,
            'parse_gff': 0.0,
            'parse_attributes': 0.0,
            'extract_target_type_entries': 0.0,
            'output_parsed_gff': 0.0}
    json.dump(test_result,open(id_tag,'w'))
