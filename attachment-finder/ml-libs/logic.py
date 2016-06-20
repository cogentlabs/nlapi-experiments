import constants as c
import utils as nl


def build_query(nlapi_elt):
    q = ''
    q = layer_entities(nlapi_elt, q)
    q = layer_add_attachment_tag(q)
    q = layer_link_entities_to_from(nlapi_elt, q)
    q = temporal_keywords(nlapi_elt, q)
    q = layer_send_keyword(nlapi_elt, q)
    q = keywords_to_label(nlapi_elt, q)
    q = filter_entities_already_indexed_by_to_from(nlapi_elt, q)
    return q


def keywords_to_label(nlapi_elt, res):
    for token in nlapi_elt['tokens']:
        if token['lemma'] in c.KEYWORDS:
            res += build(None, token['lemma'])
    return res


def pobj_to_label(nlapi_elt, res):
    # NOT USED.
    entities_list = []
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()
            entities_list.append(entity_name)
    for token in nlapi_elt['tokens']:
        if token['partOfSpeech']['tag'] == 'NOUN' and token['dependencyEdge'][None] == 'POBJ':
            if token['lemma'] not in entities_list:
                res += build(None, token['lemma'])
    return res


def layer_send_keyword(nlapi_elt, res):
    res_before = res

    entities_list = []
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()
            entities_list.append(entity_name)

    send_index = None
    for send_synonym in c.SEND_SYNONYMS:
        for i, token in enumerate(nlapi_elt['tokens']):
            if token['lemma'].lower() == send_synonym:
                send_index = i
                break

    if send_index is not None:
        try:
            reverse_graph = nl.reverse_directed_graph(nlapi_elt)
            operands = reverse_graph['reverse_directed_graph'][send_index]
            if len(operands) >= 1:
                if operands[0] < send_index:
                    # This is the sender.
                    sender = nlapi_elt['tokens'][operands[0]]['lemma'].lower()
                    sender_is_valid = False
                    if sender == 'I'.lower():
                        sender = 'me'
                        sender_is_valid = True
                    for entity in entities_list:
                        if sender in entity:
                            sender = str(entity)
                            sender_is_valid = True
                            break
                    if sender_is_valid:
                        res += build('from', sender.lower())
            if len(operands) >= 2:
                if operands[1] > send_index:
                    # could be the TO particle.
                    receiver = nlapi_elt['tokens'][operands[1]]['lemma'].lower()
                    if receiver == 'to'.lower():
                        receiver = nlapi_elt['tokens'][operands[1] + 1]['lemma']
                    if receiver == 'me' or receiver in entities_list:
                        res += build('to', receiver)
        except Exception, e:
            print(str(e))

    if send_index is not None:
        sentence = nlapi_elt['sentences'][0]['text']['content'].lower()
        if res_before == res:  # no modifications
            send_raw_text = nlapi_elt['tokens'][send_index]['text']['content']
            for entity in entities_list:
                if '{} {}'.format(send_raw_text, entity) in sentence:
                    res += build('to', entity.lower())
    return res


def temporal_keywords(nlapi_elt, res):
    sentence = nlapi_elt['sentences'][0]['text']['content']
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

    for time_unit in c.TIME_UNIT.keys():
        if 'last {}'.format(time_unit) in sentence:
            time_index = c.TIME_UNIT[time_unit]
            res += build('newer_than', '{}d'.format(time_index))
            return res

    # default.
    # last night, early morning, late morning, early afternoon and so on
    day_keywords = ['night', 'afternoon', 'morning', 'evening']
    for keyword in day_keywords:
        if keyword in sentence:
            res += build('newer_than', '1d')
            return res

    return res


def filter_entities_already_indexed_by_to_from(nlapi_elt, res):
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()

            if build('to', entity_name) in res and build(None, entity_name) in res:
                res = res.replace(build(None, entity_name), '')

            if build('from', entity_name) in res and build(None, entity_name) in res:
                res = res.replace(build(None, entity_name), '')
    return res


def layer_entities(nlapi_elt, res):
    tag = None
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:  # and entity['type'] != u'PERSON':
            val = entity['name'].lower()
            res += build(tag, val)
    return res


def layer_add_attachment_tag(res):
    return res + build('has', 'attachment')


def layer_link_entities_to_from(nlapi_elt, res):
    for entity in nlapi_elt['entities']:
        if entity['salience'] > 0.1:
            entity_name = entity['name'].lower()

            changed = False
            for token in nlapi_elt['tokens']:
                if token['lemma'].lower() == entity_name:
                    hti = token['dependencyEdge']['headTokenIndex']
                    particle = nlapi_elt['tokens'][hti]['lemma']
                    if particle == 'from':
                        res += build('from', entity_name)
                    elif particle == 'to':
                        res += build('to', entity_name)
                    changed = True
                    break

            if not changed:  # maybe it's compouned.
                sentence = nlapi_elt['sentences'][0]['text']['content'].lower()
                if 'from {}'.format(entity_name) in sentence:
                    res += build('from', entity_name)
                elif 'to {}'.format(entity_name) in sentence:
                    res += build('to', entity_name)

    return res


def build(tag, val):
    if tag is None:  # KEYWORD
        return ' {}'.format(val)
    return ' {}:{}'.format(tag, val.replace(' ', '-'))
