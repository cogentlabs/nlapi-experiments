#!/usr/bin/python2
import codecs
import sys
import json
import os.path
from glob import glob

if len(sys.argv) < 3:
    print('usage: python2 %s cluster_file json_dir' % sys.argv[0])
    sys.exit()

# Top N labels and colors to keep for each cluster
TOP_N = 10

vision_data = json.load(open(sys.argv[2], 'r'))

# Get cluster info
cluster_data  = json.load(open(sys.argv[1], 'r'))
cluster_names = [ c['label'] for c in cluster_data['clusters'] ]
id2cluster    = { p['i']: p['g'] for p in cluster_data['points'] }

# We will aggregate labels and colors 
cluster_sizes  = [ 0      for i in range(len(cluster_names)) ]
cluster_labels = [ dict() for i in range(len(cluster_names)) ]
cluster_colors = [ dict() for i in range(len(cluster_names)) ]
cluster_faces  = [ 0      for i in range(len(cluster_names)) ]
cluster_safe   = [ { k: 0 for k in ['adult', 'medical', 'spoof', 'violence'] }
                   for i in range(len(cluster_names)) ]


# For dealing with unicode printing problems in python2
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

for data in vision_data:
    # Just skip it if there is a problem; It's not important for this
    #try: data = json.load(open(os.path.join(root, file), 'r'))[0]
    #except: continue

    id = data['imageId']
    if id not in id2cluster:
        continue
    cluster = id2cluster[id]

    cluster_sizes[cluster] += 1

    # Extract most likely label
    if 'labelAnnotations' in data:
        labels = data['labelAnnotations']
        for l in labels:
            if l['description'] in cluster_labels[cluster]:
                cluster_labels[cluster][l['description']] += l['score']
            else:
                cluster_labels[cluster][l['description']] = l['score']

    # Extract colors
    if 'imagePropertiesAnnotation' in data and 'dominantColors' in data['imagePropertiesAnnotation']:
        colors = data['imagePropertiesAnnotation']['dominantColors']['colors']
        for c in colors:
            # Seems like 0 values are not included in JSON...
            cc = '#%02x%02x%02x' % tuple([ c['color'][cc] if cc in c['color'] else 0
                                           for cc in ['red','green','blue'] ])

            if cc in cluster_colors[cluster]:
                cluster_colors[cluster][cc] += c['score']
            else:
                cluster_colors[cluster][cc] = c['score']

    # Count faces
    if 'faceAnnotations' in data:
        cluster_faces[cluster] += len(data['faceAnnotations'])
    
    # Extract safe search flags
    if 'safeSearchAnnotation' in data:
        safe = data['safeSearchAnnotation']
        for s,v in safe.items():
            cluster_safe[cluster][s] += int('UN' not in v)


# Print top N labels, top N colors, and number of faces for each cluster
rows = []
for c in range(len(cluster_names)):
    top_labels = sorted(cluster_labels[c].items(), key=lambda x: x[1], reverse=True)
    top_labels = top_labels[:TOP_N] + \
                 [('other', sum([ x[1] for x in top_labels[TOP_N:] ]) )]

    top_colors = sorted(cluster_colors[c].items(), key=lambda x: x[1], reverse=True)
    top_colors = top_colors[:TOP_N] + \
                 [('other', sum([ x[1] for x in top_colors[TOP_N:] ]) )]

    safe_ratios = [ (k, v / cluster_sizes[c]) for k, v in cluster_safe[c].items() ]

    rows.append([('Number of images', cluster_sizes[c])] + \
                top_labels + \
                top_colors + \
                cluster_safe[c].items() + \
                [('Number of faces', cluster_faces[c])])

# Dealing with python printing nonsense
def safe_print(s):
    if type(s) == int:
        fstr = '%d'
    elif type(s) == float:
        fstr = '%f'
    else:
        fstr = '%s'
    return fstr % s

# Use zip(*) to transpose, i.e. make the rows into columns
# This results in the following:
#
#    cluster1_____ cluster2_____ ... clusterN_____
#    label1 count1 label1 count1 ... label1 count1
#    label2 count2 label2 count2 ... label2 count2
#    ...     ...   ...    ...    ... ...    ...
#    labelN countN labelN countN ... labelN countN
#    other  count  other  count  ... other  count
#    color1 count1 color1 count1 ... color1 count1
#    color2 count2 color2 count2 ... color2 count2
#    ...     ...   ...    ...    ... ...    ...
#    colorN countN colorN countN ... colorN countN
#
print ','.join([ 'Cluster %s,' % i for i in range(len(cluster_names)) ])

for col in zip(*[r for r in rows]):
    print ','.join( safe_print(s) for s in sum(col, ()) )
