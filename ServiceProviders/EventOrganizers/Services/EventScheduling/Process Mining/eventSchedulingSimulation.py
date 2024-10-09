import csv
from datetime import datetime, timedelta
import random
import os

# Define actions and actors for the event scheduling service
organizer = "Event Organizer"
customer = "Customer"
case_id = 0

# Define a function to log events into a CSV file
def log_event(case_id, log_file, actor, action, outcome, start_time, complete_time):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([case_id, actor, action, outcome, start_time.strftime('%Y-%m-%d %H:%M:%S'), complete_time.strftime('%Y-%m-%d %H:%M:%S')])

# Initialize the log file
log_file = "event_logs.csv"

# Check if the log file already exists
if not os.path.exists(log_file):
    # If it doesn't exist, create it and write the header row
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Case ID", "Actor", "Action", "Outcome", "Start Timestamp", "Complete Timestamp"])

# Simulation of event scheduling service process

# T1: Event Organizer creates a new event schedule
start_time = datetime.now()
complete_time = start_time + timedelta(minutes=random.randint(1,5))
case_id = random.randint(1000, 9999)
log_event(case_id,log_file, organizer, "Creates a new event schedule", "Success", start_time, complete_time)

# T2: Send event details to the customer
start_time = complete_time
complete_time = start_time + timedelta(minutes=random.randint(1,7))
case_id = random.randint(1000, 9999)
log_event(case_id,log_file, organizer, "Send event details to the customer", "Success", start_time, complete_time)

# T3: Customer receives the proposed event schedule
start_time = complete_time
complete_time = start_time + timedelta(minutes=random.randint(1,3))
case_id = random.randint(1000, 9999)
log_event(case_id,log_file, customer, "Receive proposed event schedule", "Success", start_time, complete_time)

# Randomly decide if the customer accepts or requests changes
if random.choice([True, False]):
    # Customer confirms the proposed schedule
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,4))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, customer, "Confirm proposed schedule", "Success", start_time, complete_time)

    # T14: Event Organizer secures the venue and resources
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,5))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, organizer, "Secure the venue and resources", "Success", start_time, complete_time)

    # T15: Send a confirmation notification
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,2))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, organizer, "Send a confirmation notification", "Success", start_time, complete_time)

    # T16: Customer receives the confirmation notification
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,2))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, customer, "Receive confirmation notification", "Success", start_time, complete_time)

else:
    # T5: Customer requests changes to the schedule
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,3))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, customer, "Request changes to the schedule", "Success", start_time, complete_time)
    
    # T5: Organizer review the customer requested schedule changes
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,5))
    case_id = random.randint(1000, 9999)
    log_event(case_id,log_file, organizer, "Review Requested changes", "Success", start_time, complete_time)

    # T6: Event Organizer reviews requested changes
    start_time = complete_time
    complete_time = start_time + timedelta(minutes=random.randint(1,3))
    feasible_change = random.choice([True, False])
    if feasible_change:
        # T7: Update requested schedule and notify the customer
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,6))
        case_id = random.randint(1000, 9999)
        log_event(case_id,log_file, organizer, "Update requested schedule and notify the customer", "Feasible change", start_time, complete_time)

        # T8: Customer reviews updated schedule
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,4))
        case_id = random.randint(1000, 9999)
        log_event(case_id,log_file, customer, "Review updated schedule", "Success", start_time, complete_time)
        
        # customer response to confirm the updated schedule or not wihin 5 days
        customer_respond = random.choice([True, False])
        
        if(customer_respond == True):
            # T9: Customer confirms the updated schedule
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,3))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, customer, "Confirm updated schedule", "Success", start_time, complete_time)

            # T14: Event Organizer secures the venue and resources
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,3))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, organizer, "Secure the venue and resources", "Success", start_time, complete_time)

            # T15: Send a confirmation notification
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,2))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, organizer, "Send a confirmation notification", "Success", start_time, complete_time)

            # T16: Customer receives the confirmation notification
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,3))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, customer, "Receive confirmation notification", "Success", start_time, complete_time)
        else:
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,2))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, organizer, "Send reminder notification", "Reminder", start_time, complete_time)
            
            # if customer didn't respond after 3 days cancel the event scheduling
            customer_replied_after = random.choice([True, False])
            if(customer_replied_after == True):
                # T9: Customer confirms the updated schedule
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Confirm updated schedule within 3 days", "Success", start_time, complete_time)

                # T14: Event Organizer secures the venue and resources
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,4))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Secure the venue and resources", "Success", start_time, complete_time)

                # T15: Send a confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,5))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Send a confirmation notification", "Success", start_time, complete_time)

                # T16: Customer receives the confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Receive confirmation notification", "Success", start_time, complete_time)
            else:
                # customer didn't reply back even after 3 days
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,2))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Cancel event scheduling process", "No Response within 3 days", start_time, complete_time)
    else:
        # T11: Inform customer and provide alternatives
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,5))
        case_id = random.randint(1000, 9999)
        log_event(case_id,log_file, organizer, "Inform customer and provide alternatives", "Not feasible", start_time, complete_time)

        # T12: Customer reviews provided alternatives
        start_time = complete_time
        complete_time = start_time + timedelta(minutes=random.randint(1,4))
        case_id = random.randint(1000, 9999)
        log_event(case_id,log_file, customer, "Review provided alternatives", "Success", start_time, complete_time)
        
        # customer response to confirm the updated schedule or not wihin 5 days
        customer_respond = random.choice([True, False])
        
        if(customer_respond == True):
            # Randomly decide if the customer accepts the alternatives
            if random.choice([True, False]):
                # T13: Customer confirms the alternatives
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Confirm alternatives", "Success", start_time, complete_time)

                # T14: Event Organizer secures the venue and resources
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Secure the venue and resources", "Success", start_time, complete_time)

                # T15: Send a confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Send a confirmation notification", "Success", start_time, complete_time)

                # T16: Customer receives the confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,2))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Receive confirmation notification", "Success", start_time, complete_time)
            else:
                # T17: Customer declines the alternatives
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Decline alternatives", "Success", start_time, complete_time)
        else: 
            start_time = complete_time
            complete_time = start_time + timedelta(minutes=random.randint(1,4))
            case_id = random.randint(1000, 9999)
            log_event(case_id,log_file, organizer, "Send reminder notification", "Reminder", start_time, complete_time)
            
            # if customer didn't respond after 3 days cancel the event scheduling
            customer_replied_after = random.choice([True, False])
            if(customer_replied_after == True):
                # T9: Customer confirms the updated schedule
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Confirm alternatives within 3 days", "Success", start_time, complete_time)

                # T14: Event Organizer secures the venue and resources
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                log_event(case_id,log_file, organizer, "Secure the venue and resources", "Success", start_time, complete_time)

                # T15: Send a confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,3))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Send a confirmation notification", "Success", start_time, complete_time)

                # T16: Customer receives the confirmation notification
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,4))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, customer, "Receive confirmation notification", "Success", start_time, complete_time)
            else:
                # customer didn't reply back even after 3 days
                start_time = complete_time
                complete_time = start_time + timedelta(minutes=random.randint(1,2))
                case_id = random.randint(1000, 9999)
                log_event(case_id,log_file, organizer, "Cancel event scheduling process", "No Response within 3 days", start_time, complete_time)