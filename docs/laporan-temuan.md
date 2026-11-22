# Laporan latihan tinjauan keamanan

## Metadata tinjauan

- Branch latihan: `fitur/perbaikan-keamanan`.
- `main` diperiksa pada `7380d7136f3f023d4696cbb27f00a307dee933cf`; `main` telah sinkron dengan `origin/main`.
- Aplikasi diperiksa secara baca-saja pada `fitur/autentikasi`, commit `3f30d7f`, karena kode aplikasi belum tergabung ke `main`.
- Acuan kategori: [OWASP Top 10:2025](https://owasp.org/Top10/2025/).
- Metode: tinjauan statis dan tes defensif lokal pada aplikasi sendiri. Tidak menjalankan payload pada aplikasi atau pihak lain.

## Prediksi kategori yang relevan

1. **A01 — Broken Access Control:** semua rute dan perubahan data harus memeriksa identitas/peran di server.
2. **A02 — Security Misconfiguration:** secret, cookie, mode debug, dan header browser perlu konfigurasi aman.
3. **A07 — Authentication Failures:** hash password, sesi, dan pembatasan percobaan login menjadi fokus autentikasi.

Kategori tambahan yang juga diperiksa: A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A09 Security Logging & Alerting Failures, dan A10 Mishandling of Exceptional Conditions.

## Latihan kasus sintetis (10 butir)

Lampiran `kasus_rentan.py` tidak terdapat pada repositori atau lampiran yang tersedia. Sesuai izin untuk menentukan isi sendiri, tabel berikut adalah **skenario hipotetis untuk diskusi**, bukan analisis atas file sumber dan bukan kode yang dijalankan. Kolom lokasi menunjuk nomor kasus hipotetis; jangan menafsirkan sebagai lokasi pada aplikasi proyek.

| No. | Masalah pada kasus hipotetis | Kategori OWASP 2025 | Dampak | Risiko |
|---:|---|---|---|---|
| (1) | Query membangun SQL dengan menggabungkan masukan pengguna. | A05 — Injection | Kondisi/query dapat dimanipulasi dan data dapat terbaca atau berubah di luar maksud aplikasi. | Tinggi |
| (2) | Rute perubahan data tidak memeriksa autentikasi dan izin di server. | A01 — Broken Access Control | Pengguna tanpa hak dapat mencoba perubahan data langsung. | Kritis |
| (3) | Tujuan redirect menerima URL eksternal tanpa validasi. | A01 — Broken Access Control | Pengguna dapat diarahkan ke situs penipu melalui alur yang dipercaya. | Sedang |
| (4) | Password disimpan atau dicatat sebagai teks biasa. | A04 — Cryptographic Failures | Kebocoran basis data/log mengungkap kredensial yang dapat digunakan kembali. | Kritis |
| (5) | Form perubahan tidak memiliki perlindungan CSRF. | A01 — Broken Access Control | Browser pengguna yang masuk dapat mengirim perubahan tanpa persetujuan yang dimaksud. | Tinggi |
| (6) | Password di-hash memakai hash cepat tanpa salt khusus password. | A04 — Cryptographic Failures | Password lebih mudah dipulihkan dari dump hash melalui tebakan offline. | Tinggi |
| (7) | Respons kesalahan menampilkan traceback, query, atau lokasi internal. | A10 — Mishandling of Exceptional Conditions | Informasi implementasi membantu penyalahgunaan lanjutan dan mengungkap detail internal. | Sedang |
| (8) | Validasi hanya di browser; server menerima nilai di luar aturan. | A06 — Insecure Design | Data invalid dapat disimpan dengan melewati validasi klien. | Sedang |
| (9) | Login gagal dan akses ditolak tidak tercatat untuk pemantauan. | A09 — Security Logging & Alerting Failures | Percobaan berulang atau penyalahgunaan sulit dideteksi dan ditelusuri. | Sedang |
| (10) | Login tidak membatasi percobaan password berulang. | A07 — Authentication Failures | Tebakan kredensial otomatis dapat berlanjut dan membebani verifikasi password. | Tinggi |

### Lima temuan kasus terpenting

Semua baris di bawah tetap **hipotesis latihan**, bukan temuan pada repositori. Dampak dan remediasi konseptual ditulis supaya kelompok dapat membahas akar penyebab.

| ID | Lokasi | Kategori | Deskripsi | Bukti | Dampak | Risiko | Perbaikan akar masalah | Status |
|---|---|---|---|---|---|---|---|---|
| K-02 | Kasus (2) | A01 — Broken Access Control | Endpoint mutasi tidak menegakkan autentikasi/otorisasi di server. | Skenario sintetis; berkas kasus asli tidak tersedia. Tidak diuji. | Perubahan oleh identitas yang tidak berhak. | Kritis | Terapkan pemeriksaan identitas dan peran di setiap handler, termasuk POST; uji akses allowed/denied. | Contoh pembelajaran saja; bukan kode proyek. |
| K-04 | Kasus (4) | A04 — Cryptographic Failures | Password disimpan dalam bentuk yang dapat dibaca. | Skenario sintetis; berkas kasus asli tidak tersedia. Tidak diuji. | Password terbuka jika basis data/log bocor. | Kritis | Simpan hash password adaptif ber-garam melalui API tepercaya; jangan log password. | Contoh pembelajaran saja; bukan kode proyek. |
| K-01 | Kasus (1) | A05 — Injection | Masukan digabungkan langsung ke SQL. | Skenario sintetis; berkas kasus asli tidak tersedia. Tidak diuji. | Query dan data dapat diakses atau diubah di luar maksud. | Tinggi | Gunakan query berparameter di lapisan model; hindari menyusun SQL dari masukan. | Contoh pembelajaran saja; bukan kode proyek. |
| K-05 | Kasus (5) | A01 — Broken Access Control | Permintaan perubahan tidak memverifikasi token anti-CSRF. | Skenario sintetis; berkas kasus asli tidak tersedia. Tidak diuji. | Browser pengguna dapat dimanfaatkan untuk mengirim perubahan yang tidak dimaksudkan. | Tinggi | Verifikasi token CSRF pada semua metode perubahan dan semua form POST. | Contoh pembelajaran saja; bukan kode proyek. |
| K-10 | Kasus (10) | A07 — Authentication Failures | Login tidak memiliki batas percobaan. | Skenario sintetis; berkas kasus asli tidak tersedia. Tidak diuji. | Tebakan kredensial otomatis tidak diperlambat atau dihentikan. | Tinggi | Terapkan throttling berbatas waktu per alamat dan username, log tanpa password, serta respons 429. | Contoh pembelajaran saja; kontrol serupa ditambahkan ke branch latihan. |

### Catatan evaluasi perbaikan AI

Kasus sumber tidak tersedia, sehingga tidak ada kode rentan yang diklaim telah diperbaiki. Rekomendasi di tabel memperbaiki penyebab (parameterisasi SQL, pemeriksaan izin di server, hash password, token CSRF, dan throttling), bukan sekadar mengubah pesan. Sebelum memakai kode hasil AI, tinjau seluruh rute, semua form, dan lapisan penyimpanan serta jalankan tes regresi. Tidak ada payload serangan atau aplikasi rentan yang dijalankan.

## Bukti defensif pada aplikasi milik proyek

Kode aplikasi belum ada di `main`; bukti berikut dijalankan pada branch proyek sendiri `fitur/perbaikan-keamanan` (yang memuat kode `fitur/autentikasi`), menggunakan test client dan SQLite sementara. Ini memverifikasi kontrol mitigasi, bukan eksploitasi.

| Kategori | Tes yang dijalankan | Hasil |
|---|---|---|
| A05 Injection | `tests.test_app.BahanAppTest.test_sql_injection_text_is_stored_as_data` | Lulus: input mirip SQL diperlakukan sebagai teks biasa. |
| A01 Broken Access Control | `tests.test_auth.AutentikasiAppTest.test_guest_post_is_redirected_and_does_not_change_data` | Lulus: guest dialihkan, data tidak berubah. |
| A01 Broken Access Control | `tests.test_auth.AutentikasiAppTest.test_limited_role_can_read_but_cannot_write_from_get_or_post` | Lulus: peran baca mendapat 403 untuk GET/POST mutasi; data tidak berubah. |
| A01 — redirect lokal | `tests.test_auth.AutentikasiAppTest.test_login_ignores_external_and_protocol_relative_next_urls` | Lulus: target eksternal/protocol-relative tidak digunakan. |

Sebelum perbaikan keamanan tambahan, baseline yang tercatat adalah `35 tests ... OK`; `tests/uji_cepat.py`: `8 tests ... OK` dan `SEMUA UJI LULUS`. Sesudah perubahan pada branch ini, validasi final `python -m unittest discover -s tests -v` menghasilkan **41 tests ... OK**; `python tests/uji_cepat.py` menghasilkan **11 tests ... OK** dan `SEMUA UJI LULUS`; `python tests/cek_skema.py` menolak **semua 5** pelanggaran skema. `git diff --check` juga lulus.

## Tinjauan proyek sendiri — lima temuan

Temuan berikut berasal dari tinjauan baca-saja pada commit `3f30d7f`, **bukan** kondisi `main` pada saat langkah 7. Status diperbarui menurut implementasi branch perbaikan.

| ID | Lokasi pada commit yang ditinjau | Kategori | Deskripsi | Bukti | Dampak | Risiko | Perbaikan | Status |
|---|---|---|---|---|---|---|---|---|
| P-01 | `app.py` login handler; `services.py` autentikasi | A07 — Authentication Failures | Tidak ada pembatasan percobaan login. | Tinjauan statis commit `3f30d7f`; handler melakukan verifikasi password pada setiap POST. | Tebakan password berulang dan biaya scrypt berulang. | Sedang | Lima gagal per 5 menit per pasangan alamat/username; berikutnya 429; expiry dan log diuji. | Diperbaiki pada branch ini. |
| P-02 | `app.py` hook `after_request` | A02 — Security Misconfiguration | Header browser keamanan dasar tidak disetel. | Tinjauan statis commit `3f30d7f`; hook hanya menambahkan cookie CSRF. | Risiko framing/content sniffing dan referrer berlebih. | Sedang | Tambahkan `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`. | Diperbaiki pada branch ini. |
| P-03 | `app.py` login, CSRF, dan decorator peran | A09 — Security Logging & Alerting Failures | Peristiwa keamanan penting belum dicatat. | Tinjauan statis commit `3f30d7f`; tidak ada log untuk login gagal, lockout, CSRF, atau akses ditolak. | Deteksi dan investigasi penyalahgunaan menjadi sulit. | Sedang | Log peristiwa dengan konteks minimum; jangan log password; uji isi log. | Event logging diperbaiki; alerting/retensi terpusat belum dikonfigurasi. |
| P-04 | `docs/fitur-autentikasi.md`, matriks akses | A06 — Insecure Design | Matriks izin adalah asumsi Jobsheet yang belum disetujui klien. | Dokumen sumber menyebut autentikasi/peran belum menjadi kebutuhan SRS. | Izin aktual dapat berbeda dari kebutuhan operasional. | Sedang | Minta persetujuan aktor/izin, perbarui SRS dan tes setelah keputusan diterima. | Ditunda; memerlukan keputusan klien/kelompok. |
| P-05 | `app.py` konfigurasi cookie dan mode | A02 — Security Misconfiguration | Pengaturan cookie/secret/debug perlu gagal-aman pada production. | Default Secure sudah aktif, tetapi deployment dapat mengubah config. | Cookie sesi berisiko dikirim tanpa TLS atau debug membocorkan detail. | Sedang | Wajibkan secret; production menolak Secure nonaktif/debug; dokumentasikan HTTPS. | Diperbaiki pada branch ini; HTTPS deployment belum diverifikasi. |
| P-06 | `requirements.txt` dan pipeline uji | A03 — Software Supply Chain Failures | Versi dependensi dipin eksak tetapi belum dipindai terhadap advisori CVE. | `python -m pip_audit --version` gagal karena modul tidak terpasang; audit tidak dijalankan. | Dependensi yang rentan bisa tidak diketahui sebelum rilis. | Sedang | Jalankan pemindai di CI dan perbarui pin setelah tinjauan kompatibilitas. | Ditunda; catat hasil pemindaian sebelum rilis. |

## Tinjauan diff perbaikan AI

- Pembatasan memakai reservasi atomik SQLite (`BEGIN IMMEDIATE`) untuk lima percobaan per pasangan alamat dan username yang dinormalisasi, dengan fingerprint HMAC; password benar pada percobaan keenam tetap ditolak setelah lima kegagalan.
- Masa batas berakhir setelah 300 detik; login sukses membersihkan hitungan. Penyimpanan batas ada di SQLite agar tidak bergantung pada state proses.
- Log hanya menyertakan fingerprint HMAC atau ID/peran/endpoint; password tidak ditulis.
- Header disetel secara terpusat di response hook. Cookie default aman dan startup production menolak konfigurasi debug/secure yang tidak sesuai.
- Dependensi yang tercantum sudah memiliki versi eksak. Pemindai dependensi `pip-audit` belum dijalankan karena tidak tersedia; hasilnya tidak diklaim.

| Paket yang dipin | Alasan |
|---|---|
| Flask | Framework aplikasi dan routing. |
| Werkzeug | API hash/password dan utilitas yang digunakan Flask. |
| itsdangerous | Tanda tangan token CSRF. |
| Jinja2 | Template HTML yang dirender Flask. |
| MarkupSafe | Escaping template, dependensi Jinja2. |
| click | CLI Flask, dependensi Flask. |
| blinker | Signal Flask, dependensi Flask. |

## Tindak lanjut

- Minta persetujuan matriks peran dan jalankan review silang sejawat.
- Jalankan `pip-audit` pada environment CI atau catat hasil pemindaian sebelum rilis.
- Uji konfigurasi HTTPS, cookie browser, dan tampilan error pada deployment.
- Buat permalink/issue review silang setelah branch kode tersedia pada remote dan review dilakukan.
