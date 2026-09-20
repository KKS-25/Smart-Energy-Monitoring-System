import json
from google.cloud import pubsub_v1

PROJECT_ID = "smart-energy-monitoring-509113"
TOPIC_ID = "energy-readings"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

reading = {
    "meter_id": "METER_TEST",
    "timestamp": "2026-09-20T19:30:00",
    "electricity_consumed": 0.90,
    "temperature": 0.50,
    "humidity": 0.50,
    "wind_speed": 0.30,
    "avg_past_consumption": 0.50,
    "anomaly_label": "Anomaly"
}

message = json.dumps(reading).encode("utf-8")

future = publisher.publish(topic_path, message)

print("Test alert reading published!")
print("Message ID:", future.result())