'''
Helper module for getting songs information from Drive.
'''

from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pymongo import MongoClient

from audio.Tracklist import add_song, create_song_collection
from audio.Tracklist import get_song
from other_scripts.download import download_file

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1H6ixLWatqnVGOY2gWaZaGoH0_hYcPhpAby2Rk_Oge94'
SAMPLE_RANGE_NAME = 'Descriptors!A2:H100'

client = MongoClient()
db = client.test_database
sessionID = 'test'
checkDataBaseFlag = True

def main():
    """
    Connect to the Google Api, retrieve song information, add it to the database.
    (Optional): Also download and convert songs into a playable format.
    """

    create_song_collection(db, sessionID)

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            descriptors = {
                'genre': row[1],
                'dynamics': row[2],
                'tempo': row[3],
                'key': row[4],
                'lyrics': row[5],
                'language': row[6]
            }
            print('Downloading %s...' % row[0])
            if checkDataBaseFlag:
                if get_song(db, sessionID, row[0]) is None:
                    add_song(db, sessionID, row[0], descriptors)
            download_file(row[0], row[7])



if __name__ == '__main__':
    main()
