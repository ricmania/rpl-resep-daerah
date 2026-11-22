from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """Return the request-scoped SQLite connection with foreign keys enabled."""
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    database_path = Path(current_app.config["DATABASE"])
    schema_path = Path(current_app.config["SCHEMA"])
    database_path.parent.mkdir(parents=True, exist_ok=True)
    initialize = not database_path.exists() or database_path.stat().st_size == 0

    if not schema_path.is_file():
        raise FileNotFoundError(f"Skema SQLite tidak ditemukan: {schema_path}")

    connection = get_db()
    if initialize:
        schema = schema_path.read_text(encoding="utf-8")
        try:
            connection.executescript(f"BEGIN;\n{schema}\nCOMMIT;")
        except sqlite3.Error:
            connection.rollback()
            raise


def list_bahan() -> list[sqlite3.Row]:
    return get_db().execute(
        "SELECT id, nama FROM bahan ORDER BY nama COLLATE NOCASE, id"
    ).fetchall()


def list_resep() -> list[sqlite3.Row]:
    return get_db().execute(
        "SELECT id, nama FROM resep ORDER BY nama COLLATE NOCASE, id"
    ).fetchall()


def get_bahan(bahan_id: int) -> sqlite3.Row | None:
    return get_db().execute(
        "SELECT id, nama FROM bahan WHERE id = ?",
        (bahan_id,),
    ).fetchone()


def get_resep(resep_id: int) -> sqlite3.Row | None:
    return get_db().execute(
        "SELECT id, nama FROM resep WHERE id = ?",
        (resep_id,),
    ).fetchone()


def get_resep_detail(
    resep_id: int,
) -> tuple[sqlite3.Row, list[sqlite3.Row], list[sqlite3.Row]] | None:
    resep = get_resep(resep_id)
    if resep is None:
        return None

    connection = get_db()
    bahan = connection.execute(
        """
        SELECT b.nama AS bahan_nama, rb.jumlah, rb.satuan
        FROM resep_bahan AS rb
        JOIN bahan AS b ON b.id = rb.bahan_id
        WHERE rb.resep_id = ?
        ORDER BY rb.id
        """,
        (resep_id,),
    ).fetchall()
    langkah = connection.execute(
        """
        SELECT urutan, instruksi
        FROM langkah_resep
        WHERE resep_id = ?
        ORDER BY urutan
        """,
        (resep_id,),
    ).fetchall()
    return resep, bahan, langkah


def list_resep_bahan() -> list[sqlite3.Row]:
    return get_db().execute(
        """
        SELECT rb.id, rb.resep_id, r.nama AS resep_nama,
               rb.bahan_id, b.nama AS bahan_nama, rb.jumlah, rb.satuan
        FROM resep_bahan AS rb
        JOIN resep AS r ON r.id = rb.resep_id
        JOIN bahan AS b ON b.id = rb.bahan_id
        ORDER BY r.nama COLLATE NOCASE, b.nama COLLATE NOCASE, rb.id
        """
    ).fetchall()


def create_bahan(nama: str) -> int:
    connection = get_db()
    with connection:
        cursor = connection.execute(
            "INSERT INTO bahan (nama) VALUES (?)",
            (nama,),
        )
    return cursor.lastrowid


def update_bahan(bahan_id: int, nama: str) -> bool:
    connection = get_db()
    with connection:
        cursor = connection.execute(
            "UPDATE bahan SET nama = ? WHERE id = ?",
            (nama, bahan_id),
        )
    return cursor.rowcount == 1


def delete_bahan(bahan_id: int) -> bool:
    connection = get_db()
    with connection:
        cursor = connection.execute(
            "DELETE FROM bahan WHERE id = ?",
            (bahan_id,),
        )
    return cursor.rowcount == 1


def create_resep_bahan(
    resep_id: int,
    bahan_id: int,
    jumlah: float | None,
    satuan: str | None,
) -> int:
    connection = get_db()
    with connection:
        cursor = connection.execute(
            """
            INSERT INTO resep_bahan (resep_id, bahan_id, jumlah, satuan)
            VALUES (?, ?, ?, ?)
            """,
            (resep_id, bahan_id, jumlah, satuan),
        )
    return cursor.lastrowid


def create_resep(
    nama: str,
    bahan: list[tuple[int, float | None, str | None]],
    langkah: list[str],
) -> int:
    connection = get_db()
    with connection:
        cursor = connection.execute(
            "INSERT INTO resep (nama) VALUES (?)",
            (nama,),
        )
        resep_id = cursor.lastrowid
        connection.executemany(
            """
            INSERT INTO resep_bahan (resep_id, bahan_id, jumlah, satuan)
            VALUES (?, ?, ?, ?)
            """,
            [
                (resep_id, bahan_id, jumlah, satuan)
                for bahan_id, jumlah, satuan in bahan
            ],
        )
        connection.executemany(
            """
            INSERT INTO langkah_resep (resep_id, urutan, instruksi)
            VALUES (?, ?, ?)
            """,
            [
                (resep_id, urutan, instruksi)
                for urutan, instruksi in enumerate(langkah, start=1)
            ],
        )
    return resep_id
