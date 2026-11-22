# Jurnal Vibe Coding

Kesalahan AI yang perlu paling diwaspadai pada rancangan ini adalah menganggap contoh entitas toko dalam panduan sebagai kebutuhan proyek; model diturunkan dari SRS resep dan `jumlah`/`satuan` ditandai sebagai asumsi yang perlu dikonfirmasi.

Pada rancangan antarmuka, kesalahan AI yang perlu dihindari adalah menyajikan login atau ambang jumlah sebagai kebutuhan klien padahal belum ada di SRS; keduanya ditandai sebagai placeholder/asumsi sampai dikonfirmasi. Pelajaran dari review silang belum dicatat karena review belum dilakukan.

## Jurnal pengujian

### Entri 1 — Draf test case berbasis kebutuhan yang tersedia

- **Prompt/ringkasan tugas:** susun pytest dari SRS dan skema di branch `main`, dengan fixture database sementara; jangan mengarang fungsi aplikasi yang tidak tersedia.
- **Draf AI:** mengusulkan pengujian batas dan constraint SQLite yang ada serta menandai alur KF-02 sebagai tertunda karena kode aplikasi dan aturan pencarian tidak tersedia.
- **Pemeriksaan manusia:** sesuai, namun test tingkat HTTP/client, akun, dan token CSRF tidak dapat dibuat tanpa aplikasi. PRD juga tidak ada; hanya KF-01 dan KF-02 yang boleh dimasukkan.
- **Keputusan:** ubah cakupan menjadi validasi skema terisolasi dan catat kesenjangan secara eksplisit.

### Entri 2 — Pemeriksaan independen dan mutasi

- **Pemeriksaan mandiri:** uji integritas skema menggunakan nilai tepi dan masukan salah, bukan hanya memeriksa bahwa query berhasil.
- **Temuan awal eksploratif:** SQLite menerima teks nonangka pada `REAL`, pecahan/teks pada `INTEGER`, dan BLOB pada kolom `TEXT`; reproduksi dilakukan pada database sementara.
- **Koreksi uji:** tambahkan asersi yang mensyaratkan tipe SQLite dan hasil penolakan, kemudian validasi dengan varian skema termutasi sebelum menyatakan uji menangkap regresi.
- **Hasil merah awal:** `python -m pytest -q tests/test_validasi.py` menghasilkan 7 gagal dan 25 lulus. Kegagalan tepat pada tipe yang disebut di atas; uji skema yang ada tetap menolak empat pelanggaran yang diperiksanya.
- **Batasan:** mutasi `services.py` tidak dapat dilakukan pada branch `main` karena file itu tidak ada. Hasil uji mutasi skema dicatat terpisah.
