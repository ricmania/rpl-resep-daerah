# Fitur KF-01 — catat resep

## Dasar dan cakupan

Fitur berikutnya yang belum ada adalah KF-01 (Must usulan), sesuai backlog yang tersedia pada branch dokumentasi: menyimpan nama resep, bahan, dan langkah. Form mengikuti wireframe catat resep dan keadaan validasi dari Jobsheet 7. Pencarian tidak termasuk cakupan fitur ini.

Kriteria atribut wajib bisnis pada PRD/SRS belum disepakati kelompok atau klien. Untuk prototipe ini, pengguna memilih aturan sementara: **nama wajib, minimal satu bahan, dan minimal satu langkah**. Ini keputusan implementasi prototipe, bukan persetujuan klien. Jumlah dan satuan bahan tetap opsional sesuai skema; bila jumlah diisi, nilainya harus angka hingga lebih besar dari nol.

## Kriteria penerimaan yang diuji

| ID | Given / When | Then | Uji |
|---|---|---|---|
| KF-01-01 | Nama, bahan yang ada, dan minimal satu langkah valid diisi; pengelola menyimpan. | Resep, rincian bahan, dan langkah tersimpan bersama; aplikasi mengalihkan ke rincian resep dan menampilkan pesan sukses. | `test_create_recipe_saves_ingredients_and_ordered_steps`; `tests/uji_cepat.py` |
| KF-01-02 | Nama kosong, bahan tidak dipilih, langkah kosong, atau jumlah tidak valid. | Form menampilkan pesan yang sesuai, mempertahankan isian, dan tidak menyimpan sebagian data. | `test_incomplete_recipe_is_rejected_without_saving_and_preserves_input` |
| KF-01-03 | Salah satu FK anak gagal saat penyimpanan multi-tabel. | Transaksi dibatalkan dan baris resep induk tidak tertinggal. | `test_recipe_save_rolls_back_parent_when_child_foreign_key_fails` |
| KF-01-04 | Resep berhasil disimpan. | Tersedia daftar dan halaman rincian berisi nama, bahan, jumlah/satuan yang diketahui, serta langkah berurutan. | `test_recipe_list_shows_empty_state_and_missing_detail_is_404`; `test_create_recipe_saves_ingredients_and_ordered_steps` |

## Pelaksanaan dan batasan

- Semua SQL tetap berada di `models.py`; resep, rincian bahan, dan langkah disimpan pada satu koneksi dan satu transaksi.
- Form mengambil bahan yang sudah ada. Jika belum ada, pengguna diarahkan untuk membuat bahan lebih dahulu.
- `jumlah` dan `satuan` tidak dipaksakan menjadi wajib karena kamus data/skema memperbolehkan NULL.
- Login dan otorisasi sekarang diterapkan terpisah sebagai prototipe Jobsheet; keduanya belum disetujui klien dan bukan bagian dari KF-01. Pencarian serta keputusan atribut wajib final masih tertunda.
- Data pengujian berada pada SQLite sementara; tidak memakai basis data aplikasi.
