from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load availability data from JSON file
def load_availability_data():
    with open('availabilityData.json', 'r') as file:
        return json.load(file)["availabilityData"]

# Save updated availability data to the JSON file
def save_availability_data(availability):
    with open('availabilityData.json', 'w') as file:
        json.dump({"availabilityData": availability}, file, indent=4)

# In-memory availability data
availability = load_availability_data()

# GET request - Check vehicle availability
@app.route('/availability', methods=['GET'])
def check_availability():
    vehicle = request.args.get('vehicle')
    time = request.args.get('time')
    
    if availability.get(vehicle, {}).get(time) == "available":
        return jsonify({"status": "available"}), 200
    else:
        return jsonify({"status": "unavailable"}), 400

# PUT request - Update availability (e.g., mark as booked or available)
@app.route('/availability/<vehicle>', methods=['PUT'])
def update_availability(vehicle):
    data = request.json
    time = data.get('time')
    availability_status = data.get('availability')

    if vehicle not in availability:
        availability[vehicle] = {}

    availability[vehicle][time] = availability_status
    save_availability_data(availability)
    
    return jsonify({"message": "Availability updated", "vehicle": vehicle, "availability": availability_status}), 200

if __name__ == "__main__":
    app.run(port=5003)
