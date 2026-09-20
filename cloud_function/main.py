import base64
import json
from datetime import datetime, timezone

from google.cloud import bigquery
import functions_framework


PROJECT_ID = "smart-energy-monitoring-509113"
DATASET_ID = "energy_monitoring"
TABLE_ID = "meter_readings"


@functions_framework.cloud_event
def process_energy_reading(cloud_event):

    pubsub_message = cloud_event.data["message"]
    encoded_data = pubsub_message["data"]

    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    reading = json.loads(decoded_data)

    meter_id = reading["meter_id"]
    timestamp = reading["timestamp"]
    electricity_consumed = float(reading["electricity_consumed"])
    temperature = float(reading["temperature"])
    humidity = float(reading["humidity"])
    wind_speed = float(reading["wind_speed"])
    avg_past_consumption = float(reading["avg_past_consumption"])
    anomaly_label = reading["anomaly_label"]

    if avg_past_consumption > 0:
        consumption_ratio = electricity_consumed / avg_past_consumption
    else:
        consumption_ratio = 0

    if consumption_ratio >= 1.5:
        system_alert = True
        alert_reason = "Consumption is at least 50% above historical average"
    else:
        system_alert = False
        alert_reason = "Normal consumption"

    client = bigquery.Client()

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    row = {
        "meter_id": meter_id,
        "timestamp": timestamp,
        "electricity_consumed": electricity_consumed,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "avg_past_consumption": avg_past_consumption,
        "anomaly_label": anomaly_label,
        "consumption_ratio": consumption_ratio,
        "system_alert": system_alert,
        "alert_reason": alert_reason,
        "processed_at": datetime.now(timezone.utc).isoformat()
    }

    errors = client.insert_rows_json(table_ref, [row])

    if errors:
        print("BigQuery errors:", errors)
        raise RuntimeError(f"BigQuery insertion failed: {errors}")

    print(
        f"Processed {meter_id}: "
        f"consumption={electricity_consumed}, "
        f"ratio={consumption_ratio:.2f}, "
        f"alert={system_alert}"
    )
