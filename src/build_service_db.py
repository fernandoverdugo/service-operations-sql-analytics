import json
import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
DB = PROCESSED / "service_operations.db"


def read_sql(path):
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    required = {
        "clients": RAW / "clients.csv",
        "referrals": RAW / "referrals.csv",
        "cases": RAW / "cases.csv",
        "appointments": RAW / "appointments.csv",
        "service_events": RAW / "service_events.csv",
    }

    missing = [str(path) for path in required.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing synthetic CSV files: " + ", ".join(missing)
        )

    frames = {
        name: pd.read_csv(path)
        for name, path in required.items()
    }

    PROCESSED.mkdir(parents=True, exist_ok=True)

    if DB.exists():
        DB.unlink()

    with sqlite3.connect(DB) as connection:
        connection.executescript(read_sql("sql/01_schema.sql"))

        for name, frame in frames.items():
            frame.to_sql(
                name,
                connection,
                if_exists="append",
                index=False,
            )

        outputs = {
            "core_kpis": pd.read_sql_query(
                read_sql("sql/02_core_kpis.sql"),
                connection,
            ),
            "funnel": pd.read_sql_query(
                read_sql("sql/03_funnel.sql"),
                connection,
            ),
            "appointment_performance": pd.read_sql_query(
                read_sql("sql/04_appointment_performance.sql"),
                connection,
            ),
            "sla_performance": pd.read_sql_query(
                read_sql("sql/05_sla_performance.sql"),
                connection,
            ),
            "executive_scorecard": pd.read_sql_query(
                read_sql("sql/06_executive_scorecard.sql"),
                connection,
            ),
            "referral_channel_funnel": pd.read_sql_query(
                read_sql("sql/07_referral_channel_funnel.sql"),
                connection,
            ),
            "monthly_trends": pd.read_sql_query(
                read_sql("sql/08_monthly_trends.sql"),
                connection,
            ),
            "client_repeat_service": pd.read_sql_query(
                read_sql("sql/09_client_repeat_service.sql"),
                connection,
            ),
            "referral_cohorts": pd.read_sql_query(
                read_sql("sql/10_referral_cohorts.sql"),
                connection,
            ),
            "site_program_rankings": pd.read_sql_query(
                read_sql("sql/11_site_program_rankings.sql"),
                connection,
            ),
            "dashboard_executive": pd.read_sql_query(
                read_sql("sql/12_executive_dashboard_mart.sql"),
                connection,
            ),
            "dashboard_monthly": pd.read_sql_query(
                read_sql("sql/13_monthly_dashboard_mart.sql"),
                connection,
            ),
            "dashboard_site_program": pd.read_sql_query(
                read_sql("sql/14_site_program_dashboard_mart.sql"),
                connection,
            ),
        }

    for name, frame in outputs.items():
        frame.to_csv(
            PROCESSED / f"{name}.csv",
            index=False,
        )

    profile = {
        "clients": int(len(frames["clients"])),
        "referrals": int(len(frames["referrals"])),
        "cases": int(len(frames["cases"])),
        "appointments": int(len(frames["appointments"])),
        "service_events": int(len(frames["service_events"])),
        "sites": int(frames["referrals"]["site"].nunique()),
        "programs": int(frames["referrals"]["program"].nunique()),
        "referral_channels": int(
            frames["referrals"]["referral_channel"].nunique()
        ),
    }

    (PROCESSED / "dataset_profile.json").write_text(
        json.dumps(profile, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
