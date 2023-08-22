# MQTT
Docker Application
To run this code
Steps to run the project with Docker

1. Install Docker
2. Docker should be running
3. In the project root run `docker-compose build` and `docker-compose up -d`
4. Go to `localhost:8000` to interact with the API endpoints
5. For endpoint that allows users to fetch sensor readings by specifying a start and end range use 'localhost:8000/sensor-readings?start=<start_date>&end=<end_date>' eg:-'localhost:8000/sensor-readings?start=2023-08-01T00:00:00&end=2024-08-01T00:00:00'
6. For endpoint to retrieve the last ten sensor readings for a specific sensor use 'localhost:8000/sensor-readings/<sensor-id>'.Currently supports two mock sensors humidity_sensor,temperature_sensor.eg:-'localhost:8000/sensor-readings/temperature_sensor

mqtt_publisher is used to send mock data.
mqtt_subscriber is used for receiving the data and saving it to mongodb collection and redis
app.py then connects to both mongodb and redis containers to retrieve the data upon API request

# Challenges faced
New to using docker so there was trial and error involed when setting up the application
TBH everything used except for fastAPI and basic python programing was new and required learning
