import utils as u
from constants import *


def layer_filter_unique_values(nl_api_elt, query):
    output = set()
    for element in query.split():
        output.add(element)
    return ' '.join(output)


def layer_add_keywords(nl_api_elt, query):
    for token in nl_api_elt['tokens']:
        lemma = token['lemma']
        if lemma in KEYWORDS:
            query += u.build(None, lemma)
    return query


def layer_add_keywords_send_related(nl_api_elt, query):
    tokens = nl_api_elt['tokens']
    entity_list = u.extract_relevant_entities(nl_api_elt)
    send_index = None
    for send_synonym in SEND_SYNONYMS:
        for i, token in enumerate(tokens):
            if token['lemma'].lower() == send_synonym:
                send_index = i
                break
    if send_index is not None:
        query_before = str(query)  # track changes.
        try:
            reverse_graph = u.reverse_directed_graph(nl_api_elt)
            operands = reverse_graph['reverse_directed_graph'][send_index]
            op_left = operands[0]
            if len(operands) >= 1:
                if op_left < send_index:
                    # Sender part.
                    sender = tokens[op_left]['lemma'].lower()
                    if sender == 'I'.lower():
                        query += u.build('from', 'me')
                    else:
                        entities_sender = [v for v in entity_list if sender in v]
                        if len(entities_sender) > 0:
                            query += u.build('from', entities_sender[0])
            if len(operands) >= 2:
                op_right = operands[1]
                if op_right > send_index:
                    # Receiver part. could be the particle TO.
                    receiver = tokens[op_right]['lemma'].lower()
                    if receiver == 'to':
                        receiver = tokens[op_right + 1]['lemma'].lower()
                    if receiver == 'me' or receiver in entity_list:
                        query += u.build('to', receiver)
        except Exception, e:
            print(str(e))
        sentence = u.extract_original_sentence(nl_api_elt)
        if query_before == query:  # no modifications
            send_raw_text = tokens[send_index]['text']['content']
            for entity_name in u.extract_relevant_entities(nl_api_elt):
                if '{} {}'.format(send_raw_text, entity_name) in sentence:
                    query += u.build('to', entity_name)
    return query


def layer_add_temporal_keywords(nl_api_elt, query):
    sentence = u.extract_original_sentence(nl_api_elt)
    if 'yesterday' in sentence:
        return query + u.build('newer_than', '1d')
    for digit in DIGITS.keys():
        for time_unit in TIME_UNIT.keys():
            pattern_1 = '{} {} ago'.format(digit, time_unit)
            pattern_2 = '{} {}s ago'.format(digit, time_unit)
            if pattern_1 in sentence or pattern_2 in sentence:
                time_index = DIGITS[digit] * TIME_UNIT[time_unit]
                return query + u.build('newer_than', '{}d'.format(time_index))
    for time_unit in TIME_UNIT.keys():
        if 'last {}'.format(time_unit) in sentence:
            time_index = TIME_UNIT[time_unit]
            return query + u.build('newer_than', '{}d'.format(time_index))
    for keyword in ['night', 'afternoon', 'morning', 'evening']:
        if keyword in sentence:
            return query + u.build('newer_than', '1d')
    return query


def layer_filter_entities_already_indexed_by_to_from(nl_api_elt, query):
    for entity_name in u.extract_relevant_entities(nl_api_elt):
        if u.build('to', entity_name) in query and u.build(None, entity_name) in query:
            query = query.replace(u.build(None, entity_name), '')
        if u.build('from', entity_name) in query and u.build(None, entity_name) in query:
            query = query.replace(u.build(None, entity_name), '')
    return query


def layer_entities(nl_api_elt, query):
    for entity_name in u.extract_relevant_entities(nl_api_elt):
        query += u.build(None, entity_name)
    return query


def layer_add_attachment_tag(nl_api_elt, query):
    return query + u.build('has', 'attachment')


def layer_link_entities_to_from(nl_api_elt, query):
    for entity_name in u.extract_relevant_entities(nl_api_elt):
        changed = False
        for token in nl_api_elt['tokens']:
            if token['lemma'].lower() == entity_name:
                hti = token['dependencyEdge']['headTokenIndex']
                particle = nl_api_elt['tokens'][hti]['lemma']
                if particle == 'from':
                    query += u.build('from', entity_name)
                elif particle == 'to':
                    query += u.build('to', entity_name)
                changed = True
                break
        if not changed:  # maybe it's compound.
            sentence = u.extract_original_sentence(nl_api_elt)
            if 'from {}'.format(entity_name) in sentence:
                query += u.build('from', entity_name)
            elif 'to {}'.format(entity_name) in sentence:
                query += u.build('to', entity_name)
    return query


# Order matters.
LAYERS = [layer_add_attachment_tag,
          layer_entities,
          layer_link_entities_to_from,
          layer_add_temporal_keywords,
          layer_add_keywords_send_related,
          layer_add_keywords,
          layer_filter_entities_already_indexed_by_to_from,
          layer_filter_unique_values]


def build_query(nl_api_elt):
    q = str()
    for layer_ptr in LAYERS:
        prev_q = q
        q = layer_ptr(nl_api_elt, q).strip()
        if DEBUG:
            print('LAYER = {}, INPUT = {}, OUTPUT = {}'.format(layer_ptr, prev_q, q))
    return q
