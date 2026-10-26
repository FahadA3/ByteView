-- UUID extension if needed in Supabase
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Dentist', 'Dental Assistant', 'Developer')),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Patient Table
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL, -- Stored encrypted through fernet hopfully 
    last_name VARCHAR(255) NOT NULL,  -- Stored encrypted through fernet hopefully
    dob TIMESTAMP NOT NULL,
    phone VARCHAR(255),              -- Stored encrypted through fernet hopefully 
    email VARCHAR(255) UNIQUE,       -- Stored encrypted through fernet hopefully
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tooth Record Table (32-tooth visualizer data)
CREATE TABLE tooth_records (
    record_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    tooth_number INT NOT NULL CHECK (tooth_number BETWEEN 1 AND 32),
    gum_decay FLOAT DEFAULT 0.0 CHECK (gum_decay BETWEEN 0.0 AND 10.0),
    symptom_notes TEXT,
    start_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    change_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Staged_Edits Table (For Dentist Staging Queue)
CREATE TABLE staged_edits (
    edit_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    edit_payload TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Staged' CHECK (status IN ('Staged', 'Approved', 'Rejected')),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs Table (Immutable HIPAA Compliance Trail)
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id) ON DELETE SET NULL,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    action_description TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);