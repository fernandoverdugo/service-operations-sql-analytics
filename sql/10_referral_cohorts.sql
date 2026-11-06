WITH ordered_referrals AS (
    SELECT
        r.client_id,
        r.referral_id,
        r.referral_date,
        r.program,
        r.site,
        ROW_NUMBER() OVER (
            PARTITION BY r.client_id
            ORDER BY r.referral_date, r.referral_id
        ) AS referral_number,
        LEAD(r.referral_date) OVER (
            PARTITION BY r.client_id
            ORDER BY r.referral_date, r.referral_id
        ) AS next_referral_date
    FROM referrals r
),
first_referrals AS (
    SELECT
        client_id,
        referral_id,
        referral_date,
        substr(referral_date, 1, 7) AS cohort_month,
        program,
        site,
        next_referral_date,
        CASE
            WHEN next_referral_date IS NOT NULL
             AND julianday(next_referral_date)
                 - julianday(referral_date) <= 90
            THEN 1 ELSE 0
        END AS repeat_within_90_days
    FROM ordered_referrals
    WHERE referral_number = 1
)
SELECT
    cohort_month,
    COUNT(*) AS clients,
    SUM(repeat_within_90_days) AS repeat_within_90_days,
    ROUND(AVG(repeat_within_90_days * 1.0), 4)
        AS repeat_within_90_days_rate
FROM first_referrals
GROUP BY cohort_month
ORDER BY cohort_month;
