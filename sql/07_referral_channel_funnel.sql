WITH referral_level AS (
    SELECT
        r.referral_id,
        r.referral_channel,
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
        r.referral_channel,
        r.referral_date,
        c.intake_date
)
SELECT
    referral_channel,
    COUNT(*) AS referrals,
    SUM(CASE WHEN intake_date IS NOT NULL THEN 1 ELSE 0 END) AS intakes,
    SUM(CASE WHEN first_service_date IS NOT NULL THEN 1 ELSE 0 END)
        AS referrals_served,
    ROUND(
        AVG(CASE WHEN intake_date IS NOT NULL THEN 1.0 ELSE 0.0 END),
        4
    ) AS referral_to_intake_rate,
    ROUND(
        AVG(CASE WHEN first_service_date IS NOT NULL THEN 1.0 ELSE 0.0 END),
        4
    ) AS referral_to_service_rate,
    ROUND(
        AVG(
            CASE WHEN first_service_date IS NOT NULL
                 THEN julianday(first_service_date) - julianday(referral_date)
            END
        ),
        2
    ) AS avg_days_referral_to_service
FROM referral_level
GROUP BY referral_channel
ORDER BY referral_to_service_rate DESC;
