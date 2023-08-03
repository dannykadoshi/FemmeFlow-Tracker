import os
import textwrap
import sys
import pyfiglet
from colorama import init, Fore
from termcolor import colored, cprint

# Module for opening Google Forms in the webbrowser
import webbrowser

# Module for working with Google Sheets and authentication
import gspread
from google.oauth2.service_account import Credentials

# Module for working with time and importing the
# sleep function from time module
import time
from time import sleep

# Module for representing time intervals
import datetime
from datetime import timedelta

# Module for creating and formatting tables in the terminal
import prettytable
from prettytable import PrettyTable

# Module for parsing date strings
from dateutil.parser import parse


# Set up Google Sheets credentials and scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the service account file and create scoped credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorize the gspread client using the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheets document named 'FemmeFlow Tracker (Responses)'
SHEET = GSPREAD_CLIENT.open('FemmeFlow Tracker (Responses)')

# Access the 'responses' worksheet within the Google Sheets document
responses = SHEET.worksheet('responses')


def animate_processing():
    """
    This function displays a sequence of processing symbols
    to simulate an animation while a task is being processed.
    """
    processing_symbols = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        # Print the animation on the same line using carriage return '\r'
        print(
            f"\rProcessing... "
            f"{processing_symbols[i % len(processing_symbols)]}",
            end='', flush=True
        )


def animate_text(message, delay=0.04):
    """
    This function simulates the effect of a typewriter by printing each
    character of the input message with a specified delay between characters.
    """
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)


def wrap_text(text, width=70, color=None):
    """
    This function wraps the input text to the specified maximum width,
    breaking the text into multiple lines.
    If a color is provided, it applies the color to the wrapped text.
    """
    if isinstance(text, list):
        wrapped_list = []
        for item in text:
            if isinstance(item, str):
                wrapped_text = textwrap.fill(item, width=width)
                if color:
                    wrapped_text = f"{color}{wrapped_text}{Fore.RESET}"
                wrapped_list.append(wrapped_text)
            else:
                wrapped_list.append(str(item))
        return wrapped_list
    else:
        wrapped_text = textwrap.fill(text, width=width)
        if color:
            wrapped_text = f"{color}{wrapped_text}{Fore.RESET}"
        return wrapped_text


