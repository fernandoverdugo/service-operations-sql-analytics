SELECT
    r.site,
    r.program,
    a.appointment_type,
    COUNT(*) AS appointments,
    SUM(CASE WHEN a.appointment_status = 'Completed' THEN 1 ELSE 0 END)
        AS completed,
    SUM(CASE WHEN a.appointment_status = 'No Show' THEN 1 ELSE 0 END)
        AS no_shows,
    SUM(CASE WHEN a.appointment_status = 'Cancelled' THEN 1 ELSE 0 END)
        AS cancelled,
    ROUND(
        AVG(CASE WHEN a.appointment_status = 'No Show' THEN 1.0 ELSE 0.0 END),
        4
    ) AS no_show_rate,
    ROUND(
        AVG(CASE WHEN a.appointment_status = 'Cancelled' THEN 1.0 ELSE 0.0 END),
        4
    ) AS cancellation_rate
FROM appointments a
JOIN cases c
  ON c.case_id = a.case_id
JOIN referrals r
  ON r.referral_id = c.referral_id
GROUP BY r.site, r.program, a.appointment_type
ORDER BY no_show_rate DESC, appointments DESC;
