import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"
DASHBOARD = ROOT / "docs" / "dashboard.html"
PREVIEW = ROOT / "docs" / "figures" / "dashboard_preview.svg"


def pct(value):
    return f"{value * 100:.1f}%"


def main():
    if not DASHBOARD.exists():
        raise RuntimeError("Dashboard HTML is missing.")

    if not PREVIEW.exists():
        raise RuntimeError("Dashboard preview figure is missing.")

    milestone1 = json.loads(
        (METADATA / "milestone1_summary.json").read_text(
            encoding="utf-8"
        )
    )
    milestone2 = json.loads(
        (METADATA / "milestone2_summary.json").read_text(
            encoding="utf-8"
        )
    )

    html = DASHBOARD.read_text(encoding="utf-8")

    executive = milestone1["executive_scorecard"]
    repeat = milestone2["repeat_behavior"]
    latest = milestone2["latest_month"]

    expected = [
        f'{executive["referrals"]:,}',
        pct(executive["referral_to_intake_rate"]),
        pct(executive["referral_to_service_rate"]),
        f'{executive["avg_days_referral_to_service"]:.2f}',
        pct(executive["service_sla_rate_among_served"]),
        pct(executive["no_show_rate"]),
        pct(executive["cancellation_rate"]),
        pct(executive["goals_met_closure_rate"]),
        pct(repeat["repeat_referral_rate"]),
        pct(repeat["multi_program_rate"]),
        pct(repeat["repeat_service_rate"]),
        str(latest["referral_month"]),
        pct(latest["referral_to_service_rate"]),
    ]

    missing = [value for value in expected if value not in html]
    if missing:
        raise RuntimeError(
            "Dashboard is missing expected KPI values: "
            + ", ".join(missing)
        )

    for channel in milestone1["referral_channels"]:
        if channel["referral_channel"] not in html:
            raise RuntimeError(
                "Dashboard is missing referral channel "
                + channel["referral_channel"]
            )

    print("Dashboard semantic validation passed.")


if __name__ == "__main__":
    main()
