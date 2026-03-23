with trips as (
    select * from {{ ref('int_trips') }}
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
)
select 
    trips.trip_id,
    trips.vendor_id,
    trips.service_type, -- Identify if it was Yellow or Green
    
    -- Joining pickup info
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone,
    
    -- Joining dropoff info
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    
    trips.pickup_datetime,
    trips.dropoff_datetime,
    
    -- Calculations
    trips.fare_amount,
    trips.total_amount,
    trips.passenger_count,
    trips.trip_distance
    
from trips
inner join dim_zones as pickup_zone
    on trips.pickup_location_id = pickup_zone.location_id
inner join dim_zones as dropoff_zone
    on trips.dropoff_location_id = dropoff_zone.location_id