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

-- 2. Create Native Table
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
```
## 📝 Homework Walkthrough & Logic

### Q1. Counting Records
* **Answer:** 20,332,093

### Q2. Data Read Estimation (External vs. Native)
* **Logic:** BigQuery stores **native metadata** for materialized tables, which allows it to provide a byte estimation before the query runs. External tables require reading the files from GCS at runtime to determine the schema and data size, resulting in a **0 MB** initial estimate in the query validator.
* **Answer:** 0 MB for the External Table and 155.12 MB for the Materialized Table.

### Q4. Counting Zero Fare Trips
* **Query:** ```sql
    SELECT COUNT(*) 
    FROM \`tactile-anthem-485519-v6.zoomcamp.yellow_tripdata_2024Q1Q2_native\` 
    WHERE fare_amount = 0;
    ```
* **Answer:** 8,333

### Q5. Partitioning and Clustering Strategy
* **Logic:** **Partitioning** by date (`tpep_dropoff_datetime`) physically separates the data into segments, making date-range filters much faster. **Clustering** by `VendorID` sorts the data within those partitions, which optimizes queries that group or filter by that specific ID.
* **Answer:** Partition by `tpep_dropoff_datetime` and Cluster on `VendorID`.

### Q6. Impact of Partitioning on Performance
* **Non-Partitioned Scan:** ~310.24 MB
* **Partitioned Scan:** ~26.84 MB
* **Answer:** 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table.

### Q9. Metadata Queries (The 0 Byte Scan)
* **Logic:** When you perform a simple `COUNT(*)` on a native BigQuery table without any `WHERE` clauses, BigQuery retrieves the result directly from the **table metadata** rather than scanning the actual rows of the table.
* **Answer:** 0 bytes.
