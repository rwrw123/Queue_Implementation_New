from flask import Flask, request, jsonify
from datetime import datetime, timezone
import logging
import json
from pymongo import MongoClient

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthMonitoringAPI")

class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.message} | {json.dumps(self.kwargs)}"

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        # Items are appended to the end of the list to maintain FIFO order
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # Removes the first item from the list

    def size(self):
        return len(self.items)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client['health_monitoring_db']

# MongoDB collections
users = db.users
devices = db.devices
appointments = db.appointments
messages = db.messages

alert_queue = Queue()

@app.route('/')
def index():
    return 'Health Monitoring API is running!'

@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if not all(k in data for k in ['name', 'email']):
        return jsonify({"error": "Missing name or email"}), 400
    user_id = users.insert_one({"name": data['name'], "email": data['email'], "roles": []}).inserted_id
    return jsonify({"userId": str(user_id), "status": "success"})

@app.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    device_id = devices.insert_one({"deviceId": data['deviceId'], "type": data['type'], "status": "enabled"}).inserted_id
    return jsonify({"status": "success"})

@app.route('/patients/<patient_id>/measurements', methods=['POST'])
def submit_measurement(patient_id):
    data = request.json
    measurement_type = data['type']
    value = data.get('value')
    if value is None or not isinstance(value, (int, float)):
        return jsonify({"error": "Invalid measurement value"}), 400

    thresholds = {
        'bloodPressure': {'low': 90, 'high': 140},
        'temperature': {'low': 36.5, 'high': 37.5},
        'glucoseLevel': {'low': 70, 'high': 140},
    }

    if measurement_type in thresholds:
        threshold = thresholds[measurement_type]
        if not threshold['low'] <= value <= threshold['high']:
            generate_alert(patient_id, measurement_type, value, threshold)
            return jsonify({"status": "success", "alert": "Measurement outside of threshold"})
    else:
        return jsonify({"status": "success", "alert": "No threshold set for this measurement type"})

def generate_alert(patient_id, measurement_type, value, threshold):
    alert_message = StructuredMessage("ALERT", patient_id=patient_id,
                                      measurement_type=measurement_type,
                                      value=value, threshold=threshold).__str__()
    alert_queue.enqueue(alert_message)
    logger.info("New alert enqueued: " + alert_message)

@app.route('/process_alerts', methods=['GET'])
def process_alerts():
    if not alert_queue.is_empty():
        alert_to_process = alert_queue.dequeue()
        logger.info(f"Processing alert: {alert_to_process}")
        # Simulate sending a notification
        send_notification(alert_to_process)
        return jsonify({"status": "success", "alert_processed": alert_to_process})
    else:
        return jsonify({"status": "success", "message": "No alerts to process"})

def send_notification(alert):
    # Placeholder for real notification sending logic
    logger.info(f"Notification sent for alert: {alert}")
    # Simulated notification action
    print(f"Simulated notification action: {alert}")

if __name__ == '__main__':
    app.run(debug=True)
