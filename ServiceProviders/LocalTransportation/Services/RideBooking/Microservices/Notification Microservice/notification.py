from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load notifications data from JSON file
def load_notifications_data():
    with open('notificationData.json', 'r') as file:
        return json.load(file)["notificationData"]

# Save updated notifications to the JSON file
def save_notifications_data(notifications):
    with open('notificationData.json', 'w') as file:
        json.dump({"notificationData": notifications}, file, indent=4)

# In-memory notification log
notifications = load_notifications_data()

@app.route('/notifications', methods=['POST'])
def send_notification():
    notification_data = request.json
    notifications.append(notification_data)
    save_notifications_data(notifications)
    
    return jsonify({"message": "Notification sent", "data": notification_data}), 201

if __name__ == "__main__":
    app.run(port=5004)
