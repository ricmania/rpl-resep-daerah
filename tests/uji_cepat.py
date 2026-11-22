from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from models import get_db
import services


class UjiCepatResep(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
                "DATABASE": str(Path(self.temporary_directory.name) / "uji.db"),
                "SESSION_COOKIE_SECURE": False,
            }
        )
        with self.app.app_context():
            services.create_pengguna(
                "pengelola_uji",
                "kata-sandi-uji-123",
                "pengelola",
            )
        self.client = self.app.test_client()
        self.client.get("/login")
        csrf_token = self.client.get_cookie("csrf_token").value
        self.client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": "pengelola_uji",
                "password": "kata-sandi-uji-123",
            },
        )
        self.csrf_token = self.client.get_cookie("csrf_token").value

    def login_as(self, username: str, peran: str):
        with self.app.app_context():
            services.create_pengguna(
                username,
                "kata-sandi-uji-123",
                peran,
            )
        client = self.app.test_client()
        client.get("/login")
        csrf_token = client.get_cookie("csrf_token").value
        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": username,
                "password": "kata-sandi-uji-123",
            },
        )
        self.assertEqual(response.status_code, 302)
        return client

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def post_form(self, path: str, data: dict | None = None, **kwargs):
        form_data = dict(data or {})
        form_data.setdefault("csrf_token", self.csrf_token)
        return self.client.post(path, data=form_data, **kwargs)

    def test_catat_resep_menyimpan_bahan_dan_langkah(self) -> None:
        self.post_form("/bahan/tambah", data={"nama": "Jahe"})
        with self.app.app_context():
            bahan_id = get_db().execute(
                "SELECT id FROM bahan WHERE nama = ?",
                ("Jahe",),
            ).fetchone()["id"]

        response = self.post_form(
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

    def test_guest_is_redirected_to_login(self) -> None:
        response = self.app.test_client().get("/bahan")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].startswith("/login?next="))

    def test_unknown_username_and_wrong_password_share_error_message(self) -> None:
        responses = []
        for username, password in (
            ("pengelola_uji", "kata-sandi-salah"),
            ("akun_tidak_ada", "kata-sandi-uji-123"),
        ):
            client = self.app.test_client()
            client.get("/login")
            csrf_token = client.get_cookie("csrf_token").value
            responses.append(
                client.post(
                    "/login",
                    data={
                        "csrf_token": csrf_token,
                        "username": username,
                        "password": password,
                    },
                )
            )

        self.assertEqual([response.status_code for response in responses], [401, 401])
        expected = b"Nama pengguna atau kata sandi salah."
        self.assertIn(expected, responses[0].data)
        self.assertIn(expected, responses[1].data)

    def test_external_next_url_is_ignored(self) -> None:
        client = self.app.test_client()
        client.get("/login")
        csrf_token = client.get_cookie("csrf_token").value
        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": "pengelola_uji",
                "password": "kata-sandi-uji-123",
                "next": "https://jahat.example",
            },
        )
        self.assertEqual(response.headers["Location"], "/")

    def test_password_is_stored_as_scrypt_hash(self) -> None:
        with self.app.app_context():
            pengguna = get_db().execute(
                "SELECT password_hash FROM pengguna WHERE username = ?",
                ("pengelola_uji",),
            ).fetchone()
        self.assertIsNotNone(pengguna)
        self.assertTrue(pengguna["password_hash"].startswith("scrypt:"))
        self.assertNotEqual(pengguna["password_hash"], "kata-sandi-uji-123")

    def test_limited_role_is_denied_write_page_and_post(self) -> None:
        client = self.login_as("pembaca_uji", "pengguna")
        self.assertEqual(client.get("/bahan").status_code, 200)
        self.assertEqual(client.get("/bahan/tambah").status_code, 403)
        csrf_token = client.get_cookie("csrf_token").value
        response = client.post(
            "/bahan/tambah",
            data={"csrf_token": csrf_token, "nama": "Tidak disimpan"},
        )
        self.assertEqual(response.status_code, 403)
        with self.app.app_context():
            count = get_db().execute("SELECT COUNT(*) FROM bahan").fetchone()[0]
        self.assertEqual(count, 0)

    def test_manager_can_add_bahan(self) -> None:
        response = self.post_form("/bahan/tambah", data={"nama": "Kunyit"})
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            row = get_db().execute(
                "SELECT nama FROM bahan WHERE nama = ?",
                ("Kunyit",),
            ).fetchone()
        self.assertIsNotNone(row)

    def test_logout_uses_post_and_clears_session(self) -> None:
        self.assertEqual(self.client.get("/logout").status_code, 405)
        csrf_token = self.client.get_cookie("csrf_token").value
        response = self.client.post(
            "/logout",
            data={"csrf_token": csrf_token},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        self.assertEqual(self.client.get("/bahan").status_code, 302)

    def test_post_without_csrf_is_rejected_and_logged(self) -> None:
        client = self.app.test_client()
        client.get("/login")
        with self.assertLogs(self.app.logger, level="WARNING") as captured:
            response = client.post(
                "/login",
                data={
                    "username": "pengelola_uji",
                    "password": "kata-sandi-uji-123",
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("security.csrf_rejected", "\n".join(captured.output))
        self.assertNotIn("kata-sandi-uji-123", "\n".join(captured.output))

    def test_login_limit_returns_429_then_expires_after_five_minutes(self) -> None:
        client = self.app.test_client()
        client.get("/login")
        csrf_token = client.get_cookie("csrf_token").value
        with patch("app.epoch_time", return_value=1000):
            for _ in range(5):
                response = client.post(
                    "/login",
                    data={
                        "csrf_token": csrf_token,
                        "username": "pengelola_uji",
                        "password": "kata-sandi-salah",
                    },
                )
                self.assertEqual(response.status_code, 401)

            locked_response = client.post(
                "/login",
                data={
                    "csrf_token": csrf_token,
                    "username": "pengelola_uji",
                    "password": "kata-sandi-uji-123",
                },
            )
        self.assertEqual(locked_response.status_code, 429)

        with patch("app.epoch_time", return_value=1300):
            allowed_response = client.post(
                "/login",
                data={
                    "csrf_token": csrf_token,
                    "username": "pengelola_uji",
                    "password": "kata-sandi-uji-123",
                },
            )
        self.assertEqual(allowed_response.status_code, 302)

    def test_security_headers_are_present(self) -> None:
        response = self.client.get("/login")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(
            response.headers["Referrer-Policy"],
            "strict-origin-when-cross-origin",
        )


if __name__ == "__main__":
    result = unittest.main(exit=False).result
    if result.wasSuccessful():
        print("SEMUA UJI LULUS")
    else:
        raise SystemExit(1)
