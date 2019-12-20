import ast
import csv

class ExtractorConst(object):

    SEP_EXT = '.'
    SEP_PATH = '/'

    PATH_DATA_DIR = 'data'

    FILE_EXT  = 'csv'
    FILE_SAMPLE_COL_IDX = 11

class Extractor(object):

    def __init__(self):
        self.metadata = None

    def load_metadata(self, term):
        with open(
                ExtractorConst.SEP_PATH.join([
                    ExtractorConst.PATH_DATA_DIR,
                    ExtractorConst.SEP_EXT.join([term, ExtractorConst.FILE_EXT])]),
                'r') as f:
            reader = csv.reader(f)
            next(reader)
            self.metadata = list(reader)

    def get_sample_column(self):
        sample_col = []

        for row in self.metadata:
            sample_col.append(ast.literal_eval(row[ExtractorConst.FILE_SAMPLE_COL_IDX]))
        return sample_col

    def _get_srx_list_batch(self, sample_list):
        srx_list = []

        for sample in sample_list:
            if type(sample) is str:
                pass
            elif type(sample) is tuple:
                _, srx = sample
                srx_list.append(srx)
        return srx_list

    def get_srx_list(self, sample_col):
        srx_list = []

        for sample_list in sample_col:
            srx_list.extend(self._get_srx_list_batch(sample_list))
        return srx_list

    def extract(self, term):
        self.load_metadata(term)
        sample_col  = self.get_sample_column()
        srx_list    = self.get_srx_list(sample_col)
        return list(set(srx_list))

if __name__ == '__main__':

    disease = 'stroke'

    extractor = Extractor()
    srx_list = extractor.extract(disease)

    validate_list = [
        'SRX501844',
        'SRX501845',
        'SRX501846',
        'SRX501847',
        'SRX501848',
        'SRX501849',
        'SRX501850',
        'SRX501851',
        'SRX501852',
        'SRX501853',
        'SRX501854',
        'SRX501855',
        'SRX501856',
        'SRX5027114',
        'SRX5027115',
        'SRX5027116',
        'SRX5027117',
        'SRX5027118',
        'SRX5027119',
        'SRX5027120',
        'SRX5027121',
        'SRX5027122',
        'SRX5027123',
        'SRX5027124',
        'SRX5027125',
        'SRX5027126',
        'SRX5027127',
        'SRX5027128',
        'SRX7131021',
        'SRX7131022',
        'SRX7131023',
        'SRX7131024',
        'SRX7131025',
        'SRX7131026',
        'SRX5717122',
        'SRX5717123',
        'SRX5717124',
        'SRX5717125',
        'SRX5717126',
        'SRX5717127',
        'SRX5717128',
        'SRX5717129']

    non_include = []

    for srx in validate_list:
        if not srx in srx_list:
            non_include.append(srx)

    print(non_include)
    print(len(non_include))