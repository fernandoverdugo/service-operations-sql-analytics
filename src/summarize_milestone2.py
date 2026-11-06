import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def main():
    trends = pd.read_csv(PROCESSED / "monthly_trends.csv")
    repeat = pd.read_csv(PROCESSED / "client_repeat_service.csv")
    cohorts = pd.read_csv(PROCESSED / "referral_cohorts.csv")
    rankings = pd.read_csv(PROCESSED / "site_program_rankings.csv")

    latest = trends.iloc[-1]

    result = {
        "monthly_periods": int(len(trends)),
        "latest_month": {
            "referral_month": str(latest["referral_month"]),
            "referrals": int(latest["referrals"]),
            "referral_to_intake_rate": float(
                latest["referral_to_intake_rate"]
            ),
            "referral_to_service_rate": float(
                latest["referral_to_service_rate"]
            ),
            "referral_to_service_rate_3m": float(
                latest["referral_to_service_rate_3m"]
            ),
            "avg_days_referral_to_service": float(
                latest["avg_days_referral_to_service"]
            ),
        },
        "repeat_behavior": {
            "clients": int(len(repeat)),
            "repeat_referral_clients": int(
                repeat["repeat_referral_flag"].sum()
            ),
            "repeat_referral_rate": float(
                repeat["repeat_referral_flag"].mean()
            ),
            "multi_program_clients": int(
                repeat["multi_program_flag"].sum()
            ),
            "multi_program_rate": float(
                repeat["multi_program_flag"].mean()
            ),
            "repeat_service_clients": int(
                repeat["repeat_service_flag"].sum()
            ),
            "repeat_service_rate": float(
                repeat["repeat_service_flag"].mean()
            ),
        },
        "cohorts": {
            "cohort_months": int(len(cohorts)),
            "highest_repeat_90_day_cohort": (
                cohorts.sort_values(
                    "repeat_within_90_days_rate",
                    ascending=False,
                )
                .head(1)
                .to_dict(orient="records")[0]
            ),
            "lowest_repeat_90_day_cohort": (
                cohorts.sort_values(
                    "repeat_within_90_days_rate",
                    ascending=True,
                )
                .head(1)
                .to_dict(orient="records")[0]
            ),
        },
        "rankings": {
            "top_overall_service_rate": (
                rankings.sort_values(
                    "overall_service_rate_rank"
                )
                .head(5)[
                    [
                        "site",
                        "program",
                        "service_rate",
                        "avg_days_to_service",
                        "no_show_rate",
                        "overall_service_rate_rank",
                    ]
                ]
                .to_dict(orient="records")
            ),
            "bottom_overall_service_rate": (
                rankings.sort_values(
                    "overall_service_rate_rank",
                    ascending=False,
                )
                .head(5)[
                    [
                        "site",
                        "program",
                        "service_rate",
                        "avg_days_to_service",
                        "no_show_rate",
                        "overall_service_rate_rank",
                    ]
                ]
                .to_dict(orient="records")
            ),
        },
    }

    (PROCESSED / "milestone2_summary.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
