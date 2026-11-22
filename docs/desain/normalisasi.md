# Normalisasi data resep

> **Contoh sintetis untuk latihan, bukan dokumen atau data dari klien.** Sumber kebutuhan yang tersedia adalah draf [SRS](../srs.md), khususnya KF-01. Dokumen data mentah klien belum tersedia. Contoh nilai dan pemisahan bahan berikut harus diganti atau divalidasi bersama klien.

## Data mentah tak ternormalisasi (UNF)

Satu baris catatan resep dapat memuat kelompok bahan dan langkah berulang dalam satu sel:

| nama_resep | bahan_dan_jumlah | langkah |
|---|---|---|
| Sayur bening (contoh) | bayam: 1 ikat; jagung: 1 buah; air: 500 ml | Cuci bahan; Rebus air; Masukkan bahan dan masak hingga matang |

Nilai tersebut hanya ilustrasi struktur data, bukan resep klien.

## Bentuk normal pertama (1NF)

Pisahkan nilai kelompok menjadi baris dengan nilai atomik. Untuk memperlihatkan kedua kelompok berulang tanpa menyimpan daftar dalam sel, bentuk datar sementara berikut memakai satu baris per kombinasi bahan dan langkah:

| nama_resep | nama_bahan | jumlah | satuan | urutan_langkah | instruksi |
|---|---|---:|---|---:|---|
| Sayur bening (contoh) | bayam | 1 | ikat | 1 | Cuci bahan |
| Sayur bening (contoh) | bayam | 1 | ikat | 2 | Rebus air |
| Sayur bening (contoh) | jagung | 1 | buah | 1 | Cuci bahan |
| Sayur bening (contoh) | jagung | 1 | buah | 2 | Rebus air |

Baris lain berlanjut untuk semua bahan dan langkah. Setiap sel berisi satu nilai, tetapi bentuk datar ini menduplikasi data resep, bahan, dan langkah. Pasangan bahan-langkah juga membentuk kombinasi yang tidak bermakna sebagai entitas tersendiri. Baris contoh diringkas; tabel produksi tidak perlu membuat kombinasi silang.

## Bentuk normal kedua (2NF)

Pada tabel datar, satu kunci gabungan yang mungkin adalah `(resep, bahan, urutan_langkah)`. Nama resep bergantung hanya pada resep, nama bahan/jumlah/satuan bergantung pada pasangan resep-bahan, sedangkan instruksi bergantung pada resep dan urutan langkah. Ketergantungan parsial ini menyebabkan pengulangan serta anomali pembaruan.

Pisahkan kelompok dengan ketergantungan yang berbeda:

- **RESEP**: satu baris untuk identitas dan nama resep.
- **BAHAN**: satu baris untuk identitas dan nama bahan.
- **RESEP_BAHAN**: satu baris untuk penggunaan bahan pada resep; `jumlah` dan `satuan` adalah atribut hubungan.
- **LANGKAH_RESEP**: satu baris untuk satu langkah dalam resep; `urutan` dan `instruksi` disimpan bersama resep.

Setiap atribut nonkunci sekarang bergantung pada seluruh kunci tabelnya. Di tabel penghubung, `jumlah` dan `satuan` bergantung pada penggunaan bahan dalam suatu resep, bukan hanya pada bahan.

## Bentuk normal ketiga (3NF)

Periksa ketergantungan transitif setelah pemisahan 2NF. Nama bahan hanya berada di BAHAN; instruksi hanya berada di LANGKAH_RESEP; nama resep hanya berada di RESEP. Tabel penghubung tidak menyalin nama resep atau nama bahan. Tidak ada jumlah bahan keseluruhan, total, atau nilai turunan lain yang disimpan.

### Hasil 3NF

| Tabel | Atribut |
|---|---|
| RESEP | `id` (PK), `nama` |
| BAHAN | `id` (PK), `nama` |
| RESEP_BAHAN | `id` (PK), `resep_id` (FK), `bahan_id` (FK), `jumlah`, `satuan` |
| LANGKAH_RESEP | `id` (PK), `resep_id` (FK), `urutan`, `instruksi` |

Hasil ini sama dengan entitas pada [ERD](./erd.mmd), [kamus data](./kamus-data.md), dan [skema SQLite](./schema.sql). Pemodelan kuantitas/satuan sebagai atribut hubungan adalah usulan desain yang perlu dikonfirmasi; SRS belum menentukan detail pencatatan bahan. Aturan atribut wajib, penghapusan, dan retensi juga menunggu konfirmasi klien.
