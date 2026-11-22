from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from werkzeug.security import check_password_hash

from app import create_app
from models import get_db
import services


class AutentikasiAppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
                "DATABASE": str(Path(self.temporary_directory.name) / "auth.db"),
                "SESSION_COOKIE_SECURE": False,
            }
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_create_user_stores_scrypt_hash_and_random_salt(self) -> None:
        with self.app.app_context():
            first_id = services.create_pengguna(
                "pengelola_uji",
                "kata-sandi-karangan-1",
                "pengelola",
            )
            second_id = services.create_pengguna(
                "pembaca_uji",
                "kata-sandi-karangan-1",
                "pengguna",
            )
            rows = get_db().execute(
                """
                SELECT id, username, password_hash, peran
                FROM pengguna
                WHERE id IN (?, ?)
                ORDER BY id
                """,
                (first_id, second_id),
            ).fetchall()

        self.assertEqual(len(rows), 2)
        first_hash, second_hash = rows[0]["password_hash"], rows[1]["password_hash"]
        self.assertTrue(first_hash.startswith("scrypt:"))
        self.assertTrue(second_hash.startswith("scrypt:"))
        self.assertNotEqual(first_hash, "kata-sandi-karangan-1")
        self.assertNotEqual(second_hash, "kata-sandi-karangan-1")
        self.assertNotEqual(first_hash, second_hash)
        self.assertTrue(check_password_hash(first_hash, "kata-sandi-karangan-1"))
        self.assertTrue(check_password_hash(second_hash, "kata-sandi-karangan-1"))
        self.assertEqual(
            [(row["username"], row["peran"]) for row in rows],
            [("pengelola_uji", "pengelola"), ("pembaca_uji", "pengguna")],
        )

    def test_create_user_rejects_invalid_username_password_and_role(self) -> None:
        invalid_accounts = [
            ("ab", "kata-sandi-karangan", "pengelola"),
            ("nama pengguna", "kata-sandi-karangan", "pengelola"),
            ("akun", "singkat", "pengelola"),
            ("akun", "x" * 129, "pengelola"),
            ("akun", "kata-sandi-karangan", "admin"),
        ]
        for username, password, peran in invalid_accounts:
            with self.subTest(username=username, peran=peran):
                with self.app.app_context(), self.assertRaises(
                    services.ValidationError
                ):
                    services.create_pengguna(username, password, peran)

        with self.app.app_context():
            count = get_db().execute(
                "SELECT COUNT(*) FROM pengguna"
            ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_username_is_unique_case_insensitively(self) -> None:
        with self.app.app_context():
            services.create_pengguna(
                "Pengelola",
                "kata-sandi-karangan",
                "pengelola",
            )
            with self.assertRaises(sqlite3.IntegrityError):
                services.create_pengguna(
                    "pengelola",
                    "kata-sandi-karangan",
                    "pengguna",
                )
