from flask import Flask, json, request, jsonify

app = Flask(__name__)

# Load availability data from a JSON file
def load_availability_data():
    with open('avaliabilityData.json', 'r') as file:
        return json.load(file)["avaliabilityData"]

# Save updated availability data back to the JSON file
def save_availability_data(availability):
    with open('avaliabilityData.json', 'w') as file:
        json.dump({"avaliabilityData": availability}, file, indent=4)

# In-memory availability data
availability = load_availability_data()

# Helper function to find availability by venue
def find_venue(venue, availability):
    for item in availability:
        if item["venue"] == venue:
            return item
    return None

# GET request - Check availability
@app.route('/availability', methods=['GET'])
def check_availability():
    venue = request.args.get('venue')
    time = request.args.get('time')

    venue_data = find_venue(venue, availability)
    
    if venue_data:
        if venue_data["avaliability"] == "available":
            return jsonify({"status": "available"}), 200
        else:
            return jsonify({"status": "unavailable"}), 400
    else:
        return jsonify({"error": "Venue or time not found"}), 404

# POST request - Add new availability
@app.route('/availability', methods=['POST'])
def add_availability():
    data = request.json
    venue = data.get('venue')
    time = data.get('time')
    availability_status = data.get('avaliability')

    # Check if venue already exists
    if find_venue(venue, availability):
        return jsonify({"error": "Venue already exists"}), 400
    
    # Add new availability entry
    new_availability = {"venue": venue, "time": time, "avaliability": availability_status}
    availability.append(new_availability)
    save_availability_data(availability)
    
    return jsonify({"message": "New availability added", "venue": venue, "avaliability": availability_status}), 201

# PUT request - Update existing availability
@app.route('/availability/<venue>', methods=['PUT'])
def update_availability(venue):
    data = request.json
    time = data.get('time')
    availability_status = data.get('avaliability')

    venue_data = find_venue(venue, availability)

    if not venue_data:
        return jsonify({"error": "Venue not found"}), 404

    # Update the availability entry
    venue_data["time"] = time
    venue_data["avaliability"] = availability_status
    save_availability_data(availability)
    
    return jsonify({"message": "Availability updated", "venue": venue, "avaliability": availability_status}), 200

# DELETE request - Remove availability
@app.route('/availability/<venue>', methods=['DELETE'])
def delete_availability(venue):
    venue_data = find_venue(venue, availability)

    if not venue_data:
        return jsonify({"error": "Venue not found"}), 404

    # Remove the availability entry
    availability.remove(venue_data)
    save_availability_data(availability)
    
    return jsonify({"message": "Availability deleted", "venue": venue}), 200

if __name__ == "__main__":
    app.run(port=5001)
