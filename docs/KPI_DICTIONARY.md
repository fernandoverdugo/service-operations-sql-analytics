# KPI Dictionary

This project treats KPI definitions as part of the analytical product rather than leaving business logic implicit in a dashboard.

| KPI | Definition | Why it matters |
| --- | --- | --- |
| Referral-to-intake conversion | Completed intakes divided by total referrals | Measures how effectively referrals move into formal service intake |
| Referral-to-service conversion | Referrals receiving at least one service event divided by total referrals | Measures end-to-end progression from referral to actual service delivery |
| Average referral-to-intake time | Mean calendar days from referral date to intake date among completed intakes | Monitors front-end access and intake responsiveness |
| Average referral-to-service time | Mean calendar days from referral date to first service date among served referrals | Measures overall speed of service access |
| Intake SLA rate | Share of completed intakes occurring within 5 days of referral | Tracks adherence to the simulated intake timeliness standard |
| Service SLA rate | Share of served referrals reaching first service within 14 days | Tracks timeliness among clients who ultimately receive service |
| No-show rate | No-show appointments divided by all scheduled appointments | Identifies appointment-access and engagement friction |
| Cancellation rate | Cancelled appointments divided by all scheduled appointments | Helps distinguish cancellations from no-shows and other attendance outcomes |
| Goals-met closure rate | Cases closed as Goals Met divided by cases with a recorded case outcome | Provides a simple outcome-oriented case-closure measure |
| Repeat-referral rate | Clients with at least two referrals divided by all clients | Measures repeated entry into the referral system |
| Multi-program rate | Clients referred to at least two programs divided by all clients | Indicates cross-program service utilization |
| Repeat-service rate | Clients with at least two service events divided by all clients | Measures continued service engagement |
| 3-month service conversion | Rolling three-month average of monthly referral-to-service conversion | Reduces month-to-month noise for operational monitoring |

## Reporting principles

- Conversion denominators are based on referrals, not only completed cases.
- Wait-time metrics are calculated only when the downstream event exists.
- SLA rates clearly identify the population to which the SLA applies.
- Cohort comparisons use only fully observed follow-up windows.
- Site/program rankings should be interpreted alongside volume, wait time, and appointment performance rather than as standalone quality scores.
- All values in this project are derived from deterministic synthetic data and are intended to demonstrate analytical workflow, not real program performance.
