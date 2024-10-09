from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load availability data from JSON file
def load_availability_data():
    with open('availabilityData.json', 'r') as file:
        return json.load(file)["availabilityData"]

# Save updated availability data to JSON file
def save_availability_data(availability):
    with open('availabilityData.json', 'w') as file:
        json.dump({"availabilityData": availability}, file, indent=4)

# In-memory availability storage for demo purposes
availability = load_availability_data()

# GET request - Check table availability
@app.route('/availability', methods=['GET'])
def check_availability():
    table = request.args.get('table')
    time = request.args.get('time')
    
    if availability.get(table, {}).get(time) == "available":
        return jsonify({"status": "available"}), 200
    else:
        return jsonify({"status": "unavailable"}), 400

# PUT request - Update availability (e.g., mark as booked or available)
@app.route('/availability/<table>', methods=['PUT'])
def update_availability(table):
    data = request.json
    time = data.get('time')
    availability_status = data.get('availability')

    if table not in availability:
        availability[table] = {}

    availability[table][time] = availability_status
    save_availability_data(availability)
    
    return jsonify({"message": "Availability updated", "table": table, "availability": availability_status}), 200

if __name__ == "__main__":
    app.run(port=5008)
