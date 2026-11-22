import sqlite3
from pathlib import Path


def test_resep_valid_disimpan_di_basis_data_sementara(
    db: sqlite3.Connection, tmp_path: Path
) -> None:
    database_path = Path(db.execute("PRAGMA database_list").fetchone()[2])

    db.execute("INSERT INTO resep (nama) VALUES (?)", ("Sayur contoh",))

    row = db.execute("SELECT nama FROM resep").fetchone()
    assert row == ("Sayur contoh",)
    assert database_path.parent == tmp_path
