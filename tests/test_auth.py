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

    def create_account(
        self,
        username: str = "pengelola_uji",
        peran: str = "pengelola",
        password: str = "kata-sandi-karangan",
    ) -> int:
        with self.app.app_context():
            return services.create_pengguna(username, password, peran)

    def csrf_token_for(self, client):
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)
        csrf_cookie = client.get_cookie("csrf_token")
        self.assertIsNotNone(csrf_cookie)
        return csrf_cookie.value

    def authenticated_client(self, username: str, peran: str):
        self.create_account(username=username, peran=peran)
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)
        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": username,
                "password": "kata-sandi-karangan",
            },
        )
        self.assertEqual(response.status_code, 302)
        return client

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

    def test_login_clears_session_and_stores_only_user_id(self) -> None:
        pengguna_id = self.create_account()
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)

        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": "pengelola_uji",
                "password": "kata-sandi-karangan",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        with client.session_transaction() as browser_session:
            self.assertEqual(dict(browser_session), {"pengguna_id": pengguna_id})

    def test_invalid_username_and_password_have_the_same_message(self) -> None:
        self.create_account()
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)
        responses = [
            client.post(
                "/login",
                data={
                    "csrf_token": csrf_token,
                    "username": "pengelola_uji",
                    "password": "kata-sandi-salah",
                },
            ),
            client.post(
                "/login",
                data={
                    "csrf_token": csrf_token,
                    "username": "akun_tidak_ada",
                    "password": "kata-sandi-karangan",
                },
            ),
        ]
        self.assertEqual([response.status_code for response in responses], [401, 401])
        self.assertIn(b"Nama pengguna atau kata sandi salah.", responses[0].data)
        self.assertIn(b"Nama pengguna atau kata sandi salah.", responses[1].data)

    def test_login_ignores_external_and_protocol_relative_next_urls(self) -> None:
        self.create_account()
        for unsafe_next in (
            "https://jahat.example",
            "//jahat.example",
            "/%2f%2fjahat.example",
            "/%5c%5cjahat.example",
        ):
            with self.subTest(next=unsafe_next):
                client = self.app.test_client()
                csrf_token = self.csrf_token_for(client)
                response = client.post(
                    "/login",
                    data={
                        "csrf_token": csrf_token,
                        "username": "pengelola_uji",
                        "password": "kata-sandi-karangan",
                        "next": unsafe_next,
                    },
                )
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers["Location"], "/")

    def test_login_accepts_local_next_url(self) -> None:
        self.create_account()
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)
        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": "pengelola_uji",
                "password": "kata-sandi-karangan",
                "next": "/resep",
            },
        )
        self.assertEqual(response.headers["Location"], "/resep")

    def test_logout_requires_post_and_clears_session(self) -> None:
        pengguna_id = self.create_account()
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)
        client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": "pengelola_uji",
                "password": "kata-sandi-karangan",
            },
        )
        self.assertEqual(client.get("/logout").status_code, 405)
        rotated_token = client.get_cookie("csrf_token").value
        response = client.post(
            "/logout",
            data={"csrf_token": rotated_token},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        with client.session_transaction() as browser_session:
            self.assertEqual(dict(browser_session), {})
        self.assertNotEqual(client.get_cookie("csrf_token").value, rotated_token)
        self.assertIsNotNone(pengguna_id)

    def test_post_without_valid_csrf_token_is_rejected(self) -> None:
        client = self.app.test_client()
        self.csrf_token_for(client)
        missing_token_response = client.post(
            "/login",
            data={"username": "nobody", "password": "irrelevant"},
        )
        self.assertEqual(missing_token_response.status_code, 400)
        forged_token_response = client.post(
            "/login",
            data={
                "csrf_token": "forged-token",
                "username": "nobody",
                "password": "irrelevant",
            },
        )
        self.assertEqual(forged_token_response.status_code, 400)

    def test_guest_is_redirected_to_login_with_requested_path(self) -> None:
        client = self.app.test_client()
        response = client.get("/bahan?cari=jahe")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"],
            "/login?next=/bahan?cari%3Djahe",
        )

    def test_limited_role_can_read_but_cannot_write_from_get_or_post(self) -> None:
        client = self.authenticated_client("pembaca_uji", "pengguna")
        read_response = client.get("/bahan")
        self.assertEqual(read_response.status_code, 200)
        self.assertNotIn(b"Tambah bahan", read_response.data)

        csrf_token = client.get_cookie("csrf_token").value
        forbidden_paths = (
            "/bahan/tambah",
            "/bahan/1/ubah",
            "/bahan/1/hapus",
            "/resep/tambah",
            "/resep-bahan/tambah",
        )
        for path in forbidden_paths:
            with self.subTest(path=path):
                self.assertEqual(client.get(path).status_code, 403)
                response = client.post(
                    path,
                    data={"csrf_token": csrf_token, "nama": "Tidak disimpan"},
                )
                self.assertEqual(response.status_code, 403)
                self.assertIn(b"Akses ditolak", response.data)

        with self.app.app_context():
            self.assertEqual(
                get_db().execute("SELECT COUNT(*) FROM bahan").fetchone()[0],
                0,
            )

    def test_manager_can_write_and_limited_role_sees_read_only_list(self) -> None:
        manager = self.authenticated_client("pengelola_uji", "pengelola")
        csrf_token = manager.get_cookie("csrf_token").value
        response = manager.post(
            "/bahan/tambah",
            data={"csrf_token": csrf_token, "nama": "Jahe"},
        )
        self.assertEqual(response.status_code, 302)

        reader = self.authenticated_client("pembaca_uji", "pengguna")
        read_response = reader.get("/bahan", follow_redirects=True)
        self.assertEqual(read_response.status_code, 200)
        self.assertIn(b"Jahe", read_response.data)
        self.assertNotIn(b"Ubah", read_response.data)
        self.assertNotIn(b"Hapus", read_response.data)

    def test_guest_post_is_redirected_and_does_not_change_data(self) -> None:
        client = self.app.test_client()
        csrf_token = self.csrf_token_for(client)
        response = client.post(
            "/bahan/tambah",
            data={"csrf_token": csrf_token, "nama": "Tamu"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].startswith("/login?next="))
        with self.app.app_context():
            self.assertEqual(
                get_db().execute("SELECT COUNT(*) FROM bahan").fetchone()[0],
                0,
            )
