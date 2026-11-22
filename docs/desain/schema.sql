PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS resep (
    id INTEGER PRIMARY KEY,
    nama TEXT NOT NULL CHECK (length(trim(nama)) > 0)
);

CREATE TABLE IF NOT EXISTS bahan (
    id INTEGER PRIMARY KEY,
    nama TEXT NOT NULL CHECK (length(trim(nama)) > 0)
);

CREATE TABLE IF NOT EXISTS resep_bahan (
    id INTEGER PRIMARY KEY,
    resep_id INTEGER NOT NULL REFERENCES resep(id),
    bahan_id INTEGER NOT NULL REFERENCES bahan(id),
    jumlah REAL CHECK (jumlah IS NULL OR jumlah > 0),
    satuan TEXT CHECK (satuan IS NULL OR length(trim(satuan)) > 0)
);

CREATE TABLE IF NOT EXISTS langkah_resep (
    id INTEGER PRIMARY KEY,
    resep_id INTEGER NOT NULL REFERENCES resep(id),
    urutan INTEGER NOT NULL CHECK (urutan > 0),
    instruksi TEXT NOT NULL CHECK (length(trim(instruksi)) > 0),
    UNIQUE (resep_id, urutan)
);

CREATE TABLE IF NOT EXISTS pengguna (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE
        CHECK (length(trim(username)) BETWEEN 3 AND 32),
    password_hash TEXT NOT NULL,
    peran TEXT NOT NULL CHECK (peran IN ('pengelola', 'pengguna'))
);

CREATE TABLE IF NOT EXISTS login_attempts (
    fingerprint TEXT PRIMARY KEY,
    window_started_at REAL NOT NULL,
    failures INTEGER NOT NULL CHECK (failures > 0)
);
