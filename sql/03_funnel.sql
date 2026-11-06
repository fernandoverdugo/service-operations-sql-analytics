WITH referral_level AS (
    SELECT
        r.referral_id,
        r.site,
        r.program,
        r.referral_date,
        c.case_id,
        c.intake_date,
        MIN(se.service_date) AS first_service_date
    FROM referrals r
    LEFT JOIN cases c
      ON c.referral_id = r.referral_id
    LEFT JOIN service_events se
      ON se.case_id = c.case_id
    GROUP BY
        r.referral_id,
        r.site,
        r.program,
        r.referral_date,
        c.case_id,
        c.intake_date
)
SELECT
    site,
    program,
    COUNT(*) AS referred,
    SUM(CASE WHEN intake_date IS NOT NULL THEN 1 ELSE 0 END) AS completed_intake,
    SUM(CASE WHEN first_service_date IS NOT NULL THEN 1 ELSE 0 END) AS received_service,
    ROUND(
        SUM(CASE WHEN intake_date IS NOT NULL THEN 1.0 ELSE 0 END)
        / COUNT(*),
        4
    ) AS referral_to_intake_rate,
    ROUND(
        SUM(CASE WHEN first_service_date IS NOT NULL THEN 1.0 ELSE 0 END)
        / COUNT(*),
        4
    ) AS referral_to_service_rate
FROM referral_level
GROUP BY site, program
ORDER BY site, program;
