with base as (
    select * from {{ ref('stg_kenya_finance') }}
)

select
    county,
    region,
    year,
    population,
    mpesa_penetration_pct,
    bank_penetration_pct,
    exclusion_rate_pct,

    mpesa_users - bank_accounts AS mobile_money_gap,

    ROUND((mpesa_users + bank_accounts + sacco_members) / population * 100, 2) AS overall_inclusion_pct,

    CASE
        WHEN exclusion_rate_pct < 10 THEN 'Highly Included'
        WHEN exclusion_rate_pct BETWEEN 10 AND 30 THEN 'Moderately Included'
        WHEN exclusion_rate_pct BETWEEN 30 AND 50 THEN 'Underserved'
        ELSE 'Severely Excluded'
    END AS inclusion_category

from base
order by overall_inclusion_pct DESC
