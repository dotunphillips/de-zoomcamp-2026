{{
    config(
        materialized='view'
    )
}}

with trips_unioned as (
    select * from {{ ref('int_trips_unioned') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
)

select
    -- We can generate the trip_id here or in staging
    {{ dbt_utils.generate_surrogate_key(['vendor_id', 'pickup_datetime']) }} as trip_id,
    t.*,
    -- Join with zones to get the pickup/dropoff borough and zone names
    pz.borough as pickup_borough,
    pz.zone as pickup_zone,
    dz.borough as dropoff_borough,
    dz.zone as dropoff_zone

from trips_unioned t
left join dim_zones pz on t.pickup_location_id = pz.location_id
left join dim_zones dz on t.dropoff_location_id = dz.location_id