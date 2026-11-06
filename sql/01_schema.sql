CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    home_site TEXT NOT NULL
);

CREATE TABLE referrals (
    referral_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    referral_date TEXT NOT NULL,
    program TEXT NOT NULL,
    referral_channel TEXT NOT NULL,
    site TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE cases (
    case_id INTEGER PRIMARY KEY,
    referral_id INTEGER NOT NULL,
    intake_date TEXT,
    close_date TEXT,
    close_reason TEXT,
    FOREIGN KEY (referral_id) REFERENCES referrals(referral_id)
);

CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_type TEXT NOT NULL,
    appointment_status TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

CREATE TABLE service_events (
    service_event_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    service_date TEXT NOT NULL,
    service_type TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);
