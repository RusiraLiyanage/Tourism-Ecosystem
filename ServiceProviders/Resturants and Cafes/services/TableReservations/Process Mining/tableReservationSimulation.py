import csv
import random
from datetime import datetime, timedelta

# Event log generator
def generate_event_log(case_id, actor, action, outcome, start_time, complete_time):
    return {
        "Case ID": case_id,
        "Actor": actor,
        "Action": action,
        "Outcome": outcome,
        "Start Timestamp": start_time,
        "Complete Timestamp": complete_time
    }

# Simulate a booking process event log
def simulate_event_logs():
    # Expanded list of actions to prevent repetition of Case ID
    events = [
        ("Customer", "Creates a new booking", "Success"),
        ("Customer", "Selects Date", "Success"),
        ("Customer", "Selects Time", "Success"),
        ("Local Transportation System", "Booking failed", "Fail"),
        ("Local Transportation System", "Checks Availability", "Success"),
        ("Customer", "Submits booking request", "Success"),
        ("Local Transportation System", "Confirm notification", "Success"),
        ("Customer", "Confirms booking", "Success"),
        ("Local Transportation System", "Sends confirmation to customer", "Success"),
        ("Local Transportation System", "Closes booking process", "Success"),
    ]

    event_logs = []

    # Generate 20 unique large numeric case IDs (e.g., between 1000 and 9999)
    case_ids = random.sample(range(1000, 10000), 20)

    # For each Case ID, we will log a unique action only once
    for case_id in case_ids:
        start_time = datetime.now() + timedelta(seconds=random.randint(1, 10))
        
        # Randomly pick an event action for each unique case
        actor, action, outcome = random.choice(events)
        complete_time = start_time + timedelta(seconds=random.randint(1, 5))

        # Create log entry
        event_log = generate_event_log(case_id, actor, action, outcome, start_time.strftime('%Y-%m-%d %H:%M:%S'), complete_time.strftime('%Y-%m-%d %H:%M:%S'))
        event_logs.append(event_log)

    # Save logs to CSV
    with open('event_logs.csv', 'w', newline='') as csvfile:
        fieldnames = ["Case ID", "Actor", "Action", "Outcome", "Start Timestamp", "Complete Timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for log in event_logs:
            writer.writerow(log)

    print("Event logs generated and saved to event_logs.csv")

# Run the simulation to generate the logs
simulate_event_logs()