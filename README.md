# rpl-resep-daerah

## Konfigurasi aplikasi

Aplikasi memerlukan `SECRET_KEY` dari environment; tidak ada nilai fallback untuk secret. Pada deployment, simpan kunci acak di secret manager dan jangan commit ke Git.

Konfigurasi yang dipakai:

- `APP_ENV`: `development`, `test`, atau `production` (default `development`).
- `APP_DEBUG`: boolean eksplisit bila debug diperlukan; default `false`. Aplikasi menolak debug pada `production`.
- `SESSION_COOKIE_SECURE`: default `true`; wajib `true` pada `production`.
- `SECRET_KEY`: wajib di semua environment.
- `DATABASE_PATH`: opsional; lokasi basis data SQLite.

Untuk production, gunakan HTTPS dan set `APP_ENV=production`, `APP_DEBUG=false`, serta `SESSION_COOKIE_SECURE=true`. Aplikasi gagal start bila secret tidak ada, debug aktif, atau cookie Secure dimatikan. Pengujian memakai konfigurasi tes terisolasi dan tidak menggambarkan konfigurasi production.

Dependensi runtime dikunci ke versi eksak pada `requirements.txt`. Jalankan `python -m pip install -r requirements.txt` di environment virtual proyek sebelum menjalankan aplikasi atau tes.