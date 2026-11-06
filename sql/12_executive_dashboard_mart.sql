WITH executive AS (
    SELECT *
    FROM (
        WITH journey AS (
            SELECT
                r.referral_id,
                c.case_id,
                r.referral_date,
                c.intake_date,
                c.close_reason,
                MIN(se.service_date) AS first_service_date
            FROM referrals r
            LEFT JOIN cases c
              ON c.referral_id = r.referral_id
            LEFT JOIN service_events se
              ON se.case_id = c.case_id
            GROUP BY
                r.referral_id,
                c.case_id,
                r.referral_date,
                c.intake_date,
                c.close_reason
        ),
        appointment_summary AS (
            SELECT
                COUNT(*) AS appointments,
                SUM(CASE WHEN appointment_status = 'No Show' THEN 1 ELSE 0 END)
                    AS no_shows,
                SUM(CASE WHEN appointment_status = 'Cancelled' THEN 1 ELSE 0 END)
                    AS cancellations
            FROM appointments
        )
        SELECT
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
            ) AS avg_days_referral_to_service,
            ROUND(
                AVG(
                    CASE
                        WHEN first_service_date IS NOT NULL
                        THEN julianday(first_service_date) - julianday(referral_date) <= 14
                    END
                ),
                4
            ) AS service_sla_rate_among_served,
            ROUND(
                (SELECT no_shows * 1.0 / appointments FROM appointment_summary),
                4
            ) AS no_show_rate,
            ROUND(
                (SELECT cancellations * 1.0 / appointments FROM appointment_summary),
                4
            ) AS cancellation_rate
        FROM journey
    )
)
SELECT
    'all_services' AS scope,
    referrals,
    intakes,
    referrals_served,
    referral_to_intake_rate,
    referral_to_service_rate,
    avg_days_referral_to_service,
    service_sla_rate_among_served,
    no_show_rate,
    cancellation_rate
FROM executive;
