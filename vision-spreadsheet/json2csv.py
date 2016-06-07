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

# Get cluster info
cluster_data  = json.load(open(sys.argv[1], 'r'))
cluster_names = [ c['label'] for c in cluster_data['clusters'] ]
id2cluster    = { p['i']: p['g'] for p in cluster_data['points'] }

# We will aggregate labels and colors 
cluster_labels = [ dict() for i in range(len(cluster_names)) ]
cluster_colors = [ dict() for i in range(len(cluster_names)) ]
cluster_faces  = [ 0      for i in range(len(cluster_names)) ]


# For dealing with unicode printing problems in python2
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# Walk the dir in case there is a large number of files
for root, dirs, files in os.walk(sys.argv[2]):
    for file in files:
        if not file.endswith(".json"):
            continue

        # Just skip it if there is a problem; It's not important for this
        try: data = json.load(open(os.path.join(root, file), 'r'))[0]
        except: continue

        id = file.replace('.json', '')
        if id not in id2cluster:
            continue
        cluster = id2cluster[id]

        # Extract most likely label
        if 'labelAnnotations' in data:
            label = data['labelAnnotations'][0]['description']

            if label in cluster_labels[cluster]:
                cluster_labels[cluster][label] += 1
            else:
                cluster_labels[cluster][label] = 1

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


# Header line
print ','.join(['Cluster ID', 'Cluster Name'] + \
               [ 'Label %d,Label Count %d' % (i,i) for i in range(1,11) ] + \
               [ 'Color %d,Color Count %d' % (i,i) for i in range(1,11) ] + \
               ['Number of Faces'])

# Print top N labels, top N colors, and number of faces for each cluster
for c in range(len(cluster_names)):
    top_labels = sum(sorted(cluster_labels[c].items(), key=lambda x: x[1])[-TOP_N:][::-1], ())
    top_colors = sum(sorted(cluster_colors[c].items(), key=lambda x: x[1])[-TOP_N:][::-1], ())
    num_faces  = cluster_faces[c]

    print ','.join([ '%d' % c, cluster_names[c]] + \
                   [ '%d' % x if type(x)==int else x for x in top_labels] + \
                   [ '%f' % x if type(x)==float else x for x in top_colors] + \
                   [ '%d' % num_faces])
