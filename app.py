from __future__ import annotations

import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path
from time import time as epoch_time

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from itsdangerous import BadData, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

import models
import services


PROJECT_ROOT = Path(__file__).resolve().parent
CSRF_COOKIE_NAME = "csrf_token"
CSRF_TOKEN_MAX_AGE = 86400
LOGIN_ATTEMPT_WINDOW_SECONDS = 300
LOGIN_MAX_FAILURES = 5


def environment_flag(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise RuntimeError(f"Nilai environment {name} harus berupa boolean.")


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=os.environ.get(
            "DATABASE_PATH",
            str(PROJECT_ROOT / "instance" / "resep.db"),
        ),
        SCHEMA=str(PROJECT_ROOT / "docs" / "desain" / "schema.sql"),
        APP_ENV=os.environ.get("APP_ENV", "development").strip().casefold(),
        DEBUG=environment_flag("APP_DEBUG", False),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=environment_flag("SESSION_COOKIE_SECURE", True),
        SESSION_COOKIE_SAMESITE="Lax",
        LOGIN_ATTEMPT_WINDOW_SECONDS=LOGIN_ATTEMPT_WINDOW_SECONDS,
        LOGIN_MAX_FAILURES=LOGIN_MAX_FAILURES,
    )
    if test_config is not None:
        app.config.update(test_config)
    if app.config["APP_ENV"] not in {"development", "test", "production"}:
        raise RuntimeError("APP_ENV harus development, test, atau production.")
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "Variabel lingkungan SECRET_KEY wajib diatur sebelum menjalankan aplikasi."
        )
    if app.config["APP_ENV"] == "production":
        if app.config["DEBUG"]:
            raise RuntimeError("Mode debug tidak boleh aktif pada production.")
        if not app.config["SESSION_COOKIE_SECURE"]:
            raise RuntimeError(
                "SESSION_COOKIE_SECURE wajib aktif pada production."
            )
    app.config.setdefault(
        "DUMMY_PASSWORD_HASH",
        generate_password_hash(secrets.token_urlsafe(32), method="scrypt"),
    )
    csrf_serializer = URLSafeTimedSerializer(app.secret_key, salt="resep-csrf")

    app.teardown_appcontext(models.close_db)
    with app.app_context():
        models.init_db()

    @app.before_request
    def protect_post_requests():
        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        try:
            if csrf_cookie is None:
                raise BadData("missing CSRF cookie")
            csrf_serializer.loads(csrf_cookie, max_age=CSRF_TOKEN_MAX_AGE)
        except BadData:
            csrf_cookie = csrf_serializer.dumps(secrets.token_urlsafe(32))
            g.csrf_cookie_to_set = csrf_cookie
        g.csrf_token = csrf_cookie

        if request.method == "POST":
            submitted_token = request.form.get("csrf_token", "")
            if (
                not submitted_token
                or not secrets.compare_digest(submitted_token, csrf_cookie)
            ):
                app.logger.warning(
                    "security.csrf_rejected endpoint=%s",
                    request.endpoint or "unknown",
                )
                abort(400)
            try:
                csrf_serializer.loads(submitted_token, max_age=CSRF_TOKEN_MAX_AGE)
            except BadData:
                app.logger.warning(
                    "security.csrf_rejected endpoint=%s",
                    request.endpoint or "unknown",
                )
                abort(400)

        pengguna_id = session.get("pengguna_id")
        g.pengguna = (
            models.get_pengguna_by_id(pengguna_id)
            if isinstance(pengguna_id, int) and not isinstance(pengguna_id, bool)
            else None
        )
        if pengguna_id is not None and g.pengguna is None:
            session.clear()

    @app.after_request
    def set_csrf_cookie(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin",
        )
        csrf_cookie = getattr(g, "csrf_cookie_to_set", None)
        if csrf_cookie is not None:
            response.set_cookie(
                CSRF_COOKIE_NAME,
                csrf_cookie,
                max_age=CSRF_TOKEN_MAX_AGE,
                httponly=True,
                secure=app.config["SESSION_COOKIE_SECURE"],
                samesite="Lax",
                path="/",
            )
        return response

    @app.context_processor
    def provide_csrf_token():
        return {
            "csrf_token": lambda: g.csrf_token,
            "current_user": lambda: g.get("pengguna"),
        }

    def peran_diperlukan(*peran_diizinkan: str):
        def decorate(view):
            @wraps(view)
            def wrapped(*args, **kwargs):
                if g.pengguna is None:
                    next_url = request.full_path
                    if next_url.endswith("?"):
                        next_url = next_url[:-1]
                    return redirect(url_for("login", next=next_url))
                if g.pengguna["peran"] not in peran_diizinkan:
                    app.logger.warning(
                        "security.access_denied pengguna_id=%s peran=%s endpoint=%s",
                        g.pengguna["id"],
                        g.pengguna["peran"],
                        request.endpoint or "unknown",
                    )
                    abort(403)
                return view(*args, **kwargs)

            return wrapped

        return decorate

    @app.get("/login")
    def login():
        if request.args.get("next"):
            next_url = services.safe_next_url(request.args["next"])
        else:
            next_url = None
        return render_template("login.html", next_url=next_url)

    @app.post("/login")
    def login_submit():
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        fingerprint = services.login_attempt_fingerprint(
            request.remote_addr,
            username,
        )
        now = epoch_time()
        attempt_allowed = models.reserve_login_attempt(
            fingerprint,
            now,
            app.config["LOGIN_ATTEMPT_WINDOW_SECONDS"],
            app.config["LOGIN_MAX_FAILURES"],
        )
        next_url = services.safe_next_url(request.form.get("next"))
        if not attempt_allowed:
            app.logger.warning(
                "auth.login_locked fingerprint=%s",
                fingerprint,
            )
            return (
                render_template(
                    "login.html",
                    username=username,
                    next_url=next_url,
                    error="Terlalu banyak percobaan masuk. Coba lagi beberapa menit.",
                ),
                429,
            )

        pengguna = services.authenticate_pengguna(username, password)
        if pengguna is None:
            app.logger.warning(
                "auth.login_failed fingerprint=%s",
                fingerprint,
            )
            return (
                render_template(
                    "login.html",
                    username=username,
                    next_url=next_url,
                    error="Nama pengguna atau kata sandi salah.",
                ),
                401,
            )

        models.clear_login_failures(fingerprint)
        session.clear()
        session["pengguna_id"] = pengguna["id"]
        g.csrf_cookie_to_set = csrf_serializer.dumps(secrets.token_urlsafe(32))
        next_url = services.safe_next_url(request.form.get("next"))
        return redirect(next_url or url_for("home"))

    @app.post("/logout")
    @peran_diperlukan("pengelola", "pengguna")
    def logout():
        session.clear()
        g.csrf_cookie_to_set = csrf_serializer.dumps(secrets.token_urlsafe(32))
        return redirect(url_for("login"))

    @app.get("/")
    @peran_diperlukan("pengelola", "pengguna")
    def home():
        return redirect(url_for("bahan_list"))

    @app.get("/bahan")
    @peran_diperlukan("pengelola", "pengguna")
    def bahan_list():
        return render_template("bahan/list.html", bahan=services.list_bahan())

    @app.get("/resep")
    @peran_diperlukan("pengelola", "pengguna")
    def resep_list():
        return render_template("resep/list.html", resep=services.list_resep())

    @app.get("/resep/<int:resep_id>")
    @peran_diperlukan("pengelola", "pengguna")
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
    @peran_diperlukan("pengelola")
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
    @peran_diperlukan("pengelola", "pengguna")
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
    @peran_diperlukan("pengelola")
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
    @peran_diperlukan("pengelola")
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
    @peran_diperlukan("pengelola")
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
    @peran_diperlukan("pengelola")
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

    @app.errorhandler(400)
    def bad_request(_error):
        return render_template("400.html"), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("403.html"), 403

    return app


if __name__ == "__main__":
    create_app().run()
