#Vision-spreadsheets

##Create CSV of Vision API data

Use `json2csv.py` with a cluster definition JSON to convert a directory of
Vision API JSON into one CSV containing the following:

1. Most common image labels (counts of most likely label for each image in cluster)
2. Most common colors (based on sum of scores across all images in cluster)
3. Number of faces in all images in the cluster

```
python2 json2csv cluster_json_file img_json_dir/ > my_images.csv
```

##Upload to Google Drive

Upload to Google Drive using your client secret file named `client\_secret.json`:

```
python2 vision-spreadsheet.py filepath name
```

where `filepath` is the file to upload and `name` is your desired filename in Drive.

*NOTE*: this will generate a credential file for this app that must be deleted
if you wish to change you `client\_secret.json` or other properties of the app
inside the code.

