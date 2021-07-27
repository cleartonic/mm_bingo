# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:21:04 2021

@author: PMAC
"""
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Shsrl6EerL5-gR6zKX4nnOhS7mJHwyUGQsCOE7U8f6w'
SAMPLE_RANGE_NAME = 'questions'

def get_latest_bingo():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None


    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    df = pd.DataFrame(values)
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    
    return df

if __name__ == '__main__':
    df = get_latest_bingo()
    df.to_csv('testing.csv',index=None)