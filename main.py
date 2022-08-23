import html2text
import requests
import itertools
import datetime
import os
import sys
import shutil

from datetime import datetime, timedelta
from dateutil.parser import *
from datetime import date
from twilio.rest import Client


def reminderBot():
    #Set variables for Twilio
    account_sid = "[REDACTED]"
    auth_token  = "[REDACTED]"
    client = Client(account_sid, auth_token)

    #Get and cleanup text from NAF booking page
    html = requests.get("https://www.nafsalon.com/book")
    raw_text = html.text
    clean_text = html2text.html2text(raw_text)
    list_text = clean_text.split()
    start_index = list_text.index('open') - 12
    end_index = list_text.index('open') + 5
    clean_index = (list_text[start_index:end_index])
    
    #Checks to make sure the NAF booking page is in the expected format - kills the function and sends a message if it is not
    if clean_index[0] != '11am' or clean_index[1] != '11am':
        message = client.messages.create(
        to="[REDACTED]",
        from_="[REDACTED]",
        body=("Something has gone wrong with the NAF reminder system, please check the logs."))
        print("Message sent to JD - Message ID: " + message.sid)
        print("Something has gone wrong with the NAF reminder system. Function exited.")
        return

    #Gets the first opening time
    time_one = []
    time_one.append([clean_index[0]])
    time_one.append([clean_index[13]])
    time_one.append([clean_index[14]])
    time_one = ' '.join(list(itertools.chain.from_iterable(time_one)))
    time_one = parse(time_one)
    print("According to my calculations - the next calendar opening time is:" + str(time_one))

    #Gets the second opening time
    time_two = []
    time_two.append([clean_index[1]])
    time_two.append([clean_index[15]])
    time_two.append([clean_index[16]])
    time_two = ' '.join(list(itertools.chain.from_iterable(time_two)))
    time_two = parse(time_two)
    print("According to my calculations - the following calendar opening time is:" + str(time_two))

    #Checks whether the opening time to use is time one, or time two
    if datetime.now().replace(minute=0, second=0, microsecond=0) > time_one:
        use_time = time_two
        print('As ' + str(datetime.now().replace(minute=0, second=0, microsecond=0)) + ' is after ' + str(time_one) + '. Im going to use ' + str(time_two) + '(time two) for my calculations.')
    else:
        use_time = time_one
        print('As ' + str(datetime.now().replace(minute=0, second=0, microsecond=0)) + ' is before ' + str(time_one) + '. Im going to use ' + str(time_one) + '(time one) for my calculations.')

    #Used for testing - [uncomment minutes=30 for next hour] [uncomment days=1 for tomorrow]
    #use_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)

    #Logging variables
    print("The date today is " + str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)))
    print("The time right now is " + str(datetime.now().replace(minute=0, second=0, microsecond=0)))
    print("The date/time used for calculation is " + str(use_time))

    #Sends one day reminder
    if datetime.now().replace(minute=0, second=0, microsecond=0) == use_time - timedelta(days=1):
        message = client.messages.create(
        to="[REDACTED]",
        from_="[REDACTED]",
        body=("NAF calendars open tomorrow!"))
        print("Message sent to GC - Message ID: " + message.sid)

        message = client.messages.create(
        to="[REDACTED]",
        from_="[REDACTED]",
        body=("NAF calendars open tomorrow!"))
        print("Message sent to JD - Message ID: " + message.sid)

        print("Today is " + str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + " and the time is " + str(datetime.now().replace(minute=0, second=0, microsecond=0)) + ". Calendars open in 24 hours - one day reminder sent")

    #Sends 1 hour reminder
    if datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) == use_time.replace(hour=0, minute=0, second=0, microsecond=0):
        d = datetime.utcnow()
        #Accounting for BST
        current_hour = d.hour +1
        if current_hour == 10:
            print("Today is " + str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + " and the hour is " + str(current_hour) + ". Calendars open in an hour! - one hour reminder sent")

            message = client.messages.create(
            to="[REDACTED]",
            from_="[REDACTED]",
            body=("NAF calendars open in an hour! Book here! https://www.nafsalon.com/book"))
            print("Message sent to GC - Message ID: " + message.sid)

            message = client.messages.create(
            to="[REDACTED]",
            from_="[REDACTED]",
            body=("NAF calendars open in an hour! Book here! https://www.nafsalon.com/book"))
            print("Message sent to JD - Message ID: " + message.sid)
        else:
            print("Today is " + str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + " and the hour is " + str(current_hour) + ". Calendars open today, but not in an hour - one hour reminder not sent")
    #Logs that no message needs to be sent
    else:
        print("Today is " + str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + ". Calendars do not open today - one hour reminder not sent")
    print("end of script")
reminderBot()

