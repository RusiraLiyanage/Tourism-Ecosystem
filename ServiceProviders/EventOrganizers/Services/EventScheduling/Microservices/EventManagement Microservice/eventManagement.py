from flask import Flask, json, request, jsonify
import requests

app = Flask(__name__)

def load_events_data():
    with open('eventManagementData.json', 'r') as file:
        theData = json.load(file)
        return theData["eventData"]

# Save updated events back to the JSON file
def save_events_data(event_data):
    with open('eventManagementData.json', 'w') as file:
        json.dump({"eventData": event_data}, file, indent=4)

# Helper function to call the availability microservice to update venue availability
def update_venue_availability(venue, time, availability_status):
    availability_service_url = f"http://localhost:5001/availability/{venue}"
    availability_data = {
        "time": time,
        "avaliability": availability_status
    }
    response = requests.put(availability_service_url, json=availability_data)
    return response

# In-memory event storage for demo purposes
events = load_events_data()

# Add new event to the JSON file and in-memory events dictionary
def add_event_to_file(event):
    # Load the existing data
    current_events = load_events_data()
    
    # Generate a new event ID based on the current list size
    event_id = len(current_events) + 1
    
    # Add event_id to the event data
    event_with_id = {
        "event_id": event_id,
        **event  # Merge event_id with the existing event data
    }
    
    # Add the new event (with event_id) to the list
    current_events.append(event_with_id)
    
    # Save the updated event list to the file
    save_events_data(current_events)
    return event_id

@app.route('/events', methods=['POST'])
def create_event():
    event_data = request.json
    
    # Call Availability Microservice to check availability
    availability_service_url = "http://localhost:5001/availability"
    response = requests.get(availability_service_url, params={"venue": event_data['venue'], "time": event_data['time']})
    
    if response.status_code == 200 and response.json().get("status") == "available":
        # Add the new event to the JSON file and get the new event ID
        event_id = add_event_to_file(event_data)
        
         # Mark the venue as unavailable
        update_venue_availability(event_data['venue'], event_data['time'], "unavailable")
        
        # Prepare notification details
        notification_data = {
            "event_id": event_id,
            "type": "confirmation",
            "recipient": "customer",  # Assuming the customer is the recipient
            "message": f"Your event '{event_data['event_name']}' has been successfully scheduled for {event_data['time']} at {event_data['venue']}."
        }
        
        # Call Notification Microservice to send confirmation
        notification_service_url = "http://localhost:5002/notifications"
        notification_response = requests.post(notification_service_url, json=notification_data)

        # Capture the response from the Notification Service
        if notification_response.status_code == 201:
            notification_message = notification_response.json()
        else:
            notification_message = "Failed to send notification"
        
        # Return the event scheduling confirmation along with the notification response
        return jsonify({
            "message": "Event scheduled",
            "event_id": event_id,
            "notification_status": notification_message  # Include the notification response
        }), 201
    else:
        return jsonify({"error": "Venue is unavaliable"}), 400

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event_data = request.json
    current_events = load_events_data()
    
    for event in current_events:
        if event['event_id'] == event_id:
            old_venue = event['venue']
            old_time = event['time']
            event.update(event_data)  # Update the event details
            save_events_data(current_events)
            
            # If venue has changed, mark old venue as available and new venue as unavailable
            if old_venue != event_data['venue']:
                update_venue_availability(old_venue, old_time, "available")  # Old venue becomes available
                update_venue_availability(event_data['venue'], event_data['time'], "unavailable")  # New venue becomes unavailable
            else:
                # If only time changed, update availability with the new time
                update_venue_availability(event_data['venue'], event_data['time'], "unavailable")
            
            # Prepare notification details for the update
            notification_data = {
                "event_id": event_id,
                "type": "update",
                "recipient": "customer",
                "message": f"Your event '{event['event_name']}' has been successfully updated to {event['time']} at {event['venue']}. Thank you for your patience!"
            }
            notification_service_url = "http://localhost:5002/notifications"
            notification_response = requests.post(notification_service_url, json=notification_data)

            # Capture the response from the Notification Service
            if notification_response.status_code == 201:
                notification_message = notification_response.json()  # Full notification response
            else:
                notification_message = "Failed to send notification"

            # Prepare the JSON response
            return jsonify({
                "message": "Event updated",
                "event_id": event_id,
                "notification_status": notification_message  # Include the notification response
            }), 200
            
    return jsonify({"error": "Event not found"}), 404

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    current_events = load_events_data()
    
    for i, event in enumerate(current_events):
        if event['event_id'] == event_id:
            venue = event['venue']
            time = event['time']
            del current_events[i]  # Remove the event from the list
            save_events_data(current_events)
            
            update_venue_availability(venue, time, "available")
            
            # Prepare notification details for cancellation
            notification_data = {
                "event_id": event_id,
                "type": "cancellation",
                "recipient": "customer",
                "message": f"We regret to inform you that your event '{event['event_name']}' scheduled for {event['time']} at {event['venue']} has been canceled. Please contact us for further assistance."
            }
            notification_service_url = "http://localhost:5002/notifications"
            notification_response = requests.post(notification_service_url, json=notification_data)

            # Capture the response from the Notification Service
            if notification_response.status_code == 201:
                notification_message = notification_response.json()  # Full notification response
            else:
                notification_message = "Failed to send notification"

            # Prepare the JSON response
            return jsonify({
                "message": "Event canceled",
                "event_id": event_id,
                "notification_status": notification_message  # Include the notification response
            }), 200
            
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)
