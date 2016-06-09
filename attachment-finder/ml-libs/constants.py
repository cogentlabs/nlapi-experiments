from __future__ import print_function

GLOVE_WORD2VEC_FILENAME = 'data/glove.6B.300d.MINI.txt'

SENTENCES_FILENAME = 'data/sentences.txt'
EXPECTED_QUERIES_FILENAME = 'data/expected_queries.txt'

TMP_FILENAME = 'tmp/api_calls.p'

USE_PREVIOUS_CALLS_FROM_API = True


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

vars = {k: v for k, v in locals().iteritems() if '__' not in k and 'pdb' not in k and k.isupper()}

print('__________ Constants __________')
for name, value in vars.iteritems():
    print('{} = {}'.format(name, value))
print('_______________________________')
