from __future__ import print_function

import os
import pickle as p

import numpy as np
from PyDictionary import PyDictionary

import logic
import utils as nl
from constants import *

if __name__ == '__main__':

    with open(EXPECTED_QUERIES_FILENAME, 'r') as f:
        queries = f.readlines()
        queries = [line.rstrip('\n') for line in queries]

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    KEYWORD_SYNONYMS_DICT = dict()
    for keyword in ['send']:
        KEYWORD_SYNONYMS_DICT[keyword] = KEYWORD_SYNONYMS_DICT.get(keyword, [])
        for synonym in PyDictionary().synonym(keyword.lower()):
            KEYWORD_SYNONYMS_DICT[keyword].append(synonym)

    if USE_PREVIOUS_CALLS_FROM_API and os.path.isfile(TMP_FILENAME):
        nlapi_obj = p.load(open(TMP_FILENAME, 'r'))
    else:
        nlapi_obj = []
        with open(SENTENCES_FILENAME, 'r') as f:
            sentences = f.readlines()
            sentences = [line.rstrip('\n') for line in sentences]
            for sentence in sentences:
                nlapi_obj.append(nl.call_nl_api(sentence))

        p.dump(nlapi_obj, open(TMP_FILENAME, 'w'))

    precisions = []
    for i, nl_api_element in enumerate(nlapi_obj):
        print('______________________')
        print('Sentence = {}'.format(nl_api_element['sentences'][0]['text']['content']))
        predicted_query = logic.build_query(nl_api_element)
        precisions.append(nl.validate_query(predicted_query, queries[i]))

    final_precision = np.mean(precisions)
    print('\n______________________\nFINAL PRECISION IS {}'.format(final_precision))

    if np.abs(final_precision - 0.97011) > 0.00001:
        print('FAIL!')
    else:
        print('OKAY!')
