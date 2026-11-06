# Milestone 1 — Operational Scorecard & Funnel

## Scope

Milestone 1 establishes the SQL-first operational analytics foundation of the project.

The synthetic dataset contains:

- **3,000 clients**
- **3,968 referrals**
- **3,384 cases**
- **6,783 appointments**
- **4,127 service events**
- **4 sites**
- **4 programs**
- **4 referral channels**

All data are synthetic and generated deterministically with seed 699.

## Executive scorecard

| KPI | Result |
| --- | ---: |
| Referral-to-intake rate | **85.3%** |
| Referral-to-service rate | **66.8%** |
| Average referral-to-intake time | **3.91 days** |
| Average referral-to-service time | **12.03 days** |
| Intake SLA rate among completed intakes | **70.0%** |
| Service SLA rate among served referrals | **75.0%** |
| Appointment no-show rate | **16.6%** |
| Appointment cancellation rate | **8.8%** |
| Goals-met closure rate | **58.1%** |

## Referral channel performance

| Channel | Referrals | Intake rate | Service rate | Avg. days to service |
| --- | ---: | ---: | ---: | ---: |
| Partner Referral | 1,633 | **90.2%** | **71.0%** | 12.21 |
| Self Referral | 1,146 | 80.7% | 65.3% | 11.75 |
| Walk-In | 494 | 87.7% | 64.4% | **11.43** |
| Hotline | 695 | **79.6%** | **61.3%** | 12.46 |

Partner referrals show the strongest conversion through service, while Hotline referrals have the lowest intake and service conversion.

Because the data are synthetic, these differences illustrate the analytical workflow rather than real-world program performance.

## Site/program observations

The strongest referral-to-service group is **Central / Benefits**, with a **71.5%** service conversion rate across 256 referrals.

The lowest is **West / Housing Support**, with a **59.2%** service conversion rate across 262 referrals.

The strongest first-service SLA performance is **North / Employment**, where **81.8%** of served referrals reach service within the 14-day SLA.

The highest observed no-show rate occurs for **South / Employment — Intake Follow-Up**, with a **20.4%** no-show rate across 196 appointments.

## Analyst value

Milestone 1 includes:

1. relational schema design;
2. multi-table SQL joins;
3. operational KPI definition;
4. referral-to-service funnel construction;
5. wait-time calculations;
6. SLA monitoring;
7. no-show and cancellation analysis;
8. site/program comparison;
9. referral-channel analysis;
10. automated data and output validation.

## Status

**Complete**

Milestone 1 is retained as the operational foundation for the completed project. Later layers add monthly trends, cohorts, ranked performance, dashboard marts, and stakeholder reporting.
