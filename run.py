import datetime
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

# Get the last row of data in the Google Sheets
data = responses.get_all_values()
last_row = data[-1]

# Define the number of expected columns
EXPECTED_COLUMNS = 10

# If the number of columns in last_row is less than EXPECTED_COLUMNS, fill in the missing values with empty strings
last_row.extend([''] * (EXPECTED_COLUMNS - len(last_row)))

# Extract the user's inputs from the Google Sheets
timestamp_str, last_period_str, cycle_length_str, period_duration_str, cycle_type, cycle_lengths, symptoms, email, name, age = last_row

# Convert the date strings to datetime objects
timestamp = datetime.datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M:%S")
last_period = datetime.datetime.strptime(last_period_str, "%d/%m/%Y").date()
cycle_length = int(cycle_length_str)
period_duration = int(period_duration_str)

# Print the fetched data
print("Last Form Submission Data:")
print(f"Timestamp: {timestamp}")
print(f"Last Period Date: {last_period}")
print(f"Cycle Length: {cycle_length} days")
print(f"Period Duration: {period_duration} days")
print(f"Cycle Type: {cycle_type}")
print(f"Cycle Lengths (if irregular): {cycle_lengths}")
print(f"Symptoms/Additional Information: {symptoms}")
print(f"Email: {email}")
print(f"Name: {name}")
print(f"Age: {age}")