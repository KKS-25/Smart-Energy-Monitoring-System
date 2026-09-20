import pandas as pd
import json
import time

from google.cloud import pubsub_v1

PROJECT_ID = "smart-energy-monitoring-509113"
TOPIC_ID = "energy-readings"

CSV_FILE = "smart_meter_data.csv"

METER_ID = "METER_001"

PUBLISH_INTERVAL = 5

print("Loading smart meter dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Dataset loaded successfully.")
print(f"Total readings available: {len(df)}")
print()

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(
    PROJECT_ID,
    TOPIC_ID
)

print(f"Publishing to:")
print(topic_path)
print()

print("Starting smart meter simulator...")
print("Press CTRL+C to stop.\n")

try:

    for index, row in df.iterrows():

        reading = {

            "meter_id": METER_ID,

            "timestamp": str(
                row["Timestamp"]
            ),

            "electricity_consumed": float(
                row["Electricity_Consumed"]
            ),

            "temperature": float(
                row["Temperature"]
            ),

            "humidity": float(
                row["Humidity"]
            ),

            "wind_speed": float(
                row["Wind_Speed"]
            ),

            "avg_past_consumption": float(
                row["Avg_Past_Consumption"]
            ),

            "anomaly_label": str(
                row["Anomaly_Label"]
            )
        }

        message = json.dumps(
            reading
        ).encode("utf-8")

        future = publisher.publish(
            topic_path,
            message
        )

        message_id = future.result()

        print(
            f"Reading {index + 1}/{len(df)} | "
            f"Meter: {METER_ID} | "
            f"Consumption: "
            f"{reading['electricity_consumed']:.4f} | "
            f"Label: {reading['anomaly_label']} | "
            f"Message ID: {message_id}"
        )

        time.sleep(
            PUBLISH_INTERVAL
        )

except KeyboardInterrupt:

    print("\nSimulator stopped.")
