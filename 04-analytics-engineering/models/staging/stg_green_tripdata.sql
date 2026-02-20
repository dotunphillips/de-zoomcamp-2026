SELECT 
    -- identifiers
    CAST(vendorid AS int64) AS vendor_id,
    'Green' AS service_type,
    CAST(ratecodeid AS int64) AS rate_code_id,
    CAST(pulocationid AS int64) AS pickup_location_id,
    CAST(dolocationid AS int64) AS dropoff_location_id,

    -- timestamps
    CAST(lpep_pickup_datetime AS timestamp) AS pickup_datetime,
    CAST(lpep_dropoff_datetime AS timestamp) AS dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    CAST(passenger_count AS int64) AS passenger_count,
    CAST(trip_distance AS numeric) AS trip_distance,
    CAST(trip_type AS int64) AS trip_type,

    -- payment info
    CAST(fare_amount AS numeric) AS fare_amount,
    CAST(extra AS numeric) AS extra,
    CAST(mta_tax AS numeric) AS mta_tax,
    CAST(tip_amount AS numeric) AS tip_amount,
    CAST(tolls_amount AS numeric) AS tolls_amount,
    CAST(ehail_fee AS numeric) AS ehail_fee,
    CAST(improvement_surcharge AS numeric) AS improvement_surcharge,
    CAST(total_amount AS numeric) AS total_amount,
    CAST(payment_type AS int64) AS payment_type

FROM {{ source('raw_data', 'green_tripdata') }}
WHERE vendorid IS NOT NULL