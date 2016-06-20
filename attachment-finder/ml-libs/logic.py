import constants as c
import utils as u


def build_query(nlapi_elt):
    q = ''
    q = layer_add_attachment_tag(q)
    q = layer_entities(nlapi_elt, q)
    q = layer_link_entities_to_from(nlapi_elt, q)
    q = layer_add_temporal_keywords(nlapi_elt, q)
    q = layer_add_keywords_send_related(nlapi_elt, q)
    q = layer_add_keywords(nlapi_elt, q)
    q = filter_entities_already_indexed_by_to_from(nlapi_elt, q)
    return q


def layer_add_keywords(nlapi_elt, res):
    for token in nlapi_elt['tokens']:
        if token['lemma'] in c.KEYWORDS:
            res += build(None, token['lemma'])
    return res


def layer_add_keywords_send_related(nlapi_elt, res):
    entity_list = u.extract_relevant_entities(nlapi_elt)
    res_before = res
    send_index = None
    for send_synonym in c.SEND_SYNONYMS:
        for i, token in enumerate(nlapi_elt['tokens']):
            if token['lemma'].lower() == send_synonym:
                send_index = i
                break
    if send_index is not None:
        try:
            reverse_graph = u.reverse_directed_graph(nlapi_elt)
            operands = reverse_graph['reverse_directed_graph'][send_index]
            if len(operands) >= 1:
                if operands[0] < send_index:
                    # This is the sender.
                    sender = nlapi_elt['tokens'][operands[0]]['lemma'].lower()
                    sender_is_valid = False
                    if sender == 'I'.lower():
                        sender = 'me'
                        sender_is_valid = True
                    for entity in entity_list:
                        if sender in entity:
                            sender = str(entity)
                            sender_is_valid = True
                            break
                    if sender_is_valid:
                        res += build('from', sender)
            if len(operands) >= 2:
                if operands[1] > send_index:
                    # could be the TO particle.
                    receiver = nlapi_elt['tokens'][operands[1]]['lemma'].lower()
                    if receiver == 'to':
                        receiver = nlapi_elt['tokens'][operands[1] + 1]['lemma']
                    if receiver == 'me' or receiver in entity_list:
                        res += build('to', receiver)
        except Exception, e:
            print(str(e))

    if send_index is not None:
        sentence = u.extract_original_sentence(nlapi_elt)
        if res_before == res:  # no modifications
            send_raw_text = nlapi_elt['tokens'][send_index]['text']['content']
            for entity_name in u.extract_relevant_entities(nlapi_elt):
                if '{} {}'.format(send_raw_text, entity_name) in sentence:
                    res += build('to', entity_name)
    return res


def layer_add_temporal_keywords(nlapi_elt, res):
    sentence = u.extract_original_sentence(nlapi_elt)
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
    # last night, early morning, late morning, early afternoon and so on
    day_keywords = ['night', 'afternoon', 'morning', 'evening']
    for keyword in day_keywords:
        if keyword in sentence:
            res += build('newer_than', '1d')
            return res
    return res


def filter_entities_already_indexed_by_to_from(nlapi_elt, res):
    for entity_name in u.extract_relevant_entities(nlapi_elt):
        if build('to', entity_name) in res and build(None, entity_name) in res:
            res = res.replace(build(None, entity_name), '')
        if build('from', entity_name) in res and build(None, entity_name) in res:
            res = res.replace(build(None, entity_name), '')
    return res


def layer_entities(nlapi_elt, res):
    for entity_name in u.extract_relevant_entities(nlapi_elt):
        res += build(None, entity_name)
    return res


def layer_add_attachment_tag(res):
    return res + build('has', 'attachment')


def layer_link_entities_to_from(nlapi_elt, res):
    for entity_name in u.extract_relevant_entities(nlapi_elt):
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
        if not changed:  # maybe it's compound.
            sentence = u.extract_original_sentence(nlapi_elt)
            if 'from {}'.format(entity_name) in sentence:
                res += build('from', entity_name)
            elif 'to {}'.format(entity_name) in sentence:
                res += build('to', entity_name)
    return res


def build(tag, val):
    val = val.lower()
    if tag is None:  # KEYWORD
        return ' {}'.format(val)
    return ' {}:{}'.format(tag, val.replace(' ', '-'))
