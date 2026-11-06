from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_files_exist():
    required = [
        "README.md",
        "config/simulation.json",
        "docs/RESEARCH_DESIGN.md",
        "sql/01_schema.sql",
        "sql/02_core_kpis.sql",
        "sql/03_funnel.sql",
        "sql/04_appointment_performance.sql",
        "sql/05_sla_performance.sql",
    ]
    for path in required:
        assert (ROOT / path).exists()
