import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets credentials and scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('FemmeFlow Tracker (Responses)')

responses = SHEET.worksheet('responses')

data = responses.get_all_values()

print(data)