# Milestone 2 — Trends, Cohorts & Ranked Performance

## Purpose

Milestone 2 extends the SQL-first analyst workflow beyond static KPIs.

The project now includes:

- monthly referral trends
- three-month rolling conversion rates
- month-over-month service-rate changes
- client-level repeat-referral behavior
- multi-program participation
- repeat-service behavior
- 90-day referral cohorts
- site/program ranking with window functions

## Monthly trends

The synthetic referral window contains **18 monthly periods**.

For June 2026:

| KPI | Result |
| --- | ---: |
| Referrals | **217** |
| Referral-to-intake rate | **83.9%** |
| Referral-to-service rate | **67.7%** |
| 3-month service conversion | **66.7%** |
| Average referral-to-service time | **12.34 days** |

The monthly trend query uses `LAG()` for month-over-month change and a rolling window for three-month service conversion.

## Repeat behavior

Across 3,000 clients:

- **811 clients** had at least two referrals (**27.0%**)
- **628 clients** were referred to at least two programs (**20.9%**)
- **1,157 clients** recorded at least two service events (**38.6%**)

These measures describe service-use patterns rather than client risk.

## 90-day referral cohorts

Repeat-referral cohorts are evaluated only when the entire cohort month has a complete 90-day follow-up window.

This avoids right-censoring recent cohorts.

There are **15 fully observed cohort months**.

The highest observed 90-day repeat-referral rate is:

- March 2025
- 203 clients
- 27 repeats within 90 days
- **13.3% repeat rate**

The lowest fully observed cohort is:

- October 2025
- 155 clients
- 8 repeats within 90 days
- **5.2% repeat rate**

Because all data are synthetic, these differences demonstrate cohort methodology rather than real-world client behavior.

## Site/program rankings

The ranking layer uses `DENSE_RANK()` to compare service conversion across site/program combinations.

Top three combinations:

| Rank | Site | Program | Service rate | Avg. days to service | No-show rate |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | Central | Benefits | **71.5%** | 11.49 | 16.5% |
| 2 | North | Benefits | **71.4%** | 11.52 | 15.2% |
| 3 | West | Benefits | **71.0%** | 12.07 | 18.8% |

Lowest three combinations:

| Rank | Site | Program | Service rate | Avg. days to service | No-show rate |
| ---: | --- | --- | ---: | ---: | ---: |
| 16 | West | Housing Support | **59.2%** | 12.20 | 16.7% |
| 15 | Central | Housing Support | **59.9%** | 12.53 | 17.5% |
| 14 | Central | Employment | **62.0%** | 12.59 | 17.4% |

## SQL techniques demonstrated

Milestone 2 adds clear examples of:

- `ROW_NUMBER()`
- `LEAD()`
- `LAG()`
- `DENSE_RANK()`
- rolling window frames
- conditional aggregation
- cohort construction
- right-censoring controls
- multi-table joins
- grouped operational comparisons

## Status

**Complete**

Milestone 2 feeds the completed dashboard marts and stakeholder-facing reporting layer documented in Milestone 3.
