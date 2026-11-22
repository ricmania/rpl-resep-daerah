PRAGMA foreign_keys = ON;

CREATE TABLE resep (
    id INTEGER PRIMARY KEY,
    nama TEXT NOT NULL CHECK (
        typeof(nama) = 'text' AND length(trim(nama)) > 0
    )
);

CREATE TABLE bahan (
    id INTEGER PRIMARY KEY,
    nama TEXT NOT NULL CHECK (
        typeof(nama) = 'text' AND length(trim(nama)) > 0
    )
);

CREATE TABLE resep_bahan (
    id INTEGER PRIMARY KEY,
    resep_id INTEGER NOT NULL REFERENCES resep(id),
    bahan_id INTEGER NOT NULL REFERENCES bahan(id),
    jumlah REAL CHECK (
        jumlah IS NULL
        OR (typeof(jumlah) IN ('integer', 'real') AND jumlah > 0)
    ),
    satuan TEXT CHECK (
        satuan IS NULL
        OR (typeof(satuan) = 'text' AND length(trim(satuan)) > 0)
    )
);

CREATE TABLE langkah_resep (
    id INTEGER PRIMARY KEY,
    resep_id INTEGER NOT NULL REFERENCES resep(id),
    urutan INTEGER NOT NULL CHECK (typeof(urutan) = 'integer' AND urutan > 0),
    instruksi TEXT NOT NULL CHECK (
        typeof(instruksi) = 'text' AND length(trim(instruksi)) > 0
    ),
    UNIQUE (resep_id, urutan)
);
