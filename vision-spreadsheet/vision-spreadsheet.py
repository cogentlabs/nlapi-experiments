import httplib2
import os
from sys import argv, exit

from apiclient import discovery
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import client
from oauth2client import tools


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Vision Spreadsheet'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload_csv(service, filepath, name):
    metadata = {
        'name': name,
        'mimeType': 'text/csv'
        #'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
    media = MediaFileUpload(filepath,
                            mimetype='text/csv',
                            resumable=True)
    fileid = service.files().create(body=metadata,
                                    media_body=media,
                                    fields='id').execute()
    return fileid

def main():
    if len(argv) != 3:
        print 'usage: python2 %s filepath name' % argv[0]
        exit()

    filepath, name = argv[1], argv[2]

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    fileid = upload_csv(service, filepath, name)

if __name__ == '__main__':
    main()
