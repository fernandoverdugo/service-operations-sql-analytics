import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads(
    (ROOT / "config" / "simulation.json").read_text(encoding="utf-8")
)


def main():
    rng = np.random.default_rng(CONFIG["seed"])
    n_clients = CONFIG["clients"]
    start = pd.Timestamp(CONFIG["start_date"])
    end = start + pd.DateOffset(months=CONFIG["months"])

    client_ids = np.arange(1, n_clients + 1)
    home_sites = rng.choice(CONFIG["sites"], size=n_clients)

    clients = pd.DataFrame({
        "client_id": client_ids,
        "home_site": home_sites,
    })

    referral_records = []
    case_records = []
    appointment_records = []
    service_records = []

    referral_id = 1
    case_id = 1
    appointment_id = 1
    service_event_id = 1

    for client_id, home_site in zip(client_ids, home_sites):
        referral_count = int(rng.choice([1, 2, 3], p=[0.72, 0.23, 0.05]))

        for _ in range(referral_count):
            days_range = max(1, (end - start).days)
            referral_date = start + pd.Timedelta(
                days=int(rng.integers(0, days_range))
            )
            program = rng.choice(CONFIG["programs"])
            channel = rng.choice(
                CONFIG["channels"],
                p=[0.42, 0.28, 0.18, 0.12],
            )
            site = home_site if rng.random() < 0.82 else rng.choice(CONFIG["sites"])

            referral_records.append({
                "referral_id": referral_id,
                "client_id": int(client_id),
                "referral_date": referral_date.date().isoformat(),
                "program": program,
                "referral_channel": channel,
                "site": site,
            })

            intake_probability = {
                "Partner Referral": 0.90,
                "Self Referral": 0.82,
                "Hotline": 0.76,
                "Walk-In": 0.86,
            }[channel]

            if rng.random() < intake_probability:
                intake_delay = max(0, int(rng.normal(4.2, 3.5)))
                intake_date = referral_date + pd.Timedelta(days=intake_delay)

                service_probability = {
                    "Employment": 0.82,
                    "Benefits": 0.88,
                    "Health Navigation": 0.85,
                    "Housing Support": 0.74,
                }[program]

                case_records.append({
                    "case_id": case_id,
                    "referral_id": referral_id,
                    "intake_date": intake_date.date().isoformat(),
                    "close_date": None,
                    "close_reason": None,
                })

                appointment_count = int(
                    rng.choice([1, 2, 3, 4], p=[0.38, 0.34, 0.20, 0.08])
                )
                service_completed = False

                for appt_num in range(appointment_count):
                    appointment_date = intake_date + pd.Timedelta(
                        days=int(3 + appt_num * rng.integers(7, 20))
                    )
                    status = rng.choice(
                        ["Completed", "No Show", "Cancelled"],
                        p=[0.75, 0.16, 0.09],
                    )
                    appt_type = "Intake Follow-Up" if appt_num == 0 else "Follow-Up"

                    appointment_records.append({
                        "appointment_id": appointment_id,
                        "case_id": case_id,
                        "appointment_date": appointment_date.date().isoformat(),
                        "appointment_type": appt_type,
                        "appointment_status": status,
                    })

                    if status == "Completed" and rng.random() < service_probability:
                        service_date = appointment_date + pd.Timedelta(
                            days=int(rng.integers(0, 4))
                        )
                        service_records.append({
                            "service_event_id": service_event_id,
                            "case_id": case_id,
                            "service_date": service_date.date().isoformat(),
                            "service_type": program,
                        })
                        service_event_id += 1
                        service_completed = True

                    appointment_id += 1

                if service_completed:
                    close_reason = rng.choice(
                        ["Goals Met", "Transferred", "Client Requested"],
                        p=[0.74, 0.10, 0.16],
                    )
                    close_date = intake_date + pd.Timedelta(
                        days=int(rng.integers(30, 120))
                    )
                else:
                    close_reason = rng.choice(
                        ["Unable to Contact", "Client Requested", "Transferred"],
                        p=[0.64, 0.24, 0.12],
                    )
                    close_date = intake_date + pd.Timedelta(
                        days=int(rng.integers(14, 75))
                    )

                case_records[-1]["close_date"] = close_date.date().isoformat()
                case_records[-1]["close_reason"] = close_reason
                case_id += 1

            referral_id += 1

    raw = ROOT / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(clients).to_csv(raw / "clients.csv", index=False)
    pd.DataFrame(referral_records).to_csv(raw / "referrals.csv", index=False)
    pd.DataFrame(case_records).to_csv(raw / "cases.csv", index=False)
    pd.DataFrame(appointment_records).to_csv(raw / "appointments.csv", index=False)
    pd.DataFrame(service_records).to_csv(raw / "service_events.csv", index=False)

    print(json.dumps({
        "clients": len(clients),
        "referrals": len(referral_records),
        "cases": len(case_records),
        "appointments": len(appointment_records),
        "service_events": len(service_records),
    }, indent=2))


if __name__ == "__main__":
    main()
