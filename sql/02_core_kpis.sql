WITH journey AS (
    SELECT
        r.referral_id,
        r.site,
        r.program,
        r.referral_date,
        c.intake_date,
        MIN(CASE WHEN a.appointment_status = 'Completed'
                 THEN a.appointment_date END) AS first_completed_appointment,
        MIN(se.service_date) AS first_service_date
    FROM referrals r
    LEFT JOIN cases c
      ON c.referral_id = r.referral_id
    LEFT JOIN appointments a
      ON a.case_id = c.case_id
    LEFT JOIN service_events se
      ON se.case_id = c.case_id
    GROUP BY
        r.referral_id,
        r.site,
        r.program,
        r.referral_date,
        c.intake_date
)
SELECT
    site,
    program,
    COUNT(*) AS referrals,
    SUM(CASE WHEN intake_date IS NOT NULL THEN 1 ELSE 0 END) AS intakes,
    SUM(CASE WHEN first_service_date IS NOT NULL THEN 1 ELSE 0 END) AS served,
    ROUND(
        AVG(
            CASE WHEN intake_date IS NOT NULL
                 THEN julianday(intake_date) - julianday(referral_date)
            END
        ),
        2
    ) AS avg_days_referral_to_intake,
    ROUND(
        AVG(
            CASE WHEN first_service_date IS NOT NULL
                 THEN julianday(first_service_date) - julianday(referral_date)
            END
        ),
        2
    ) AS avg_days_referral_to_service
FROM journey
GROUP BY site, program
ORDER BY site, program;
