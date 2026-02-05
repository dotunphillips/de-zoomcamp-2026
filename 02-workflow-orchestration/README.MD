# Data Engineering Zoomcamp 2026 - Module 2: Workflow Orchestration

This repository contains the solution for Module 2 of the Data Engineering Zoomcamp. This module focuses on orchestrating ETL pipelines using **Kestra** to ingest NYC Taxi data (Yellow and Green) into **Google Cloud Storage (GCS)** and **BigQuery**.

## Project Structure
* `docker-compose.yaml`: Configuration to run Kestra and its Postgres database.
* `.gitignore`: Configured to protect sensitive `.env` files and GCP JSON keys.
* `flows/`: Contains the Kestra YAML flows.
    * `07_gcp_setup.yaml`: Initial setup for GCS buckets and BigQuery datasets.
    * `09_gcp_taxi_scheduled.yaml`: The main ETL flow for Yellow and Green taxi data.

## Setup & Orchestration
### 1. Credentials Management
To maintain security, GCP Service Account credentials were not hardcoded in the YAML files:
* Local environment variables were stored in a `.env` file (excluded from Git).
* The Service Account JSON was added to the Kestra **KV Store** within the `zoomcamp` namespace as `GCP_CREDS`.

### 2. Backfill Logic
The 2021 data (January to July) was ingested using Kestra's **Backfill** feature. 
* The flow `09_gcp_taxi_scheduled` uses a `Schedule` trigger.
* I implemented a "Dual-Run" logic to handle both manual executions and trigger-based backfills interchangeably using the following Pebble expression:
  `active_date: "{{ trigger.date ? trigger.date : inputs.month }}"`

---

## Quiz Answers

### Q1: Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size?
**Answer:** `128.3 MiB`
* *Verified via Kestra task output metadata.*

### Q2: What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
**Answer:** `green_tripdata_2020-04.csv`

### Q3: How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
**Answer:** `24,648,499`
* *Verified via BigQuery:* `SELECT count(*) FROM ... WHERE filename LIKE 'yellow_tripdata_2020%'`

### Q4: How many rows are there for the Green Taxi data for all CSV files in the year 2020?
**Answer:** `1,734,051`
* *Verified via BigQuery:* `SELECT count(*) FROM ... WHERE filename LIKE 'green_tripdata_2020%'`

### Q5: How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
**Answer:** `1,925,152`

### Q6: How would you configure the timezone to New York in a Schedule trigger?
**Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`

---

## How to Run
1. Start Kestra: `docker compose up -d`
2. Access the UI at `http://localhost:8082`.
3. Configure the `zoomcamp` namespace KV Store with your `GCP_PROJECT_ID`, `GCP_BUCKET_NAME`, and `GCP_CREDS`.
4. Import the flows from the `flows/` directory and execute.