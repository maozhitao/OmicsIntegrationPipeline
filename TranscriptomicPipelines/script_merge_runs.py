import pickle
import sys
from transcriptomic_pipeline import GeneralParameters
from transcriptomic_pipeline import GeneralConstant

if __name__ == "__main__":
    sample_mapping_worker = pickle.load(open(sys.argv[1], 'rb'))

    sample_mapping_worker.do_run()

    sample_mapping_worker.results.done = True
    pickle.dump(sample_mapping_worker.results, open(sys.argv[2], 'wb'))
