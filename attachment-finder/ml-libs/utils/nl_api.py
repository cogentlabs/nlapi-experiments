from __future__ import print_function

import commands
import json


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
    return {'reverse_directed_graph': reverse_graph, 'ROOT': root_index}
