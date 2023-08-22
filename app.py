from fastapi import FastAPI, HTTPException, Query
import pymongo
import redis
import json
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()

# MongoDB Connection
mongo_client = pymongo.MongoClient("mongodb://mqtt:mqttpass@mongodb:27017/")
db = mongo_client["mqtt_data"]
collection = db["sensor_readings"]

# Redis Connection
redis_client = redis.StrictRedis(host="redis", port=6379, db=0)

class SensorReading(BaseModel):
    sensor_id: str
    value: float
    timestamp: datetime

@app.get("/sensor-readings")
def get_sensor_readings(start: datetime = Query(...), end: datetime = Query(...)):
    start_iso = start.isoformat()
    end_iso = end.isoformat()
    # print(start_iso,end_iso)
    result = []
    cursor = collection.find({"timestamp": {"$gte": start_iso, "$lte": end_iso}})
    for document in cursor:
        print(document['value'])
        result.append(SensorReading(**document))
    return result

@app.get("/latest-readings/{sensor_id}")
def get_latest_readings(sensor_id: str):
    readings = redis_client.lrange(sensor_id, 0, -1)
    latest_readings = [json.loads(reading) for reading in readings]
    print(latest_readings)
    return latest_readings
