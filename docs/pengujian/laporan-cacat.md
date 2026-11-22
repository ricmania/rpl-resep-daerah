# Laporan Cacat Pengujian

> Pemeriksaan eksploratif dibatasi pada `docs/desain/schema.sql` di branch `main`, menggunakan SQLite sementara dan data sintetis. Tiga temuan di bawah adalah perilaku yang berhasil direproduksi; tidak ada klaim tentang rute aplikasi karena aplikasi belum tersedia pada branch ini.

| ID | Langkah reproduksi | Aktual | Diharapkan | Keparahan | Prioritas | Status |
|---|---|---|---|---|---|---|
| D-01 | Buat skema; buat resep dan bahan; masukkan `jumlah='abc'` ke `resep_bahan`. | SQLite menerima nilai teks `abc` pada kolom `REAL` karena perbandingan CHECK dinamis tidak menolaknya. | Jumlah hanya NULL atau angka positif. | Sedang | P1 | Diperbaiki: CHECK mewajibkan kelas tipe numerik. |
| D-02 | Buat resep; masukkan langkah dengan `urutan=1.5` atau `urutan='abc'`. | SQLite menerima nilai pecahan dan teks pada kolom berafinitas `INTEGER`. | Urutan harus bilangan bulat positif. | Sedang | P1 | Diperbaiki: CHECK mewajibkan kelas tipe integer. |
| D-03 | Masukkan `sqlite3.Binary(b'Nama')` pada `resep.nama` (juga dapat dicoba pada kolom teks lain). | BLOB diterima pada kolom berafinitas `TEXT`; pemeriksaan tidak mengunci kelas tipe. | Kolom teks hanya menerima nilai TEXT nonkosong. | Sedang | P1 | Diperbaiki: CHECK mengunci tipe TEXT pada semua kolom teks. |

Ketiga temuan menunjukkan keterbatasan yang sama pada penggunaan afinitas tipe SQLite, tetapi masing-masing mempunyai masukan reproduksi dan uji regresi terpisah. Hasil awal direproduksi di database `:memory:` dan akan dicatat kembali melalui pytest sebelum/sesudah perbaikan. Temuan baru berstatus diperbaiki setelah test regresi lulus dan commit tercatat.

## Permintaan perubahan

- Belum ada permintaan perubahan yang dapat dikonfirmasi. Aturan wajib nama/jumlah dan semantik pencarian perlu disepakati dari PRD/klien; jangan menganggap asumsi teknis sebagai permintaan perubahan.

## Batas pemeriksaan

- Tidak ada tiga cacat aplikasi/UI yang diklaim; `main` tidak memiliki `app.py`, `services.py`, atau client HTTP.
- Perubahan skema perlu diuji terhadap basis data baru. Migrasi data persisten dan kompatibilitas data lama belum termasuk.
