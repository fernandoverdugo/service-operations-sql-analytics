WITH client_activity AS (
    SELECT
        cl.client_id,
        cl.home_site,
        COUNT(DISTINCT r.referral_id) AS referral_count,
        COUNT(DISTINCT c.case_id) AS case_count,
        COUNT(DISTINCT se.service_event_id) AS service_event_count,
        COUNT(DISTINCT r.program) AS programs_referred,
        MIN(r.referral_date) AS first_referral_date,
        MAX(r.referral_date) AS last_referral_date
    FROM clients cl
    LEFT JOIN referrals r
      ON r.client_id = cl.client_id
    LEFT JOIN cases c
      ON c.referral_id = r.referral_id
    LEFT JOIN service_events se
      ON se.case_id = c.case_id
    GROUP BY
        cl.client_id,
        cl.home_site
)
SELECT
    client_id,
    home_site,
    referral_count,
    case_count,
    service_event_count,
    programs_referred,
    first_referral_date,
    last_referral_date,
    CASE WHEN referral_count >= 2 THEN 1 ELSE 0 END AS repeat_referral_flag,
    CASE WHEN programs_referred >= 2 THEN 1 ELSE 0 END AS multi_program_flag,
    CASE WHEN service_event_count >= 2 THEN 1 ELSE 0 END
        AS repeat_service_flag,
    CASE
        WHEN first_referral_date IS NOT NULL
         AND last_referral_date IS NOT NULL
        THEN CAST(
            julianday(last_referral_date)
            - julianday(first_referral_date)
            AS INTEGER
        )
    END AS referral_span_days
FROM client_activity
ORDER BY client_id;
