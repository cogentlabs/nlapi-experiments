import constants as c
import utils.nl_api as nl


def build_query(nl_api_elt):
    # print json.dumps(nl_api_elt, indent=2, sort_keys=True)
    result = ''
    result = layer_entities(nl_api_elt, result)
    result = layer_add_attachment_tag(result)
    result = layer_link_entities_to_from(nl_api_elt, result)
    result = temporal_keywords(nl_api_elt, result)
    result = layer_send_keyword(nl_api_elt, result)
    result = keywords_to_label(nl_api_elt, result)
    result = filter_entities_already_indexed_by_to_from(nl_api_elt, result)
    return result


def keywords_to_label(nl_api_elt, res):
    for token in nl_api_elt['tokens']:
        if token['lemma'] in c.KEYWORDS:
            res += build('label', token['lemma'])
    return res


def pobj_to_label(nl_api_elt, res):
    # NOT USED.
    entities_list = []
    for entity in nl_api_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()
            entities_list.append(entity_name)
    for token in nl_api_elt['tokens']:
        if token['partOfSpeech']['tag'] == 'NOUN' and token['dependencyEdge']['label'] == 'POBJ':
            if token['lemma'] not in entities_list:
                res += build('label', token['lemma'])
    return res


def layer_send_keyword(nl_api_elt, res):
    entities_list = []
    for entity in nl_api_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()
            entities_list.append(entity_name)

    send_index = None
    for send_synonym in c.SEND_SYNONYMS:
        for i, token in enumerate(nl_api_elt['tokens']):
            if token['lemma'].lower() == send_synonym:
                send_index = i
                break

    if send_index is not None:
        try:
            reverse_graph = nl.reverse_directed_graph(nl_api_elt)
            operands = reverse_graph['reverse_directed_graph'][send_index]
            if len(operands) >= 1:
                if operands[0] < send_index:
                    # This is the sender.
                    sender = nl_api_elt['tokens'][operands[0]]['lemma'].lower()
                    if sender == 'I'.lower():
                        sender = 'me'
                    for entity in entities_list:
                        if sender in entity:
                            sender = str(entity)
                    res += build('from', sender.lower())
            if len(operands) >= 2:
                if operands[1] > send_index:
                    # could be the TO particle.
                    receiver = nl_api_elt['tokens'][operands[1]]['lemma'].lower()
                    if receiver == 'to'.lower():
                        receiver = nl_api_elt['tokens'][operands[1] + 1]['lemma']
                    if receiver == 'me' or receiver in entities_list:
                        res += build('to', receiver)
        except Exception, e:
            print(str(e))

    return res


def temporal_keywords(nl_api_elt, res):
    sentence = nl_api_elt['sentences'][0]['text']['content']
    if 'yesterday' in sentence:
        res += build('newer_than', '1d')
        return res

    for digit in c.DIGITS.keys():
        for time_unit in c.TIME_UNIT.keys():
            str_to_find = '{} {} ago'.format(digit, time_unit)
            str_to_find2 = '{} {}s ago'.format(digit, time_unit)
            if str_to_find in sentence or str_to_find2 in sentence:
                time_index = c.DIGITS[digit] * c.TIME_UNIT[time_unit]
                res += build('newer_than', '{}d'.format(time_index))
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

            changed = False
            for token in nl_api_elt['tokens']:
                if token['lemma'].lower() == entity_name:
                    hti = token['dependencyEdge']['headTokenIndex']
                    particle = nl_api_elt['tokens'][hti]['lemma']
                    if particle == 'from':
                        res += build('from', entity_name)
                    elif particle == 'to':
                        res += build('to', entity_name)
                    changed = True
                    break

            if not changed:  # maybe it's compouned.
                sentence = nl_api_elt['sentences'][0]['text']['content'].lower()
                if 'from {}'.format(entity_name) in sentence:
                    res += build('from', entity_name)
                elif 'to {}'.format(entity_name) in sentence:
                    res += build('to', entity_name)

    return res


def build(tag, val):
    return ' {}:{}'.format(tag, val.replace(' ', '-'))
