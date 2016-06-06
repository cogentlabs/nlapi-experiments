#!/usr/bin/python2
import codecs
import sys
import json
import os.path
from glob import glob

if len(sys.argv) < 2:
    print('usage: python3 %s dir' % sys.argv[0])
    sys.exit()

# For dealing with unicode printing problems in python2
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# Number of labels to keep
TOP_N = 10

# Header line
print 'Filename,' + ','.join([ 'Label %d,Probability %d' % (i,i)
                               for i in range(1,11) ])

# For each JSON file in the given dir, extract the labels and probabilities
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if not file.endswith(".json"):
            continue

        try:    data = json.load(open(os.path.join(root, file), 'r'))
        except: continue

        if 'labelAnnotations' not in data[0]:
            continue

        labels = sum([ [d['description'], str(d['score'])]
                       for d in data[0]['labelAnnotations'][:TOP_N] ], [])

        # Pad labels if less than desired (x2 because the label and probability)
        labels += ['', '0']*(TOP_N - len(labels))

        print(','.join([file.replace('.json', '')] + labels))
