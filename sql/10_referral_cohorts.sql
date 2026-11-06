WITH observation AS (
    SELECT
        MAX(referral_date) AS observation_end,
        date(MAX(referral_date), '-90 days') AS latest_eligible_first_referral
    FROM referrals
),
ordered_referrals AS (
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
        o.client_id,
        o.referral_id,
        o.referral_date,
        substr(o.referral_date, 1, 7) AS cohort_month,
        o.program,
        o.site,
        o.next_referral_date,
        CASE
            WHEN o.next_referral_date IS NOT NULL
             AND julianday(o.next_referral_date)
                 - julianday(o.referral_date) <= 90
            THEN 1 ELSE 0
        END AS repeat_within_90_days
    FROM ordered_referrals o
    CROSS JOIN observation obs
    WHERE o.referral_number = 1
      AND o.referral_date <= obs.latest_eligible_first_referral
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
