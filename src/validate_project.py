import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def markdown_paths(text):
    targets = re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", text)
    result = []
    for target in targets:
        target = target.strip()
        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("#")
            or target.startswith("mailto:")
        ):
            continue
        path = target.split("#", 1)[0]
        if path:
            result.append(path)
    return result


def validate_markdown_links():
    markdown_files = [ROOT / "README.md"] + sorted(
        (ROOT / "docs").glob("*.md")
    )
    missing = []

    for markdown in markdown_files:
        text = markdown.read_text(encoding="utf-8")
        for target in markdown_paths(text):
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                missing.append(
                    f"{markdown.relative_to(ROOT)} -> {target}"
                )

    if missing:
        raise RuntimeError(
            "Broken internal markdown links:\n"
            + "\n".join(missing)
        )


def validate_required_artifacts():
    required = [
        ".github/workflows/quality-checks.yml",
        "config/simulation.json",
        "data/metadata/milestone1_summary.json",
        "data/metadata/milestone2_summary.json",
        "docs/EXECUTIVE_SUMMARY.md",
        "docs/MILESTONE1_OPERATIONAL_SCORECARD.md",
        "docs/MILESTONE2_TRENDS_COHORTS.md",
        "docs/MILESTONE3_DASHBOARD.md",
        "docs/dashboard.html",
        "docs/figures/dashboard_preview.svg",
        "sql/01_schema.sql",
        "sql/02_core_kpis.sql",
        "sql/03_funnel.sql",
        "sql/04_appointment_performance.sql",
        "sql/05_sla_performance.sql",
        "sql/06_executive_scorecard.sql",
        "sql/07_referral_channel_funnel.sql",
        "sql/08_monthly_trends.sql",
        "sql/09_client_repeat_service.sql",
        "sql/10_referral_cohorts.sql",
        "sql/11_site_program_rankings.sql",
        "sql/12_executive_dashboard_mart.sql",
        "sql/13_monthly_dashboard_mart.sql",
        "sql/14_site_program_dashboard_mart.sql",
        "src/build_service_db.py",
        "src/build_dashboard.py",
        "src/validate_dashboard.py",
        "src/validate_dataset.py",
    ]
    missing = [
        path for path in required
        if not (ROOT / path).exists()
    ]
    if missing:
        raise RuntimeError(
            "Missing required project artifacts: "
            + ", ".join(missing)
        )


def validate_metadata():
    milestone1 = json.loads(
        (
            ROOT
            / "data"
            / "metadata"
            / "milestone1_summary.json"
        ).read_text(encoding="utf-8")
    )
    milestone2 = json.loads(
        (
            ROOT
            / "data"
            / "metadata"
            / "milestone2_summary.json"
        ).read_text(encoding="utf-8")
    )

    executive = milestone1["executive_scorecard"]

    if executive["clients"] != 3000:
        raise RuntimeError("Unexpected client count.")

    if executive["referrals"] != 3968:
        raise RuntimeError("Unexpected referral count.")

    if milestone2["monthly_periods"] != 18:
        raise RuntimeError("Unexpected monthly trend count.")

    if milestone2["cohorts"]["cohort_months"] != 15:
        raise RuntimeError("Unexpected eligible cohort count.")

    if len(milestone2["top_overall_service_rate"]) != 3:
        raise RuntimeError("Expected three top-ranked site/program groups.")

    if len(milestone2["bottom_overall_service_rate"]) != 3:
        raise RuntimeError("Expected three bottom-ranked site/program groups.")

    if milestone1["provenance"]["seed"] != 699:
        raise RuntimeError("Unexpected Milestone 1 simulation seed.")

    if milestone2["provenance"]["seed"] != 699:
        raise RuntimeError("Unexpected Milestone 2 simulation seed.")


def main():
    validate_required_artifacts()
    validate_metadata()
    validate_markdown_links()
    print("Project integrity validation passed.")


if __name__ == "__main__":
    main()
