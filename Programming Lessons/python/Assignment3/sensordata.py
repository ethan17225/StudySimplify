import requests
from flask import Flask, jsonify, request

# Initialize the Flask app
app = Flask(__name__)

# Dictionary to store sensor data (city temperatures will be fetched dynamically)
sensors = {
    "ho_chi_minh": {"sensor_id": "ho_chi_minh", "location": "Ho Chi Minh City", "latitude": 10.8231, "longitude": 106.6297, "type": "Temperature"},
    "toronto": {"sensor_id": "toronto", "location": "Toronto", "latitude": 43.65107, "longitude": -79.347015, "type": "Temperature"},
    "seoul": {"sensor_id": "seoul", "location": "Seoul", "latitude": 37.5665, "longitude": 126.978, "type": "Temperature"},
    "san_jose": {"sensor_id": "san_jose", "location": "San Jose", "latitude": 37.7749, "longitude": -122.4194, "type": "Temperature"},
    "tokyo": {"sensor_id": "tokyo", "location": "Tokyo", "latitude": 35.6762, "longitude": 139.6503, "type": "Temperature"}
}

# Open-Meteo API configuration
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Function to fetch the current temperature for a city using Open-Meteo API
def get_temperature(latitude, longitude):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true',
        'temperature_unit': 'celsius'
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['current_weather']['temperature']
        return temp
    else:
        return None

# Welcome route
@app.route('/')
def home():
    return "Welcome to the IoT Sensor Management API for city temperatures!"

# 1. GET /sensors: Returns data from all sensors (temperatures of cities)
@app.route('/sensors', methods=['GET'])
def get_sensors():
    for city in sensors:
        latitude = sensors[city]['latitude']
        longitude = sensors[city]['longitude']
        temp = get_temperature(latitude, longitude)
        if temp is not None:
            sensors[city]['value'] = temp
        else:
            sensors[city]['value'] = "Error fetching temperature"
    return jsonify(sensors)

# 2. GET /sensors/<sensor_id>: Returns data from a specific sensor based on its ID
@app.route('/sensors/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = sensors.get(sensor_id)
    if not sensor:
        return jsonify({"error": "Sensor not found"}), 404
    
    # Fetch temperature for this specific sensor (city)
    latitude = sensor['latitude']
    longitude = sensor['longitude']
    temp = get_temperature(latitude, longitude)
    if temp is not None:
        sensor['value'] = temp
    else:
        sensor['value'] = "Error fetching temperature"

    return jsonify(sensor)

# 3. GET /sensors?type=<sensor_type>: Returns sensors of a specific type (e.g., Temperature)
@app.route('/sensors', methods=['GET'])
def get_sensors_by_type():
    sensor_type = request.args.get('type')
    if not sensor_type:
        return jsonify({"error": "Sensor type is required"}), 400

    filtered_sensors = {key: sensor for key, sensor in sensors.items() if sensor['type'] == sensor_type}
    return jsonify(filtered_sensors)

# 4. POST /sensors: Allows adding a new sensor (new temperature sensor data)
@app.route('/sensors', methods=['POST'])
def add_sensor():
    new_sensor = request.get_json()

    # Check if sensor_id is provided
    if 'sensor_id' not in new_sensor:
        return jsonify({"error": "sensor_id is required"}), 400

    sensor_id = new_sensor['sensor_id']
    
    # Add new sensor to the dictionary
    sensors[sensor_id] = new_sensor
    return jsonify({"message": "Sensor added successfully", "sensor": new_sensor}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
