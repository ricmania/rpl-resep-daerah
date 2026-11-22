import sqlite3

import pytest


@pytest.mark.parametrize(
    "nama",
    ["Sayur bening", "Rendang"],
)
def test_nama_resep_valid_dapat_disimpan(db: sqlite3.Connection, nama: str) -> None:
    db.execute("INSERT INTO resep (nama) VALUES (?)", (nama,))
    assert db.execute("SELECT nama FROM resep").fetchone() == (nama,)


@pytest.mark.parametrize("nama", ["", "   ", None, sqlite3.Binary(b"Resep")])
def test_nama_resep_kosong_atau_bukan_teks_ditolak(
    db: sqlite3.Connection, nama: object
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO resep (nama) VALUES (?)", (nama,))


def test_nama_bahan_valid_dapat_disimpan(db: sqlite3.Connection) -> None:
    db.execute("INSERT INTO bahan (nama) VALUES (?)", ("Bayam",))
    assert db.execute("SELECT nama FROM bahan").fetchone() == ("Bayam",)


@pytest.mark.parametrize(
    "nama",
    ["", "   ", None, sqlite3.Binary(b"Bahan")],
)
def test_nama_bahan_kosong_atau_bukan_teks_ditolak(
    db: sqlite3.Connection, nama: object
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO bahan (nama) VALUES (?)", (nama,))


@pytest.mark.parametrize(
    ("jumlah", "diterima"),
    [
        (None, True),
        (0.01, True),
        (0, False),
        (-0.01, False),
        ("abc", False),
    ],
)
def test_jumlah_bahan_mengikuti_batas_skema(
    db: sqlite3.Connection,
    resep_id: int,
    bahan_id: int,
    jumlah: object,
    diterima: bool,
) -> None:
    statement = (
        "INSERT INTO resep_bahan (resep_id, bahan_id, jumlah) VALUES (?, ?, ?)"
    )
    if diterima:
        db.execute(statement, (resep_id, bahan_id, jumlah))
        assert db.execute("SELECT jumlah FROM resep_bahan").fetchone() is not None
    else:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(statement, (resep_id, bahan_id, jumlah))


@pytest.mark.parametrize(
    ("satuan", "diterima"),
    [
        (None, True),
        ("ikat", True),
        ("", False),
        ("   ", False),
        (sqlite3.Binary(b"ikat"), False),
    ],
)
def test_satuan_opsional_tetap_bertipe_teks(
    db: sqlite3.Connection,
    resep_id: int,
    bahan_id: int,
    satuan: object,
    diterima: bool,
) -> None:
    statement = (
        "INSERT INTO resep_bahan (resep_id, bahan_id, satuan) VALUES (?, ?, ?)"
    )
    if diterima:
        db.execute(statement, (resep_id, bahan_id, satuan))
        assert db.execute("SELECT satuan FROM resep_bahan").fetchone() is not None
    else:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(statement, (resep_id, bahan_id, satuan))


@pytest.mark.parametrize(
    ("urutan", "diterima"),
    [
        (1, True),
        (0, False),
        (-1, False),
        (1.5, False),
        ("abc", False),
    ],
)
def test_urutan_langkah_adalah_bilangan_bulat_positif(
    db: sqlite3.Connection,
    resep_id: int,
    urutan: object,
    diterima: bool,
) -> None:
    statement = (
        "INSERT INTO langkah_resep (resep_id, urutan, instruksi) VALUES (?, ?, ?)"
    )
    if diterima:
        db.execute(statement, (resep_id, urutan, "Masak hingga matang"))
        assert db.execute("SELECT urutan FROM langkah_resep").fetchone() == (urutan,)
    else:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(statement, (resep_id, urutan, "Masak hingga matang"))


@pytest.mark.parametrize(
    "instruksi",
    ["", "   ", sqlite3.Binary(b"masak")],
)
def test_instruksi_kosong_atau_bukan_teks_ditolak(
    db: sqlite3.Connection, resep_id: int, instruksi: object
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO langkah_resep (resep_id, urutan, instruksi) "
            "VALUES (?, 1, ?)",
            (resep_id, instruksi),
        )


def test_fk_bahan_tidak_dapat_menunjuk_baris_yang_tidak_ada(
    db: sqlite3.Connection, resep_id: int
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO resep_bahan (resep_id, bahan_id) VALUES (?, 999)",
            (resep_id,),
        )


def test_dua_langkah_tidak_dapat_memakai_urutan_yang_sama(
    db: sqlite3.Connection, resep_id: int
) -> None:
    db.execute(
        "INSERT INTO langkah_resep (resep_id, urutan, instruksi) VALUES (?, 1, ?)",
        (resep_id, "Potong bahan"),
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO langkah_resep (resep_id, urutan, instruksi) "
            "VALUES (?, 1, ?)",
            (resep_id, "Masak bahan"),
        )


def test_fk_resep_tidak_dapat_menunjuk_baris_yang_tidak_ada(
    db: sqlite3.Connection,
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO langkah_resep (resep_id, urutan, instruksi) "
            "VALUES (999, 1, ?)",
            ("Masak hingga matang",),
        )
