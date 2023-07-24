import datetime
import webbrowser
import pyfiglet
from colorama import init, Fore
import os
import prettytable
import gspread
import textwrap
import cursor
import sys
import time
from google.oauth2.service_account import Credentials
from time import sleep
from datetime import timedelta
from prettytable import PrettyTable

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


def animate_text(message, delay=0.05):
    """
    Prints the passed string to the console, simulating a typewriter.
    """
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)


def wrap_text(text, width=75, color=None):
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
    sleep(1)

    # Clear the screen again
    clear()

# Function to center the logo
def center_logo(logo_lines, width):
    centered_logo = []
    for line in logo_lines:
        centered_line = line.center(width)
        centered_logo.append(centered_line)
    return '\n'.join(centered_logo)

# Function to display the welcome message in red and bigger
def display_welcome_message():
    welcome_message = "🌺 WELCOME TO FEMMEFLOW TRACKER! 🌺"
    red_welcome_message = f"{Fore.RED}{welcome_message}{Fore.RESET}"
    print(red_welcome_message)

# Introduction page for the application
def introduction():
    display_name()
    display_welcome_message()
    print()

    wrapped_text = wrap_text("This application allows you to track your menstrual cycle and "
                             "predict your next period date. "
                             "You can enter your menstrual cycle data in the Google Form, "
                             "and we'll calculate the next period date for you.", color=Fore.GREEN)

    for line in wrapped_text:
        animate_text(line)

    print()
    print()
    animate_text("Let's get started! 🚀")
    print()
    print()

# Call the introduction function
introduction()

def open_google_form():
    form_url = "https://forms.gle/ja7VxdgBAutRLz348"
    webbrowser.open(form_url)

    print(wrap_text(
        "Google Form opened in your web browser. "
        "Please enter your information there."
    ))
    print()
    print(wrap_text(
        "After entering the information, "
        "you can come back to this terminal to see "
        "the calculated next period date."
    ))
    print()
    print()

# Get the email address used in the Google Form
def get_user_email():
    animate_text("\nIf you have filled in the form, please enter the email address used:  ")
    print()
    print()
    print(Fore.GREEN, end='')
    user_email = input().strip().lower()
    while not user_email:
        animate_text(Fore.RED + "Please enter a valid email address." + Fore.RESET)
        user_email = input().strip().lower()
    return user_email

# Prompt the user with an option to open the Google Form
animate_text("Would you like to enter your information in the Google Form? (yes/no)")
print()
print()
response = input().strip().lower()
clear()

# Validate the user's response
while response not in ['yes', 'no']:
    print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
    response = input().strip().lower()

# If the user enters 'yes', open the Google Form in the web browser
if response == 'yes':
    open_google_form()
    input("Press Enter when you have submitted the data in the Google Form...")
else:
    animate_text("You chose not to enter your information in the Google Form.")
    print()
    print()
    animate_text("For FemmeFlow Tracker to work, it requires your menstrual cycle data.")
    print()
    print()
    reconsider_response = input("Would you like to reconsider and open the Google Form now? (yes/no)  ").strip().lower()
    clear()

    while reconsider_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
        reconsider_response = input().strip().lower()

    if reconsider_response == 'yes':
        print()
        open_google_form()
        input("Press Enter when you have submitted the data in the Google Form...")
    elif reconsider_response == 'no':
        print("Thank you for using FemmeFlow Tracker! Have a great day!")
        print()
        exit()  # Exit the application

# Get the user's email address and proceed to display options
user_email = get_user_email()
clear()

# Fetch the user's data based on the provided email address
def fetch_user_data(email, expected_columns):
    try:
        # Find all rows with the matching email address
        email_column = 8  # Column index for the email address (zero-based)
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
            key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S"),
            reverse=True,
        )

        return valid_user_data
    except gspread.exceptions.CellNotFound:
        return None

# Define the number of expected columns
EXPECTED_COLUMNS = 11

# Fetch the user data from Google Sheets
user_data = fetch_user_data(user_email, EXPECTED_COLUMNS)

