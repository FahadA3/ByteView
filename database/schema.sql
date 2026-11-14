-- UUID extension if needed in Supabase
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- NOTE:
-- Every Fernet token beings with 'gAAAAA', checking prevents plaintext PHI

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth_id UUID NOT NULL UNIQUE
            REFERENCES auth.users(id) ON DELETE RESTRICT,
    username VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL 
            CHECK (role IN ('Dentist', 'Dental Assistant', 'Developer')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Patients Table
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL CHECK (first_name LIKE 'gAAAAA%'), -- Fernet Encrypted
    last_name TEXT NOT NULL CHECK (last_name LIKE 'gAAAAA%'), -- Fernet Encrypted
    first_name_hash CHAR(64) NOT NULL CHECK (first_name_hash ~ '^[0-9a-f]{64}$'), -- Regex translates to "exactly 64 hex chars"
    last_name_hash CHAR(64) NOT NULL CHECK (last_name_hash ~ '^[0-9a-f]{64}$'),
    dob DATE NOT NULL CHECK (dob > DATE '1900-01-01'),
    phone TEXT CHECK (phone LIKE 'gAAAAA%'), -- Fernet Encrypted
    email TEXT CHECK (email LIKE 'gAAAAA%'), -- Fernet Encrypted
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Search by patient_id (primary), dob, first_name, last_name
CREATE INDEX patients_last_name_hash_idx ON patients (last_name_hash);
CREATE INDEX patients_first_name_hash_idx ON patients (first_name_hash);
CREATE INDEX patients_dob_idx ON patients (dob);

-- Staged_Edits Table (For Dentist Staging Queue)
CREATE TABLE staged_edits (
    edit_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    tooth_number INT CHECK (tooth_number BETWEEN 1 and 32),
    edit_payload JSONB NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Staged' 
                    CHECK (status IN ('Staged', 'Approved', 'Rejected')),
    reviewed_by INT REFERENCES users(id) ON DELETE RESTRICT,
    reviewed_at TIMESTAMPTZ,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

-- Each payload must be a non-empty object.
    CHECK (jsonb_typeof(edit_payload) = 'object'),
    CHECK (edit_payload <> '{}'::jsonb),
    CHECK (edit_payload - 'gum_decay' - 'symptom_notes' = '{}'::jsonb),

-- Only a decided edit will record who decided/when, while a staged edit will not.
    CHECK (
        (status = 'Staged' AND reviewed_by IS NULL AND reviewed_at IS NULL) OR
        (status <> 'Staged' AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL)
    ),

-- Nobody can approve their own edit.
    CHECK (reviewed_by <> user_id)
);

-- Partial index for only staged, faster queries for staged queue
CREATE INDEX staged_edits_queue_idx ON staged_edits (patient_id) WHERE status = 'Staged';

-- Tooth_Record Table (32-tooth visualizer data)
CREATE TABLE tooth_records (
    record_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE RESTRICT,
    tooth_number INT CHECK (tooth_number BETWEEN 1 AND 32),         -- NULL = whole mouth
    gum_decay NUMERIC(3, 1) CHECK (gum_decay BETWEEN 0.0 AND 10.0), -- NULL = not measured
    symptom_notes TEXT CHECK (symptom_notes LIKE 'gAAAAA%'),
    user_id INT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    edit_id INT UNIQUE REFERENCES staged_edits(edit_id) ON DELETE RESTRICT, -- NULL = dentist entered it directly
    start_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    change_date TIMESTAMPTZ,

-- Both should not be NULL, otherwise the record is empty.
    CHECK (gum_decay IS NOT NULL OR symptom_notes IS NOT NULL),
    CHECK (change_date IS NULL OR change_date >= start_date)
);

-- There should be at most one current version per tooth per patient. 0 will represent the whole mouth.
CREATE UNIQUE INDEX tooth_records_one_current_idx
    ON tooth_records (patient_id, COALESCE(tooth_number, 0))
    WHERE change_date IS NULL;

-- Timeline Dashboard: Index by patient_id, tooth_number, start_date
CREATE INDEX tooth_records_timeline_idx ON tooth_records (patient_id, tooth_number, start_date);

-- Audit Logs Table (Immutable HIPAA Compliance Trail)
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id) ON DELETE RESTRICT,
    user_id INT REFERENCES users(id) ON DELETE RESTRICT,
    record_id INT REFERENCES tooth_records(record_id) ON DELETE RESTRICT,
    edit_id INT REFERENCES staged_edits(edit_id) ON DELETE RESTRICT,
    action VARCHAR(50) NOT NULL
            CHECK (action IN ('LOGIN', 'LOGIN_FAILED', 'SEARCH', 'VIEW', 'CREATE', 'UPDATE', 'ARCHIVE', 'STAGE_EDIT', 'APPROVE_EDIT', 'REJECT_EDIT')),
    action_description TEXT NOT NULL, -- Should never use PHI values
    timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index rows first by patient_id, then by timestamp.
CREATE INDEX audit_logs_patient_idx ON audit_logs (patient_id, timestamp);
-- Index rows by user_id, then by timestamp.
CREATE INDEX audit_logs_user_idx ON audit_logs(user_id, timestamp);

-- Row Level Security: Blocks Supabase's public Data API from reading these tables.
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE staged_edits ENABLE ROW LEVEL SECURITY;
ALTER TABLE tooth_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;