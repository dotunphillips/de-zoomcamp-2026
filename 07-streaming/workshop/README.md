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

## Detailed Work & Verification

### Q1 & Q2: Infrastructure & Throughput
The Redpanda version was verified via `docker exec`:
```bash
docker exec -it redpanda-1 rpk version
```
### Q3 & Q4: Stream Analytics (PyFlink SQL)
```sql
-- Distance Filter
SELECT count(*) FROM green_tripdata WHERE trip_distance > 5;

-- Top PULocationID
SELECT PULocationID, count(*) as cnt 
FROM green_tripdata 
GROUP BY PULocationID 
ORDER BY cnt DESC LIMIT 1;
```

### Q5: Session Windowing
```sql
SELECT 
    window_start, window_end, 
    TIMESTAMPDIFF(MINUTE, window_start, window_end) as duration
FROM TABLE(SESSION(TABLE events, DESCRIPTOR(event_time), INTERVAL '5' MINUTES))
ORDER BY duration DESC LIMIT 1;
```

### Q6: Streaming Aggregation
```sql
SELECT 
    window_start, 
    window_end, 
    SUM(tip_amount) AS total_tip
FROM TABLE(
    TUMBLE(
        TABLE green_tripdata, 
        DESCRIPTOR(lpep_pickup_datetime), 
        INTERVAL '1' HOURS
    )
)
GROUP BY window_start, window_end
ORDER BY total_tip DESC 
LIMIT 1;
```

## How to Run
1. Start infrastructure: `docker-compose up -d`
2. Run producer: `uv run src/producers/homework_producer.py`
3. Run Flink job: `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/tip_job.py`