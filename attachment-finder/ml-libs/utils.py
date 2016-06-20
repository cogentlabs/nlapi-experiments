import commands
import json

import numpy as np

from constants import DEBUG


def validate_query(actual, expected, debug=DEBUG):
    precision_term = np.mean([(v in actual) for v in expected.split()])
    regularization_term = np.mean([(v not in expected) for v in actual.split()])
    score = precision_term - regularization_term
    if score < 0.0:
        score = 0.0
    if debug:
        print('PRED = {}, EXPECTED = {}, SCORE = {}'.format(actual, expected, score))
    return score


def call_nl_api(text):
    cmd = 'cd utils; export GOOGLE_API_KEY=AIzaSyBs_VIYtRfZY7nQpjIBSSS9auNVI-Cq1N8; ' \
          'echo \"{}\" > tmp.txt; node nl.js -f tmp.txt; rm tmp.txt'.format(text)
    print('[NL API] Query : {}'.format(cmd))
    out = commands.getstatusoutput(cmd)[1]
    nl_api_json = json.loads(out)
    return nl_api_json


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
    if tag is None:  # KEYWORD => tag.
        return ' {}'.format(val)
    return ' {}:{}'.format(tag, val.replace(' ', '-'))
