from flask import Flask, json, request, jsonify

app = Flask(__name__)

# Load existing notifications from the JSON file
def load_notifications_data():
    with open('notificationData.json', 'r') as file:
        data = json.load(file)
        return data["notificationData"]

# Save updated notifications back to the JSON file
def save_notifications_data(notifications):
    with open('notificationData.json', 'w') as file:
        json.dump({"notificationData": notifications}, file, indent=4)

# In-memory notification log for demo purposes
notifications = load_notifications_data()


@app.route('/notifications', methods=['POST'])
def send_notification():
    notification_data = request.json
    notifications.append(notification_data)  # Append new notification

    # Save the updated notifications to the JSON file
    save_notifications_data(notifications)

    # Simulate sending a notification (e.g., email or SMS)
    # In a real system, you would use email or SMS gateways to actually send messages
    return jsonify({"message": "Notification Sent Successfully", "data": notification_data}), 201
if __name__ == "__main__":
    app.run(port=5002)
