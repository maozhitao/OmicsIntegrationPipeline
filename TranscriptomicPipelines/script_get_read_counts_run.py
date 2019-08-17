import pickle
import sys
from transcriptomic_pipeline import GeneralParameters
from transcriptomic_pipeline import GeneralConstant

if __name__ == "__main__":
    data_retrieval_worker = pickle.load(open(sys.argv[1], 'rb'))
    value_extraction_worker = pickle.load(open(sys.argv[2], 'rb'))

    data_retrieval_worker.do_run()
    value_extraction_worker.do_run()

    value_extraction_worker.results.done = True
    pickle.dump(value_extraction_worker.results, open(sys.argv[3], 'wb'))
