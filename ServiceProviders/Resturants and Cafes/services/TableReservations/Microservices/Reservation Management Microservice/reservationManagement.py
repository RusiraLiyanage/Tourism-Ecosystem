from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load reservation data from JSON file
def load_reservations_data():
    with open('reservationData.json', 'r') as file:
        return json.load(file)["reservations"]

# Save updated reservation data back to JSON file
def save_reservations_data(reservations):
    with open('reservationData.json', 'w') as file:
        json.dump({"reservations": reservations}, file, indent=4)

# In-memory reservation storage for demo purposes
reservations = load_reservations_data()

# Helper function to call the availability microservice to update table availability
def update_table_availability(table, time, availability_status):
    availability_service_url = f"http://localhost:5001/availability/{table}"
    availability_data = {
        "time": time,
        "availability": availability_status
    }
    response = requests.put(availability_service_url, json=availability_data)
    return response

@app.route('/reservations', methods=['POST'])
def create_reservation():
    reservation_data = request.json
    # Call Availability Microservice to check table availability
    availability_service_url = f"http://localhost:5001/availability"
    available = requests.get(availability_service_url, params={"table": reservation_data['table'], "time": reservation_data['time']})
    
    if available.json().get("status") == "available":
        reservation_id = len(reservations) + 1
        reservation_data["reservation_id"] = reservation_id
        reservations[reservation_id] = reservation_data
        save_reservations_data(reservations)
        
        # Mark the table as booked
        update_table_availability(reservation_data['table'], reservation_data['time'], "booked")
        
        # Call Notification Microservice to send confirmation
        notification_data = {
            "reservation_id": reservation_id,
            "type": "confirmation",
            "message": f"Your table reservation for table {reservation_data['table']} at {reservation_data['time']} is confirmed."
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Reservation created", "reservation_id": reservation_id}), 201
    else:
        return jsonify({"error": "Table not available"}), 400

@app.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    reservation_data = request.json
    if reservation_id in reservations:
        old_table = reservations[reservation_id]["table"]
        old_time = reservations[reservation_id]["time"]
        
        reservations[reservation_id].update(reservation_data)
        save_reservations_data(reservations)
        
        # If table or time has changed, update availability
        if old_table != reservation_data["table"] or old_time != reservation_data["time"]:
            update_table_availability(old_table, old_time, "available")
            update_table_availability(reservation_data["table"], reservation_data["time"], "booked")
        
        # Notify the customer about the updated reservation
        notification_data = {
            "reservation_id": reservation_id,
            "type": "update",
            "message": f"Your reservation for table {reservation_data['table']} at {reservation_data['time']} has been updated."
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Reservation updated", "reservation_id": reservation_id}), 200
    return jsonify({"error": "Reservation not found"}), 404

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    if reservation_id in reservations:
        table = reservations[reservation_id]['table']
        time = reservations[reservation_id]['time']
        
        del reservations[reservation_id]
        save_reservations_data(reservations)
        
        # Mark the table as available again
        update_table_availability(table, time, "available")
        
        # Notify the customer about the cancellation
        notification_data = {
            "reservation_id": reservation_id,
            "type": "cancellation",
            "message": f"Your reservation for table {table} at {time} has been canceled."
        }
        requests.post("http://localhost:5002/notifications", json=notification_data)
        
        return jsonify({"message": "Reservation canceled", "reservation_id": reservation_id}), 200
    return jsonify({"error": "Reservation not found"}), 404

if __name__ == "__main__":
    app.run(port=5006)
