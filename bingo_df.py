from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
import sys, os

THIS_FILEPATH = os.path.dirname(__file__)

import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Shsrl6EerL5-gR6zKX4nnOhS7mJHwyUGQsCOE7U8f6w'
SAMPLE_RANGE_NAME = 'bingo'

def get_latest_bingo():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None

# If there are no (valid) credentials available, let the user log in.
    print("Authenticating...")
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(THIS_FILEPATH,'credentials','token.pickle')):
        with open(os.path.join(THIS_FILEPATH,'credentials','token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(THIS_FILEPATH,'credentials','credentials.json'), SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(os.path.join(THIS_FILEPATH,'credentials','token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    

    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # # print("CREDS %s " % creds)
    # # print("CREDS VALID %s " % creds.valid)
    
    
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())
            
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    ###########################
    ####### BINGO GOALS #######
    ###########################
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    df = pd.DataFrame(values)
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    
    df = df[df['rank']==df['rank']]
    
    df.to_csv('latest_data.csv',index=None)




    ###########################
    #######  BINGO FAQ  #######
    ###########################
    
    
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="rules").execute()
    values = result.get('values', [])
    
    df2 = pd.DataFrame(values)
    df2.columns = df2.iloc[0]
    df2.drop(df2.index[0], inplace=True)
    df2 = df2[df2['goal']==df2['goal']]
    
    df2.to_csv('latest_faq.csv',index=None)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return df

if __name__ == '__main__':
    df = get_latest_bingo()
    df.to_csv('latest_data.csv',index=None)