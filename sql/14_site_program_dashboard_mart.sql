WITH referral_summary AS (
    SELECT
        r.site,
        r.program,
        COUNT(*) AS referrals,
        AVG(CASE WHEN c.intake_date IS NOT NULL THEN 1.0 ELSE 0.0 END)
            AS intake_rate,
        AVG(
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM service_events se
                    WHERE se.case_id = c.case_id
                )
                THEN 1.0 ELSE 0.0
            END
        ) AS service_rate,
        AVG(
            CASE
                WHEN c.case_id IS NOT NULL
                THEN (
                    SELECT MIN(
                        julianday(se.service_date)
                        - julianday(r.referral_date)
                    )
                    FROM service_events se
                    WHERE se.case_id = c.case_id
                )
            END
        ) AS avg_days_to_service
    FROM referrals r
    LEFT JOIN cases c
      ON c.referral_id = r.referral_id
    GROUP BY r.site, r.program
),
appointment_summary AS (
    SELECT
        r.site,
        r.program,
        COUNT(*) AS appointments,
        AVG(CASE WHEN a.appointment_status = 'No Show'
                 THEN 1.0 ELSE 0.0 END) AS no_show_rate,
        AVG(CASE WHEN a.appointment_status = 'Cancelled'
                 THEN 1.0 ELSE 0.0 END) AS cancellation_rate
    FROM appointments a
    JOIN cases c
      ON c.case_id = a.case_id
    JOIN referrals r
      ON r.referral_id = c.referral_id
    GROUP BY r.site, r.program
)
SELECT
    r.site,
    r.program,
    r.referrals,
    ROUND(r.intake_rate, 4) AS intake_rate,
    ROUND(r.service_rate, 4) AS service_rate,
    ROUND(r.avg_days_to_service, 2) AS avg_days_to_service,
    a.appointments,
    ROUND(a.no_show_rate, 4) AS no_show_rate,
    ROUND(a.cancellation_rate, 4) AS cancellation_rate,
    DENSE_RANK() OVER (
        ORDER BY r.service_rate DESC
    ) AS service_rate_rank
FROM referral_summary r
JOIN appointment_summary a
  ON a.site = r.site
 AND a.program = r.program
ORDER BY service_rate_rank, r.site, r.program;
