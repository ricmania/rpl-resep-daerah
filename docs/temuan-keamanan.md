# Temuan keamanan proyek

## Ruang lingkup dan acuan

- `main` ditinjau pada commit `7380d7136f3f023d4696cbb27f00a307dee933cf`. Saat itu branch hanya berisi dokumentasi/skema dan tidak memiliki kode aplikasi, `requirements.txt`, tes cepat, atau laporan keamanan. Tidak ada kerentanan aplikasi yang dapat dikonfirmasi dari `main`.
- Tinjauan implementasi dilakukan secara baca-saja pada `fitur/autentikasi`, commit `3f30d7f`, karena itulah branch berisi aplikasi yang paling dekat dengan target. Hasilnya tidak boleh dianggap sebagai audit atas kode yang sudah tergabung di `main`.
- Kategori menggunakan [OWASP Top 10:2025](https://owasp.org/Top10/2025/). Prioritas prediksi proyek: **A01 Broken Access Control**, **A02 Security Misconfiguration**, dan **A07 Authentication Failures**. A05 Injection dan A09 Security Logging & Alerting Failures juga relevan untuk diperiksa.

## Temuan, triase, dan status

| ID | Kategori OWASP 2025 | Risiko | Temuan dan bukti | Keputusan | Perbaikan / tindak lanjut |
|---|---|---|---|---|---|
| P-01 | A07 Authentication Failures | Sedang | Pada `3f30d7f`, setiap POST login memverifikasi password tanpa penghitung atau batas percobaan. | Diperbaiki | Batasi lima kegagalan per kombinasi alamat dan username selama lima menit; percobaan berikutnya mendapat 429 termasuk bila password benar. Penghitung ada di SQLite dan sidik jari HMAC, bukan alamat/nama asli. |
| P-02 | A02 Security Misconfiguration | Sedang | Pada `3f30d7f`, respons tidak menambahkan `X-Content-Type-Options`, `X-Frame-Options`, atau `Referrer-Policy`. | Diperbaiki | Tambahkan ketiga header di hook respons dan uji pada respons halaman. |
| P-03 | A09 Security Logging & Alerting Failures | Sedang | Pada `3f30d7f`, kegagalan login, CSRF, dan penolakan peran belum menghasilkan peristiwa audit. | Diperbaiki sebagian | Catat peristiwa tanpa password; login memakai sidik jari HMAC dan otorisasi memakai ID/peran/endpoint. Pengumpulan terpusat/alerting belum dikonfigurasi. |
| P-04 | A06 Insecure Design | Sedang — risiko kebutuhan, bukan bypass terbukti | Matriks peran `pengelola`/`pengguna` berasal dari Jobsheet, bukan kebutuhan yang disetujui klien. Hak tulis yang tidak sesuai kebutuhan dapat memberi izin berlebih atau menghalangi pengguna sah. | Ditunda | Minta persetujuan aktor dan izin setiap rute dari kelompok/klien; revisi SRS/matriks dan tes sebelum pemakaian operasional. |
| P-05 | A02 Security Misconfiguration | Sedang — risiko deployment | Cookie Secure bernilai aman secara default, tetapi konfigurasi deployment dapat mengubah `SESSION_COOKIE_SECURE`. | Diperbaiki | Pada `APP_ENV=production`, aplikasi menolak Secure nonaktif, `DEBUG=True`, atau tidak adanya `SECRET_KEY`. Verifikasi HTTPS saat deployment tetap diperlukan. |
| P-06 | A03 Software Supply Chain Failures | Sedang — ketidakpastian, bukan CVE terkonfirmasi | Paket runtime dipin eksak, tetapi pemindai CVE dependensi belum tersedia/dijalankan. | Ditunda | Jalankan `pip-audit` atau pemindai setara di CI sebelum rilis; jangan menyimpulkan paket bebas CVE hanya dari pin versi. |
| P-07 | A01 Broken Access Control | Rendah — penguatan defense-in-depth, bukan bypass terkonfirmasi | CSRF memakai token signed double-submit global pada setiap POST; tidak ada pemeriksaan tambahan `Origin`/`Sec-Fetch-Site`. | Ditunda | Pertahankan pemeriksaan token dan SameSite; minta review implementasi CSRF. Tambahkan pemeriksaan origin bila dibutuhkan threat model dan kompatibilitasnya telah diuji. |

### Keputusan triase

- P-01, P-02, P-03, dan P-05 diperbaiki dalam branch latihan; uji regresi membuktikan reservasi lima percobaan, masa 5 menit, header, log tanpa password, dan penolakan konfigurasi production yang tidak aman.
- P-04 ditunda karena memerlukan keputusan pemilik kebutuhan, bukan perubahan kode sepihak.
- P-06 ditunda karena `pip-audit` tidak terpasang dan tidak ada pemindaian CVE; pin versi saja bukan bukti bebas kerentanan.
- P-07 adalah lapisan penguatan yang belum diimplementasikan; tidak ada bukti bypass token CSRF dalam pengujian saat ini.
- P-03 logging peristiwa ditangani, tetapi alerting/retensi log tetap bergantung pada konfigurasi deployment.
- Tidak ada issue kelompok peninjau yang diberikan pada sesi ini. Tinjauan sejawat dan persetujuan PR masih diperlukan.

## Inventaris kontrol yang diperiksa

- Password: hash scrypt ber-garam; tidak ada kredensial contoh di kode.
- SQL dan HTML: query berparameter dan escaping Jinja; tes input menyerupai SQL disimpan sebagai teks.
- Akses: dekorator memeriksa peran pada rute baca/tulis, termasuk POST; tes guest dan pembaca memeriksa penolakan.
- CSRF: token bertanda tangan diperiksa global untuk POST dan kegagalannya dicatat tanpa isi formulir.
- Redirect login: `next` disaring agar hanya menerima path lokal.
- Dependensi: `requirements.txt` memakai pin versi eksak; `pip-audit` belum tersedia/dijalankan di environment ini. Jadwalkan pemindaian saat alat tersedia.
- Cookie: `HttpOnly`, `SameSite=Lax`, dan Secure aktif; produksi menolak override Secure nonaktif. Validasi HTTPS di deployment belum dilakukan.
- Error: halaman 400/403/404 tidak menampilkan traceback. Uji deployment untuk memastikan mode debug tetap mati di production.

## Log uji defensif lokal

Uji hanya memakai klien Flask dan basis data sementara pada kode proyek sendiri; tidak ada serangan ke aplikasi pihak lain.

| Pemeriksaan | Perintah / tes | Hasil |
|---|---|---|
| Teks mirip SQL diperlakukan sebagai data | `python -m unittest tests.test_app.BahanAppTest.test_sql_injection_text_is_stored_as_data -v` | Lulus; nilai tetap data dan tabel tetap ada. |
| Guest tidak dapat mengubah data | `python -m unittest tests.test_auth.AutentikasiAppTest.test_guest_post_is_redirected_and_does_not_change_data -v` | Lulus; guest dialihkan dan jumlah baris tidak berubah. |
| Redirect eksternal ditolak | `python -m unittest tests.test_auth.AutentikasiAppTest.test_login_ignores_external_and_protocol_relative_next_urls -v` | Lulus; login sukses kembali ke halaman lokal. |
| Percobaan login dan header | `python -m unittest tests.test_auth -v` | Lulus setelah perubahan; mencakup 429, kedaluwarsa lima menit, log, dan header. |

Tes tersebut membuktikan kontrol mitigasi yang diuji, bukan bukti bahwa aplikasi rentan berhasil dieksploitasi.
