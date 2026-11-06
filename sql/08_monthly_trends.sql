WITH referral_level AS (
    SELECT
        r.referral_id,
        substr(r.referral_date, 1, 7) AS referral_month,
        r.referral_date,
        c.intake_date,
        MIN(se.service_date) AS first_service_date
    FROM referrals r
    LEFT JOIN cases c
      ON c.referral_id = r.referral_id
    LEFT JOIN service_events se
      ON se.case_id = c.case_id
    GROUP BY
        r.referral_id,
        r.referral_date,
        c.intake_date
),
monthly AS (
    SELECT
        referral_month,
        COUNT(*) AS referrals,
        SUM(CASE WHEN intake_date IS NOT NULL THEN 1 ELSE 0 END) AS intakes,
        SUM(CASE WHEN first_service_date IS NOT NULL THEN 1 ELSE 0 END)
            AS referrals_served,
        AVG(CASE WHEN intake_date IS NOT NULL THEN 1.0 ELSE 0.0 END)
            AS referral_to_intake_rate,
        AVG(CASE WHEN first_service_date IS NOT NULL THEN 1.0 ELSE 0.0 END)
            AS referral_to_service_rate,
        AVG(
            CASE WHEN intake_date IS NOT NULL
                 THEN julianday(intake_date) - julianday(referral_date)
            END
        ) AS avg_days_referral_to_intake,
        AVG(
            CASE WHEN first_service_date IS NOT NULL
                 THEN julianday(first_service_date) - julianday(referral_date)
            END
        ) AS avg_days_referral_to_service
    FROM referral_level
    GROUP BY referral_month
)
SELECT
    referral_month,
    referrals,
    intakes,
    referrals_served,
    ROUND(referral_to_intake_rate, 4) AS referral_to_intake_rate,
    ROUND(referral_to_service_rate, 4) AS referral_to_service_rate,
    ROUND(
        AVG(referral_to_service_rate) OVER (
            ORDER BY referral_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS referral_to_service_rate_3m,
    ROUND(
        referral_to_service_rate
        - LAG(referral_to_service_rate) OVER (
            ORDER BY referral_month
        ),
        4
    ) AS service_rate_month_over_month_change,
    ROUND(avg_days_referral_to_intake, 2)
        AS avg_days_referral_to_intake,
    ROUND(avg_days_referral_to_service, 2)
        AS avg_days_referral_to_service
FROM monthly
ORDER BY referral_month;
