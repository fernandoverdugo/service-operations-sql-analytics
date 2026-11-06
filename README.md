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

## Next milestone

Milestone 2 will add monthly trends, cohort analysis, repeat-service behavior, and window-function-based site/program rankings.
