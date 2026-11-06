import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
METADATA = ROOT / "data" / "metadata"
CONFIG = json.loads(
    (ROOT / "config" / "simulation.json").read_text(encoding="utf-8")
)


def write_summary(result, filename):
    payload = json.dumps(result, indent=2) + "\n"
    PROCESSED.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    (PROCESSED / filename).write_text(payload, encoding="utf-8")
    (METADATA / filename).write_text(payload, encoding="utf-8")


def main():
    executive = pd.read_csv(
        PROCESSED / "executive_scorecard.csv"
    ).iloc[0]
    kpis = pd.read_csv(PROCESSED / "core_kpis.csv")
    funnel = pd.read_csv(PROCESSED / "funnel.csv")
    appointments = pd.read_csv(
        PROCESSED / "appointment_performance.csv"
    )
    sla = pd.read_csv(PROCESSED / "sla_performance.csv")
    channels = pd.read_csv(
        PROCESSED / "referral_channel_funnel.csv"
    )

    site_program = (
        funnel.merge(
            kpis,
            on=["site", "program"],
            suffixes=("_funnel", "_kpi"),
        )
        .merge(
            sla,
            on=["site", "program"],
            suffixes=("", "_sla"),
        )
    )

    result = {
        "executive_scorecard": {
            key: (
                int(value)
                if key in {
                    "clients",
                    "referrals",
                    "intakes",
                    "referrals_served",
                    "appointments",
                }
                else float(value)
            )
            for key, value in executive.to_dict().items()
        },
        "best_referral_to_service_group": (
            site_program.sort_values(
                "referral_to_service_rate",
                ascending=False,
            )
            .head(1)[
                [
                    "site",
                    "program",
                    "referred",
                    "referral_to_service_rate",
                    "avg_days_referral_to_service",
                ]
            ]
            .to_dict(orient="records")[0]
        ),
        "lowest_referral_to_service_group": (
            site_program.sort_values(
                "referral_to_service_rate",
                ascending=True,
            )
            .head(1)[
                [
                    "site",
                    "program",
                    "referred",
                    "referral_to_service_rate",
                    "avg_days_referral_to_service",
                ]
            ]
            .to_dict(orient="records")[0]
        ),
        "best_service_sla_group": (
            sla.sort_values(
                "service_sla_rate",
                ascending=False,
            )
            .head(1)[
                [
                    "site",
                    "program",
                    "referrals",
                    "service_sla_rate",
                ]
            ]
            .to_dict(orient="records")[0]
        ),
        "highest_no_show_group": (
            appointments.sort_values(
                ["no_show_rate", "appointments"],
                ascending=[False, False],
            )
            .head(1)[
                [
                    "site",
                    "program",
                    "appointment_type",
                    "appointments",
                    "no_show_rate",
                ]
            ]
            .to_dict(orient="records")[0]
        ),
        "referral_channels": channels.to_dict(
            orient="records"
        ),
        "provenance": {
            "seed": int(CONFIG["seed"]),
            "note": (
                "Deterministic synthetic service-operations simulation; "
                "aggregate outputs only."
            ),
        },
    }

    write_summary(result, "milestone1_summary.json")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
