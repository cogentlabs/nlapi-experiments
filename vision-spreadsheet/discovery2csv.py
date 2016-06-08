#!/usr/bin/python2
import sys
import json
import codecs

if len(sys.argv) < 2:
    print('usage: python2 %s cluster_pie_json' % sys.argv[0])
    sys.exit()

# Get cluster info
clusters = json.load(open(sys.argv[1], 'r'))

# For dealing with unicode printing problems in python2
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def safe_print(s):
    if   type(s) == int  : fstr = '%d'
    elif type(s) == float: fstr = '%f'
    else                 : fstr = '%s'
    return fstr % s

# Use zip(*) to transpose the pairs for pie chart format in Sheets
# This results in the following:
#
#    ___cluster1__ ___cluster2__ ... ___clusterN__
#    label1 count1 label1 count1 ... label1 count1
#    label2 count2 label2 count2 ... label2 count2
#    ...     ...   ...    ...    ... ...    ...
#    labelN countN labelN countN ... labelN countN
#
# Note that cluster header takes up two columns, so the following line
# includes an extra comma on purpose.
#
print ','.join([ 'Cluster: %s,' % c for c in clusters ])

for vals in zip(*[clusters[c] for c in clusters]):
    print ','.join(map(safe_print, sum(vals, [])))
