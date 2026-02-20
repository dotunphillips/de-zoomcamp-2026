SELECT
    -- identifiers
    CAST(vendorid AS int64) AS vendor_id,
    CAST(ratecodeid AS int64) AS rate_code_id,
    CAST(pulocationid AS int64) AS pickup_location_id,
    CAST(dolocationid AS int64) AS dropoff_location_id,

    -- timestamps
    CAST(tpep_pickup_datetime AS timestamp) AS pickup_datetime,
    CAST(tpep_dropoff_datetime AS timestamp) AS dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    CAST(passenger_count AS int64) AS passenger_count, 
    CAST(trip_distance AS float64) AS trip_distance,   
    1 AS trip_type, 

    -- payment info
    CAST(fare_amount AS numeric) AS fare_amount,       
    CAST(extra AS numeric) AS extra,                   
    CAST(mta_tax AS numeric) AS mta_tax,               
    CAST(tip_amount AS numeric) AS tip_amount,         
    CAST(tolls_amount AS numeric) AS tolls_amount,     
    CAST(improvement_surcharge AS numeric) AS improvement_surcharge, 
    CAST(0 AS numeric) AS ehail_fee,                   
    CAST(total_amount AS numeric) AS total_amount,     
    CAST(payment_type AS int64) AS payment_type        

FROM {{ source('raw_data', 'yellow_tripdata') }}
WHERE vendorid IS NOT NULL