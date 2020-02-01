## Reference by https://github.com/pdtyreus/coronavirus-ds

import pickle
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import glob
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w'

def main():
    # query data from google sheet
    data_query()
    
    # merge all dataset to one csv
    folder_path="rawData/*.csv"
    data_cleaning(folder_path,stored_path ="mergedData/combined.csv")
    
    
def data_query():    
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()

    for sheet in spreadsheet['sheets']:
        range_name = sheet['properties']['title']+'!A:G'
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        rows = result.get('values', [])
        print('{0} {1} rows retrieved.'.format(sheet['properties']['title'],len(rows)))
        filename = './rawData/csse_'+sheet['properties']['title']+'.csv'
        if not os.path.exists(filename):
            with open(filename, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
                print(' wrote new file {0}.'.format(sheet['properties']['title']))


def data_cleaning(folder_path,stored_path):
    """Merge all datasets (different dates), 
    saved in `rawData` to `mergedData` folder
    """
    all_filenames=[i for i in glob.glob(folder_path)]
    combined_csv=pd.concat([pd.read_csv(f) for f in all_filenames],ignore_index=True,sort=False)
    combined_csv["Last Update"]=pd.to_datetime(combined_csv["Last Update"])
    combined_csv=combined_csv.sort_values(by=["Last Update"])
    combined_csv["Day"]=[d.date() for d in combined_csv["Last Update"]]
    combined_csv["Time"]=[d.time() for d in combined_csv["Last Update"]]
    combined_csv=combined_csv[["Province/State",'Country/Region',"Day","Time","Confirmed",
                               "Suspected","Recovered","Deaths","Demised"]]
    idx=combined_csv.groupby("Day")["Time"].transform(max)==combined_csv["Time"]
    combined_csv=combined_csv[idx]
    cleaned_data=combined_csv.to_csv(stored_path,header=True,index=False)
    print("Saved merged dataset to mergedData/combined.csv")
                

                
if __name__ == '__main__':
    main()
