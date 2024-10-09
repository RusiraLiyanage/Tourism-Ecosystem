from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load ride data from JSON file
def load_rides_data():
    with open('rideManagementData.json', 'r') as file:
        return json.load(file)["rideData"]

# Save updated ride data to JSON file
def save_rides_data(ride_data):
    with open('rideManagementData.json', 'w') as file:
        json.dump({"rideData": ride_data}, file, indent=4)

# In-memory ride storage for demo purposes
rides = load_rides_data()

# Helper function to call the availability microservice to update vehicle availability
def update_vehicle_availability(vehicle, time, availability_status):
    availability_service_url = f"http://localhost:5001/availability/{vehicle}"
    availability_data = {
        "time": time,
        "availability": availability_status
    }
    response = requests.put(availability_service_url, json=availability_data)
    return response

@app.route('/rides', methods=['POST'])
def create_ride():
    ride_data = request.json
    # Call Availability Microservice to check vehicle availability
    availability_service_url = f"http://localhost:5001/availability"
    available = requests.get(availability_service_url, params={"vehicle": ride_data['vehicle'], "time": ride_data['time']})
    
    if available.json().get("status") == "available":
        ride_id = len(rides) + 1
        ride_data["ride_id"] = ride_id
        rides[ride_id] = ride_data
        save_rides_data(rides)
        
        # Mark the vehicle as unavailable
        update_vehicle_availability(ride_data['vehicle'], ride_data['time'], "booked")
        
        # Call Notification Microservice to send confirmation
        notification_data = {
            "ride_id": ride_id,
            "type": "confirmation",
            "message": f"Your ride with {ride_data['vehicle']} has been booked for {ride_data['time']}"
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Ride booked", "ride_id": ride_id}), 201
    else:
        return jsonify({"error": "Vehicle or time not available"}), 400

@app.route('/rides/<int:ride_id>', methods=['PUT'])
def update_ride(ride_id):
    ride_data = request.json
    if ride_id in rides:
        old_vehicle = rides[ride_id]["vehicle"]
        old_time = rides[ride_id]["time"]
        
        rides[ride_id].update(ride_data)
        save_rides_data(rides)

        # Update vehicle availability if vehicle or time has changed
        if old_vehicle != ride_data["vehicle"] or old_time != ride_data["time"]:
            update_vehicle_availability(old_vehicle, old_time, "available")
            update_vehicle_availability(ride_data["vehicle"], ride_data["time"], "booked")
        
        # Notify rider and driver about the updated ride
        notification_data = {
            "ride_id": ride_id,
            "type": "update",
            "message": f"Your ride with {ride_data['vehicle']} has been updated to {ride_data['time']}"
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Ride updated", "ride_id": ride_id}), 200
    return jsonify({"error": "Ride not found"}), 404

@app.route('/rides/<int:ride_id>', methods=['DELETE'])
def delete_ride(ride_id):
    if ride_id in rides:
        vehicle = rides[ride_id]['vehicle']
        time = rides[ride_id]['time']
        
        del rides[ride_id]
        save_rides_data(rides)
        
        # Mark the vehicle as available again
        update_vehicle_availability(vehicle, time, "available")
        
        # Notify rider and driver about the cancellation
        notification_data = {
            "ride_id": ride_id,
            "type": "cancellation",
            "message": f"Your ride with {vehicle} scheduled for {time} has been canceled."
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Ride canceled", "ride_id": ride_id}), 200
    return jsonify({"error": "Ride not found"}), 404

if __name__ == "__main__":
    app.run(port=5005)
