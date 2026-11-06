# Milestone 3 — Dashboard Marts & Stakeholder Reporting

## Purpose

Milestone 3 converts the validated SQL analysis into a management-facing reporting layer.

The goal is not to add more modeling. It is to translate normalized operational tables into clean reporting marts and a concise dashboard.

## Dashboard marts

The project now includes three dedicated SQL marts.

### Executive dashboard mart

`sql/12_executive_dashboard_mart.sql`

One-row operational summary with:

- total referrals
- completed intakes
- referrals served
- referral-to-intake conversion
- referral-to-service conversion
- average days to service
- service SLA performance
- no-show rate
- cancellation rate

### Monthly dashboard mart

`sql/13_monthly_dashboard_mart.sql`

Monthly referral reporting with:

- referrals
- intakes
- referrals served
- conversion rates
- three-month rolling service conversion
- average days to service

### Site/program dashboard mart

`sql/14_site_program_dashboard_mart.sql`

Site/program performance with:

- referral volume
- intake conversion
- service conversion
- average days to service
- appointment volume
- no-show rate
- cancellation rate
- ranked service conversion

These marts isolate presentation-ready metrics from the underlying normalized transaction tables.

## Stakeholder dashboard

The repository includes a lightweight HTML dashboard generated from the validated analytical summaries.

It presents:

- headline operational KPIs
- referral funnel
- service SLA performance
- no-show and cancellation rates
- referral-channel conversion
- repeat-referral and repeat-service behavior
- latest-month performance
- top and bottom site/program combinations

The dashboard is intentionally concise. It is meant to answer the first questions a program manager or operations leader would ask rather than expose every available metric.

## Dashboard headline metrics

| KPI | Result |
| --- | ---: |
| Referrals | **3,968** |
| Referral-to-intake conversion | **85.3%** |
| Referral-to-service conversion | **66.8%** |
| Average days to service | **12.03** |
| Service SLA among served referrals | **75.0%** |
| No-show rate | **16.6%** |
| Cancellation rate | **8.8%** |
| Repeat-referral rate | **27.0%** |
| Repeat-service rate | **38.6%** |

## Reporting architecture

```text
normalized operational tables
        ↓
SQL analytical queries
        ↓
validated dashboard marts
        ↓
committed aggregate summaries
        ↓
stakeholder HTML dashboard
```

This keeps business logic in SQL rather than hiding KPI definitions inside the visualization layer.

## Quality controls

The build pipeline validates:

- one-row executive mart
- 18 monthly trend rows
- 16 site/program combinations
- valid rate ranges
- dashboard presence
- dashboard preview presence
- consistency between committed dashboard values and validated metadata

The dashboard generator remains available in `src/build_dashboard.py`.

## Status

**Complete**

The project now connects the full workflow from relational data to SQL analysis to management-facing reporting.

The documentation and quality-control pass is complete. The repository includes concise executive documentation, reproducibility instructions, project-integrity validation, licensing, and automated GitHub Actions checks that rebuild and validate the analytical workflow.
