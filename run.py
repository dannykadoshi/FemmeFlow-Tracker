import datetime
import webbrowser
import pyfiglet
from colorama import init, Fore
import os
import prettytable
import gspread
import textwrap
from google.oauth2.service_account import Credentials
from time import sleep
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


# Function to wrap text to a maximum width of 75
def wrap_text(text):
    return textwrap.fill(text, width=75)


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
    print(
        wrap_text("This application allows you to track your menstrual cycle and "
                  "predict your next period date. "
                  "You can enter your menstrual cycle data in the Google Form, "
                  "and we'll calculate the next period date for you. "
                )
    )
    print()
    print("Let's get started! 🚀")
    print()


# Call the introduction function
introduction()

# Open google form in the browser
def open_google_form():
    form_url = "https://forms.gle/ja7VxdgBAutRLz348"
    webbrowser.open(form_url)
    print(wrap_text(
        "Google Form opened in your web browser. "
        "Please enter your information there. "
    ))
    print()
    print(wrap_text(
        "After entering the information, "
        "you can come back to this terminal to see "
        "the calculated next period date."
    ))
    print()

# Get the email address used in the Google Form
def get_user_email():
    print("\nIf you have filled in the form, please enter the email address used:")
    user_email = input().strip().lower()
    while not user_email:
        print(Fore.RED + "Please enter a valid email address." + Fore.RESET)
        user_email = input().strip().lower()
    return user_email

# Prompt the user with an option to open the Google Form
print("Would you like to enter your information in the Google Form? (yes/no)")
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
    print("You chose not to enter your information in the Google Form.")
    print("For FemmeFlow Tracker to work, it requires your menstrual cycle data.")
    reconsider_response = input("Would you like to reconsider and open the Google Form now? (yes/no)").strip().lower()

    while reconsider_response not in ['yes', 'no']:
        print(Fore.RED + "Invalid response. Please enter 'yes' or 'no'." + Fore.RESET)
        reconsider_response = input().strip().lower()

    if reconsider_response == 'yes':
        open_google_form()
        input("Press Enter when you have submitted the data in the Google Form...")
    elif reconsider_response == 'no':
        print("Thank you for using FemmeFlow Tracker! Have a great day!")
        exit()  # Exit the application

# Get the user's email address and proceed to display options
user_email = get_user_email()

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


    print("Data updated successfully.")


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
    print("\nHealth Tips:")
    tips = {
        1: "Maintain a healthy diet and drink plenty of water.",
        2: "Exercise regularly to improve overall health and manage stress.",
        3: "Ensure you get enough sleep and rest during your menstrual cycle.",
        4: "Consider using a menstrual tracking app to keep track of your cycles and symptoms.",
        5: "Manage stress through relaxation techniques like meditation or deep breathing.",
        6: "Limit caffeine and alcohol intake, as they can affect your menstrual cycle.",
        7: "Avoid smoking and exposure to secondhand smoke for better reproductive health.",
        8: "Engage in activities that bring you joy and help you relax.",
        9: "Consider taking supplements like iron and calcium to support your health.",
        10: "Listen to your body and take breaks when needed, especially during your period.",
    }

    if cycle_type.lower() == 'irregular':
        tips[11] = "If you have irregular cycles, consider keeping a symptom diary to identify patterns."
        tips[12] = "Talk to your healthcare provider to rule out any underlying health issues."
        tips[13] = "Stay prepared with period supplies since irregular cycles can be unpredictable."

    # Create a table with two columns: Tip Number and Tip Text
    table = PrettyTable()
    table.field_names = ["Tip Number", "Tip Text"]

    # Set the maximum width for the Tip Text column
    table.max_width["Tip Text"] = 60

    # Add each tip to the table
    for tip_number, tip_text in tips.items():
        table.add_row([tip_number, wrap_text(tip_text)])

    # Print the table
    print(table)



# Function to display personalized recommendations in a table
def display_recommendations_table(symptom, tips):
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

# Function to display personalized recommendations
def personalized_recommendations(cycle_length, period_duration, symptoms):
    print("\033[91mBased on your menstrual cycle data and symptoms,"
          " we have some personalized recommendations to help you stay healthy"
          " and comfortable during your period:\033[0m")

    # Check the cycle length and offer relevant advice
    if cycle_length < 28:
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

    # Check if the period length is too short
    if period_duration < 3:
        print(
            "- If you experience very short periods,"
            " consider discussing this with a healthcare professional."
        )    

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
        # Add more symptoms and recommendations here
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
        display_recommendations_table(symptom, recommendations[symptom])

    print("\nThese recommendations are meant to provide general guidance."
          " For personalized advice, consult with a healthcare professional.")


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


# Function to display the Form Submission Data in a table
def display_form_submission_data(timestamp, last_period, cycle_length, period_duration,
                                 cycle_type, cycle_lengths, symptoms, email, name, age):
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.add_row(["Timestamp", timestamp])
    table.add_row(["Last Period Date", last_period.strftime('%d/%m/%Y')])
    table.add_row(["Cycle Length", f"{cycle_length} days"])
    table.add_row(["Period Duration", f"{period_duration} days"])
    table.add_row(["Cycle Type", cycle_type])
    table.add_row(["Cycle Lengths (if irregular)", cycle_lengths])
    table.add_row(["Symptoms/Additional Information", symptoms])
    table.add_row(["Email", email])
    table.add_row(["Name", name])
    table.add_row(["Age", age])

    print("\nForm Submission Data:")
    print(table)

# Function to display fertile days
def display_fertile_days(fertile_start, fertile_end):
    print("\nFertile Days:")
    table = PrettyTable(["Start Date", "End Date"])
    table.add_row([fertile_start.strftime('%d/%m/%Y'), fertile_end.strftime('%d/%m/%Y')])
    print(table)

# Function to display the calculated next period date
def display_next_period_date(next_period):
    print("\nNext Period Date:")
    table = PrettyTable(["Date"])
    table.add_row([next_period.strftime('%d/%m/%Y')])
    print(table)    


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
        display_form_submission_data(
            timestamp, last_period, cycle_length, period_duration, cycle_type,
            cycle_lengths, symptoms, email, name, age
        )
        # Offer the option to update the data
        print("\nWould you like to update your data? (yes/no)")
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