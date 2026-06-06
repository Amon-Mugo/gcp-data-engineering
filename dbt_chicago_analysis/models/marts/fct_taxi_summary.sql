with trips as (
    select * from {{ ref('stg_chicago_taxi') }}
)

select
    EXTRACT(YEAR FROM trip_start_timestamp) AS year,
    EXTRACT(MONTH FROM trip_start_timestamp) AS month,
    payment_type,
    company,
    COUNT(*) AS total_trips,
    ROUND(AVG(trip_miles), 2) AS avg_miles,
    ROUND(AVG(trip_seconds)/60, 2) AS avg_minutes,
    ROUND(AVG(fare), 2) AS avg_fare,
    ROUND(SUM(trip_total), 2) AS total_revenue
from trips
group by year, month, payment_type, company
