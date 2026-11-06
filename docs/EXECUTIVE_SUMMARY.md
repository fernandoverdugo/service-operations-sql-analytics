# Executive Summary

## What this project demonstrates

This project simulates a multi-site public-service organization and shows how a Data Analyst can move from normalized operational tables to stakeholder-ready reporting.

It is intentionally SQL-first.

The project emphasizes:

- relational data modeling
- KPI definition
- funnel analysis
- wait-time and SLA reporting
- no-show and cancellation analysis
- cohort analysis
- repeat-service behavior
- SQL window functions
- dashboard marts
- stakeholder-facing visualization
- reproducible validation

All data are synthetic.

## Business problem

Service organizations need to understand where clients experience friction between referral and service delivery.

The central analytical question is:

> Where do clients experience delay or drop-off in the referral-to-service journey, and which operational patterns should managers address first?

## Synthetic service system

The final dataset contains:

- **3,000 clients**
- **3,968 referrals**
- **3,384 cases**
- **6,783 appointments**
- **4,127 service events**
- **4 sites**
- **4 programs**
- **4 referral channels**
- **18 monthly reporting periods**

## Core operational findings

| KPI | Result |
| --- | ---: |
| Referral-to-intake conversion | **85.3%** |
| Referral-to-service conversion | **66.8%** |
| Average referral-to-intake time | **3.91 days** |
| Average referral-to-service time | **12.03 days** |
| Service SLA among served referrals | **75.0%** |
| Appointment no-show rate | **16.6%** |
| Appointment cancellation rate | **8.8%** |
| Goals-met closure rate | **58.1%** |

## Referral-channel findings

Partner Referral has the strongest service conversion:

- 1,633 referrals
- 90.2% intake conversion
- 71.0% service conversion

Hotline has the lowest:

- 695 referrals
- 79.6% intake conversion
- 61.3% service conversion

These are synthetic differences used to demonstrate comparative operational analysis.

## Client journey and cohort analysis

Across 3,000 clients:

- **27.0%** have repeat referrals
- **20.9%** interact with multiple programs
- **38.6%** have repeat service events

Ninety-day repeat-referral cohorts are limited to fully observed cohort months so recent cohorts are not artificially depressed by right-censoring.

Across 15 eligible cohort months, observed repeat-referral rates range from **5.2% to 13.3%**.

## Ranked site/program performance

SQL window functions are used to rank site/program combinations.

Highest service-conversion combinations include:

1. Central / Benefits — **71.5%**
2. North / Benefits — **71.4%**
3. West / Benefits — **71.0%**

Lowest include:

- West / Housing Support — **59.2%**
- Central / Housing Support — **59.9%**
- Central / Employment — **62.0%**

## Management priorities

The analytical outputs point to four practical follow-up questions a manager could investigate in the synthetic scenario:

1. **Hotline conversion:** why does the Hotline channel have the lowest referral-to-service conversion at 61.3%?
2. **Housing Support performance:** why do West / Housing Support and Central / Housing Support rank at the bottom of site/program service conversion?
3. **Appointment friction:** what operational factors contribute to the 16.6% no-show rate?
4. **Trend stability:** does the latest 66.7% rolling three-month service-conversion rate indicate stable performance or an emerging change?

These are investigation priorities rather than causal conclusions. The project demonstrates how an analyst moves from KPI reporting to operational questions that can guide deeper review.

## SQL techniques demonstrated

The project includes practical examples of:

- multi-table joins
- common table expressions
- conditional aggregation
- correlated subqueries
- date arithmetic
- ROW_NUMBER()
- LEAD()
- LAG()
- DENSE_RANK()
- rolling window frames
- cohort construction
- right-censoring controls
- ranked operational scorecards

## Reporting layer

Three dedicated dashboard marts separate business logic from presentation:

1. executive KPI mart
2. monthly trend mart
3. site/program performance mart

These feed a concise stakeholder-facing HTML dashboard.

This architecture keeps KPI definitions in SQL rather than embedding them inside visualization code.

## Technical stack

**SQL · SQLite · Python · pandas · NumPy · pytest · GitHub Actions · HTML/CSS**

## Bottom line

The project demonstrates the end-to-end workflow expected of an operational Data Analyst:

**relational data → SQL analysis → validated KPIs → cohorts and rankings → dashboard marts → stakeholder reporting**

It complements the portfolio's research and predictive-modeling projects by emphasizing SQL, operational decision support, and business-facing communication.