# Check if the user data is found
while not user_data:
    print(
        Fore.RED + "User data not found for the provided email address." + Fore.RESET
    )
    print("Do you want to try entering the correct email address again? (yes/no)")
    print()
    retry_response = input().strip().lower()

    while retry_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
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
    cycle_type, cycle_lengths, symptoms, email, \
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


# Function to display the available options for the user to choose from
def print_options():
    # Initialize colorama
    init(autoreset=True)

    # Description guiding the user
    description = (
        "Please choose an option by entering the corresponding number"
    )
    print(f"{Fore.YELLOW}{description}{Fore.RESET}")
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
    global last_period, cycle_length, period_duration, cycle_type, cycle_lengths, symptoms

    print("\nUpdate Data:")
    print("Enter 'skip' for any field you want to leave unchanged.")

    # Get the updated last period date
    updated_last_period = input(
        f"Last Period Date ({last_period.strftime('%d/%m/%Y')}): "
    ).strip()
    if updated_last_period.lower() != 'skip':
        try:
            last_period = datetime.datetime.strptime(
                updated_last_period, "%d/%m/%Y"
            ).date()
        except ValueError:
            print(Fore.RED + "Invalid date format. Last Period Date not updated." + Fore.RESET)

    # Get the updated cycle length
    updated_cycle_length = input(
        f"Cycle Length ({cycle_length} days): "
    ).strip()
    if updated_cycle_length.lower() != 'skip':
        try:
            cycle_length = int(updated_cycle_length)
        except ValueError:
            print(Fore.RED + "Invalid input. Cycle Length not updated." + Fore.RESET)

    # Get the updated period duration
    updated_period_duration = input(
        f"Period Duration ({period_duration} days): "
    ).strip()
    if updated_period_duration.lower() != 'skip':
        try:
            period_duration = int(updated_period_duration)
        except ValueError:
            print(Fore.RED + "Invalid input. Period Duration not updated." + Fore.RESET)

    # Get the updated cycle type
    updated_cycle_type = input(
        f"Cycle Type ({cycle_type}): "
    ).strip()
    if updated_cycle_type.lower() != 'skip':
        cycle_type = updated_cycle_type

    # Get the updated cycle lengths for irregular cycles
    updated_cycle_lengths = input(
        f"Cycle Lengths (if irregular) ({cycle_lengths}): "
    ).strip()
    if updated_cycle_lengths.lower() != 'skip':
        cycle_lengths = updated_cycle_lengths

    # Get the updated symptoms/additional information
    updated_symptoms = input(
        f"Symptoms/Additional Information ({symptoms}): "
    ).strip()
    if updated_symptoms.lower() != 'skip':
        symptoms = updated_symptoms

    # Update the Google Sheets with the new data
    update_google_sheets(user_email, last_period, cycle_length, period_duration, cycle_type, cycle_lengths, symptoms)

     # Animate the "Data updated successfully" message
    print() 
    print(Fore.GREEN, end='')
    success_message = "Data updated successfully."
    animate_text(success_message)
    print()
    print()


def update_google_sheets(email, last_period, cycle_length, period_duration, cycle_type, cycle_lengths, symptoms):
    # Find all rows with the matching email address
    email_column = 8  # Column index for the email address (zero-based)
    email_cells = responses.findall(email)
    user_rows = {cell.row for cell in email_cells}

    # Update each row with the new data
    for row in user_rows:
        SHEET.worksheet('responses').update_cell(row, 2, last_period.strftime('%d/%m/%Y'))
        SHEET.worksheet('responses').update_cell(row, 3, str(cycle_length))
        SHEET.worksheet('responses').update_cell(row, 4, str(period_duration))
        SHEET.worksheet('responses').update_cell(row, 5, cycle_type)
        SHEET.worksheet('responses').update_cell(row, 6, cycle_lengths)
        SHEET.worksheet('responses').update_cell(row, 7, symptoms)


