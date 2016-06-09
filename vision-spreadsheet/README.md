#Vision-spreadsheets

##Create CSV of Vision API data

Use `cluster_level_json2csv.py` with a cluster definition JSON and another JSON of
all the image API results in a list to produce a CSV containing the following:

1. Number of images in each cluster
2. Most common image labels (based on sum of scores across all images in cluster)
3. Most common colors (based on sum of scores across all images in cluster)
4. Count of images in the cluster that were tagged with each Safe Search type
   (anything that is not 'UNLIKELY' or 'VERY\_UNLIKELY')
5. Number of faces in all images in the cluster

The format is like this:
```
    cluster1_______ cluster2_______ ... clusterN_______
    'numImg' numImg 'numImg' numImg     'numImg' numImg 
    label1   score1 label1   score1 ... label1   score1
    label2   score2 label2   score2 ... label2   score2
    ...       ...   ...      ...    ... ...      ...
    labelN   scoreN labelN   scoreN ... labelN   scoreN
    other    score  other    score  ... other    score
    color1   score1 color1   score1 ... color1   score1
    color2   score2 color2   score2 ... color2   score2
    ...       ...   ...      ...    ... ...      ...
    colorN   scoreN colorN   scoreN ... colorN   scoreN
    other    score  other    score  ... other    score
    'faces'  faces  'faces'  faces  ... 'faces'  faces
```

```
python2 json2csv cluster_def.json vision_api.json > cluster_stats.csv
```

##Upload to Google Drive

Upload to Google Drive using your client secret file named `client\_secret.json`:

```
python2 vision-spreadsheet.py filepath name
```

where `filepath` is the file to upload and `name` is your desired filename in Drive.

CSV file will automatically be converted to Google Sheets format.

*NOTE*: this will generate a credential file for this app that must be deleted
if you wish to change you `client\_secret.json` or other properties of the app
inside the code.

