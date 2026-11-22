from __future__ import annotations

import getpass
import sqlite3

from app import create_app
import services


PERAN_MENU = {
    "1": ("pengelola", "Pengelola resep"),
    "2": ("pengguna", "Pengguna resep"),
}


def main() -> None:
    app = create_app()
    print("Buat akun baru (kata sandi tidak ditampilkan atau disimpan sebagai teks).")
    username = input("Nama pengguna: ").strip()
    print("Pilih peran:")
    for nomor, (_, label) in PERAN_MENU.items():
        print(f"{nomor}. {label}")
    pilihan = input("Nomor peran: ").strip()
    if pilihan not in PERAN_MENU:
        raise SystemExit("Peran tidak valid; gunakan 1 atau 2.")

    password = getpass.getpass("Kata sandi (12–128 karakter): ")
    confirmation = getpass.getpass("Ulangi kata sandi: ")
    if password != confirmation:
        raise SystemExit("Konfirmasi kata sandi tidak cocok.")

    peran, label = PERAN_MENU[pilihan]
    with app.app_context():
        try:
            pengguna_id = services.create_pengguna(username, password, peran)
        except services.ValidationError as error:
            raise SystemExit(str(error)) from error
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed" in str(error):
                raise SystemExit("Nama pengguna tersebut sudah digunakan.") from error
            raise

    print(f"Akun {username} ({label}) berhasil dibuat dengan ID {pengguna_id}.")


if __name__ == "__main__":
    main()
