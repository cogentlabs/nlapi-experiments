from __future__ import print_function

import numpy as np
import requests as r
import os
from constants import *


def validate_query(actual, expected):
    precision_term = np.mean([(v in actual) for v in expected.split()])
    regularization_term = np.mean([(v not in expected) for v in actual.split()])
    score = precision_term - regularization_term
    if score < 0.0:
        score = 0.0
    if DEBUG:
        print('PRED = {}, EXPECTED = {}, SCORE = {}'.format(actual, expected, score))
    return score


def reverse_directed_graph(nl_api_json):
    directed_graph = dict()
    root_index = None
    for i, token in enumerate(nl_api_json['tokens']):
        directed_graph[i] = token['dependencyEdge']['headTokenIndex']
        if token['dependencyEdge']['label'] == u'ROOT':
            root_index = i  # can have some cycles even though it's not ROOT

    if root_index is None:
        raise Exception('ROOT tag is not present.')

    reverse_graph = {}
    for k, v in directed_graph.iteritems():
        reverse_graph[v] = reverse_graph.get(v, [])
        reverse_graph[v].append(k)

    reverse_graph[root_index].remove(root_index)
    return {'reverse_directed_graph': reverse_graph, 'ROOT': root_index}


def extract_original_sentence(nlapi_elt):
    return nlapi_elt['sentences'][0]['text']['content'].lower()


def extract_relevant_entities(nlapi_elt):
    entity_list = []
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()
            entity_list.append(entity_name)
    return entity_list


def build(tag, val):
    val = val.lower()
    if tag is None:
        return ' {}'.format(val)
    return ' {}:{}'.format(tag, val.replace(' ', '-'))


def call_nl_api(text):
    key = os.environ.get('GOOGLE_API_KEY')
    if key is None:
        print('The env variable GOOGLE_API_KEY is not defined.')
        print('export GOOGLE_API_KEY=<key>')
        print('Program will exit.')
        exit(1)
    annotate_text_json = get_annotate_text(text, key)
    return dict(annotate_text_json.items())


def get_entities(text, key):
    url = 'https://language.googleapis.com/v1alpha1/documents:analyzeEntities?key={}'.format(key)
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': 'UTF8',
    }
    return trigger_post_query(url, data)


def get_annotate_text(text, key):
    url = 'https://language.googleapis.com/v1alpha1/documents:annotateText?key={}'.format(key)
    data = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extractSyntax': True,
            'extractEntities': True,
            'extractDocumentSentiment': True
        },
        'encoding_type': 'UTF8',
    }
    return trigger_post_query(url, data)


def trigger_post_query(url, data):
    if DEBUG:
        print('URL = {}, DATA = {}'.format(url, data))
    out = r.post(url, json=data)
    return out.json()
