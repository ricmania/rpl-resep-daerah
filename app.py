from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import models
import services


PROJECT_ROOT = Path(__file__).resolve().parent


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=os.environ.get(
            "DATABASE_PATH",
            str(PROJECT_ROOT / "instance" / "resep.db"),
        ),
        SCHEMA=str(PROJECT_ROOT / "docs" / "desain" / "schema.sql"),
    )
    if test_config is not None:
        app.config.update(test_config)
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "Variabel lingkungan SECRET_KEY wajib diatur sebelum menjalankan aplikasi."
        )

    app.teardown_appcontext(models.close_db)
    with app.app_context():
        models.init_db()

    @app.get("/")
    def home():
        return redirect(url_for("bahan_list"))

    @app.get("/bahan")
    def bahan_list():
        return render_template("bahan/list.html", bahan=services.list_bahan())

    @app.get("/resep")
    def resep_list():
        return render_template("resep/list.html", resep=services.list_resep())

    @app.get("/resep/<int:resep_id>")
    def resep_detail(resep_id: int):
        resep_detail_data = services.get_resep_detail(resep_id)
        if resep_detail_data is None:
            abort(404)
        resep, bahan, langkah = resep_detail_data
        return render_template(
            "resep/detail.html",
            resep=resep,
            bahan=bahan,
            langkah=langkah,
        )

    def render_resep_form(
        *,
        nama: str = "",
        bahan_ids: list[str] | None = None,
        jumlahs: list[str] | None = None,
        satuans: list[str] | None = None,
        instruksi_langkah: list[str] | None = None,
        error: str | None = None,
        status: int = 200,
    ):
        ingredient_ids = bahan_ids or [""]
        quantities = jumlahs or [""]
        units = satuans or [""]
        row_count = max(len(ingredient_ids), len(quantities), len(units), 1)
        ingredient_ids.extend([""] * (row_count - len(ingredient_ids)))
        quantities.extend([""] * (row_count - len(quantities)))
        units.extend([""] * (row_count - len(units)))
        steps = instruksi_langkah or [""]
        if not steps:
            steps = [""]
        return (
            render_template(
                "resep/form.html",
                nama=nama,
                bahan=services.list_bahan(),
                bahan_ids=ingredient_ids,
                jumlahs=quantities,
                satuans=units,
                instruksi_langkah=steps,
                error=error,
            ),
            status,
        )

    @app.route("/resep/tambah", methods=["GET", "POST"])
    def resep_create():
        if request.method == "GET":
            return render_resep_form()

        nama = request.form.get("nama", "")
        bahan_ids = request.form.getlist("bahan_id")
        jumlahs = request.form.getlist("jumlah")
        satuans = request.form.getlist("satuan")
        instruksi_langkah = request.form.getlist("instruksi")
        try:
            resep_id = services.create_resep(
                nama,
                bahan_ids,
                jumlahs,
                satuans,
                instruksi_langkah,
            )
        except services.ValidationError as error:
            return render_resep_form(
                nama=nama,
                bahan_ids=bahan_ids,
                jumlahs=jumlahs,
                satuans=satuans,
                instruksi_langkah=instruksi_langkah,
                error=str(error),
                status=400,
            )
        except sqlite3.IntegrityError:
            return render_resep_form(
                nama=nama,
                bahan_ids=bahan_ids,
                jumlahs=jumlahs,
                satuans=satuans,
                instruksi_langkah=instruksi_langkah,
                error="Resep tidak dapat disimpan karena melanggar aturan data.",
                status=400,
            )

        flash("Resep berhasil disimpan.", "success")
        return redirect(url_for("resep_detail", resep_id=resep_id))

    @app.get("/resep-bahan")
    def resep_bahan_list():
        return render_template(
            "resep_bahan/list.html",
            resep_bahan=services.list_resep_bahan(),
        )

    def render_resep_bahan_form(
        *,
        resep_id: str = "",
        bahan_id: str = "",
        jumlah: str = "",
        satuan: str = "",
        error: str | None = None,
        status: int = 200,
    ):
        return (
            render_template(
                "resep_bahan/form.html",
                resep=services.list_resep(),
                bahan=services.list_bahan(),
                resep_id=resep_id,
                bahan_id=bahan_id,
                jumlah=jumlah,
                satuan=satuan,
                error=error,
            ),
            status,
        )

    @app.route("/resep-bahan/tambah", methods=["GET", "POST"])
    def resep_bahan_create():
        if request.method == "GET":
            return render_resep_bahan_form()

        resep_id = request.form.get("resep_id", "")
        bahan_id = request.form.get("bahan_id", "")
        jumlah = request.form.get("jumlah", "")
        satuan = request.form.get("satuan", "")
        try:
            services.create_resep_bahan(resep_id, bahan_id, jumlah, satuan)
        except services.ValidationError as error:
            return render_resep_bahan_form(
                resep_id=resep_id,
                bahan_id=bahan_id,
                jumlah=jumlah,
                satuan=satuan,
                error=str(error),
                status=400,
            )
        except sqlite3.IntegrityError:
            return render_resep_bahan_form(
                resep_id=resep_id,
                bahan_id=bahan_id,
                jumlah=jumlah,
                satuan=satuan,
                error="Data resep-bahan tidak dapat disimpan karena melanggar aturan data.",
                status=400,
            )

        flash("Bahan resep berhasil ditambahkan.", "success")
        return redirect(url_for("resep_bahan_list"))

    @app.route("/bahan/tambah", methods=["GET", "POST"])
    def bahan_create():
        if request.method == "GET":
            return render_template(
                "bahan/form.html",
                page_title="Tambah bahan",
                nama="",
                form_action=url_for("bahan_create"),
            )

        nama = request.form.get("nama", "")
        try:
            services.create_bahan(nama)
        except services.ValidationError as error:
            return (
                render_template(
                    "bahan/form.html",
                    page_title="Tambah bahan",
                    nama=nama,
                    error=str(error),
                    form_action=url_for("bahan_create"),
                ),
                400,
            )
        except sqlite3.IntegrityError:
            return (
                render_template(
                    "bahan/form.html",
                    page_title="Tambah bahan",
                    nama=nama,
                    error="Bahan tidak dapat disimpan karena melanggar aturan data.",
                    form_action=url_for("bahan_create"),
                ),
                400,
            )

        flash("Bahan berhasil ditambahkan.", "success")
        return redirect(url_for("bahan_list"))

    @app.route("/bahan/<int:bahan_id>/ubah", methods=["GET", "POST"])
    def bahan_update(bahan_id: int):
        bahan = services.get_bahan(bahan_id)
        if bahan is None:
            abort(404)

        if request.method == "GET":
            return render_template(
                "bahan/form.html",
                page_title="Ubah bahan",
                nama=bahan["nama"],
                form_action=url_for("bahan_update", bahan_id=bahan_id),
            )

        nama = request.form.get("nama", "")
        try:
            services.update_bahan(bahan_id, nama)
        except services.ValidationError as error:
            return (
                render_template(
                    "bahan/form.html",
                    page_title="Ubah bahan",
                    nama=nama,
                    error=str(error),
                    form_action=url_for("bahan_update", bahan_id=bahan_id),
                ),
                400,
            )
        except sqlite3.IntegrityError:
            return (
                render_template(
                    "bahan/form.html",
                    page_title="Ubah bahan",
                    nama=nama,
                    error="Bahan tidak dapat diubah karena melanggar aturan data.",
                    form_action=url_for("bahan_update", bahan_id=bahan_id),
                ),
                400,
            )

        flash("Bahan berhasil diubah.", "success")
        return redirect(url_for("bahan_list"))

    @app.route("/bahan/<int:bahan_id>/hapus", methods=["GET", "POST"])
    def bahan_delete(bahan_id: int):
        bahan = services.get_bahan(bahan_id)
        if bahan is None:
            abort(404)

        if request.method == "GET":
            return render_template("bahan/delete.html", bahan=bahan)

        try:
            services.delete_bahan(bahan_id)
        except sqlite3.IntegrityError:
            flash(
                "Bahan tidak dapat dihapus karena masih digunakan oleh resep.",
                "error",
            )
            return redirect(url_for("bahan_list"))

        flash("Bahan berhasil dihapus.", "success")
        return redirect(url_for("bahan_list"))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    create_app().run()
