from oauth2client.service_account import ServiceAccountCredentials
import gspread


def get_spreadsheet(sheet_name, worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = '/home/atti/googleds/pen_jutalék/google/gds-dataupload-444ed56fca7c.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, scope)

    client = gspread.authorize(credentials)

    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet


