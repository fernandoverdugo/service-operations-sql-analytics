# Service Operations & Client Journey Analytics

A SQL-first portfolio project that simulates a multi-site public-service organization and analyzes how clients move from referral through intake, appointment, service delivery, and case closure.

## Core question

Where do clients experience delays or drop-off in the service journey, and which operational patterns should managers address first?

## Why this project

This project is intentionally designed around the work expected of a Data Analyst:

- relational data modeling
- SQL joins
- KPI definition
- funnel analysis
- cohorts
- wait-time and SLA reporting
- no-show analysis
- repeat-service behavior
- window functions
- site and program comparisons
- dashboard-ready marts
- executive recommendations

Machine learning is not the centerpiece. The goal is to demonstrate strong operational analytics and stakeholder-facing SQL work.

## Synthetic scenario

A public-service organization operates multiple sites and programs. Clients may be referred, complete intake, schedule appointments, receive services, return for follow-up, and eventually close their cases.

All data are synthetic. No real client, provider, program, or case information is used.

## Milestone 1 — operational scorecard and funnel

**Complete**

Validated synthetic dataset:

| Measure | Result |
| --- | ---: |
| Clients | **3,000** |
| Referrals | **3,968** |
| Cases | **3,384** |
| Appointments | **6,783** |
| Service events | **4,127** |

Key operational results:

- referral-to-intake rate: **85.3%**
- referral-to-service rate: **66.8%**
- average referral-to-service time: **12.03 days**
- no-show rate: **16.6%**
- service SLA rate among served referrals: **75.0%**

[Read the Milestone 1 findings](docs/MILESTONE1_OPERATIONAL_SCORECARD.md)

## Milestone 2 — trends, cohorts, and ranked performance

**Complete**

The SQL layer now includes:

- 18 monthly referral trend periods
- 3-month rolling service-conversion rates
- month-over-month change with `LAG()`
- client-level repeat-referral and repeat-service behavior
- fully observed 90-day referral cohorts
- `ROW_NUMBER()`, `LEAD()`, and `DENSE_RANK()`
- ranked site/program performance

Selected results:

- repeat-referral clients: **27.0%**
- multi-program clients: **20.9%**
- repeat-service clients: **38.6%**
- highest fully observed 90-day repeat cohort: **13.3%**
- lowest fully observed 90-day repeat cohort: **5.2%**

[Read the Milestone 2 findings](docs/MILESTONE2_TRENDS_COHORTS.md)

## Next milestone

Milestone 3 will convert the validated SQL outputs into dashboard-ready analytical marts and a stakeholder-facing visualization layer.
