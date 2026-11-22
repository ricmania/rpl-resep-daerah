from __future__ import annotations

import math
import re
from werkzeug.security import generate_password_hash

import models


class ValidationError(ValueError):
    """Raised when a form value violates an application rule."""


PERAN_VALID = {"pengelola", "pengguna"}
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]{3,32}$")
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 128


def validate_bahan_name(nama: str) -> str:
    if not isinstance(nama, str):
        raise ValidationError("Nama bahan wajib berupa teks.")

    normalized_name = nama.strip()
    if not normalized_name:
        raise ValidationError("Nama bahan wajib diisi.")

    return normalized_name


def list_bahan():
    return models.list_bahan()


def create_pengguna(username: str, password: str, peran: str) -> int:
    normalized_username = username.strip()
    if not USERNAME_PATTERN.fullmatch(normalized_username):
        raise ValidationError(
            "Nama pengguna harus 3–32 karakter: huruf, angka, titik, garis bawah, atau tanda hubung."
        )
    if not PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH:
        raise ValidationError(
            f"Kata sandi harus {PASSWORD_MIN_LENGTH}–{PASSWORD_MAX_LENGTH} karakter."
        )
    if peran not in PERAN_VALID:
        raise ValidationError("Peran pengguna tidak valid.")

    password_hash = generate_password_hash(password, method="scrypt")
    return models.create_pengguna(normalized_username, password_hash, peran)


def get_bahan(bahan_id: int):
    return models.get_bahan(bahan_id)


def create_bahan(nama: str) -> int:
    return models.create_bahan(validate_bahan_name(nama))


def update_bahan(bahan_id: int, nama: str) -> bool:
    return models.update_bahan(bahan_id, validate_bahan_name(nama))


def delete_bahan(bahan_id: int) -> bool:
    return models.delete_bahan(bahan_id)


def list_resep_bahan():
    return models.list_resep_bahan()


def list_resep():
    return models.list_resep()


def get_resep_detail(resep_id: int):
    return models.get_resep_detail(resep_id)


def create_resep_bahan(
    resep_id: str,
    bahan_id: str,
    jumlah: str,
    satuan: str,
) -> int:
    try:
        parsed_resep_id = int(resep_id)
    except (TypeError, ValueError):
        raise ValidationError("Pilih resep yang tersedia.") from None
    if parsed_resep_id <= 0 or models.get_resep(parsed_resep_id) is None:
        raise ValidationError("Pilih resep yang tersedia.")

    try:
        parsed_bahan_id = int(bahan_id)
    except (TypeError, ValueError):
        raise ValidationError("Pilih bahan yang tersedia.") from None
    if parsed_bahan_id <= 0 or models.get_bahan(parsed_bahan_id) is None:
        raise ValidationError("Pilih bahan yang tersedia.")

    normalized_jumlah = jumlah.strip()
    if normalized_jumlah:
        try:
            parsed_jumlah = float(normalized_jumlah)
        except ValueError:
            raise ValidationError("Jumlah harus berupa angka lebih besar dari 0.") from None
        if not math.isfinite(parsed_jumlah) or parsed_jumlah <= 0:
            raise ValidationError("Jumlah harus berupa angka lebih besar dari 0.")
    else:
        parsed_jumlah = None

    normalized_satuan = satuan.strip() or None
    return models.create_resep_bahan(
        parsed_resep_id,
        parsed_bahan_id,
        parsed_jumlah,
        normalized_satuan,
    )


def create_resep(
    nama: str,
    bahan_ids: list[str],
    jumlahs: list[str],
    satuans: list[str],
    instruksi_langkah: list[str],
) -> int:
    normalized_name = nama.strip()
    if not normalized_name:
        raise ValidationError("Nama resep wajib diisi.")

    if len(jumlahs) > len(bahan_ids) or len(satuans) > len(bahan_ids):
        raise ValidationError("Periksa kembali baris bahan pada resep.")
    normalized_jumlahs = jumlahs + [""] * (len(bahan_ids) - len(jumlahs))
    normalized_satuans = satuans + [""] * (len(bahan_ids) - len(satuans))

    bahan: list[tuple[int, float | None, str | None]] = []
    for bahan_id, jumlah, satuan in zip(
        bahan_ids,
        normalized_jumlahs,
        normalized_satuans,
    ):
        if not bahan_id.strip():
            continue
        try:
            parsed_bahan_id = int(bahan_id)
        except ValueError:
            raise ValidationError("Pilih bahan yang tersedia.") from None
        if parsed_bahan_id <= 0 or models.get_bahan(parsed_bahan_id) is None:
            raise ValidationError("Pilih bahan yang tersedia.")

        normalized_jumlah = jumlah.strip()
        if normalized_jumlah:
            try:
                parsed_jumlah = float(normalized_jumlah)
            except ValueError:
                raise ValidationError(
                    "Jumlah bahan harus berupa angka lebih besar dari 0."
                ) from None
            if not math.isfinite(parsed_jumlah) or parsed_jumlah <= 0:
                raise ValidationError(
                    "Jumlah bahan harus berupa angka lebih besar dari 0."
                )
        else:
            parsed_jumlah = None

        normalized_satuan = satuan.strip() or None
        bahan.append((parsed_bahan_id, parsed_jumlah, normalized_satuan))

    if not bahan:
        raise ValidationError("Tambahkan minimal satu bahan.")

    langkah = [instruksi.strip() for instruksi in instruksi_langkah]
    langkah = [instruksi for instruksi in langkah if instruksi]
    if not langkah:
        raise ValidationError("Tambahkan minimal satu langkah.")

    return models.create_resep(normalized_name, bahan, langkah)
