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
- **Koreksi uji:** tambahkan asersi yang mensyaratkan tipe SQLite dan hasil penolakan. Suite akhir berisi 33 kasus parametrik pada 12 fungsi, semuanya lulus.
- **Hasil merah awal:** `python -m pytest -q tests/test_validasi.py` menghasilkan 7 gagal dan 25 lulus. Kegagalan tepat pada tipe yang disebut di atas; uji skema yang ada tetap menolak empat pelanggaran yang diperiksanya.
- **Mutasi 1 — jumlah:** pemeriksaan `typeof(jumlah)` dihapus sementara; `pytest -k jumlah` menangkap 1 kasus gagal dan 4 lulus. Perubahan dikembalikan.
- **Mutasi 2 — urutan:** pemeriksaan tipe integer dihapus sementara; `pytest -k urutan` menangkap 2 kasus gagal dan 4 lulus. Perubahan dikembalikan.
- **Mutasi 3 — kolom teks:** pemeriksaan tipe TEXT pada nama resep dihapus sementara; `pytest -k nama_resep` menangkap 1 kasus gagal dan 5 lulus. Perubahan dikembalikan.
- **Batasan:** mutasi `services.py` tidak dapat dilakukan pada branch `main` karena file itu tidak ada; mutasi dilakukan pada constraint skema yang memang tersedia.

### Entri 3 — Pemeriksaan basis awal

- **Observasi:** `fitur/pengujian` berbasis `main`; file aplikasi dan `tests/uji_cepat.py` tidak ada. Perintah uji cepat gagal karena file tidak ditemukan.
- **Bukti yang tersedia:** `tests/cek_skema.py` berjalan dan empat pelanggaran DDL ditolak.
- **Keputusan:** pertahankan basis `main` sesuai arahan; jangan menyalin implementasi aplikasi dari branch lain karena akan mengubah basis/scope PR.

### Entri 4 — Perbaikan D-01: tipe jumlah

- **Merah:** kasus `jumlah='abc'` tidak menghasilkan `IntegrityError`.
- **Perbaikan:** CHECK hanya menerima NULL atau kelas numerik positif.
- **Hijau/commit:** lima uji jumlah lulus; perubahan dicatat pada commit `cb4c41e`.

### Entri 5 — Perbaikan D-02: tipe urutan

- **Merah:** nilai `1.5` dan `abc` lolos pada kolom berafinitas INTEGER.
- **Perbaikan:** CHECK mensyaratkan `typeof(urutan)='integer'` dan nilai positif.
- **Hijau/commit:** enam uji urutan lulus; perubahan dicatat pada commit `0161824`.

### Entri 6 — Perbaikan D-03: kolom teks

- **Merah:** SQLite menerima BLOB pada kolom berafinitas TEXT.
- **Perbaikan:** semua kolom teks nonkosong memeriksa `typeof(...)='text'`; satuan opsional tetap mengizinkan NULL.
- **Hijau/commit:** 19 uji nama, satuan, dan instruksi lulus; perubahan dicatat pada commit `bd2a535`.

### Entri 7 — Uji regresi

- **Hasil:** `pytest -q tests` lulus 33 kasus pada 12 fungsi uji; `tests/cek_skema.py` menolak empat pelanggaran; `git diff --check` bersih.
- **Batas:** semua bukti ini menguji skema SQLite sementara, bukan route HTTP atau aplikasi yang belum tersedia di `main`.

### Entri 8 — Rencana UAT

- **Hasil:** draf lima skenario KF-01/KF-02 dan kriteria lulus dibuat di `docs/pengujian/rencana-uat.md`.
- **Belum selesai:** klien belum dimintai konfirmasi; tanggal, tempat, peserta, dan durasi belum disepakati. Tidak ada persetujuan klien yang diklaim.

### Entri 9 — Kesenjangan review

- **Temuan:** PRD, daftar KF tambahan, aplikasi di `main`, dan balasan klien tidak tersedia. Target enam KF dan uji HTTP tidak dapat dibuktikan dari materi saat ini.
- **Kualitas AI:** mutasi yang dibuat untuk pemeriksaan tipe memang tertangkap pytest; belum ada pemeriksaan independen anggota. Tidak diklaim bahwa manusia menemukan kelemahan yang tidak ditemukan AI, dan rasio Terima/Ubah/Tolak masih menunggu review manusia.
