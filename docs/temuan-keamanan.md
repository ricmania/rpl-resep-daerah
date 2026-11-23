# Temuan keamanan — autentikasi dan otorisasi

| No. | Temuan | Dampak / bukti | Tindakan dan status |
|---:|---|---|---|
| 1 | Belum ada pembatasan percobaan login. | Percobaan password berulang dapat membebani verifikasi scrypt dan meningkatkan peluang tebakan kredensial. | **Ditunda untuk Pertemuan 12.** Tentukan batas, jendela waktu, respons, serta penyimpanan penghitung sebelum menerapkan; jangan mengunci akun permanen sehingga menjadi sarana DoS. |
| 2 | Perlindungan CSRF dibuat khusus dengan cookie bertanda tangan dan token form. | Kesalahan konfigurasi/pemeriksaan pada tiap formulir POST dapat membuka aksi lintas situs. | **Ditangani pada prototipe.** Pemeriksaan konsistensi dan tanda tangan berlaku global untuk POST; token berotasi setelah login/logout. Tes token hilang/palsu dan formulir POST ditambahkan. Minta tinjauan sejawat sebelum penggunaan nyata. |
| 3 | Keamanan cookie bergantung pada konfigurasi deployment. | `SESSION_COOKIE_SECURE` harus aktif agar cookie sesi tidak dikirim lewat HTTP; contoh konfigurasi tes memakai nilai `False`. | **Ditangani dengan default aman, perlu verifikasi deployment.** Nilai default aplikasi `True`; gunakan HTTPS dan jangan menyalin konfigurasi tes ke produksi. Cookie sesi juga `HttpOnly` dan `SameSite=Lax`. |
| 4 | Matriks peran merupakan asumsi Jobsheet, belum kebutuhan yang disetujui. | Jika hak baca/tulis aktual berbeda, akses dapat diberikan kepada peran yang salah. | **Terbuka.** Konfirmasi aktor dan setiap izin dengan kelompok/klien; revisi SRS/matriks sebelum penggunaan operasional. |

Temuan 1 dan 4 belum diselesaikan karena memerlukan keputusan desain/kebutuhan. Implementasi ini adalah latihan, bukan klaim sertifikasi atau kesiapan produksi. Review sejawat belum dilakukan.
