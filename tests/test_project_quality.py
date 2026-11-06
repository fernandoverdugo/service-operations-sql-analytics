import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from validate_project import markdown_paths


def test_markdown_paths_filters_external_links():
    text = """
[Local](docs/file.md)
![Figure](docs/figure.svg)
[Web](https://example.com)
[Anchor](#section)
"""
    assert markdown_paths(text) == [
        "docs/file.md",
        "docs/figure.svg",
    ]


def test_dashboard_metadata_schema():
    import json

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

    assert "executive_scorecard" in milestone1
    assert "referral_channels" in milestone1
    assert milestone1["provenance"]["seed"] == 699

    assert "latest_month" in milestone2
    assert "repeat_behavior" in milestone2
    assert "cohorts" in milestone2
    assert len(milestone2["top_overall_service_rate"]) == 3
    assert len(milestone2["bottom_overall_service_rate"]) == 3
    assert milestone2["provenance"]["seed"] == 699
