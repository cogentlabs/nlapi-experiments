from __future__ import print_function

import os
import pickle as p

import numpy as np
from PyDictionary import PyDictionary

import constants as c
import logic
import utils.nl_api as nl


def validate_query(actual, expected):
    precision_list = []
    for expected_chunk in expected.split():
        precision_list.append(expected_chunk in actual)

    # penalize it when we go wrong.
    penalizer_list = []
    for predicted_chunk in actual.split():
        penalizer_list.append(predicted_chunk not in expected)

    precision = np.mean(precision_list)
    penalizer = np.mean(penalizer_list)
    accuracy = precision - penalizer
    if accuracy < 0:
        accuracy = 0
    print('PRED = {}, EXPECTED = {}, ACC = {}'.format(actual, expected, accuracy))
    return accuracy


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
        print('______________________')
        print('Sentence = {}'.format(nl_api_element['sentences'][0]['text']['content']))
        predicted_query = logic.build_query(nl_api_element)
        precisions.append(validate_query(predicted_query, queries[i]))

    print('\n______________________\nFINAL PRECISION IS {}'.format(np.mean(precisions)))