# Function to calculate dates and personalized recommendations based on user data
def calculate_dates_and_recommendations():
    global fertile_start, fertile_end, next_period
    next_period = last_period + datetime.timedelta(days=cycle_length)
    fertile_start = last_period + datetime.timedelta(days=13)
    fertile_end = last_period + datetime.timedelta(days=19)

    # Calculate personalized recommendations based on user data
    personalized_recommendations(cycle_length, period_duration, symptoms)


# Function to display health tips
def display_health_tips():
    print(f"\n{Fore.YELLOW}HEALTH TIPS 🌟{Fore.RESET}")
    print()

    # Description of the tips
    description = wrap_text(
        f"{Fore.GREEN}Taking care of your health during your menstrual cycle is essential. "
        "Follow these tips to improve your well-being and make your period more manageable. "
        "Explore personalized recommendations in the main menu to discover more insights related to the data you've provided."
    )
    print(description)
    print()

    tips = {
        1: "Maintain a healthy diet and drink plenty of water.",
        2: "Exercise regularly to improve overall health and manage stress.",
        3: "Ensure you get enough sleep and rest during your menstrual cycle.",
        4: "Manage stress through relaxation techniques like meditation or deep breathing.",
        5: "Limit caffeine and alcohol intake, as they can affect your menstrual cycle.",
        6: "Avoid smoking and exposure to secondhand smoke for better reproductive health.",
        7: "Consider taking supplements like iron and calcium to support your health.",
        8: "Listen to your body and take breaks when needed, especially during your period.",
    }

    if cycle_type.lower() == 'irregular':
        tips[9] = "If you have irregular cycles, consider keeping a symptom diary to identify patterns."
        tips[10] = "Talk to your healthcare provider to rule out any underlying health issues."
        tips[11] = "Stay prepared with period supplies since irregular cycles can be unpredictable."

    # Create a table with two columns: Tip Number and Tip Text
    table = PrettyTable()
    table.field_names = ["Tip Number", "Tip Text"]

    # Set the maximum width for the Tip Text column
    table.max_width["Tip Text"] = 70

    # Add each tip to the table
    for tip_number, tip_text in tips.items():
        table.add_row([tip_number, wrap_text(tip_text)])

    # Print the table
    print(table)
    print()



# Function to display personalized recommendations in a table
def display_recommendations_table(symptom, tips):
    print(f"\n\033[91mHere are some tips for dealing with {symptom}:\033[0m")

    # Create a table with two columns: Tip Number and Tip Text
    table = PrettyTable()
    table.field_names = ["Tip Number", "Tip Text"]

    # Set the maximum width for the columns
    table.max_width["Tip Text"] = 70

    # Add each tip to the table
    for i, tip in enumerate(tips, start=1):
        table.add_row([i, tip])

    # Print the table
    print(table)


