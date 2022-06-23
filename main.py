# IMPORTING LIBRARIES
import smtplib
import datetime as dt
import random
import pandas as pd


# CONSTANTS
# FILES
BIRTHDAYS_FILE = "birthdays.csv"
LETTER_1_FILE = "letter_templates/letter_1.txt"
LETTER_2_FILE = "letter_templates/letter_2.txt"
LETTER_3_FILE = "letter_templates/letter_3.txt"
LETTER_FILE = [LETTER_1_FILE, LETTER_2_FILE, LETTER_3_FILE]

# DUMMY CREDENTIALS
FROM_MAIL = "random@yahoo.com"
PASSWORD = "password123"
SMTP_SERVER = "smtp.mail.yahoo.com"
SUBJECT = "Subject:Happy Birthday\n"
RECEIVER_PLACEHOLDER = "[TO_NAME]"
SENDER_PLACEHOLDER = "[FROM_NAME]"
SENDER_NAME = "Adam"


# SEND BIRTHDAY WISH
def send_wish(from_smtp_server, from_mail, password, to_mail, birthday_message):
    try:
        with smtplib.SMTP(from_smtp_server) as connection:
            connection.starttls()
            connection.login(user=from_mail, password=password)
            connection.sendmail(
                from_addr=from_mail, to_addrs=to_mail, msg=birthday_message
            )
    except:
        print(f"Message could not be sent to {to_mail} from {from_mail}.")
    return


# CHECK BIRTHDAY AND SEND WISHES
def check_birthday(birthday_data, current_month, current_date):
    for (_, row) in birthday_data.iterrows():
        try:
            day = row["day"]
            month = row["month"]
            to_mail = row["email"]
            receiver_name = row["name"]
        except:
            print("Birthday File is not properly formatted.")
        else:
            if (day == current_date) and (month == current_month):
                letter_file = random.choice(LETTER_FILE)
                letter = customize_letter(letter_file, SENDER_NAME, receiver_name)
                if letter != "":
                    birthday_message = SUBJECT + letter
                    send_wish(
                        SMTP_SERVER, FROM_MAIL, PASSWORD, to_mail, birthday_message
                    )
                else:
                    print(f"{letter_file} could not be opened.")
    return


# CUSTOMISE LETTER
def customize_letter(letter_file, sender_name, receiver_name):
    try:
        with open(letter_file, "r") as file:
            sample_letter = file.readlines()
    except:
        letter = ""
    else:
        letter = ""
        for lines in sample_letter:
            line = lines.strip()
            line = line.replace(RECEIVER_PLACEHOLDER, receiver_name)
            line = line.replace(SENDER_PLACEHOLDER, sender_name)
            letter = letter + "\n" + line
    return letter


# CURRENT DATETIME
current_datetime = dt.datetime.now()
current_date = current_datetime.date().day
current_month = current_datetime.month

try:
    birthday_data = pd.read_csv(BIRTHDAYS_FILE)
    check_birthday(birthday_data, current_month, current_date)
except:
    print("Birthday wish could not be sent.")
