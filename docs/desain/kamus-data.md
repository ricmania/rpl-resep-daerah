# Kamus data

> Draf rancangan dari SRS resep. Atribut wajib dan kebijakan data belum divalidasi klien. Lihat [pertanyaan konfirmasi data](./konfirmasi-klien.md). `PK` = kunci utama, `FK` = kunci asing. `INTEGER PRIMARY KEY` SQLite menjadi ID bilangan bulat yang dibuat otomatis. Atribut `jumlah` dan `satuan` adalah usulan untuk rincian bahan dan perlu dikonfirmasi.

## Tabel `resep`

| Nama | Tipe SQLite | Wajib | Kunci | Aturan nilai | Sumber KF |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Dibuat otomatis; tidak boleh NULL. | KF-01 (identitas untuk penyimpanan); KF-02 (membuka resep) |
| `nama` | TEXT | Ya* | — | Setelah `trim`, tidak boleh kosong. Keunikan nama belum ditetapkan. | KF-01 (mencatat nama); KF-02 (menampilkan/mencari resep) |

## Tabel `bahan`

| Nama | Tipe SQLite | Wajib | Kunci | Aturan nilai | Sumber KF |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Dibuat otomatis; tidak boleh NULL. | KF-01 (identitas bahan dalam resep) |
| `nama` | TEXT | Ya* | — | Setelah `trim`, tidak boleh kosong. Keunikan dan penyamaan nama bahan belum ditetapkan. | KF-01 (mencatat bahan); KF-02 (menampilkan rincian bahan) |

## Tabel `resep_bahan`

| Nama | Tipe SQLite | Wajib | Kunci | Aturan nilai | Sumber KF |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Dibuat otomatis; tidak boleh NULL. | KF-01 (menyimpan bahan untuk resep) |
| `resep_id` | INTEGER | Ya | FK → `resep.id` | Harus menunjuk resep yang ada. | KF-01, KF-02 |
| `bahan_id` | INTEGER | Ya | FK → `bahan.id` | Harus menunjuk bahan yang ada. | KF-01, KF-02 |
| `jumlah` | REAL | Tidak | — | Jika diisi, harus lebih besar dari 0. Tipe dan presisi perlu dikonfirmasi. | KF-01 (rincian bahan; usulan) |
| `satuan` | TEXT | Tidak | — | Jika diisi, tidak boleh kosong setelah `trim`. | KF-01 (rincian bahan; usulan) |

## Tabel `langkah_resep`

| Nama | Tipe SQLite | Wajib | Kunci | Aturan nilai | Sumber KF |
|---|---|---|---|---|---|
| `id` | INTEGER | Ya | PK | Dibuat otomatis; tidak boleh NULL. | KF-01 (identitas langkah) |
| `resep_id` | INTEGER | Ya | FK → `resep.id`; bagian dari UK gabungan dengan `urutan` | Harus menunjuk resep yang ada. | KF-01, KF-02 |
| `urutan` | INTEGER | Ya | Bagian dari UK gabungan dengan `resep_id` | Bilangan bulat positif; unik dalam satu resep. | KF-01 (langkah berurutan; usulan pemodelan) |
| `instruksi` | TEXT | Ya* | — | Setelah `trim`, tidak boleh kosong. | KF-01 (mencatat langkah); KF-02 (menampilkan langkah) |

`*` Wajib pada DDL sebagai perlindungan integritas dasar, tetapi daftar atribut wajib bisnis pada SRS belum disepakati. Relasi mengizinkan resep yang sementara belum memiliki baris bahan atau langkah selama proses penyuntingan; syarat kelengkapan saat penyimpanan perlu ditetapkan pada validasi aplikasi setelah konfirmasi.

Tidak ada total, jumlah hasil, atau kolom lain yang nilainya dapat dihitung dari atribut tersimpan.