#Function to define Personalized recommendations based on the User data
def personalized_recommendations(cycle_length, period_duration, symptoms):
    intro_message = (
        "Based on your menstrual cycle data and symptoms,"
        " we have some personalized recommendations to help you stay healthy"
        " and comfortable during your period:"
    )
    print(wrap_text(intro_message))

    # Check the cycle length and offer relevant advice
    if cycle_length < 28:
        cycle_advice = [
            "- Maintain a healthy lifestyle with regular exercise and a balanced diet.",
            "- Get plenty of rest and manage stress during your period."
        ]
        print("\n\033[1mCycle Length Advice (if cycle < 28 days):\033[0m")
        cycle_table = PrettyTable(["Recommendations"])
        cycle_table.max_width["Recommendations"] = 70
        for rec in cycle_advice:
            cycle_table.add_row([wrap_text(rec)])
        print(cycle_table)

    # Check the period duration and offer relevant advice
    if period_duration > 7:
        duration_advice = [
            "- If you experience prolonged periods, consider consulting a healthcare professional."
        ]
        print("\n\033[1mPeriod Duration Advice (if duration > 7 days):\033[0m")
        duration_table = PrettyTable(["Recommendations"])
        duration_table.max_width["Recommendations"] = 70
        for rec in duration_advice:
            duration_table.add_row([wrap_text(rec)])
        print(duration_table)

    # Check if the period length is too short
    if period_duration < 3:
        short_period_advice = [
            "- If you experience very short periods, consider discussing this with a healthcare professional."
        ]
        print("\n\033[1mShort Period Advice (if duration < 3 days):\033[0m")
        short_period_table = PrettyTable(["Recommendations"])
        short_period_table.max_width["Recommendations"] = 70
        for rec in short_period_advice:
            short_period_table.add_row([wrap_text(rec)])
        print(short_period_table)


    # Define the personalized recommendations for each symptom
    recommendations = {
        "Cramps": [
            "Engage in light exercises, such as yoga or walking, to reduce cramps.",
            "Apply a heating pad to the lower abdomen to soothe cramps."
        ],
        "Acne": [
            "Keep your skin clean and consider using non-comedogenic skincare products.",
            "Avoid touching your face and change pillowcases regularly to prevent acne breakouts."
        ],
        "Nausea": [
            "Avoid greasy or heavy foods, and try eating smaller, more frequent meals.",
            "Drink ginger tea or peppermint tea to help alleviate nausea."
        ],
        "Anxiety": [
            "Practice deep breathing exercises and consider talking to a supportive friend or family member.",
            "Engage in regular physical activity to help reduce anxiety."
        ],
        "Breast Tenderness": [
            "Wear a supportive bra and consider applying a warm compress to alleviate breast tenderness.",
            "Avoid consuming caffeine and salty foods, which can worsen breast tenderness."
        ],
        "Food Cravings": [
            "Satisfy cravings in moderation, and try to choose healthier alternatives when possible.",
            "Keep healthy snacks, like fruits and nuts, readily available to curb cravings."
        ],
        "Insomnia": [
            "Create a bedtime routine to relax before sleep, and avoid caffeine and electronic devices before bedtime.",
            "Use blackout curtains and white noise machines to create a sleep-friendly environment."
        ],
        "Hot Flashes": [
            "Wear lightweight and breathable clothing, and try to stay in a cool environment.",
            "Avoid triggers like spicy foods and caffeine that can worsen hot flashes."
        ],
        "Dizziness": [
            "Stay hydrated and avoid sudden changes in position. If dizziness persists, consult a healthcare professional.",
            "Practice relaxation techniques, such as deep breathing, to manage dizziness."
        ],
        "Fatigue": [
            "Ensure you are getting enough rest and consider taking short naps if needed.",
            "Eat energy-boosting foods like fruits, nuts, and whole grains to combat fatigue."
        ],
        "Insomnia": [
            "Create a bedtime routine to relax before sleep, and avoid caffeine and electronic devices before bedtime.",
            "Use blackout curtains and white noise machines to create a sleep-friendly environment."
        ],
        "Anxiety": [
            "Practice deep breathing exercises and consider talking to a supportive friend or family member.",
            "Engage in regular physical activity to help reduce anxiety."
        ]
    }
    # Filter the symptoms based on the user's input
    user_symptoms = symptoms.split(",")
    user_symptoms = [symptom.strip().capitalize() for symptom in user_symptoms if symptom.strip().capitalize() in recommendations]
    
    # Display personalized recommendations for each selected symptom
    for symptom in user_symptoms:
        print(f"\n\033[1m{symptom}:\033[0m")
        table = PrettyTable(["Recommendations"])
        table.max_width["Recommendations"] = 70  # Set the maximum width for the table
        for rec in recommendations[symptom]:
            table.add_row([wrap_text(rec)])
        print(table)
    print()
    advisory_message = (
    "🚨 These recommendations are meant to provide general guidance."
    " For personalized advice, consult with a healthcare professional. 🚨"
    )
    print(wrap_text(wrap_text(advisory_message, color=Fore.RED)))
    print()



# Function to display exercises tips
def display_exercises_tips():
    print(f"\n{Fore.YELLOW}EXERCICES TIPS 🚴‍♀️ 🏃‍♀️ 🧘‍♀️{Fore.RESET}")
    print()
    exercise_description = wrap_text(
        "Regular physical activity can help reduce menstrual cramps, "
        "improve mood, and promote overall well-being during your menstrual cycle. "
        "Here are some exercises that you can try to alleviate discomfort and boost your mood."
    )

    print(exercise_description)


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
        "Zumba",
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

    # Print the tables
    print()
    print(cramp_table)

    print()
    print(mood_table)
    print()


