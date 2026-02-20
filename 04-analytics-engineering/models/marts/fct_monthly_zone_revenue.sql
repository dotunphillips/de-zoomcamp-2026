{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fct_trips') }}
)
    select 
    -- Revenue grouping 
    pickup_zone,
    {{ dbt.date_trunc("month", "pickup_datetime") }} as revenue_month, 
    extract(year from pickup_datetime) as year,
    extract(month from pickup_datetime) as month,
    service_type, 

    -- Revenue calculation
    sum(total_amount) as revenue_monthly_total_amount,

    -- Additional calculations
    count(trip_id) as total_monthly_trips, -- Fixed from tripid to trip_id
    avg(passenger_count) as avg_monthly_passenger_count,
    avg(trip_distance) as avg_monthly_trip_distance

    from trips_data
    group by 1,2,3,4,5