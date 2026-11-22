# Modul berelasi — bahan pada resep

## Spesifikasi G1–G3

| No. | Fitur kecil | Kriteria penerimaan | Pelaksana |
|---|---|---|---|
| G1 | Daftar bahan pada resep dengan JOIN | Tabel menampilkan nama resep dan nama bahan (bukan hanya ID), jumlah, serta satuan; kondisi kosong memiliki pesan. | Belum ditetapkan |
| G2 | Tambah bahan pada resep | Form menyediakan pilihan resep dan bahan yang tersedia; ID kosong/tidak dikenal dan jumlah bukan angka positif ditolak dengan pesan; isian tetap tampil saat gagal; sukses mengalihkan ke daftar. | Belum ditetapkan |
| G3 | Dampak pada tabel lain | Tidak ada perubahan pada tabel induk atau tabel transaksi. Satu baris asosiasi disimpan di `resep_bahan`; hubungan dijaga oleh FK ke `resep` dan `bahan`. | Belum ditetapkan |

`resep_bahan` dipilih karena merupakan tabel anak dengan FK ke `bahan` (entitas pertama) dan juga ke `resep`. Nama serta jumlah FK berasal dari `docs/desain/schema.sql`. Model tidak memiliki kolom stok atau tanggal; skenario stok dan masukan tanggal pada jobsheet toko tidak berlaku dan tidak ditambahkan.

## Uji masukan form

| No. | Masukan | Hasil yang diharapkan | Hasil aktual |
|---:|---|---|---|
| 1 | Kedua induk valid, jumlah `3`, satuan `buah` | Baris tersimpan dan tampil dengan nama resep/bahan setelah redirect. | Lulus — `tests/test_app.py` |
| 2 | Resep belum dipilih | Ditolak dengan pesan “Pilih resep yang tersedia”; tidak ada baris asosiasi. | Lulus — `tests/test_app.py` |
| 3 | Jumlah `0` atau `-3` | Ditolak dengan pesan jumlah harus positif; tidak ada baris asosiasi. | Lulus — `tests/test_app.py` |
| 4 | Jumlah `abc` | Ditolak dengan pesan jumlah harus berupa angka positif; nilai form tetap tampil. | Lulus — `tests/test_app.py` |
| 5 | Tanggal `10-11-2026` | Tidak berlaku — `resep_bahan` tidak memiliki kolom tanggal. | Tidak dijalankan |
| 6 | ID resep/bahan `999` | Ditolak dengan pesan validasi; tidak ada baris parsial di `resep_bahan`. | Lulus — `tests/test_app.py` |

Jumlah dan satuan tetap opsional karena skema saat ini memperbolehkan `NULL`; apabila jumlah diisi, nilainya wajib angka hingga dan lebih besar dari nol. Tidak ada perubahan stok atau operasi tulis kedua, sehingga transaksi hanya berisi satu `INSERT` di satu koneksi dan FK SQLite memastikan kedua induk ada. Uji penghapusan bahan yang sudah dipakai memastikan FK mencegah penghapusan dan aplikasi menampilkan pesan, bukan galat.

## Catatan pelaksanaan

- Saat modul ini dikerjakan, perubahan dibuat di worktree yang masih memuat CRUD `bahan` belum di-commit. Branch lokal saat itu tertinggal tujuh commit dari `origin/main`; tidak ada pull, push, atau PR pada tahap tersebut. Pekerjaan KF-01 berikutnya dilanjutkan pada branch `fitur/catat-resep`.
- Data resep untuk pilihan form perlu disiapkan terlebih dahulu, karena modul CRUD resep belum tersedia. Uji aplikasi menyiapkan data resep sintetis pada database sementara.
- Pencarian/penyaringan G4 dan langkah Sesi 2 ditunda sesuai cakupan yang dipilih.

## Tinjauan diff lokal

Ini tinjauan mandiri, bukan tinjauan sejawat.

| Pemeriksaan / temuan | Hasil dan tindakan |
|---|---|
| Apakah perubahan dua tabel berada dalam satu transaksi? | Tidak ada perubahan ke dua tabel. Penambahan satu relasi melakukan satu `INSERT` ke `resep_bahan` dalam blok transaksi koneksi; FK menguji keberadaan kedua induk. |
| Apakah ada query di luar `models.py`? | Tidak. Pemeriksaan diff dan pencarian kode menemukan seluruh SQL di `models.py`; route memanggil layanan. |
| Apakah kolom stok hanya berubah lewat transaksi? | Tidak berlaku. Skema resep tidak memiliki kolom stok dan modul ini tidak mengubah stok. |
| Temuan: pilihan resep tidak dapat dibuat dari modul ini. | CRUD resep belum tersedia. Form menampilkan pesan kondisi kosong; uji menyiapkan resep sintetis. Tindak lanjut: siapkan data resep lewat SQLite untuk demonstrasi, atau buat modul resep terpisah setelah disepakati. |
| Temuan: jumlah dan satuan nullable pada skema. | Form tidak memaksakan isian; jika jumlah diisi, aplikasi menolak nilai bukan angka, tak hingga, nol, dan negatif. Tidak mengubah aturan skema. |
| Temuan: jobsheet contoh memakai tanggal dan dampak stok. | Tidak ada kolom tanggal/stok pada model ini. Tidak menambahkan atribut atau efek bisnis yang tidak didukung skema. |
