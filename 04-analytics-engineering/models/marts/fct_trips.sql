with trips_unioned as (
    select * from {{ ref('int_trips_unioned') }}
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
)
select 
    trips_unioned.trip_id,
    trips_unioned.vendor_id,
    trips_unioned.service_type, -- Identify if it was Yellow or Green
    
    -- Joining pickup info
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone,
    
    -- Joining dropoff info
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    
    trips_unioned.pickup_datetime,
    trips_unioned.dropoff_datetime,
    
    -- Calculations
    trips_unioned.fare_amount,
    trips_unioned.total_amount,
    trips_unioned.passenger_count,
    trips_unioned.trip_distance
    
from trips_unioned
inner join dim_zones as pickup_zone
    on trips_unioned.pickup_location_id = pickup_zone.location_id
inner join dim_zones as dropoff_zone
    on trips_unioned.dropoff_location_id = dropoff_zone.location_id