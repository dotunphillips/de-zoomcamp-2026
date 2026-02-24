/* @bruin
name: staging.trips
type: bq.sql

depends_on:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
    type: table
    strategy: time_interval
    incremental_key: pickup_datetime
    time_granularity: timestamp

custom_checks:
  - name: row_count_positive
    description: Ensure the table is not empty
    query: SELECT COUNT(*) > 0 FROM staging.trips
    value: 1
@bruin */

/* CTE 1: Normalization & Casting 
   We map the lowercase snake_case names from the ingestion table 
   to our clean staging schema.
*/
WITH trip_data_normalized AS (
    SELECT
        CAST(vendor_id AS INTEGER) as vendor_id,
        CAST(tpep_pickup_datetime AS TIMESTAMP) as pickup_datetime,
        CAST(tpep_dropoff_datetime AS TIMESTAMP) as dropoff_datetime,
        CAST(passenger_count AS INTEGER) as passenger_count,
        CAST(trip_distance AS DOUBLE) as trip_distance,
        CAST(ratecode_id AS INTEGER) as rate_code_id, 
        store_and_fwd_flag,
        CAST(pu_location_id AS INTEGER) as pickup_location_id,
        CAST(do_location_id AS INTEGER) as dropoff_location_id,
        CAST(payment_type AS INTEGER) as payment_type_id,
        CAST(fare_amount AS DOUBLE) as fare_amount,
        CAST(extra AS DOUBLE) as extra,
        CAST(mta_tax AS DOUBLE) as mta_tax,
        CAST(tip_amount AS DOUBLE) as tip_amount,
        CAST(tolls_amount AS DOUBLE) as tolls_amount,
        CAST(improvement_surcharge AS DOUBLE) as improvement_surcharge,
        CAST(total_amount AS DOUBLE) as total_amount,
        CAST(congestion_surcharge AS DOUBLE) as congestion_surcharge,
        taxi_type,
        extracted_at
    FROM ingestion.trips
    /* Filter to the specific run window for incremental processing */
    WHERE tpep_pickup_datetime >= '{{ start_datetime }}' 
      AND tpep_pickup_datetime < '{{ end_datetime }}'
),

/* CTE 2: Deduplication
   Identifies the latest record for each trip using a composite key.
*/
deduplicated_trips AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY 
                vendor_id, 
                pickup_datetime, 
                dropoff_datetime, 
                pickup_location_id, 
                dropoff_location_id, 
                fare_amount
            ORDER BY extracted_at DESC
        ) as record_rank
    FROM trip_data_normalized
)

/* Final Selection: Enrichment & Filtering 
   Joins with the payment_lookup table using the verified column names.
*/
SELECT 
    d.* EXCLUDE (record_rank),
    p.payment_type_name
FROM deduplicated_trips d
LEFT JOIN ingestion.payment_lookup p 
    ON d.payment_type_id = p.payment_type_id
WHERE d.record_rank = 1
  -- Business logic filters
  AND d.vendor_id IS NOT NULL
  AND d.trip_distance >= 0
  AND d.fare_amount >= 0
  AND d.pickup_datetime <= d.dropoff_datetime