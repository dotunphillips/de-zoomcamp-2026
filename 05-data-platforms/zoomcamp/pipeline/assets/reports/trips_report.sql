/* @bruin
name: reports.trips_report
type: bq.sql

depends_on:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: pickup_date
    type: DATE
    primary_key: true
  - name: pickup_location_id
    type: INTEGER
    primary_key: true
  - name: total_trips
    type: BIGINT
    checks:
      - name: non_negative
  - name: total_amount
    type: DOUBLE
  - name: total_distance
    type: DOUBLE
@bruin */

-- Aggregating at the Date and Location level
SELECT
    -- Dimensions
    CAST(pickup_datetime AS DATE) as pickup_date,
    pickup_location_id,
    taxi_type,
    payment_type_name,
    
    -- Volume Metrics
    COUNT(*) as total_trips,
    COUNT(DISTINCT vendor_id) as unique_vendors,
    SUM(passenger_count) as total_passengers,
    
    -- Distance Metrics
    SUM(trip_distance) as total_distance,
    AVG(trip_distance) as avg_distance,
    
    -- Financial Metrics
    SUM(fare_amount) as total_fare,
    SUM(tip_amount) as total_tips,
    SUM(tolls_amount) as total_tolls,
    SUM(improvement_surcharge) as total_improvement_surcharge,
    SUM(congestion_surcharge) as total_congestion_surcharge,
    SUM(total_amount) as total_amount_collected,
    
    -- Derived Metrics
    AVG(total_amount) as avg_total_amount

FROM staging.trips

-- Incremental Filter for the run window
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'

GROUP BY 
    pickup_date,
    pickup_location_id,
    taxi_type,
    payment_type_name