import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"
DOCS = ROOT / "docs"


def pct(value):
    return f"{value * 100:.1f}%"


def bar(value, maximum=1.0):
    width = max(0.0, min(100.0, value / maximum * 100))
    return f'<div class="bar"><span style="width:{width:.1f}%"></span></div>'


def main():
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

    executive = milestone1["executive_scorecard"]
    channels = milestone1["referral_channels"]
    repeat = milestone2["repeat_behavior"]
    top = milestone2["top_overall_service_rate"]
    bottom = milestone2["bottom_overall_service_rate"]
    latest = milestone2["latest_month"]

    channel_rows = "".join(
        f"""
        <tr>
          <td>{row["referral_channel"]}</td>
          <td>{row["referrals"]:,}</td>
          <td>{pct(row["referral_to_intake_rate"])}</td>
          <td>{pct(row["referral_to_service_rate"])}</td>
          <td>{row["avg_days_referral_to_service"]:.2f}</td>
        </tr>
        """
        for row in channels
    )

    ranking_rows = "".join(
        f"""
        <tr>
          <td>{row["overall_service_rate_rank"]}</td>
          <td>{row["site"]}</td>
          <td>{row["program"]}</td>
          <td>{pct(row["service_rate"])}</td>
          <td>{row["avg_days_to_service"]:.2f}</td>
          <td>{pct(row["no_show_rate"])}</td>
        </tr>
        """
        for row in top + bottom
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Service Operations Dashboard</title>
<style>
:root {{
  --bg:#f6f7f9;
  --card:#ffffff;
  --text:#17202a;
  --muted:#667085;
  --line:#e4e7ec;
  --accent:#2457d6;
  --accent2:#5b8def;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0;
  font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  background:var(--bg);
  color:var(--text);
}}
main {{ max-width:1180px; margin:0 auto; padding:40px 24px 64px; }}
h1 {{ margin:0; font-size:34px; }}
.subtitle {{ color:var(--muted); margin:8px 0 28px; }}
.grid {{ display:grid; gap:16px; }}
.kpis {{ grid-template-columns:repeat(4,1fr); }}
.card {{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:14px;
  padding:20px;
  box-shadow:0 1px 2px rgba(16,24,40,.04);
}}
.kpi-label {{ color:var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.04em; }}
.kpi-value {{ font-size:30px; font-weight:700; margin-top:6px; }}
.section {{ margin-top:22px; }}
.two {{ grid-template-columns:1.1fr .9fr; }}
h2 {{ margin:0 0 16px; font-size:20px; }}
.funnel-row {{ margin:16px 0; }}
.funnel-head {{ display:flex; justify-content:space-between; margin-bottom:7px; }}
.bar {{ height:12px; background:#edf0f5; border-radius:999px; overflow:hidden; }}
.bar span {{ display:block; height:100%; background:linear-gradient(90deg,var(--accent),var(--accent2)); }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ padding:11px 9px; border-bottom:1px solid var(--line); text-align:left; }}
th {{ color:var(--muted); font-weight:600; }}
.note {{ color:var(--muted); font-size:13px; line-height:1.5; }}
.metric-list {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.metric {{
  padding:14px;
  border:1px solid var(--line);
  border-radius:10px;
}}
.metric strong {{ display:block; font-size:23px; margin-top:4px; }}
@media (max-width:850px) {{
  .kpis, .two {{ grid-template-columns:1fr 1fr; }}
}}
@media (max-width:580px) {{
  .kpis, .two, .metric-list {{ grid-template-columns:1fr; }}
  main {{ padding:28px 16px 48px; }}
}}
</style>
</head>
<body>
<main>
  <h1>Service Operations & Client Journey</h1>
  <p class="subtitle">Synthetic operational dashboard • 18-month referral window • SQL-first analytical workflow</p>

  <div class="grid kpis">
    <div class="card">
      <div class="kpi-label">Referrals</div>
      <div class="kpi-value">{executive["referrals"]:,}</div>
    </div>
    <div class="card">
      <div class="kpi-label">Referral → Intake</div>
      <div class="kpi-value">{pct(executive["referral_to_intake_rate"])}</div>
    </div>
    <div class="card">
      <div class="kpi-label">Referral → Service</div>
      <div class="kpi-value">{pct(executive["referral_to_service_rate"])}</div>
    </div>
    <div class="card">
      <div class="kpi-label">Avg. Days to Service</div>
      <div class="kpi-value">{executive["avg_days_referral_to_service"]:.2f}</div>
    </div>
  </div>

  <div class="grid two section">
    <section class="card">
      <h2>Referral funnel</h2>
      <div class="funnel-row">
        <div class="funnel-head"><span>Referred</span><strong>{executive["referrals"]:,}</strong></div>
        {bar(1.0)}
      </div>
      <div class="funnel-row">
        <div class="funnel-head"><span>Completed intake</span><strong>{executive["intakes"]:,} · {pct(executive["referral_to_intake_rate"])}</strong></div>
        {bar(executive["referral_to_intake_rate"])}
      </div>
      <div class="funnel-row">
        <div class="funnel-head"><span>Received service</span><strong>{executive["referrals_served"]:,} · {pct(executive["referral_to_service_rate"])}</strong></div>
        {bar(executive["referral_to_service_rate"])}
      </div>
      <p class="note">Conversion is calculated from referral records, not from completed cases only.</p>
    </section>

    <section class="card">
      <h2>Operational quality</h2>
      <div class="metric-list">
        <div class="metric"><span class="note">Service SLA among served</span><strong>{pct(executive["service_sla_rate_among_served"])}</strong></div>
        <div class="metric"><span class="note">No-show rate</span><strong>{pct(executive["no_show_rate"])}</strong></div>
        <div class="metric"><span class="note">Cancellation rate</span><strong>{pct(executive["cancellation_rate"])}</strong></div>
        <div class="metric"><span class="note">Goals-met closure</span><strong>{pct(executive["goals_met_closure_rate"])}</strong></div>
      </div>
    </section>
  </div>

  <section class="card section">
    <h2>Referral channel performance</h2>
    <table>
      <thead><tr><th>Channel</th><th>Referrals</th><th>Intake rate</th><th>Service rate</th><th>Avg. days to service</th></tr></thead>
      <tbody>{channel_rows}</tbody>
    </table>
  </section>

  <div class="grid two section">
    <section class="card">
      <h2>Repeat-service behavior</h2>
      <div class="metric-list">
        <div class="metric"><span class="note">Repeat referrals</span><strong>{pct(repeat["repeat_referral_rate"])}</strong></div>
        <div class="metric"><span class="note">Multi-program clients</span><strong>{pct(repeat["multi_program_rate"])}</strong></div>
        <div class="metric"><span class="note">Repeat service</span><strong>{pct(repeat["repeat_service_rate"])}</strong></div>
        <div class="metric"><span class="note">Latest 3-mo service conversion</span><strong>{pct(latest["referral_to_service_rate_3m"])}</strong></div>
      </div>
    </section>

    <section class="card">
      <h2>Latest month</h2>
      <div class="metric-list">
        <div class="metric"><span class="note">Month</span><strong>{latest["referral_month"]}</strong></div>
        <div class="metric"><span class="note">Referrals</span><strong>{latest["referrals"]:,}</strong></div>
        <div class="metric"><span class="note">Service conversion</span><strong>{pct(latest["referral_to_service_rate"])}</strong></div>
        <div class="metric"><span class="note">Avg. days to service</span><strong>{latest["avg_days_referral_to_service"]:.2f}</strong></div>
      </div>
    </section>
  </div>

  <section class="card section">
    <h2>Management actions</h2>
    <div class="metric-list">
      <div class="metric"><span class="note">Investigate referral-channel drop-off</span><strong>Hotline</strong><span class="note">Lowest referral-to-service conversion at 61.3%.</span></div>
      <div class="metric"><span class="note">Review lower-performing site/program combinations</span><strong>Housing Support</strong><span class="note">West and Central rank at the bottom of service conversion.</span></div>
      <div class="metric"><span class="note">Monitor appointment friction</span><strong>{pct(executive["no_show_rate"])}</strong><span class="note">No-show rate warrants routine operational monitoring.</span></div>
      <div class="metric"><span class="note">Track trend stability</span><strong>{pct(latest["referral_to_service_rate_3m"])}</strong><span class="note">Latest rolling 3-month service conversion provides a steadier management signal.</span></div>
    </div>
    <p class="note">These are analytical follow-up priorities derived from the synthetic scenario, not recommendations for a real organization.</p>
  </section>

  <section class="card section">
    <h2>Selected site/program rankings</h2>
    <table>
      <thead><tr><th>Rank</th><th>Site</th><th>Program</th><th>Service rate</th><th>Avg. days</th><th>No-show rate</th></tr></thead>
      <tbody>{ranking_rows}</tbody>
    </table>
    <p class="note">Shows the top three and bottom three combinations by referral-to-service conversion.</p>
  </section>

  <p class="note section">
    All data are synthetic. This dashboard demonstrates operational analytics and stakeholder reporting, not real program performance.
    <br><br>
    <a href="https://github.com/fernandoverdugo/service-operations-sql-analytics">View repository</a>
    · <a href="https://github.com/fernandoverdugo/service-operations-sql-analytics/blob/main/docs/EXECUTIVE_SUMMARY.md">Executive summary</a>
    · <a href="https://github.com/fernandoverdugo/service-operations-sql-analytics/blob/main/docs/KPI_DICTIONARY.md">KPI dictionary</a>
  </p>
</main>
</body>
</html>
"""

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "dashboard.html").write_text(
        html,
        encoding="utf-8",
    )
    print("Dashboard generated: docs/dashboard.html")


if __name__ == "__main__":
    main()
