def build_query(nl_api_elt):
    # print json.dumps(nl_api_elt, indent=2, sort_keys=True)
    result = ''
    result = layer_entities(nl_api_elt, result)
    result = layer_add_attachment_tag(result)
    result = layer_link_entities_to_from(nl_api_elt, result)
    result = filter_entities_already_indexed_by_to_from(nl_api_elt, result)
    result = temporal_keywords(nl_api_elt, result)
    result = layer_send_keyword(nl_api_elt, result)
    return result


def layer_send_keyword(nl_api_elt, res):
    return res


def temporal_keywords(nl_api_elt, res):
    sentence = nl_api_elt['sentences'][0]['text']['content']
    if 'yesterday' in sentence:
        res += build('newer_than', '1d')
    return res


def filter_entities_already_indexed_by_to_from(nl_api_elt, res):
    for entity in nl_api_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()

            if build('to', entity_name) in res and build('label', entity_name) in res:
                res = res.replace(build('label', entity_name), '')

            if build('from', entity_name) in res and build('label', entity_name) in res:
                res = res.replace(build('label', entity_name), '')
    return res


def layer_entities(nl_api_elt, res):
    tag = 'label'
    for entity in nl_api_elt['entities']:
        if entity['salience'] > 0.1:  # and entity['type'] != u'PERSON':
            val = entity['name'].lower()
            res += build(tag, val)
    return res


def layer_add_attachment_tag(res):
    return res + build('has', 'attachment')


def layer_link_entities_to_from(nl_api_elt, res):
    for entity in nl_api_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()

            for token in nl_api_elt['tokens']:
                if token['lemma'].lower() == entity_name:
                    hti = token['dependencyEdge']['headTokenIndex']
                    particle = nl_api_elt['tokens'][hti]['lemma']
                    if particle == 'from':
                        res += build('from', entity_name)
                    elif particle == 'to':
                        res += build('to', entity_name)
                    break
    return res


def build(tag, val):
    return ' {}:{}'.format(tag, val.replace(' ', '-'))
