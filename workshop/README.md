# Data Engineering Zoomcamp 2026: Streaming Module Homework

This repository contains my implementation of a streaming data pipeline using **Redpanda (Kafka)**, **PyFlink**, and **PostgreSQL**.

## Pipeline Architecture
1. **Producer**: Python script using `confluent-kafka` to stream Green Taxi data from Parquet to Redpanda.
2. **Stream Processor**: PyFlink SQL job performing Tumbling and Session window aggregations.
3. **Sink**: PostgreSQL database for persistent storage of analytical results.

## Key Technical Challenges & Solutions
- **Data Sanitization**: Handled `NaN` values in the `tip_amount` column during production to prevent Flink job failures.
- **Watermark Management**: Implemented a "Future Record" injection strategy to force-close windows at the end of the stream for accurate 100% data processing.
- **Verification**: Performed a secondary **Batch Audit** using **DuckDB** to verify the mathematical "Source of Truth" within the raw Parquet file.

## Results Summary

| Question | My Result |
| :--- | :--- |
| **Q1: Redpanda Version** | `v25.3.9` |
| **Q2: Producer Timing** | `~10 seconds` |
| **Q3: Distance > 5 Count** | `8506` |
| **Q4: Top PULocationID** | `74` |
| **Q5: Longest Session** | `81` |
| **Q6: Largest Tip Hour** | `2025-10-16 18:00:00` |

### Note on Question 6
While the official benchmark for the 2026 dataset is `2025-10-22 08:00:00`, my local analysis (verified via both PyFlink and DuckDB batch processing) definitively identified `2025-10-16 18:00:00` as the peak for my specific source file. I have opted to submit the result reflected by my data audit.

## How to Run
1. Start infrastructure: `docker-compose up -d`
2. Run producer: `uv run src/producers/homework_producer.py`
3. Run Flink job: `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/tip_job.py`