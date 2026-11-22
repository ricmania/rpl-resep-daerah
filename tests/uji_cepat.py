from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from models import get_db


class UjiCepatResep(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
                "DATABASE": str(Path(self.temporary_directory.name) / "uji.db"),
            }
        )
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_catat_resep_menyimpan_bahan_dan_langkah(self) -> None:
        self.client.post("/bahan/tambah", data={"nama": "Jahe"})
        with self.app.app_context():
            bahan_id = get_db().execute(
                "SELECT id FROM bahan WHERE nama = ?",
                ("Jahe",),
            ).fetchone()["id"]

        response = self.client.post(
            "/resep/tambah",
            data={
                "nama": "Wedang jahe",
                "bahan_id": str(bahan_id),
                "jumlah": "2",
                "satuan": "ruas",
                "instruksi": "Rebus jahe hingga harum.",
            },
        )
        self.assertEqual(response.status_code, 302)
        detail = self.client.get(response.headers["Location"])
        self.assertIn(b"Wedang jahe", detail.data)
        self.assertIn(b"Jahe", detail.data)
        self.assertIn(b"Rebus jahe hingga harum.", detail.data)


if __name__ == "__main__":
    result = unittest.main(exit=False).result
    if result.wasSuccessful():
        print("SEMUA UJI LULUS")
    else:
        raise SystemExit(1)
