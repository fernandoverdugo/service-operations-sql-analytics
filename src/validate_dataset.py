import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def assert_unique(frame, columns, label):
    if frame.duplicated(columns).any():
        raise RuntimeError(f"{label} contains duplicate keys.")


def main():
    clients = pd.read_csv(RAW / "clients.csv")
    referrals = pd.read_csv(RAW / "referrals.csv")
    cases = pd.read_csv(RAW / "cases.csv")
    appointments = pd.read_csv(RAW / "appointments.csv")
    service_events = pd.read_csv(RAW / "service_events.csv")

    profile = json.loads(
        (PROCESSED / "dataset_profile.json").read_text(
            encoding="utf-8"
        )
    )
    kpis = pd.read_csv(PROCESSED / "core_kpis.csv")
    funnel = pd.read_csv(PROCESSED / "funnel.csv")
    appointments_out = pd.read_csv(
        PROCESSED / "appointment_performance.csv"
    )
    sla = pd.read_csv(PROCESSED / "sla_performance.csv")
    executive = pd.read_csv(PROCESSED / "executive_scorecard.csv")
    channels = pd.read_csv(PROCESSED / "referral_channel_funnel.csv")
    summary = json.loads(
        (PROCESSED / "milestone1_summary.json").read_text(
            encoding="utf-8"
        )
    )
    trends = pd.read_csv(PROCESSED / "monthly_trends.csv")
    repeat = pd.read_csv(PROCESSED / "client_repeat_service.csv")
    cohorts = pd.read_csv(PROCESSED / "referral_cohorts.csv")
    rankings = pd.read_csv(PROCESSED / "site_program_rankings.csv")
    milestone2 = json.loads(
        (PROCESSED / "milestone2_summary.json").read_text(
            encoding="utf-8"
        )
    )

    assert_unique(clients, ["client_id"], "clients")
    assert_unique(referrals, ["referral_id"], "referrals")
    assert_unique(cases, ["case_id"], "cases")
    assert_unique(appointments, ["appointment_id"], "appointments")
    assert_unique(
        service_events,
        ["service_event_id"],
        "service_events",
    )

    if not referrals["client_id"].isin(clients["client_id"]).all():
        raise RuntimeError("Referrals contain unknown client IDs.")

    if not cases["referral_id"].isin(referrals["referral_id"]).all():
        raise RuntimeError("Cases contain unknown referral IDs.")

    if not appointments["case_id"].isin(cases["case_id"]).all():
        raise RuntimeError("Appointments contain unknown case IDs.")

    if not service_events["case_id"].isin(cases["case_id"]).all():
        raise RuntimeError("Service events contain unknown case IDs.")

    if profile["clients"] != len(clients):
        raise RuntimeError("Client count mismatch.")

    if profile["referrals"] != len(referrals):
        raise RuntimeError("Referral count mismatch.")

    expected_groups = (
        referrals[["site", "program"]]
        .drop_duplicates()
        .shape[0]
    )
    if len(kpis) != expected_groups:
        raise RuntimeError("Core KPI group count mismatch.")

    if len(funnel) != expected_groups:
        raise RuntimeError("Funnel group count mismatch.")

    if len(sla) != expected_groups:
        raise RuntimeError("SLA group count mismatch.")

    if appointments_out.empty:
        raise RuntimeError("Appointment performance output is empty.")

    if len(executive) != 1:
        raise RuntimeError("Executive scorecard should contain one row.")

    if len(channels) != profile["referral_channels"]:
        raise RuntimeError("Referral-channel funnel count mismatch.")

    if summary["executive_scorecard"]["referrals"] != len(referrals):
        raise RuntimeError("Milestone summary referral count mismatch.")

    if not funnel["referral_to_intake_rate"].between(0, 1).all():
        raise RuntimeError("Invalid referral-to-intake rate.")

    if not funnel["referral_to_service_rate"].between(0, 1).all():
        raise RuntimeError("Invalid referral-to-service rate.")

    if not sla["intake_sla_rate"].between(0, 1).all():
        raise RuntimeError("Invalid intake SLA rate.")

    if not sla["service_sla_rate"].between(0, 1).all():
        raise RuntimeError("Invalid service SLA rate.")

    if len(trends) != 18:
        raise RuntimeError("Expected 18 monthly referral cohorts.")

    if len(repeat) != len(clients):
        raise RuntimeError(
            "Repeat-service table should contain one row per client."
        )

    if not repeat["repeat_referral_flag"].isin([0, 1]).all():
        raise RuntimeError("Invalid repeat-referral flag.")

    max_referral_date = pd.to_datetime(
        referrals["referral_date"]
    ).max()
    latest_eligible_date = max_referral_date - pd.Timedelta(days=90)
    cohort_months = pd.PeriodIndex(
        cohorts["cohort_month"],
        freq="M",
    )
    latest_cohort_end = cohort_months.max().to_timestamp(how="end").normalize()
    if latest_cohort_end > latest_eligible_date.normalize():
        raise RuntimeError(
            "90-day cohort output includes a partially observed cohort month."
        )

    if len(cohorts) < 12:
        raise RuntimeError(
            "Unexpectedly few eligible referral cohort months."
        )

    if len(rankings) != expected_groups:
        raise RuntimeError("Site/program ranking group count mismatch.")

    if milestone2["monthly_periods"] != len(trends):
        raise RuntimeError("Milestone 2 monthly-period count mismatch.")

    print("Service operations validation passed.")


if __name__ == "__main__":
    main()
