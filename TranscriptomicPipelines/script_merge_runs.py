import pickle
import sys
from transcriptomic_pipeline import GeneralParameters
from transcriptomic_pipeline import GeneralConstant
'''
from sequencing_pipeline import *

if (sys.version_info < (3, 0)):
    sys.path.insert(0, "sequencing")
    from s_sample_mapping import *
else:
    from sequencing.s_sample_mapping import *'''

if __name__ == "__main__":
    sample_mapping_worker = pickle.load(open(sys.argv[1], 'rb'))

    sample_mapping_worker.do_run()

    sample_mapping_worker.results.done = True
    pickle.dump(sample_mapping_worker.results, open(sys.argv[2], 'wb'))