# Function to display the Form Submission Data in a table
def display_form_submission_data(timestamp, last_period, cycle_length, period_duration,
                                 cycle_type, cycle_lengths, symptoms, email, name, age):
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.add_row(["Name", name])
    table.add_row(["Age", age])
    table.add_row(["Email", email])    
    table.add_row(["Last Period Date", last_period.strftime('%d/%m/%Y')])
    table.add_row(["Cycle Length", f"{cycle_length} days"])
    table.add_row(["Period Duration", f"{period_duration} days"])
    table.add_row(["Cycle Type", cycle_type])
    table.add_row(["Cycle Lengths (if irregular)", cycle_lengths])
    table.add_row(["Symptoms/Additional Information", symptoms])


    print(f"\n{Fore.YELLOW}FORM SUBMISSION DATA 🗄️  📝{Fore.RESET}")
    print()

    # Description of the Form submission data
    submission_description = wrap_text(
    f"{Fore.GREEN}Thank you for submitting your data!" 
    "Your menstrual cycle information is essential for providing personalized insights and tips." 
    "By tracking your cycle, you can better understand your body and take proactive steps to manage "
    "your well-being." 
    "Access the main menu to explore your data, view tips, and receive recommendations tailored to your needs."
    )

    print(submission_description)
    print()
    print(table)

# Function to display fertile days for the next 6 months
def display_fertile_days(fertile_start, fertile_end):
    print(f"\n{Fore.YELLOW}FERTILE DAYS FOR THE NEXT 6 MONTHS 📆  🌼{Fore.RESET}")
    print()

    # Description for the fertile days function
    fertile_description = wrap_text(
        f"{Fore.GREEN}Knowing your fertile days can be helpful if you're planning a pregnancy "
        "or want to be aware of when you are most likely to conceive." 
        "These are the projected fertile days for the next 6 months based on your menstrual cycle data."
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

# Function to display the calculated next period date for the next 6 months
def display_next_period_date(next_period):
    print(f"\n{Fore.YELLOW}NEXT PERIOD DATES FOR THE NEXT 6 MONTHS 📅  🌺{Fore.RESET}")
    table = PrettyTable(["Month", "Next Period Date"])
    for _ in range(6):
        table.add_row([
            next_period.strftime('%B %Y'),
            next_period.strftime('%d/%m/%Y')
        ])
        next_period += timedelta(days=28)
    print(table)
    print()


# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Main loop of the application
while True:
    # Clear the screen before printing the options
    clear_screen()

    # Print the options table for the user to choose from
    print_options()

    # Get the user's choice
    print()
    choice = input("Enter your choice: ")

    # Clear the screen after the user inputs their choice
    clear_screen()

    # Process the user's choice and execute the corresponding action
    if choice == "1":
        display_health_tips()
    elif choice == "2":
        # Print the fetched data and calculated dates
        display_form_submission_data(
            timestamp, last_period, cycle_length, period_duration, cycle_type,
            cycle_lengths, symptoms, email, name, age
        )
        # Offer the option to update the data
        print(f"\n{Fore.RED}❗❗ DISCLAIMER ❗❗{Fore.RESET}")
        print()
        print("Choosing 'yes' will update your data with the new information you provide.")
        print("Choosing 'no' will keep your current data unchanged.")
        print("If no changes are necessary choose 'no' to move on")
        print("\nWould you like to update your data? ('yes' / 'no')")
        print()
        update_choice = input().strip().lower()

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
        print("Thank you for using FemmeFlow Tracker! Have a great day!")
        break  # Exit the application loop if the user chooses to quit
    else:
        print(Fore.RED + "Invalid choice. Please enter a number between 1 and 7." + Fore.RESET)

    # Pause before continuing
    input("Press Enter to continue...\n")