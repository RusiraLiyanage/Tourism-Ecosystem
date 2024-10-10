import csv
from datetime import datetime, timedelta
import random
import os

# Define actions and actors for the ride booking service
organizer = "Local Transportation System"
customer = "Customer"
case_id = 0

# Define a function to log events into a CSV file
def log_event(case_id, log_file, actor, action, outcome, start_time, complete_time):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                case_id, 
                actor, 
                action, 
                outcome, 
                start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                complete_time.strftime('%Y-%m-%d %H:%M:%S')
            ])
    
# Initialize the log file
log_file = "ride_logs.csv"

# Check if the log file already exists
if not os.path.exists(log_file):
    # If it doesn't exist, create it and write the header row
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Case ID", "Actor", "Action", "Outcome", "Start Timestamp", "Complete Timestamp"])

# Simulation of ride booking service process

# T1 The customer begins
while(True):
    start_time = datetime.now()
    complete_time = start_time + timedelta(minutes=random.randint(1,5))
    case_id = random.randint(1000, 9999)
    log_event(case_id, log_file, customer, "Creates a new booking", "Success", start_time, complete_time)

    # T2 The customer selects the desired date for the ride
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,7))
    case_id = random.randint(1000, 9999)
    log_event(case_id, log_file, customer, "Selects Date", "Success", start_time, complete_time)

    # T3 The customer selects the desired time for the ride
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,5))
    case_id = random.randint(1000, 9999)
    log_event(case_id, log_file, customer, "Selects Time", "Success", start_time, complete_time)

    # T4 The system checks if the selected time and vehicle are available
    choice = random.choice([True, False])
    if(choice == True):
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,4))
        case_id = (random.randint(1000, 9999))
        log_event(case_id, log_file, organizer, "Checks Availablility", "Success", start_time, complete_time)

        # T5 The customer submits the booking request
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,5))
        case_id = random.randint(1000, 9999)
        log_event(case_id, log_file, customer, "Submits booking request", "Success", start_time, complete_time)

        # T6 The system confirms the booking status
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,9))
        case_id = random.randint(1000, 9999)
        log_event(case_id, log_file, organizer, "Confirms booking status", "Success", start_time, complete_time)

        # T7 The system sends a confirmation notification to the customer
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,2))
        case_id = random.randint(1000, 9999)
        log_event(case_id, log_file, organizer, "Confirm notification", "Success", start_time, complete_time)

        # T8 The booking is confirmed and the process is completed
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,8))
        case_id = random.randint(1000, 9999)
        log_event(case_id, log_file, organizer, "Booking confirmed", "Success", start_time, complete_time)

        # T9 The booking process ends
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,4))
        case_id = random.randint(1000, 9999)
        log_event(case_id, log_file, organizer, "Booking process finished", "Success", start_time, complete_time)
        break