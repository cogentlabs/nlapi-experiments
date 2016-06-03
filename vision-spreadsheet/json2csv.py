#!/usr/bin/python3
import json
import os
from glob import glob
from sys import argv, exit

if len(argv) < 2:
    print('usage: python3 %s dir' % argv[0])
    exit()

# Number of labels to keep
TOP_N = 10

for root, dirs, files in os.walk(argv[1]):
    for file in files:
        if not file.endswith(".json"):
            continue

        try:
            data = json.load(open(os.path.join(root, file), 'r'))
        except:
            continue

        if 'labelAnnotations' not in data[0]:
            continue

        labels = sum([ [d['description'], str(d['score'])]
                       for d in data[0]['labelAnnotations'][:TOP_N] ], [])

        # Pad labels if less than desired (x2 because the label and probability)
        labels += ['', '0']*(TOP_N - len(labels))

        print(','.join([file.replace('.json', '')] + labels))
