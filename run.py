import datetime
import webbrowser
import pyfiglet
from colorama import init, Fore
import os
import prettytable
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


# Function to display the available options for the user to choose from
def print_options():
    table = prettytable.PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "Health Tips"])
    table.add_row(["2", "Form Submission Data"])
    table.add_row(["3", "Fertile Days"])
    table.add_row(["4", "Next Period Date"])
    table.add_row(["5", "Personalized Recommendations"])
    table.add_row(["6", "Quit the application"])

    # Set the table text color to red using colorama
    red_table = f"{Fore.RED}{table}{Fore.RESET}"
    print(red_table)


# Function to display health tips
def display_health_tips():
    print("\nHealth Tips:")
    tips = {
        1: "Maintain a healthy diet and drink plenty of water.",
        2: "Exercise regularly to improve overall health and manage stress.",
        3: "Ensure you get enough sleep and rest during your menstrual cycle.",
        4: "Consider using a menstrual tracking app to keep track of your cycles and symptoms.",
    }

    if cycle_type.lower() == 'irregular':
        tips[5] = "If you have irregular cycles, consider consulting a healthcare professional for guidance."

    for tip_number, tip_text in tips.items():
        print(f"{tip_number}. {tip_text}")


# Function to display personalized recommendations
def personalized_recommendations():
    print("\nPersonalized Recommendations:")
    print("Here are some personalized recommendations for you:")
    print("- Get plenty of rest during your period.")
    print("- Consider trying relaxation techniques to manage menstrual pain.")
    print("- Stay hydrated and maintain a balanced diet.")
    print("- Engage in light exercises to reduce cramps and improve mood.")
    print("- Track your symptoms and mood to better understand your cycle.")
    print("- If you experience severe pain or irregularities, consult a healthcare professional.")


# Main loop of the application
while True:
    # Print the options table for the user to choose from
    print_options()

    # Get the user's choice
    choice = input("Enter your choice: ")

    # Process the user's choice and execute the corresponding action
    if choice == "1":
        display_health_tips()
    elif choice == "2":
        # Print the fetched data and calculated dates
        print("\nForm Submission Data:")
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
    elif choice == "3":
        # Display fertile days
        print("\nFertile Days:")
        print(f"{fertile_start.strftime('%d/%m/%Y')} to {fertile_end.strftime('%d/%m/%Y')}")
    elif choice == "4":
        # Display the calculated next period date
        print(f"\nNext Period Date: {next_period.strftime('%d/%m/%Y')}")
    elif choice == "5":
        # Display personalized recommendations
        personalized_recommendations()
    elif choice == "6":
        break  # Exit the application loop if the user chooses to quit
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")

    # Pause before clearing the screen
    input("Press Enter to continue...\n")

    # Clear the screen after the input is received
    os.system('cls' if os.name == 'nt' else 'clear')

