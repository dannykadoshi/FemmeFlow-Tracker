import datetime
import webbrowser
import pyfiglet
from colorama import init, Fore
import os
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


# Function to display the application name in big ASCII art
def display_name():
    name = "FemmeFlow Tracker"
    ascii_art = pyfiglet.figlet_format(name, font="slant")
    
    # Get the width of the terminal to center the ASCII art
    terminal_width = os.get_terminal_size().columns
    centered_ascii_art = name.center(terminal_width) + "\n" + Fore.RED + ascii_art + Fore.RESET
    print(centered_ascii_art)


# Introduction page for the application
def introduction():
    display_name()
    print("Welcome to FemmeFlow Tracker!")
    print("This application allows you to track your menstrual cycle and predict your next period date.")
    print("You can enter your menstrual cycle data in the Google Form, and we'll calculate the next period date for you.")
    print("Let's get started!\n")

# Call the introduction function
introduction()


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

# Calculate fertile days as 13 to 19 days after the last period date
fertile_start = last_period + datetime.timedelta(days=13)
fertile_end = last_period + datetime.timedelta(days=19)

# Print the fetched data and calculated dates
print("\nLast Form Submission Data:")
print(f"Timestamp: {timestamp}")
print(f"Last Period Date: {last_period.strftime('%d/%m/%Y')}")
print(f"Cycle Length: {cycle_length} days")
print(f"Period Duration: {period_duration} days")
print(f"Cycle Type: {cycle_type}")
print(f"Cycle Lengths (if irregular): {cycle_lengths}")
print(f"Symptoms/Additional Information: {symptoms}")
print(f"Email: {email}")
print(f"Name: {name}")
print(f"Age: {age}")

# Display fertile days
print("\nFertile Days:")
print(f"{fertile_start.strftime('%d/%m/%Y')} to {fertile_end.strftime('%d/%m/%Y')}")

# Display the calculated next period date
print(f"\nNext Period Date: {next_period.strftime('%d/%m/%Y')}")
