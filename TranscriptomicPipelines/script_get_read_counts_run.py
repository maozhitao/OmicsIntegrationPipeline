import pickle
import sys
from transcriptomic_pipeline import GeneralParameters
from transcriptomic_pipeline import GeneralConstant
'''
from sequencing_pipeline import *

if (sys.version_info < (3, 0)):
    sys.path.insert(0, "sequencing")
    from s_value_extraction import *
else:
    from sequencing.s_value_extraction import *'''

if __name__ == "__main__":
    value_extraction_worker = pickle.load(open(sys.argv[1], 'rb'))

    value_extraction_worker.do_run()
    value_extraction_worker.results.done = True
    print("DONE!")
    print(sys.argv[2])
    pickle.dump(value_extraction_worker.results, open(sys.argv[2], 'wb'))
