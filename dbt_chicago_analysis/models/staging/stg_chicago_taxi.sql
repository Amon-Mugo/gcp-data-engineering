with source as (
    select
        unique_key,
        taxi_id,
        trip_start_timestamp,
        trip_end_timestamp,
        trip_seconds,
        trip_miles,
        fare,
        tips,
        tolls,
        extras,
        trip_total,
        payment_type,
        company,
        pickup_community_area,
        dropoff_community_area
    from `bigquery-public-data.chicago_taxi_trips.taxi_trips`
    where trip_start_timestamp >= '2022-01-01'
    and trip_miles > 0
    and trip_seconds > 0
    and fare > 0
)

select * from source
