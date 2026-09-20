# Smart Energy Consumption Monitoring System

A cloud-based smart energy monitoring system that simulates smart-meter readings, processes electricity consumption data using Google Cloud services, detects unusually high consumption, stores the processed data in BigQuery, and visualizes the results using Looker Studio.

## System Architecture

<p align="center">
  <img width="350" alt="System Architecture" src="https://github.com/user-attachments/assets/d4beb0a8-b547-44d7-9dba-5335e86cc3ed" />
</p>


## Technologies Used

- Python
- Google Cloud Pub/Sub
- Google Cloud Run Functions
- Google BigQuery
- Looker Studio
- Pandas
- Google Cloud Python Libraries

## Features

- Simulates smart-meter readings from a dataset
- Publishes readings to Google Cloud Pub/Sub
- Processes incoming readings using a serverless Cloud Run Function
- Calculates consumption ratio
- Detects unusually high electricity consumption
- Generates automatic consumption alerts
- Stores processed readings in BigQuery
- Provides interactive data visualization using Looker Studio

## Dataset

The project uses the **Smart Meter Electricity Consumption Dataset** from Kaggle.

Dataset source:

https://www.kaggle.com/datasets/ziya07/smart-meter-electricity-consumption-dataset

The dataset contains:

- Timestamp
- Electricity Consumed
- Temperature
- Humidity
- Wind Speed
- Average Past Consumption
- Anomaly Label

## Alert Detection Logic

The system calculates:

```text
Consumption Ratio =
Electricity Consumed / Average Past Consumption
```

## Simulator

The simulator.py script reads the smart-meter dataset and publishes individual readings to the Pub/Sub topic.

A delay between readings is used to simulate a live smart-meter data stream.

Each reading contains information such as:

- Meter ID
- Timestamp
- Electricity consumption
- Temperature
- Humidity
- Wind speed
- Average past consumption
- Anomaly label

## Alert Testing

The test_alert.py script publishes a test reading with a deliberately high consumption ratio to verify the alert mechanism.

The test reading uses:

- Electricity Consumed = 0.90
- Average Past Consumption = 0.50
- Consumption Ratio = 1.80

The alert mechanism was successfully tested and produced:

- consumption_ratio = 1.8
- system_alert = true

## Google Cloud Components

### Google Cloud Pub/Sub

The Pub/Sub topic energy-readings is used to receive simulated smart-meter readings from the Python simulator.

### Cloud Run Function

The process_energy_reading Cloud Run Function receives Pub/Sub events and:

- Decodes the incoming message.
- Extracts the smart-meter readings.
- Calculates the consumption ratio.
- Determines whether an alert should be generated.
- Stores the processed reading in BigQuery.

### Google BigQuery

The processed readings are stored in:

- Dataset: energy_monitoring
- Table: meter_readings

The table contains fields including:

- Meter ID
- Timestamp
- Electricity Consumed
- Temperature
- Humidity
- Wind Speed
- Average Past Consumption
- Anomaly Label
- Consumption Ratio
- System Alert
- Alert Reason
- Processed At

### Looker Studio

Looker Studio is used to visualize the processed energy data through an interactive dashboard.

The dashboard includes:

- Consumption over time
- Actual consumption vs historical average
- Total readings
- Alert count
- Average consumption
- Normal vs anomaly distribution
- Alert details

## Dashboard

The Looker Studio dashboard provides a visual overview of the smart-meter readings, consumption trends, and detected anomalies.

The dashboard contains:

- Total readings scorecard
- Alert count scorecard
- Average consumption scorecard
- Electricity consumption time-series chart
- Actual consumption vs historical average chart
- Normal vs anomaly pie chart
- Alert details table
                         
