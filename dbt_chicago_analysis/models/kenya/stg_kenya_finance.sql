with source as (
    select * from `gcp-de-learning-498109.kenya_finance.raw_financial_inclusion`
),

cleaned as (
    select
        county,
        region,
        year,
        population,
        mpesa_users,
        bank_accounts,
        mobile_loans,
        sacco_members,
        financially_excluded,

        ROUND(mpesa_users / population * 100, 2) AS mpesa_penetration_pct,
        ROUND(bank_accounts / population * 100, 2) AS bank_penetration_pct,
        ROUND(financially_excluded / population * 100, 2) AS exclusion_rate_pct

    from source
)

select * from cleaned
