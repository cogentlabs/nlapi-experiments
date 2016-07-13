# Experimental projects
Some experimental projects using edgy APIs and machine learning.

## Attachment Finder
A chrome extension with a natural language processing server. It helps you to find attachments in GMail with voice, not only in English, but Japanese as well.

### Setup
There are two parts. The chrome extension and NL-processing server.


#### NL Processing server
```
attachment-finder/ml-libs
export GOOGLE_API_KEYS=XXX
pip install
python server.py
```

Then the server should be running at http://localhost:5000


#### Chrome extension
```
cd attachment-finder
vi src/config.js    # modify GOOGLE_API_KEYS
npm i
gulp
```

Now the Chrome plugin files should be populated in `/attachment-finder/dist`. Go Google Chrome, and load the extension (developer mode has to be enabled)

If you have a problem in Chrome-login, please see https://developer.chrome.com/apps/app_identity


#### Good to go?

Since the NL API is still in alpha, some breaking change may occur. In that case, some files under `ml-libs`. Anyway, you should be able to click on the extension on Chrome, and say whatever you're looking for. Some email having attachment should be listed.


### APIs used
- Google Natural Language API (alpha)
- Google Web Speech API
- Google Translate API
- Google Gmail API
