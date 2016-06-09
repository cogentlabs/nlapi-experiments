from __future__ import print_function

import os
import pickle as p

import numpy as np
from PyDictionary import PyDictionary

import constants as c
import utils.nl_api as nl


def build_query(nl_api_elt):
    return "has:attachment"


def validate_query(actual, expected):
    precision_list = []
    for predicted_chunk in expected.split():
        precision_list.append(predicted_chunk in actual)
    precision = 0
    if len(precision_list) != 0:
        precision = np.mean(precision_list)
    print('PRED = {}, EXPECTED = {}, PRECISION = {}'.format(actual, expected, precision))
    return precision


if __name__ == '__main__':

    dictionary = PyDictionary()
    KEYWORDS = ['send']

    with open(c.EXPECTED_QUERIES_FILENAME, 'r') as f:
        queries = f.readlines()
        queries = [line.rstrip('\n') for line in queries]

    KEYWORD_SYNONYMS_DICT = dict()
    for keyword in KEYWORDS:
        KEYWORD_SYNONYMS_DICT[keyword] = KEYWORD_SYNONYMS_DICT.get(keyword, [])
        for synonym in dictionary.synonym(keyword.lower()):
            KEYWORD_SYNONYMS_DICT[keyword].append(synonym)

    if c.USE_PREVIOUS_CALLS_FROM_API and os.path.isfile(c.TMP_FILENAME):
        nl_api_elements = p.load(open(c.TMP_FILENAME, 'r'))
    else:
        nl_api_elements = []
        with open(c.SENTENCES_FILENAME, 'r') as f:
            sentences = f.readlines()
            sentences = [line.rstrip('\n') for line in sentences]
            for sentence in sentences:
                nl_api_elements.append(nl.call_nl_api(sentence))

        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        p.dump(nl_api_elements, open(c.TMP_FILENAME, 'w'))

    precisions = []
    for i, nl_api_element in enumerate(nl_api_elements):
        print('Sentence : {}'.format(nl_api_element['sentences'][0]['text']['content']))
        predicted_query = build_query(nl_api_element)
        precisions.append(validate_query(predicted_query, queries[i]))
    print('\n______________________\nFINAL PRECISION IS {}'.format(np.mean(precisions)))
