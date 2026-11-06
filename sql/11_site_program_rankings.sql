WITH journey AS (
    SELECT
        r.referral_id,
        r.site,
        r.program,
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
        r.site,
        r.program,
        r.referral_date,
        c.intake_date
),
journey_summary AS (
    SELECT
        site,
        program,
        COUNT(*) AS referrals,
        AVG(CASE WHEN intake_date IS NOT NULL THEN 1.0 ELSE 0.0 END)
            AS intake_rate,
        AVG(CASE WHEN first_service_date IS NOT NULL THEN 1.0 ELSE 0.0 END)
            AS service_rate,
        AVG(
            CASE
                WHEN first_service_date IS NOT NULL
                THEN julianday(first_service_date) - julianday(referral_date)
            END
        ) AS avg_days_to_service
    FROM journey
    GROUP BY site, program
),
appointment_summary AS (
    SELECT
        r.site,
        r.program,
        COUNT(*) AS appointments,
        AVG(CASE WHEN a.appointment_status = 'No Show'
                 THEN 1.0 ELSE 0.0 END) AS no_show_rate
    FROM appointments a
    JOIN cases c
      ON c.case_id = a.case_id
    JOIN referrals r
      ON r.referral_id = c.referral_id
    GROUP BY r.site, r.program
),
combined AS (
    SELECT
        j.site,
        j.program,
        j.referrals,
        j.intake_rate,
        j.service_rate,
        j.avg_days_to_service,
        a.appointments,
        a.no_show_rate
    FROM journey_summary j
    JOIN appointment_summary a
      ON a.site = j.site
     AND a.program = j.program
)
SELECT
    site,
    program,
    referrals,
    ROUND(intake_rate, 4) AS intake_rate,
    ROUND(service_rate, 4) AS service_rate,
    ROUND(avg_days_to_service, 2) AS avg_days_to_service,
    appointments,
    ROUND(no_show_rate, 4) AS no_show_rate,
    DENSE_RANK() OVER (
        PARTITION BY program
        ORDER BY service_rate DESC
    ) AS service_rate_rank_within_program,
    DENSE_RANK() OVER (
        PARTITION BY program
        ORDER BY no_show_rate ASC
    ) AS no_show_rank_within_program,
    DENSE_RANK() OVER (
        ORDER BY service_rate DESC
    ) AS overall_service_rate_rank
FROM combined
ORDER BY overall_service_rate_rank, site, program;
