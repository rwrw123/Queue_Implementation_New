# Health Monitoring Queue System

## Overview
  This project introduces a queue-based system designed for health monitoring applications. It leverages a Flask-based API to handle health data and alert notifications. 
  
## Features
- Custom Queue Implementation:
  A basic yet powerful FIFO (First In, First Out) queue to manage health alerts efficiently.
- Health Measurement Alerts:
  Automatic generation of alerts for measurements like blood pressure, temperature, and glucose levels that are outside the normal range.
- Flask API Integration:
  Endpoints for adding users, registering devices, submitting patient measurements, and processing alerts.
- MongoDB database:
- Storage for users, devices, appointments, and messages, facilitating easy data management and retrieval.

## Usage
- POST /users/add: Add a new user.
- POST /devices/register: Register a new device.
- POST /patients/<patient_id>/measurements: Submit a new health measurement.
- GET /process_alerts: Process and clear the next alert in the queue.

## Tests Results
![<img width="501" alt="Screen Shot 2024-03-24 at 10 05 18 PM" src="https://github.com/rwrw123/Queue_Implementation_New/assets/113308286/9e1fe380-fea1-4637-b576-d2f6f14b2427">]


