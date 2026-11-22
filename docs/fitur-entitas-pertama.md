# Fitur kecil — entitas pertama: bahan

> SRS/PRD yang tersedia tidak menetapkan KF terpisah untuk mengubah atau menghapus bahan. Pemetaan di bawah membedakan kebutuhan tercatat dari kriteria latihan yang masih perlu persetujuan tim/klien.

| No. | Fitur kecil | Kriteria penerimaan | Keterlacakan |
|---|---|---|---|
| F1 | Kerangka proyek Flask | Aplikasi berjalan dengan secret key dari environment; database baru berisi semua tabel pada `docs/desain/schema.sql`. | Pendukung KF-01/KF-02; belum menjadi KF mandiri |
| F2 | Daftar bahan | Tampilkan ID dan nama; tampilkan “Belum ada data bahan” jika tabel kosong. | KF-01 (data bahan resep) dan KF-02 (rincian bahan), usulan |
| F3 | Tambah bahan | Nama kosong ditolak dengan pesan; nilai valid disimpan dan muncul di daftar; nama di-trim. | KF-01; atribut wajib final belum dikonfirmasi |
| F4 | Ubah bahan | Form terisi nilai lama; hanya `nama` dapat diubah; ID/data yang tidak ditemukan memberi 404; nama duplikat diperbolehkan sesuai kamus data. | Tidak ada KF CRUD-edit di SRS; kriteria latihan/proposed |
| F5 | Hapus bahan | Konfirmasi ditampilkan dengan GET; hanya POST menghapus; kegagalan FK menyampaikan bahwa bahan masih digunakan dan tidak menghapus data. | Tidak ada KF CRUD-delete di SRS; kriteria latihan/proposed |

`bahan` dipilih karena tidak memiliki FK ke tabel lain dan merupakan parent untuk `resep_bahan`. Nama bahan **tidak UNIQUE** pada kamus data dan skema rancangan, sehingga penolakan nama duplikat bukan kriteria. Hanya ID dan nama merupakan kolom bahan; ID dibuat otomatis dan tidak dapat diedit. `jumlah` bukan atribut master bahan, sehingga tidak ada isian jumlah pada form CRUD ini.

## Catatan uji masukan create/update

| No. | Masukan uji | Hasil yang diharapkan | Hasil nyata |
|---:|---|---|---|
| 1 | Nama valid, misalnya `Bayam` | Disimpan; pesan sukses; muncul di daftar melalui PRG | Lulus — diverifikasi pada `tests/test_app.py` |
| 2 | Nama kosong/spasi | Ditolak; pesan jelas; nilai form tetap ada; tidak menyimpan baris | Lulus — diverifikasi pada `tests/test_app.py` |
| 3 | Angka negatif pada kolom angka | Tidak berlaku — form bahan tidak memiliki kolom angka yang dapat diubah; ID dibuat otomatis | Tidak dijalankan sebagai masukan data; validasi jumlah negatif diuji terpisah pada `tests/cek_skema.py` untuk `resep_bahan.jumlah` |
| 4 | Teks pada kolom angka | Tidak berlaku — form bahan tidak memiliki kolom angka yang dapat diubah | Tidak berlaku; uji rute ID teks menghasilkan 404 |
| 5 | Nama duplikat | Diterima karena `bahan.nama` tidak UNIQUE dalam kamus/skema | Lulus — diverifikasi pada `tests/test_app.py` |

## Uji tambahan

- Bahan yang tidak direferensikan dapat dihapus.
- GET ke alamat konfirmasi tidak menghapus; POST setelah konfirmasi menghapus.
- Bahan yang dipakai resep tidak terhapus dan pesan penolakan tampil.
- ID yang tidak ditemukan dan ID tidak valid menghasilkan 404.
- Teks injeksi SQL tersimpan sebagai data biasa dan tabel `bahan` tetap ada.
- Masukan HTML ditampilkan ter-escape oleh Jinja2.

Hasil ini adalah hasil uji lokal sintetis, bukan UAT atau persetujuan klien. Hak akses dan atribut wajib bisnis masih menunggu konfirmasi.
