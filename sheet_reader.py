import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GoogleSheetReader:
    def __init__(self, credentials_file, sheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name)

    # Fetch data from the first worksheet
    def get_data_from_first_sheet(self):
        worksheet = self.sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
