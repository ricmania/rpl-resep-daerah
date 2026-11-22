from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app
from models import create_resep, get_db
import services


class BahanAppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        database_path = Path(self.temporary_directory.name) / "test.db"
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
                "DATABASE": str(database_path),
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

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def post_form(self, path: str, data: dict | None = None, **kwargs):
        form_data = dict(data or {})
        form_data.setdefault("csrf_token", self.csrf_token)
        return self.client.post(path, data=form_data, **kwargs)

    def create_bahan(self, nama: str) -> int:
        response = self.post_form(
            "/bahan/tambah",
            data={"nama": nama},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            row = get_db().execute(
                "SELECT id FROM bahan WHERE nama = ? ORDER BY id DESC LIMIT 1",
                (nama.strip(),),
            ).fetchone()
            self.assertIsNotNone(row)
            return row["id"]

    def create_resep(self, nama: str) -> int:
        with self.app.app_context():
            cursor = get_db().execute(
                "INSERT INTO resep (nama) VALUES (?)",
                (nama,),
            )
            get_db().commit()
            return cursor.lastrowid

    def test_home_redirects_to_bahan_list_and_shows_empty_state(self) -> None:
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Belum ada data bahan.", response.data)

    def test_create_trims_name_and_uses_post_redirect_get(self) -> None:
        response = self.post_form("/bahan/tambah", data={"nama": "  Bayam  "})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/bahan")
        listed = self.client.get(response.headers["Location"])
        self.assertIn(b"Bayam", listed.data)
        self.assertIn(b"Bahan berhasil ditambahkan.", listed.data)

    def test_blank_name_is_rejected_and_value_is_preserved(self) -> None:
        response = self.post_form(
            "/bahan/tambah",
            data={"nama": "   "},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Nama bahan wajib diisi.", response.data)
        self.assertIn(b'value="   "', response.data)
        with self.app.app_context():
            count = get_db().execute("SELECT COUNT(*) FROM bahan").fetchone()[0]
        self.assertEqual(count, 0)

    def test_duplicate_names_are_allowed_by_the_data_dictionary(self) -> None:
        first = self.post_form(
            "/bahan/tambah",
            data={"nama": "Santan"},
            follow_redirects=True,
        )
        second = self.post_form(
            "/bahan/tambah",
            data={"nama": "Santan"},
            follow_redirects=True,
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.data.count(b"Santan"), 2)

    def test_update_prefills_existing_value_and_changes_only_name(self) -> None:
        bahan_id = self.create_bahan("Jahe")
        edit_page = self.client.get(f"/bahan/{bahan_id}/ubah")
        self.assertIn(b'value="Jahe"', edit_page.data)

        updated = self.post_form(
            f"/bahan/{bahan_id}/ubah",
            data={"nama": "  Jahe merah  "},
            follow_redirects=True,
        )
        self.assertEqual(updated.status_code, 200)
        self.assertIn(b"Jahe merah", updated.data)
        with self.app.app_context():
            row = get_db().execute(
                "SELECT id, nama FROM bahan WHERE id = ?",
                (bahan_id,),
            ).fetchone()
        self.assertEqual((row["id"], row["nama"]), (bahan_id, "Jahe merah"))

    def test_missing_and_invalid_ids_return_404(self) -> None:
        self.assertEqual(self.client.get("/bahan/999/ubah").status_code, 404)
        self.assertEqual(self.post_form("/bahan/999/ubah").status_code, 404)
        self.assertEqual(self.client.get("/bahan/-1/ubah").status_code, 404)
        self.assertEqual(self.client.get("/bahan/abc/ubah").status_code, 404)

    def test_delete_requires_confirmation_page_and_post(self) -> None:
        bahan_id = self.create_bahan("Kunyit")
        confirmation = self.client.get(f"/bahan/{bahan_id}/hapus")
        self.assertEqual(confirmation.status_code, 200)
        with self.app.app_context():
            self.assertIsNotNone(get_db().execute(
                "SELECT id FROM bahan WHERE id = ?", (bahan_id,)
            ).fetchone())

        deleted = self.post_form(
            f"/bahan/{bahan_id}/hapus",
            follow_redirects=True,
        )
        self.assertEqual(deleted.status_code, 200)
        self.assertIn(b"Bahan berhasil dihapus.", deleted.data)
        with self.app.app_context():
            self.assertIsNone(get_db().execute(
                "SELECT id FROM bahan WHERE id = ?", (bahan_id,)
            ).fetchone())

    def test_referenced_bahan_is_not_deleted(self) -> None:
        bahan_id = self.create_bahan("Temulawak")
        resep_id = self.create_resep("Resep uji")
        with self.app.app_context():
            database = get_db()
            database.execute(
                "INSERT INTO resep_bahan (resep_id, bahan_id) VALUES (?, ?)",
                (resep_id, bahan_id),
            )
            database.commit()

        response = self.post_form(
            f"/bahan/{bahan_id}/hapus",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"masih digunakan oleh resep", response.data)
        with self.app.app_context():
            self.assertIsNotNone(get_db().execute(
                "SELECT id FROM bahan WHERE id = ?", (bahan_id,)
            ).fetchone())

    def test_related_list_joins_and_displays_parent_names(self) -> None:
        bahan_id = self.create_bahan("Kelapa")
        resep_id = self.create_resep("Gudeg")
        with self.app.app_context():
            get_db().execute(
                """
                INSERT INTO resep_bahan (resep_id, bahan_id, jumlah, satuan)
                VALUES (?, ?, ?, ?)
                """,
                (resep_id, bahan_id, 2, "butir"),
            )
            get_db().commit()

        response = self.client.get("/resep-bahan")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gudeg", response.data)
        self.assertIn(b"Kelapa", response.data)
        self.assertIn(b"butir", response.data)

    def test_create_recipe_saves_ingredients_and_ordered_steps(self) -> None:
        first_bahan_id = self.create_bahan("Beras")
        second_bahan_id = self.create_bahan("Santan")

        response = self.post_form(
            "/resep/tambah",
            data={
                "nama": "  Nasi Gurih  ",
                "bahan_id": [str(first_bahan_id), str(second_bahan_id)],
                "jumlah": ["2", "1"],
                "satuan": ["gelas", "ml"],
                "instruksi": ["Cuci beras.", "Masak hingga matang."],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response.headers["Location"], r"^/resep/\d+$")

        detail = self.client.get(response.headers["Location"], follow_redirects=True)
        self.assertEqual(detail.status_code, 200)
        self.assertIn(b"Resep berhasil disimpan.", detail.data)
        self.assertIn(b"Nasi Gurih", detail.data)
        self.assertIn(b"Beras", detail.data)
        self.assertIn(b"Santan", detail.data)
        self.assertLess(
            detail.data.index(b"Cuci beras."),
            detail.data.index(b"Masak hingga matang."),
        )
        with self.app.app_context():
            recipe = get_db().execute(
                "SELECT id, nama FROM resep WHERE nama = ?",
                ("Nasi Gurih",),
            ).fetchone()
            ingredient_count = get_db().execute(
                "SELECT COUNT(*) FROM resep_bahan WHERE resep_id = ?",
                (recipe["id"],),
            ).fetchone()[0]
            steps = get_db().execute(
                "SELECT urutan, instruksi FROM langkah_resep "
                "WHERE resep_id = ? ORDER BY urutan",
                (recipe["id"],),
            ).fetchall()
        self.assertEqual(ingredient_count, 2)
        self.assertEqual(
            [(step["urutan"], step["instruksi"]) for step in steps],
            [(1, "Cuci beras."), (2, "Masak hingga matang.")],
        )

    def test_recipe_form_shows_existing_ingredient_options(self) -> None:
        self.create_bahan("Daun salam")
        response = self.client.get("/resep/tambah")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Nama resep", response.data)
        self.assertIn(b"Tambah bahan", response.data)
        self.assertIn(b"Tambah langkah", response.data)
        self.assertIn(b"Daun salam", response.data)

    def test_incomplete_recipe_is_rejected_without_saving_and_preserves_input(self) -> None:
        bahan_id = self.create_bahan("Lengkuas")
        test_cases = [
            (
                {"nama": "  ", "bahan_id": str(bahan_id), "instruksi": "Rebus."},
                b"Nama resep wajib diisi.",
            ),
            (
                {"nama": "Soto", "instruksi": "Rebus."},
                b"Tambahkan minimal satu bahan.",
            ),
            (
                {"nama": "Soto", "bahan_id": str(bahan_id)},
                b"Tambahkan minimal satu langkah.",
            ),
            (
                {
                    "nama": "Soto",
                    "bahan_id": str(bahan_id),
                    "jumlah": "0",
                    "satuan": "buah",
                    "instruksi": "Rebus.",
                },
                b"Jumlah bahan harus berupa angka lebih besar dari 0.",
            ),
        ]
        for data, expected_message in test_cases:
            with self.subTest(data=data):
                response = self.post_form("/resep/tambah", data=data)
                self.assertEqual(response.status_code, 400)
                self.assertIn(expected_message, response.data)
                with self.app.app_context():
                    recipe_count = get_db().execute(
                        "SELECT COUNT(*) FROM resep"
                    ).fetchone()[0]
                    ingredient_count = get_db().execute(
                        "SELECT COUNT(*) FROM resep_bahan"
                    ).fetchone()[0]
                    step_count = get_db().execute(
                        "SELECT COUNT(*) FROM langkah_resep"
                    ).fetchone()[0]
                self.assertEqual((recipe_count, ingredient_count, step_count), (0, 0, 0))

    def test_recipe_save_rolls_back_parent_when_child_foreign_key_fails(self) -> None:
        with self.app.app_context():
            with self.assertRaises(sqlite3.IntegrityError):
                create_resep("Resep gagal", [(999, None, None)], ["Langkah valid"])
            count = get_db().execute(
                "SELECT COUNT(*) FROM resep WHERE nama = ?",
                ("Resep gagal",),
            ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_recipe_list_shows_empty_state_and_missing_detail_is_404(self) -> None:
        response = self.client.get("/resep")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Belum ada resep yang tersimpan.", response.data)
        self.assertEqual(self.client.get("/resep/999").status_code, 404)

    def test_related_list_has_empty_state(self) -> None:
        response = self.client.get("/resep-bahan")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Belum ada bahan yang dicatat pada resep.", response.data)

    def test_related_form_lists_recipe_and_ingredient_choices(self) -> None:
        self.create_resep("Soto")
        self.create_bahan("Serai")

        response = self.client.get("/resep-bahan/tambah")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<option value="1">Soto</option>', response.data)
        self.assertIn(b'<option value="1">Serai</option>', response.data)

    def test_create_related_row_uses_post_redirect_get(self) -> None:
        resep_id = self.create_resep("Rendang")
        bahan_id = self.create_bahan("Cabai")

        response = self.post_form(
            "/resep-bahan/tambah",
            data={
                "resep_id": str(resep_id),
                "bahan_id": str(bahan_id),
                "jumlah": "3",
                "satuan": "buah",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/resep-bahan")

        listed = self.client.get(response.headers["Location"])
        self.assertIn(b"Rendang", listed.data)
        self.assertIn(b"Cabai", listed.data)
        self.assertIn(b"3.0", listed.data)
        self.assertIn(b"buah", listed.data)
        with self.app.app_context():
            row = get_db().execute(
                "SELECT resep_id, bahan_id, jumlah, satuan FROM resep_bahan"
            ).fetchone()
        self.assertEqual(
            (row["resep_id"], row["bahan_id"], row["jumlah"], row["satuan"]),
            (resep_id, bahan_id, 3.0, "buah"),
        )

    def test_missing_or_unknown_parent_is_rejected_without_partial_row(self) -> None:
        bahan_id = self.create_bahan("Kemiri")
        resep_id = self.create_resep("Opor")
        test_cases = [
            ({"resep_id": "", "bahan_id": str(bahan_id)}, b"Pilih resep"),
            ({"resep_id": "999", "bahan_id": str(bahan_id)}, b"Pilih resep"),
            ({"resep_id": str(resep_id), "bahan_id": "999"}, b"Pilih bahan"),
        ]
        for data, expected_message in test_cases:
            with self.subTest(data=data):
                response = self.post_form(
                    "/resep-bahan/tambah",
                    data=data,
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn(expected_message, response.data)
                with self.app.app_context():
                    count = get_db().execute(
                        "SELECT COUNT(*) FROM resep_bahan"
                    ).fetchone()[0]
                self.assertEqual(count, 0)

    def test_invalid_quantity_is_rejected_and_form_value_is_preserved(self) -> None:
        resep_id = self.create_resep("Rawon")
        bahan_id = self.create_bahan("Kluwek")
        for jumlah in ("0", "-3", "abc", "inf", "nan"):
            with self.subTest(jumlah=jumlah):
                response = self.post_form(
                    "/resep-bahan/tambah",
                    data={
                        "resep_id": str(resep_id),
                        "bahan_id": str(bahan_id),
                        "jumlah": jumlah,
                        "satuan": "butir",
                    },
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn(b"Jumlah harus berupa angka lebih besar dari 0.", response.data)
                self.assertIn(f'value="{jumlah}"'.encode(), response.data)
                with self.app.app_context():
                    count = get_db().execute(
                        "SELECT COUNT(*) FROM resep_bahan"
                    ).fetchone()[0]
                self.assertEqual(count, 0)

    def test_sql_injection_text_is_stored_as_data(self) -> None:
        payload = "Robert'); DROP TABLE bahan;--"
        response = self.post_form(
            "/bahan/tambah",
            data={"nama": payload},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Robert&#39;); DROP TABLE bahan;--", response.data)
        with self.app.app_context():
            row = get_db().execute(
                "SELECT nama FROM bahan WHERE nama = ?",
                (payload,),
            ).fetchone()
            table = get_db().execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
                ("bahan",),
            ).fetchone()
        self.assertEqual(row["nama"], payload)
        self.assertIsNotNone(table)

    def test_user_html_is_escaped_in_list(self) -> None:
        self.post_form("/bahan/tambah", data={"nama": "<b>tes</b>"})
        response = self.client.get("/bahan")
        self.assertIn(b"&lt;b&gt;tes&lt;/b&gt;", response.data)
        self.assertNotIn(b"<b>tes</b>", response.data)

    def test_database_initialization_creates_every_schema_table(self) -> None:
        with self.app.app_context():
            tables = {
                row["name"]
                for row in get_db().execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
        self.assertTrue(
            {
                "resep",
                "bahan",
                "resep_bahan",
                "langkah_resep",
                "pengguna",
                "login_attempts",
            }.issubset(tables)
        )


if __name__ == "__main__":
    unittest.main()
