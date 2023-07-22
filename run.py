import datetime
import webbrowser
import pyfiglet
from colorama import init, Fore
import os
import prettytable
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

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


# Function to clear the screen based on the operating system
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the application name in big ASCII art with animation
def display_name():
    name = "FemmeFlow Tracker"
    ascii_art = pyfiglet.figlet_format(name, font="slant")

    # Get the width of the terminal to center the ASCII art
    terminal_width = os.get_terminal_size().columns

    # Clear the screen
    clear()

    # Animation step 1: Print centered text and sleep for 1 second
    centered_text = center_logo([name], terminal_width)
    print(centered_text)
    sleep(1)

    # Animation step 2: Print centered text in red and sleep for 2 seconds
    clear()
    print(Fore.RED + centered_text + Fore.RESET)
    sleep(2)

    # Animation step 3: Print each line of ASCII art one by one and sleep for 0.2 seconds
    for line in ascii_art.splitlines():
        print(Fore.RED + line.center(terminal_width) + Fore.RESET)
        sleep(0.2)  

    # Animation step 4: Clear the screen and sleep for 3 seconds
    clear()
    sleep(3)

    # Clear the screen again
    clear()

# Function to center the logo
def center_logo(logo_lines, width):
    centered_logo = []
    for line in logo_lines:
        centered_line = line.center(width)
        centered_logo.append(centered_line)
    return '\n'.join(centered_logo)

# Introduction page for the application
def introduction():
    display_name()
    print("Welcome to FemmeFlow Tracker!")
    print(
        "This application allows you to track your menstrual cycle and "
        "predict your next period date."
    )
    print(
        "You can enter your menstrual cycle data in the Google Form,"
        " and we'll calculate the next period date for you."
    )
    print("Let's get started!\n")

# Call the introduction function
introduction()


# Open google form in the browser
def open_google_form():
    form_url = "https://forms.gle/ja7VxdgBAutRLz348"
    webbrowser.open(form_url)
    print(
        "Google Form opened in your web browser."
        "Please enter your information there."
    )
    print(
        "After entering the information,"
        " you can come back to this terminal to see"
        " the calculated next period date."
    )


# Prompt the user with an option to open the Google Form
print("Would you like to enter your information in the Google Form? (yes/no)")
response = input().strip().lower()

# Validate the user's response
while response not in ['yes', 'no']:
    print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
    response = input().strip().lower()

# If the user enters 'yes', open the Google Form in the web browser
if response == 'yes':
    open_google_form()
    print("Thank you for submitting your data!")
    print("Your data has been recorded successfully.")
    print("Please click 'Enter' to continue to the options.")
    input()  # Wait for the user to press 'Enter' before proceeding
else:
    print("You chose not to enter your information in the Google Form.")
    print("For FemmeFlow Tracker to work, it requires your menstrual cycle data.")
    reconsider_response = input("Would you like to reconsider and open the Google Form now? (yes/no)").strip().lower()

    while reconsider_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
        reconsider_response = input().strip().lower()

    if reconsider_response == 'yes':
        open_google_form()
        print("Thank you for submitting your data!")
        print("Your data has been recorded successfully.")
        print("Please click 'Enter' to continue to the options.")
        input()  # Wait for the user to press 'Enter' before proceeding
    else:
        print("Exiting FemmeFlow Tracker. Have a great day!")
        exit()  # Exit the application


# Get the last row of data in the Google Sheets
data = responses.get_all_values()
last_row = data[-1]

# Define the number of expected columns
EXPECTED_COLUMNS = 11

# If the number of columns in last_row is less than EXPECTED_COLUMNS,
# fill in the missing values with empty strings
last_row.extend([''] * (EXPECTED_COLUMNS - len(last_row)))

# Extract the user's inputs from the Google Sheets
timestamp_str, last_period_str, cycle_length_str, period_duration_str, \
    cycle_type, cycle_lengths, symptoms, email, \
    name, age, form_publisher = last_row