def clear():
    """
    This function clears the terminal screen using the appropriate
    command based on the operating system.
    It uses 'cls' command for Windows and
    'clear' command for other operating systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def display_name():
    """
    This function displays the application name "FemmeFlow Tracker"
    using ASCII art with an animation effect.
    The ASCII art is generated using the pyfiglet library
    with the "slant" font style.
    """
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

    # Animation step 3: Print each line of ASCII art one by one
    # and sleep for 0.2 seconds
    for line in ascii_art.splitlines():
        print(Fore.RED + line.center(terminal_width) + Fore.RESET)
        sleep(0.2)

    # Animation step 4: Sleep for 1.5 seconds and Clear the screen
    sleep(1.5)
    clear()

    # Clear the screen again
    clear()


def center_logo(logo_lines, width):
    """
    This function takes a list of logo lines and centers each line within
    the specified width.
    It returns a single string containing the centered logo.
    """
    centered_logo = []
    for line in logo_lines:
        centered_line = line.center(width)
        centered_logo.append(centered_line)
    return '\n'.join(centered_logo)


user_name = None  # Initialize the user_name as None


def display_welcome_message():
    """
    This function displays the application name "FemmeFlow Tracker"
    using ASCII art with an animation effect.
    """
    print()
    welcome_message = "🌺 WELCOME TO FEMMEFLOW TRACKER! 🌺"
    red_welcome_message = f"{Fore.RED}{welcome_message}{Fore.RESET}"
    animate_text(red_welcome_message)
    print()


def introduction():
    """
    This function presents the introductory messages to the user.
    It includes the display of the application name and welcome message,
    along with a description of the application's purpose.
    The user is prompted to enter their name, and input validation
    ensures a non-empty name is provided before proceeding.
    """
    display_name()
    display_welcome_message()
    print()

    print(wrap_text("FemmeFlow Tracker is a comprehensive tool designed"
                    " to help you understand and manage your"
                    " menstrual health with ease. "
                    "Whether you want to track your menstrual cycle, predict "
                    "your next period date, receive personalized "
                    "recommendations, or access valuable health tips, "
                    "this application has got you covered! "
                    "Empower yourself with valuable insights about your body"
                    " and well-being "
                    "throughout your menstrual journey.", color=Fore.GREEN))

    print()
    print()

    animate_text("Let's get started! 🚀")
    print()
    print()

    global user_name

    # Ask for the user's name
    while True:
        user_name = input("Please enter your name: ").strip()
        clear()
        if user_name:
            break
        else:
            print(Fore.RED + "Error: Your name is required to continue"
                  + Fore.RESET)

    # Continue with the rest of the introduction
    print()
    print()


# Call the introduction function
introduction()


def open_google_form():
    """
    This function opens a specified Google Form URL in the default web browser,
    allowing the user to enter their information through the form.
    Instructions are then provided to the user, indicating that they should
    enter their information in the Google Form.
    Once the information is entered, the user can return
    to the application to access their data and utilize its features.
    """
    form_url = "https://forms.gle/ja7VxdgBAutRLz348"

    print(f"{Fore.YELLOW}GOOGLE FORM 🗃 {Fore.RESET}")
    print()
    print(Fore.RED + wrap_text("RETURNING USER?") + Fore.RESET)
    print()
    print(wrap_text(
        "Save time! Skip the form, by pressing 'Enter,' and providing the "
        "email address previously used to fill up the Google form."
    ))
    print("Your convenience matters!")
    print()
    print(Fore.GREEN + wrap_text("If you are a new user, fill up the form by "
          "copying and pasting the link bellow in your browser:" + Fore.RESET))
    print()
    cprint("COPY AND PAST THE LINK IN YOUR BROWSER: ", "red", end="")
    print(colored(form_url, "blue", attrs=["underline"]))
    print()
    print(wrap_text(
        "After entering the information, "
        "you can come back here to access "
        "your data and all features of this application"
    ))
    print()

    webbrowser.open(form_url)


def get_user_email():
    """
    This function prompts the user to enter their email address,
    which should match the email address they provided in the Google Form.
    If the user does not provide a valid email address, an error message is
    displayed, and they are prompted again until
    a valid email address is entered.
    """
    print(f"{Fore.YELLOW}{user_name},{Fore.RESET}")
    print()
    print("Enter the email address used to fill up the Form:")
    print()
    print(Fore.GREEN, end='')
    user_email = input().strip().lower()
    while not user_email:
        animate_text(Fore.RED + "Please enter a valid email "
                     "address." + Fore.RESET)
        print()
        user_email = input().strip().lower()

    return user_email


def display_prompt_message():
    """
    This function displays a prompt message informing the user about
    the requirement to complete a form with essential information in
    order to use the application.
    """
    prompt_message = "To use this application, kindly complete a " \
                     "form providing essential information."

    red_prompt_message = f"{Fore.RED}{prompt_message}{Fore.RESET}"
    animate_text(red_prompt_message)


# Prompt the user with an option to open the Google Form
display_prompt_message()
print()
print()
print(f"{Fore.YELLOW}{user_name}, would you like to enter your "
      f"information in the Google Form? (yes/no){Fore.RESET}")
print()
response = input().strip().lower()
clear()

# Validate the user's response
while response not in ['yes', 'no']:
    print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'."
          + Fore.RESET)

    response = input().strip().lower()

clear()    

# If the user enters 'yes', open the Google Form in the web browser
if response == 'yes':
    open_google_form()
    print(f"{Fore.YELLOW}Press Enter when you have submitted the "
          f"data in the Google Form...{Fore.RESET}")

    input()  # Wait for the user to press Enter
    clear()
else:
    animate_text("You chose not to enter your information in the Google Form.")
    print()
    print()
    animate_text("For FemmeFlow Tracker to work, it requires your "
                 "menstrual cycle data.")

    print()
    print()
    reconsider_response = input("Would you like to reconsider and open the "
                                "Google Form now? (yes/no)  ").strip().lower()

    clear()

    while reconsider_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'.")
        reconsider_response = input().strip().lower()
        print(Fore.RESET)

    if reconsider_response == 'yes':
        print()
        open_google_form()
        input("Press Enter when you have submitted the data "
              "in the Google Form...")

    elif reconsider_response == 'no':
        print()
        print(f"{Fore.YELLOW}{user_name}{Fore.RESET}")
        print()
        print(f"{Fore.GREEN}Thank you for accessing FemmeFlow "
              "Tracker!{Fore.RESET}")
        print(f"{Fore.GREEN}To unlock all the application functions, "
              "data submission is required!{Fore.RESET}")
        print(f"{Fore.GREEN}If you change your mind, you're welcome to "
              "come back at any time.{Fore.RESET}")
        print(f"{Fore.GREEN}We hope to see you again soon! "
              "Have a great day!{Fore.RESET}")

        print()
        exit()

# Get the user's email address and proceed to display options
user_email = get_user_email()
clear()


def fetch_user_data(email, expected_columns):
    """
    This function searches for rows in the Google Sheets response
    worksheet that match the provided email address.
    It retrieves and processes the user data, filtering out invalid entries
    and sorting the responses by timestamp to get the latest one.
    """
    try:
        # Find all rows with the matching email address
        email_cells = responses.findall(email)
        user_rows = {cell.row for cell in email_cells}

        # Get the user data from the rows
        user_data = [responses.row_values(row) for row in user_rows]

        # Filter out invalid data
        valid_user_data = [
            data for data in user_data if len(data) == expected_columns
        ]

        if not valid_user_data:
            return None

        # Sort responses by timestamp in descending order to get the latest one
        valid_user_data.sort(
            key=lambda x:
            datetime.datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S"),
            reverse=True,
        )

        return valid_user_data
    except gspread.exceptions.CellNotFound:
        return None


# Define the number of expected columns
EXPECTED_COLUMNS = 10

# Fetch the user data from Google Sheets
user_data = fetch_user_data(user_email, EXPECTED_COLUMNS)

# Check if the user data is found
while not user_data:
    print(
        Fore.RED + "User data not found for the " +
        "provided email address." + Fore.RESET
    )
    print("Do you want to try entering the correct " +
          "email address again? (yes/no)")
    print()
    retry_response = input().strip().lower()
    print()

    while retry_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." +
              Fore.RESET)
        retry_response = input().strip().lower()

    if retry_response == 'yes':
        user_email = get_user_email()
        user_data = fetch_user_data(user_email, EXPECTED_COLUMNS)
    else:
        print("Exiting FemmeFlow Tracker. Have a great day!")
        exit()  # Exit the application

# Extract the user's inputs from the latest Google Sheets response
latest_response = user_data[0]
timestamp_str, last_period_str, cycle_length_str, period_duration_str, \
    cycle_type, symptoms, email, \
    name, age, form_publisher = latest_response

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


def print_options():
    """
    This function prints a table of available options that the user can choose
    from. Each option is assigned a corresponding number, and a description of
    each option is provided.
    """
    # Initialize colorama
    init(autoreset=True)

    # Description guiding the user
    description = (
        "please choose an option by entering the corresponding number"
    )
    print()
    print(f"{Fore.YELLOW}{user_name}, {description}{Fore.RESET}")
    print()

    # Create the table with available options
    table = prettytable.PrettyTable()
    table.field_names = ["Option", "Description"]
    table.add_row(["1", "Health Tips"])
    table.add_row(["2", "Form Submission Data"])
    table.add_row(["3", "Fertile Days"])
    table.add_row(["4", "Next Period Date"])
    table.add_row(["5", "Personalized Recommendations"])
    table.add_row(["6", "Exercises Tips"])
    table.add_row(["7", "Quit the application"])

    # Set the table text color to red using colorama
    red_table = f"{Fore.RED}{table}{Fore.RESET}"
    print(red_table)


# Function to update user data in the terminal
def update_data():
    """
    Update user data in the terminal.

    This function guides the user through updating their menstrual cycle data.
    It prompts the user to input new details, if their data is wrong or
    needs to be updated.
    The user's data is updated based on the provided information.
    The user is guided through each step of the update process,"
    " and the function performs
    input validation to ensure that valid data is entered.

    The user can choose to skip updating a specific field"
    " by entering 'skip' as the input.
    """
    global last_period, cycle_length, period_duration, \
        cycle_type, symptoms

    print(f"{Fore.YELLOW}UPDATE DATA 🗃{Fore.RESET}")
    print()
    print(f"{Fore.GREEN}Please enter the new details below, and your "
          f"data will be updated in our systems.{Fore.RESET}")
    print(f"{Fore.RED}Your name and age cannot be updated{Fore.RESET}")
    print()

    # Get the updated last period date
    while True:
        updated_last_period = input(
            f"Last Period Date ({last_period.strftime('%d/%m/%Y')}): "
        ).strip()

        if updated_last_period.lower() == 'skip':
            break
        elif updated_last_period == '':
            print(Fore.RED + "Invalid input. Last Period date not " +
                  "updated." + Fore.RESET)
            break
        else:
            try:
                last_period = datetime.datetime.strptime(updated_last_period,
                                                         '%d/%m/%Y').date()

                break
            except ValueError:
                print(Fore.RED + "Invalid date format. Please enter the date"
                      " in the format dd/mm/yyyy." + Fore.RESET)

    # Get the updated cycle length
    updated_cycle_length = input(
        f"Cycle Length ({cycle_length} days): "
    ).strip()
    if updated_cycle_length.lower() != 'skip':
        try:
            cycle_length = int(updated_cycle_length)
        except ValueError:
            print(Fore.RED + "Invalid input. Cycle Length " +
                  "not updated." + Fore.RESET)

    # Get the updated period duration
    updated_period_duration = input(
        f"Period Duration ({period_duration} days): "
    ).strip()
    if updated_period_duration.lower() != 'skip':
        try:
            period_duration = int(updated_period_duration)
        except ValueError:
            print(Fore.RED + "Invalid input. Period Duration not updated." +
                  Fore.RESET)

    # Get the updated cycle type
    cycle_type_options = ["regular", "irregular", "skip"]
    updated_cycle_type = input(
        f"Cycle Type ({cycle_type}): "
    ).strip().lower()
    if updated_cycle_type in cycle_type_options:
        if updated_cycle_type != 'skip':
            cycle_type = updated_cycle_type
    else:
        print(Fore.RED + "Invalid input. Cycle Lengths (if "
              "irregular) not updated." + Fore.RESET)

    clear()

    # Get the updated symptoms/additional information
    available_symptoms = [
        "Cramps", "Headache", "Mood Swings", "Fatigue", "Bloating", "Acne",
        "Breast Tenderness", "Food Cravings", "Nausea", "Insomnia", "Anxiety",
        "Hot Flashes", "Dizziness"
    ]

    # Description for available symptoms
    symptoms_description = wrap_text(
        f"{Fore.GREEN}Here are the list of symptoms available, type all "
        "that apply separated by comma:"
    )
    print(symptoms_description)

    # Display the available symptoms in a table-like format
    symptoms_table = PrettyTable(["Available Symptoms"])
    symptoms_table.max_width["Available Symptoms"] = 40
    for symptom in available_symptoms:
        symptoms_table.add_row([wrap_text(symptom)])
    print(symptoms_table)

    # Convert all symptom names to lowercase for case-insensitive comparison
    available_symptoms_lower = [symptom.lower() for symptom in
                                available_symptoms]

    # Prompt the user to update symptoms
    while True:
        updated_symptoms = input(
            f"Symptoms/Additional Information ({wrap_text(symptoms)}): "
        ).strip().lower()  # Convert input to lowercase
        clear()

        if updated_symptoms == 'skip':
            break

        # If the user presses Enter without entering anything
        if not updated_symptoms:
            print(Fore.RED + "Invalid input. Symptoms/Additional Information "
                  "not updated." + Fore.RESET)
            print()
            clear()
            break

        # Split the input into a list of symptoms
        updated_symptoms_list = [symptom.strip()
                                 for symptom in updated_symptoms.split(",")]

        # Check if all entered symptoms are valid
        if all(symptom in available_symptoms_lower
               for symptom in updated_symptoms_list):
            # Find the corresponding symptoms in the original case
            # and update the 'symptoms' variable
            symptoms = ", ".join([
                next(symptom for symptom in available_symptoms
                     if symptom.lower() == s)
                for s in updated_symptoms_list
            ])
            break
        else:
            print(Fore.RED + "Invalid input. Please enter valid symptoms"
                  " from the list." + Fore.RESET)

    # Display the processing animation
    print()
    animate_processing()
    print()

    # Update the Google Sheets with the new data
    update_google_sheets(user_email, last_period, cycle_length,
                         period_duration, cycle_type, symptoms)

    # Animate the "Data updated successfully" message
    print()
    print(Fore.GREEN, end='')
    success_message = "Data updated successfully."
    animate_text(success_message)
    print()
    print()


def update_google_sheets(email, last_period, cycle_length,
                         period_duration, cycle_type, symptoms):
    """
    Update user data in Google Sheets based on the provided information.

    This function updates the user's menstrual cycle data in the Google Sheets
    based on the provided information.
    It finds all rows with the matching email
    address and updates each row with the new data.
    """

    # Find all rows with the matching email address
    email_cells = responses.findall(email)
    user_rows = {cell.row for cell in email_cells}

    # Update each row with the new data
    for row in user_rows:
        SHEET.worksheet('responses').update_cell(
            row, 2, last_period.strftime('%d/%m/%Y'))
        SHEET.worksheet('responses').update_cell(row, 3, str(cycle_length))
        SHEET.worksheet('responses').update_cell(row, 4, str(period_duration))
        SHEET.worksheet('responses').update_cell(row, 5, cycle_type)
        SHEET.worksheet('responses').update_cell(row, 6, symptoms)


def calculate_dates_and_recommendations():
    """
    This function calculates the next period date, fertile days start and end
    dates based on the user's last period date and cycle length.
    It also calls the 'personalized_recommendations()' function to generate
    recommendations based on cycle length, period duration, and symptoms.
    The calculated dates and recommendations are stored in global variables
    for later use.
    """
    global fertile_start, fertile_end, next_period
    next_period = last_period + datetime.timedelta(days=cycle_length)
    fertile_start = last_period + datetime.timedelta(days=13)
    fertile_end = last_period + datetime.timedelta(days=19)

    # Calculate personalized recommendations based on user data
    personalized_recommendations(cycle_length, period_duration, symptoms)


def display_health_tips():
    """
    Display health tips for managing menstrual cycle.

    This function prints a list of health tips to help individuals manage
    their menstrual cycle effectively.
    The tips cover various aspects such as diet, exercise, rest,
    stress management, and more.
    If the user has an irregular cycle, additional tips are provided to address
    specific concerns.
    The tips are displayed in a formatted table for easy readability.
    """
    print(f"\n{Fore.YELLOW}HEALTH TIPS 🌟{Fore.RESET}")
    print()

    # Description of the tips
    description = wrap_text(
        f"{Fore.GREEN}Taking care of your health during your"
        " menstrual cycle is essential. "
        "Follow these tips to improve your well-being and make "
        "your period more manageable. "
    )
    print(description)
    print()
    input("Press Enter to view tips...\n")

    clear()

    # Tips dictionary for regular cycle
    tips_regular = {
        1: "Maintain a healthy diet and drink plenty of water.",
        2: "Exercise regularly to improve health and manage stress.",
        3: "Ensure you get enough sleep and rest during your cycle.",
        4: "Manage stress through relaxation techniques like meditation or "
           "deep breathing.",
        5: "Limit caffeine and alcohol intake, as they can affect your cycle.",
        6: "Consider taking supplements like iron and calcium to support "
           "your health.",
        7: "Practice mindfulness and engage in activities that bring "
           "you joy and relaxation.",
        8: "Keep track of your menstrual cycle on a calendar to better "
           "understand patterns and changes.",

    }

    # Tips dictionary for irregular cycle
    tips_irregular = {
        1: "If you have irregular cycles, consider keeping a symptom diary "
           "to identify patterns.",
        2: "Talk to your healthcare provider to rule out any underlying "
           "health issues.",
        3: "Stay prepared with period supplies since irregular cycles can "
           "be unpredictable.",
        4: "Explore stress-reduction activities like yoga or tai chi to "
           "help regulate your cycle.",
        5: "Maintain a balanced and nutritious diet to support your overall "
           "health and menstrual cycle.",
    }

    # Create a table with two columns: Tip Number and Tip Text
    table_regular = PrettyTable()
    table_regular.field_names = ["Tip Number", "Tip Text"]
    table_irregular = PrettyTable()
    table_irregular.field_names = ["Tip Number", "Tip Text"]

    # Set the maximum width for the Tip Text columns
    table_regular.max_width["Tip Text"] = 60
    table_irregular.max_width["Tip Text"] = 60

    # Add regular tips to the regular tips table
    for tip_number, tip_text in tips_regular.items():
        table_regular.add_row([tip_number, wrap_text(tip_text)])

    # Add irregular tips to the irregular tips table
    for tip_number, tip_text in tips_irregular.items():
        table_irregular.add_row([tip_number, wrap_text(tip_text)])

    # Print the regular tips table
    print(f"\n{Fore.YELLOW}REGULAR PERIOD CYCLE TIPS 🩸{Fore.RESET}")
    print(table_regular)
    print()

    # Check if there are irregular tips to display
    if tips_irregular:
        input("Press Enter to see tips for irregular menstrual cycle...")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.YELLOW}IRREGULAR PERIOD CYCLE TIPS 🩸 🩸{Fore.RESET}")
        print(table_irregular)
        print()
    else:
        input("Press Enter to continue...")


def display_recommendations_table(symptom, tips):
    """
    Display personalized recommendations for dealing with a specific symptom.

    This function displays a table of personalized recommendations for dealing
    with a specific symptom during the menstrual cycle.
    The symptom and its corresponding tips are provided as input parameters.
    The recommendations are displayed in a formatted table for
    easy readability.
    """
    print(f"\n\033[91mHere are some tips for dealing with {symptom}:\033[0m")

    # Create a table with two columns: Tip Number and Tip Text
    table = PrettyTable()
    table.field_names = ["Tip Number", "Tip Text"]

    # Set the maximum width for the columns
    table.max_width["Tip Text"] = 60

    # Add each tip to the table
    for i, tip in enumerate(tips, start=1):
        table.add_row([i, tip])

    # Print the table
    print(table)


def personalized_recommendations(cycle_length, period_duration, symptoms):
    """
    This function generates personalized recommendations for the user based on
    their menstrual cycle data (cycle length and period duration)
    and specific symptoms. The recommendations are provided in a formatted
    manner, addressing various symptoms and offering advice for each.
    """
    print(f"\n{Fore.YELLOW}PERSONALIZED RECOMMENDATIONS ✍🏻 {Fore.RESET}")
    print()
    intro_message = (
        f"{Fore.GREEN}Based on your menstrual cycle data and symptoms,"
        " we have some personalized recommendations to help you stay healthy"
        " and comfortable during your period:"
    )
    print(wrap_text(intro_message))
    print()
    input("Press Enter to continue...")

    clear()

    # Check the cycle length and offer relevant advice
    if cycle_length < 28:
        cycle_advice = [
            "- Maintain a healthy lifestyle with regular exercise"
            " and a balanced diet.",
            "- Get plenty of rest and manage stress during your period."
        ]
        print("\n\033[1mCycle Length Advice (if cycle < 28 days):\033[0m")
        cycle_table = PrettyTable(["Recommendations"])
        cycle_table.max_width["Recommendations"] = 60
        for rec in cycle_advice:
            cycle_table.add_row([wrap_text(rec)])
        print(cycle_table)
        print()
        input("Press Enter to continue...")

    clear()

    # Check the period duration and offer relevant advice
    if period_duration > 7:
        duration_advice = [
            "- If you experience prolonged periods, consider consulting "
            "a healthcare professional."
        ]
        print("\n\033[1mPeriod Duration Advice (if duration > 7 days):\033[0m")
        duration_table = PrettyTable(["Recommendations"])
        duration_table.max_width["Recommendations"] = 60
        for rec in duration_advice:
            duration_table.add_row([wrap_text(rec)])
        print(duration_table)
        print()
        input("Press Enter to continue...")

    clear()

    # Check if the period length is too short
    if period_duration < 3:
        short_period_advice = [
            "- If you experience very short periods, consider discussing "
            "this with a healthcare professional."
        ]
        print("\n\033[1mShort Period Advice (if duration < 3 days):\033[0m")
        short_period_table = PrettyTable(["Recommendations"])
        short_period_table.max_width["Recommendations"] = 60
        for rec in short_period_advice:
            short_period_table.add_row([wrap_text(rec)])
        print(short_period_table)
        print()
        input("Press Enter to continue...")

    clear()

    # Define the personalized recommendations for each symptom
    recommendations = {
        "cramps": [
            "- Engage in light exercises, such as yoga or walking, "
            "to reduce cramps.",
            "- Apply a heating pad to the lower abdomen to soothe cramps."
        ],
        "acne": [
            "- Keep your skin clean and consider using non-comedogenic"
            " skincare products.",
            "- Avoid touching your face and change pillowcases "
            "regularly to prevent acne breakouts."
        ],
        "nausea": [
            "- Avoid greasy or heavy foods, and try eating smaller, "
            "more frequent meals.",
            "- Drink ginger tea or peppermint tea to help alleviate nausea."
        ],
        "anxiety": [
            "- Practice deep breathing exercises and consider talking "
            "to a supportive friend or family member.",
            "- Engage in regular physical activity to help reduce anxiety."
        ],
        "breast tenderness": [
            "- Wear a supportive bra and consider applying a warm compress "
            "to alleviate breast tenderness.",
            "- Avoid consuming caffeine and salty foods, which can worsen "
            "breast tenderness."
        ],
        "food cravings": [
            "- Satisfy cravings in moderation, and try to choose healthier "
            "alternatives when possible.",
            "- Keep healthy snacks, like fruits and nuts, readily available "
            "to curb cravings."
        ],
        "insomnia": [
            "- Create a bedtime routine to relax before sleep, and avoid "
            "caffeine and electronic devices before bedtime.",
            "- Use blackout curtains and white noise machines to create "
            "a sleep-friendly environment."
        ],
        "hot flashes": [
            "- Wear lightweight and breathable clothing, and try to stay "
            "in a cool environment.",
            "- Avoid triggers like spicy foods and caffeine that "
            "can worsen hot flashes."
        ],
        "dizziness": [
            "- Stay hydrated and avoid sudden changes in position."
            " If dizziness persists, consult a healthcare professional.",
            "- Practice relaxation techniques, such as deep breathing, "
            "to manage dizziness."
        ],
        "fatigue": [
            "- Ensure you are getting enough rest and consider taking short "
            "naps if needed.",
            "- Eat energy-boosting foods like fruits, nuts, and whole grains "
            "to combat fatigue."
        ],
        "mood swings": [
            "- Practice mindfulness and meditation techniques to manage "
            "mood swings.",
            "- Engage in activities that bring joy and relaxation, such as "
            "spending time with loved ones or pursuing hobbies."
            "- Consider keeping a mood journal to identify patterns and "
            "triggers for your mood swings."
        ],
        "bloating": [
            "- Stay hydrated and drink plenty of water to help reduce "
            "bloating.",
            "- Avoid consuming foods that are known to cause bloating, "
            "such as beans, cabbage, and carbonated drinks.",
            "- Consider eating smaller, more frequent meals to prevent "
            "overeating and bloating.",
            "- Incorporate foods rich in potassium, such as bananas and "
            "avocados, which can help reduce water retention.",
            "- Try incorporating ginger or peppermint tea into your diet, "
            "as they may help alleviate bloating."
        ],
        "headache": [
            "- Stay hydrated by drinking plenty of water throughout the day.",
            "- Consider applying a cold or warm compress to your forehead.",
            "- Relax in a quiet, dark room to help reduce discomfort.",
            "- Practice deep breathing exercises or meditation to "
            "ease tension.",
            "- Over-the-counter pain relievers like ibuprofen or "
            "acetaminophen may help, but consult a healthcare "
            "professional before use.",
            "- Avoid triggers like bright lights, loud noises, "
            "and certain foods.",
        ]
    }

    # Filter the symptoms based on the user's input
    user_symptoms = symptoms.split(",")
    user_symptoms = [symptom.strip().capitalize()
                     for symptom in user_symptoms
                     if symptom.strip().capitalize() in recommendations]

    # Convert user-inputted symptoms and dictionary keys to lowercase
    user_symptoms = [symptom.strip().lower()
                     for symptom in symptoms.split(",")]

    # Display personalized recommendations for each selected symptom
    for symptom in user_symptoms:
        if symptom in recommendations:
            print(f"\n\033[1m{symptom.capitalize()}:\033[0m")
            table = PrettyTable(["Recommendations"])
            table.max_width["Recommendations"] = 60
            for rec in recommendations[symptom]:
                table.add_row([wrap_text(rec)])
            print(table)
        else:
            print(f"\n\033[1m{symptom.capitalize()}:\033[0m")
            print(wrap_text("No specific recommendations available for "
                            "this symptom."))

        print()
        input("Press Enter to see the next symptom...")
        clear()

    # Display the advisory message with the specified color
    clear()
    print()
    advisory_message = (
        "🚨 These recommendations are meant to provide general guidance."
        " For personalized advice, consult with a healthcare professional. 🚨"
    )
    print(Fore.RED + wrap_text(advisory_message) + Fore.RESET)
    print()


def display_exercises_tips():
    """
    This function provides exercise recommendations that can help
    reduce menstrual cramps, improve mood,
    and promote overall well-being during the menstrual cycle.

    The function displays two separate tables: one for cramp-reducing exercises
    and another for mood-improving exercises.
    """
    print(f"\n{Fore.YELLOW}EXERCICES TIPS 🚴‍♀️ 🏃‍♀️ 🧘‍♀️{Fore.RESET}")
    print()
    exercise_description = wrap_text(
        f"{Fore.GREEN}Regular physical activity can help reduce menstrual "
        "cramps, improve mood, and promote overall well-being during "
        "your menstrual cycle. "
        "Here are some exercises that you can try to alleviate "
        "discomfort and boost your mood."
    )

    print(exercise_description)
    print()

    # List of exercises to reduce cramps and improve mood
    cramp_exercises = [
        "Yoga: Child's Pose",
        "Pilates",
        "Walking or Jogging",
        "Cycling",
        "Swimming",
    ]

    mood_exercises = [
        "Dancing",
        "Hiking",
        "Aerobics",
        "Jump Rope",
        "Tai Chi",
    ]

    # Create a table for cramp exercises
    cramp_table = PrettyTable()
    cramp_table.field_names = ["Cramp-Reducing Exercises"]
    for i, exercise in enumerate(cramp_exercises, start=1):
        cramp_table.add_row([f"{i}. {exercise}"])

    # Create a table for mood-improving exercises
    mood_table = PrettyTable()
    mood_table.field_names = ["Mood-Improving Exercises"]
    for i, exercise in enumerate(mood_exercises, start=1):
        mood_table.add_row([f"{i}. {exercise}"])

    # Get formatted table strings
    cramp_table_str = cramp_table.get_string()
    mood_table_str = mood_table.get_string()

    # Split table strings into lines
    cramp_lines = cramp_table_str.split('\n')
    mood_lines = mood_table_str.split('\n')

    # Print the tables side by side
    for cramp_line, mood_line in zip(cramp_lines, mood_lines):
        print(f"{cramp_line.ljust(40)} {mood_line}")

    print()


def display_form_submission_data(timestamp, last_period, cycle_length,
                                 period_duration, cycle_type,
                                 symptoms, email, name, age):
    """
    This function takes various form submission data as input and presents
    it in a tabular format for display.
    The information includes details about the user's name, age, email,
    last period date, cycle length, period duration, cycle type,
    and symptoms or additional information provided.
    """
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.add_row(["Name", name])
    table.add_row(["Age", age])
    table.add_row(["Email", email])
    table.add_row(["Last Period Date", last_period.strftime('%d/%m/%Y')])
    table.add_row(["Cycle Length", f"{cycle_length} days"])
    table.add_row(["Period Duration", f"{period_duration} days"])
    table.add_row(["Cycle Type", cycle_type])
    table.add_row(["Symptoms/Additional Information", symptoms])

    print(f"\n{Fore.YELLOW}FORM SUBMISSION DATA 🗄️  📝{Fore.RESET}")
    print()

    # Description of the Form submission data
    submission_description = wrap_text(
        f"{Fore.GREEN}Thank you for submitting your data! "
        "Your menstrual cycle information is essential for providing "
        "personalized insights and tips. "
        "By tracking your cycle, you can better understand your body "
        "and take proactive steps to manage "
        "your well-being. "
    )

    print(submission_description)
    print()
    input("Press Enter to view your data...\n")

    clear()

    # Set the max width for each column in the table
    table_max_width = 60
    for field in table.field_names:
        table.max_width[field] = table_max_width

    # Print the table
    print(table)


def display_fertile_days(fertile_start, fertile_end):
    """
    This function takes the start and end dates of the fertile window
    as input and displays the projected fertile days for the
    next 6 months in a tabular format.
    The fertile days information can be useful for individuals who
    are planning a pregnancy or want to be aware of their most likely
    conception periods.
    """
    print(f"\n{Fore.YELLOW}FERTILE DAYS FOR THE NEXT 6 MONTHS 📆",
          f"🌼{Fore.RESET}")

    print()

    # Description for the fertile days function
    fertile_description = wrap_text(
        f"{Fore.GREEN}Knowing your fertile days can be helpful if you're "
        "planning a pregnancy or want to be aware of when you are most "
        "likely to conceive."
        "These are the projected fertile days for the next 6 months "
        "based on your menstrual cycle data."
        f"{Fore.RESET}"
    )

    print(fertile_description)
    print()

    table = PrettyTable(["Month", "Fertile Start Date", "Fertile End Date"])
    for _ in range(6):
        table.add_row([
            fertile_start.strftime('%B %Y'),
            fertile_start.strftime('%d/%m/%Y'),
            fertile_end.strftime('%d/%m/%Y')
        ])
        fertile_start += timedelta(days=28)
        fertile_end += timedelta(days=28)
    print(table)
    print()


def display_next_period_date(next_period):
    """
    This function takes the predicted next period date as input
    and displays the projected start dates of the next six periods
    in a tabular format.
    The information can be useful for individuals who are
    tracking their menstrual cycle for reproductive health
    or planning purposes.
    """
    print(f"\n{Fore.YELLOW}NEXT PERIOD DATES FOR THE NEXT 6 MONTHS 📅",
          f"🌺{Fore.RESET}")

    print()

    # Description for Next period dates
    period_description = wrap_text(
        f"{Fore.GREEN}Tracking your menstrual cycle is vital for "
        "understanding your body and monitoring your reproductive health."
        "Here are the predicted start dates of your periods "
        "for the next six months."
        "These dates can be helpful for planning ahead and being prepared."
        "Keep in mind that individual variations are common, "
        "so the actual dates may differ slightly."
        "Remember to listen to your body and take care "
        "of yourself throughout your cycle."
    )

    print(period_description)
    print()

    table = PrettyTable(["Month", "Next Period Date"])
    for _ in range(6):
        table.add_row([
            next_period.strftime('%B %Y'),
            next_period.strftime('%d/%m/%Y')
        ])
        next_period += timedelta(days=28)
    print(table)
    print()


# Main loop of the application
while True:
    """
    The main loop of the FemmeFlow Tracker application.
    Displays options to the user, processes their choices,
    and executes corresponding actions.
    """
    # Clear the screen before printing the options
    clear()

    # Print the options table for the user to choose from
    print_options()

    # Get the user's choice
    print()
    choice = input("Enter your choice: ")

    # Clear the screen after the user inputs their choice
    clear()

    # Process the user's choice and execute the corresponding action
    if choice == "1":
        display_health_tips()
    elif choice == "2":
        # Print the fetched data and calculated dates
        display_form_submission_data(
            timestamp, last_period, cycle_length, period_duration, cycle_type,
            symptoms, email, name, age
        )
        # Offer the option to update the data
        print()
        print("Do you need to update your details?")
        print()
        print(f"\n{Fore.RED}❗❗ DISCLAIMER ❗❗{Fore.RESET}")
        print()
        text = (f"{Fore.RED}Only update your data, if there are any "
                "inaccuracies or if any changes have occurred "
                "since your last access.")
        wrapped_text = wrap_text(text)
        print(wrapped_text)
        print()
        input("Press Enter to continue...\n")

        clear()

        print()
        print(f"\n{Fore.YELLOW}UPDATING OPTIONS 🗄️  📝{Fore.RESET}")
        print()
        print("Choosing 'yes' will update your data with the new "
              "information you provide.")
        print("Choosing 'no' will keep your current data unchanged.")
        print()
        print(f"\n{Fore.RED}If no changes are necessary "
              f"choose 'no' to move on{Fore.RESET}")
        print()
        print("\nWould you like to update your data? ('yes' / 'no')")
        print()
        update_choice = input().strip().lower()
        clear()

        if update_choice == 'yes':
            update_data()
    elif choice == "3":
        # Display fertile days
        display_fertile_days(fertile_start, fertile_end)

    elif choice == "4":
        # Display the calculated next period date
        display_next_period_date(next_period)
    elif choice == "5":
        # Display personalized recommendations
        personalized_recommendations(
            cycle_length, period_duration, symptoms
        )
    elif choice == "6":
        # Display exercises tips
        display_exercises_tips()
    elif choice == "7":
        print()
        print(f"{Fore.YELLOW}{user_name}{Fore.RESET}")
        print()
        print(f"{Fore.GREEN}Thank you for using FemmeFlow Tracker!",
              f"{Fore.RESET}")
        print(f"{Fore.GREEN}We hope to see you again soon!",
              f"Have a great day!{Fore.RESET}")
        print()
        break
    else:
        print(Fore.RED + "Invalid choice. Please enter a number",
              "between 1 and 7." + Fore.RESET)

    # Pause before continuing
    input("Press Enter to continue...\n")
