import sqlite3
from pathlib import Path


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "desain" / "schema.sql"
)


def main() -> None:
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute("INSERT INTO resep (id, nama) VALUES (1, 'Sayur bening')")
        connection.execute("INSERT INTO bahan (id, nama) VALUES (1, 'Bayam')")
        connection.execute(
            "INSERT INTO resep_bahan (resep_id, bahan_id, jumlah, satuan) "
            "VALUES (1, 1, 1, 'ikat')"
        )
        connection.execute(
            "INSERT INTO langkah_resep (resep_id, urutan, instruksi) "
            "VALUES (1, 1, 'Cuci bahan')"
        )

        violations = [
            (
                "nama resep kosong",
                "INSERT INTO resep (nama) VALUES ('   ')",
            ),
            ("nama bahan kosong", "INSERT INTO bahan (nama) VALUES ('   ')"),
            (
                "jumlah bahan negatif",
                "INSERT INTO resep_bahan (resep_id, bahan_id, jumlah) "
                "VALUES (1, 1, -1)",
            ),
            (
                "foreign key bahan tidak ada",
                "INSERT INTO resep_bahan (resep_id, bahan_id) VALUES (1, 999)",
            ),
            (
                "urutan langkah duplikat",
                "INSERT INTO langkah_resep (resep_id, urutan, instruksi) "
                "VALUES (1, 1, 'Masak')",
            ),
        ]

        for description, statement in violations:
            try:
                connection.execute(statement)
            except sqlite3.IntegrityError:
                print(f"OK ditolak: {description}")
            else:
                raise AssertionError(
                    f"GAGAL: pelanggaran tidak ditolak: {description}"
                )

        print(f"Semua {len(violations)} uji pelanggaran ditolak.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