# Convert the date strings to datetime objects
timestamp = datetime.datetime.strptime(
    timestamp_str, "%d/%m/%Y %H:%M:%S"
)
last_period = datetime.datetime.strptime(last_period_str,
                                         "%d/%m/%Y").date()
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
    table.add_row(
        ["6", "Exercises Tips"]
    )  # Add "Exercises Tips" option
    table.add_row(["7", "Quit the application"])

    # Set the table text color to red using colorama
    red_table = f"{Fore.RED}{table}{Fore.RESET}"
    print(red_table)


# Function to display health tips
def display_health_tips():
    print("\nHealth Tips:")
    tips = {
        1:
        "Maintain a healthy diet and drink plenty of water.",
        2:
        "Exercise regularly to improve overall health and manage stress.",
        3:
        "Ensure you get enough sleep and rest during your menstrual cycle.",
        4:
        "Consider using a menstrual tracking app"
        " to keep track of your cycles and symptoms.",
    }

    if cycle_type.lower() == 'irregular':
        tips[
            5
        ] = "If you have irregular cycles,"
        " consider consulting a healthcare professional for guidance."

    for tip_number, tip_text in tips.items():
        print(f"{tip_number}. {tip_text}")


# Function to display personalized recommendations
def personalized_recommendations(
    cycle_length, period_duration, symptoms
):
    print("\nPersonalized Recommendations:")
    print("""
    Based on your menstrual cycle data and symptoms,
    we have some personalized recommendations to help you stay healthy
    and comfortable during your period:
    """)

    # Check the cycle length and offer relevant advice
    if cycle_length < 28:
        print(
            "- Consider tracking your cycle and "
            "symptoms to identify any patterns."
        )
        print(
            "- If you experience irregular cycles,"
            " consult a healthcare professional."
        )
    else:
        print(
            "- Maintain a healthy lifestyle with "
            "regular exercise and a balanced diet."
        )
        print(
            "- Get plenty of rest and "
            "manage stress during your period."
        )

    # Check the period duration and offer relevant advice
    if period_duration > 7:
        print(
            "- If you experience prolonged periods,"
            " consider consulting a healthcare professional."
        )

    # Check for specific symptoms and offer advice based on them
    if "cramps" in symptoms.lower():
        print(
            "- Engage in light exercises,"
            " such as yoga or walking, to reduce cramps."
        )


# Function to display exercises tips
def display_exercises_tips():
    print("\nExercises Tips:")
    print("""
    Regular physical activity can help reduce menstrual cramps,
    improve mood, and promote overall well-being during your menstrual cycle.
    Here are some exercises that you can try
    to alleviate discomfort and boost your mood:
    """)

    # List of exercises to reduce cramps and improve mood
    exercises = [
        "Yoga: Child's Pose",
        "Walking or Jogging",
        "Biking",
        "Swimming",
        "Dancing",
        "Pilates",
    ]
    for i, exercise in enumerate(exercises, start=1):
        print(f"{i}. {exercise}")


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
        print(
            f"{fertile_start.strftime('%d/%m/%Y')} to "
            f"{fertile_end.strftime('%d/%m/%Y')}"
        )

    elif choice == "4":
        # Display the calculated next period date
        print(
            f"\nNext Period Date: {next_period.strftime('%d/%m/%Y')}"
        )
    elif choice == "5":
        # Display personalized recommendations
        personalized_recommendations(
            cycle_length, period_duration, symptoms
        )
    elif choice == "6":
        # Display exercises tips
        display_exercises_tips()
    elif choice == "7":
        print(
            "Thank you for using FemmeFlow Tracker! Have a great day!"
        )
        break  # Exit the application loop if the user chooses to quit
    else:
        print(
            Fore.RED +
            "Invalid choice. Please enter a number between 1 and 7." +
            Fore.RESET
        )

    # Pause before clearing the screen
    input("Press Enter to continue...\n")

    # Clear the screen after the input is received
    os.system('cls' if os.name == 'nt' else 'clear')
