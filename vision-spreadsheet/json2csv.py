#!/usr/bin/python2
import sys
import json
import codecs

if len(sys.argv) < 2:
    print('usage: python2 %s vision_json' % sys.argv[0])
    sys.exit()

# Top N labels and colors to keep for each cluster
TOP_N = 10

# For dealing with unicode printing problems in python2
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

try:
    vision = json.load(open(sys.argv[1], 'r'))
except:
    print 'Invalid JSON'
    sys.exit()

# CSV header
print ','.join(['Image ID'] + \
               ['Number of Faces'] + \
               [ 'Label %d,Label Score %d' % (i,i) for i in range(1,TOP_N+1) ] + \
               [ 'Color %d,Color Score %d' % (i,i) for i in range(1,TOP_N+1) ])

# Extract and reformat each image
for img in vision:

    num_faces, labels, colors = 0, [], []

    # Count faces
    if 'faceAnnotations' in img:

        num_faces = len(img['faceAnnotations'])

    # Extract top N labels and their scores
    if 'labelAnnotations' in img:

        labels = img['labelAnnotations'][:TOP_N]
        labels = sum([ [l['description'], str(l['score'])] for l in labels ], [])

    # Extract top N colors and their scores
    if 'imagePropertiesAnnotation' in img and 'dominantColors' in img['imagePropertiesAnnotation']:

        for c in img['imagePropertiesAnnotation']['dominantColors']['colors'][:TOP_N]:

            color = '#%02x%02x%02x' % tuple([ c['color'][cc] if cc in c['color'] else 0
                                              for cc in ['red','green','blue'] ])
            colors += [color, str(c['score'])]


    # Pad up to N if less than N (this still works if no labels/colors data for image)
    labels += ( ('', '0.0') * ((TOP_N*2-len(labels))/2) )
    colors += ( ('', '0.0') * ((TOP_N*2-len(colors))/2) )

    print ','.join([img['imageId']] + [str(num_faces)] + labels + colors)
