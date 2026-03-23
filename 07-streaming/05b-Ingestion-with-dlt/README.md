# Data Engineering Zoomcamp 2026 - Module 1: dlt Pipeline

This repository contains the solution for the **dlt (Data Load Tool)** workshop. The project involves building a pipeline to ingest NYC taxi trip data from a REST API into a DuckDB destination and performing analytical queries.

## 🚕 Project Overview

The pipeline extracts data from a custom NYC Taxi API, normalizes the schema using `dlt`, and loads it into a local DuckDB database (`taxi_pipeline.duckdb`).

### Homework Questions & Answers

| Question | Analysis | Answer |
| :--- | :--- | :--- |
| **1. Dataset Time Range** | `MIN(trip_pickup_date_time)` to `MAX(...)` | **2009-06-01** to **2009-06-30** |
| **2. Credit Card Proportion** | Proportion of trips with `payment_type` as Credit/1 | **26.66%** |
| **3. Total Tips Generated** | `SUM(tip_amt)` for the 10,000 unique records | **$6,063.41** |

---

## 🛠️ Pipeline Implementation

The pipeline was built using Python and the `dlt` library.

### Challenges & Solutions: API Pagination
During development, I discovered that the API required explicit pagination to move beyond the first 1,000 records. A simple `requests.get(url, params=params)` was being ignored by the endpoint. 

**Solution:** I implemented a manual URL construction using f-strings to force the `offset` parameter, ensuring all 10,000 unique records were ingested.

```python
# snippet from taxi_pipeline.py
for i in range(10):
    offset = i * 1000
    # Manually constructing URL to ensure API pagination
    request_url = f"{url}?offset={offset}&limit=1000"
    response = requests.get(request_url)
    yield response.json()
```
```sql
SELECT 
    COUNT(*) AS total_rows,
    MIN(trip_pickup_date_time) AS start_time,
    MAX(trip_pickup_date_time) AS end_time,
    ROUND(AVG(CASE WHEN payment_type IN ('Credit', '1') THEN 1 ELSE 0 END) * 100, 2) AS cc_percentage,
    ROUND(SUM(tip_amt), 2) AS total_tips
FROM taxi_data.taxi_rides;
```