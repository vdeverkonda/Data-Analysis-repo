CREATE TABLE production_jobs (
    job_id TEXT PRIMARY KEY,
    date DATE,
    machine TEXT,
    shift TEXT,
    planned_units INTEGER,
    units_produced INTEGER,
    good_units INTEGER,
    scrap_units REAL,
    downtime_minutes REAL
);

CREATE TABLE inventory (
    date DATE,
    material TEXT,
    expected_qty INTEGER,
    actual_qty INTEGER,
    variance INTEGER
);

CREATE TABLE downtime_logs (
    date DATE,
    machine TEXT,
    shift TEXT,
    downtime_reason TEXT,
    minutes REAL
);
