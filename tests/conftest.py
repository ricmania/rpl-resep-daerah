from collections.abc import Iterator
import sqlite3
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "desain" / "schema.sql"


@pytest.fixture
def db(tmp_path: Path) -> Iterator[sqlite3.Connection]:
    db_path = tmp_path / "resep-test.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        yield connection
    finally:
        connection.close()


@pytest.fixture
def resep_id(db: sqlite3.Connection) -> int:
    cursor = db.execute("INSERT INTO resep (nama) VALUES (?)", ("Resep contoh",))
    return int(cursor.lastrowid)


@pytest.fixture
def bahan_id(db: sqlite3.Connection) -> int:
    cursor = db.execute("INSERT INTO bahan (nama) VALUES (?)", ("Bahan contoh",))
    return int(cursor.lastrowid)
