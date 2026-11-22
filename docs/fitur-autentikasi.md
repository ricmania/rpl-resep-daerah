# Fitur latihan — autentikasi dan peran

> Implementasi ini memenuhi Jobsheet autentikasi sebagai prototipe latihan. Autentikasi dan matriks akses belum disepakati klien dan bukan perubahan terhadap kebutuhan KF pada SRS.

## Matriks akses prototipe

| Halaman / aksi | Tamu | Pengelola | Pengguna |
|---|---:|---:|---:|
| Login | ✓ | ✓ | ✓ |
| Daftar bahan, resep, rincian, dan bahan-resep | Login | ✓ | ✓ |
| Tambah, ubah, dan hapus bahan | Login | ✓ | 403 |
| Catat resep dan bahan pada resep | Login | ✓ | 403 |
| Logout melalui POST | Login | ✓ | ✓ |

Pemeriksaan akses dilakukan pada server untuk setiap rute, termasuk POST. Navigasi dan kontrol tindakan disesuaikan dengan peran, tetapi bukan pengganti pemeriksaan server. Peran `pengguna` pada prototipe hanya dapat membaca; kedua peran bukan keputusan klien.

## Kriteria penerimaan

| ID | Fitur kecil | Kriteria penerimaan | Bukti |
|---|---|---|---|
| H1 | Akun dan hash | Username 3–32 karakter, password 12–128 karakter, peran valid; password disimpan sebagai hash scrypt ber-garam, bukan teks atau kredensial contoh di kode. | `tests.test_auth` |
| H2 | Login/logout | Pesan kredensial salah generik; sesi dibersihkan sebelum login dan hanya menyimpan `pengguna_id`; `next` hanya menerima path lokal; logout hanya POST. | `tests.test_auth`, `tests/uji_cepat.py` |
| H3 | Pembatasan peran | Tamu diarahkan ke login, peran tidak berhak mendapat 403, dan akses ditolak juga pada POST tanpa mengubah data. | `tests.test_auth`, `tests/uji_cepat.py` |
| H4 | Navigasi dan tampilan | Semua halaman memakai template induk dan CSS bersama; menu dan aksi tulis hanya terlihat untuk pengelola; halaman 403 menjelaskan penolakan. | Render template pada `tests.test_auth` |
| H5 | Validasi dua lapis | Form memakai atribut HTML yang relevan; layanan tetap memvalidasi nilai yang dikirim langsung dan mengembalikan isian ketika validasi gagal. | `tests.test_app`, `tests.test_auth` |

## Implementasi dan batasan

- Password memakai `werkzeug.security` dengan scrypt. Akun dibuat melalui `buat_pengguna.py`; rahasia diminta secara interaktif.
- Sesi hanya menyimpan ID pengguna; peran dibaca kembali dari basis data pada tiap permintaan.
- POST dilindungi token CSRF bertanda tangan. Token berubah setelah autentikasi dan logout.
- Cookie sesi default memakai `HttpOnly`, `SameSite=Lax`, dan `Secure`; konfigurasi Secure dimatikan hanya pada klien tes lokal.
- Belum ada pembatasan percobaan login, pemulihan akun, atau persetujuan klien atas peran. Lihat [temuan keamanan](./temuan-keamanan.md).
- Belum dilakukan pengujian manual dengan browser/perangkat keyboard atau lebar 360 px; pengujian tersebut tetap perlu dicatat pada checkpoint.

## Penggunaan AI

AI membantu menyusun dan memperbarui rute, templat, validasi, serta tes. Perubahan diperiksa terhadap skema, service, daftar rute, dan hasil tes. Tidak ada kata sandi produksi, data pribadi, atau secret produksi yang digunakan.
