import datetime
import webbrowser
import pyfiglet
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


# Open google form in the browser
def open_google_form():
    form_url = "https://forms.gle/ja7VxdgBAutRLz348"
    webbrowser.open(form_url)


# Prompt the user with an option to open the Google Form
print("Would you like to enter your information in the Google Form? (yes/no)")
response = input().strip().lower()

# If the user enters 'yes', open the Google Form in the web browser
if response == 'yes':
    open_google_form()
    print("Google Form opened in your web browser. Please enter your information there.")
    print("After entering the information, you can come back to this terminal to see the calculated next period date.")
else:
    print("You chose not to enter your information in the Google Form.")


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


# Calculate the next period date
next_period = last_period + datetime.timedelta(days=cycle_length)

# Print the calculated next period date
print(f"Next Period Date: {next_period.strftime('%d/%m/%Y')}")