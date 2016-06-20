from __future__ import print_function

DEBUG = True

# Only for test script, not for the server.
TEST_SENTENCES_FILENAME = 'data/sentences.txt'
TEST_EXPECTED_QUERIES_FILENAME = 'data/expected_queries.txt'
TEST_TMP_DIR = 'tmp'
TEST_TMP_FILENAME = TEST_TMP_DIR + '/api_calls.p'
TEST_USE_PREVIOUS_CALLS_FROM_API = False


class Extensions:
    DOCUMENT = ['docx', 'doc', 'pdf', 'odt']
    PRESENTATION = ['ppt']
    SPREAD_SHEET = ['xls', 'xslx', 'ods']

    def __init__(self):
        pass


# look for synonyms as well
DOCUMENTS_DICTIONARY = {'document': Extensions.DOCUMENT,
                        'word': Extensions.DOCUMENT,
                        'presentation': Extensions.PRESENTATION,
                        'powerpoint': Extensions.PRESENTATION,
                        'workbook': Extensions.SPREAD_SHEET,
                        'spreadsheet': Extensions.SPREAD_SHEET}

SEND_SYNONYMS = ['send', 'address', 'assign', 'deliver', 'dispatch',
                 'forward', 'issue', 'compose', 'communicate', 'ship', 'make']

DIGITS = {'few': 5, 'a': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
          'nine': 9, 'ten': 10}

TIME_UNIT = {'day': 1, 'week': 7, 'month': 31}

_KEYWORDS_AS_LABEL = ['resume', 'cv', 'report', 'audio', 'notes', 'paper', 'catalog', 'journal', 'cover',
                      'letter' 'recipe', 'menu', 'calendar', 'newsletter', 'list', 'todo', 'budget', 'schedule',
                      'organizer', 'sheet', 'invoice', 'tracker', 'planner', 'log', 'keynote', 'proposal', 'deck',
                      'design', 'roadmap', 'slide', 'event', 'photo', 'statement', 'assignment', 'record', 'archive']

KEYWORDS = set()
for doc in DOCUMENTS_DICTIONARY.keys():
    KEYWORDS.add(doc)
for doc in _KEYWORDS_AS_LABEL:
    KEYWORDS.add(doc)

_vars = {k: v for k, v in locals().iteritems() if '__' not in k and 'pdb' not in k and k.isupper()}

print('__________ Constants __________')
for name, value in _vars.iteritems():
    print('{} = {}'.format(name, value))
print('_______________________________')
