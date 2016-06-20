from __future__ import print_function

import os
import pickle as p

import numpy as np

import logic
import utils as nl
from constants import *

if __name__ == '__main__':

    with open(TEST_EXPECTED_QUERIES_FILENAME, 'r') as f:
        queries = f.readlines()
        queries = [line.rstrip('\n') for line in queries]

    if not os.path.exists(TEST_TMP_DIR):
        os.makedirs(TEST_TMP_DIR)

    if TEST_USE_PREVIOUS_CALLS_FROM_API and os.path.isfile(TEST_TMP_FILENAME):
        nl_api_obj = p.load(open(TEST_TMP_FILENAME, 'r'))
    else:
        nl_api_obj = []
        with open(TEST_SENTENCES_FILENAME, 'r') as f:
            sentences = f.readlines()
            sentences = [line.rstrip('\n') for line in sentences]
            for sentence in sentences:
                nl_api_obj.append(nl.call_nl_api(sentence))
        p.dump(nl_api_obj, open(TEST_TMP_FILENAME, 'w'))

    precisions = []
    for i, nl_api_element in enumerate(nl_api_obj):
        print('______________________')
        print('Sentence = {}'.format(nl_api_element['sentences'][0]['text']['content']))
        predicted_query = logic.build_query(nl_api_element)
        precisions.append(nl.validate_query(predicted_query, queries[i]))
    final_precision = np.mean(precisions)
    print('______________________\nFINAL SCORE IS {}. MAX is 1. MIN is 0.'.format(final_precision))
