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
)
SELECT
    site,
    program,
    COUNT(*) AS referrals,
    SUM(
        CASE
            WHEN intake_date IS NOT NULL
             AND julianday(intake_date) - julianday(referral_date) <= 5
            THEN 1 ELSE 0
        END
    ) AS intake_within_5_days,
    SUM(
        CASE
            WHEN first_service_date IS NOT NULL
             AND julianday(first_service_date) - julianday(referral_date) <= 14
            THEN 1 ELSE 0
        END
    ) AS service_within_14_days,
    ROUND(
        AVG(
            CASE
                WHEN intake_date IS NOT NULL
                THEN (
                    julianday(intake_date) - julianday(referral_date) <= 5
                )
            END
        ),
        4
    ) AS intake_sla_rate,
    ROUND(
        AVG(
            CASE
                WHEN first_service_date IS NOT NULL
                THEN (
                    julianday(first_service_date) - julianday(referral_date) <= 14
                )
            END
        ),
        4
    ) AS service_sla_rate
FROM journey
GROUP BY site, program
ORDER BY site, program;
