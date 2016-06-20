from __future__ import print_function

GLOVE_WORD2VEC_FILENAME = 'data/glove.6B.300d.MINI.txt'

SENTENCES_FILENAME = 'data/sentences.txt'
EXPECTED_QUERIES_FILENAME = 'data/expected_queries.txt'

TMP_DIR = 'tmp'
TMP_FILENAME = TMP_DIR + '/api_calls.p'

USE_PREVIOUS_CALLS_FROM_API = True


class Extensions:
    DOCUMENT = ['docx', 'doc', 'pdf', 'odt']
    PRESENTATION = ['ppt']
    SPREAD_SHEET = ['xls', 'xslx', 'ods']

    def __init__(self):
        pass


DEBUG = True

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

KEYWORDS = set()
_KEYWORDS_AS_LABEL = ['resume', 'cv', 'report', 'audio', 'notes', 'paper', 'catalog', 'journal', 'cover',
                      'letter' 'recipe', 'menu', 'calendar', 'newsletter', 'list', 'todo', 'budget', 'schedule',
                      'organizer', 'sheet', 'invoice', 'tracker', 'planner', 'log', 'keynote', 'proposal', 'deck',
                      'design', 'roadmap', 'slide', 'event', 'photo', 'statement', 'assignment', 'record', 'archive']

for doc in DOCUMENTS_DICTIONARY.keys():
    KEYWORDS.add(doc)
for doc in _KEYWORDS_AS_LABEL:
    KEYWORDS.add(doc)

vars = {k: v for k, v in locals().iteritems() if '__' not in k and 'pdb' not in k and k.isupper()}

print('__________ Constants __________')
for name, value in vars.iteritems():
    print('{} = {}'.format(name, value))
print('_______________________________')
