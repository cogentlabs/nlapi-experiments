#Vision-spreadsheets

##Create CSV of Vision API data

Use `json2csv.py` to convert a directory of Vision API JSON into one CSV
containing the top 10 annotations for each image with corresponding
probabilities.

```
python2 json2csv img_json/ > my_images.csv
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

