# DE Zoomcamp 2025 - Module 3: Data Warehouse Homework

This repository contains the solution for the Module 3 homework, focusing on BigQuery performance optimization through partitioning, clustering, and understanding storage types.

## 🛠️ Data Ingestion & Setup
The dataset consists of **Yellow Taxi Trip Records for 2024 (January to June)**.

### Ingestion Process
I used a Python script (`load_yellow_taxi_data.py`) to move data from the source to GCS.
- **Security:** Authenticated via **Application Default Credentials (ADC)** using the `gcloud` CLI, avoiding the use of local service account JSON keys.

### BigQuery Table Creation
```sql
-- 1. Create External Table referencing GCS Parquet files
CREATE OR REPLACE EXTERNAL TABLE `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-dotunphillips-123/yellow_tripdata_2024-*.parquet']
);

-- 2. Create Native (Materialized) Table
CREATE OR REPLACE TABLE `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_native` AS
SELECT * FROM `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_external`;

-- 3. Create Optimized Table (Partitioned by Date)
CREATE OR REPLACE TABLE `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_external`;

-- 4. Create Optimized Table (Partitioned by Date, Clustered by Vendor)
CREATE OR REPLACE TABLE `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_external`;
