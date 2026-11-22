# Daftar halaman dan keterlacakan use case

> Diturunkan dari [SRS](../../srs.md), skenario UC-01–UC-05, dan [kamus data](../kamus-data.md). SRS yang tersedia hanya mendefinisikan KF-01 dan KF-02 sebagai Must; tidak ada KF Should. Dokumen PRD tidak tersedia di workspace. Karena itu, rancangan halaman tidak mengasumsikan fitur di luar dua KF tersebut.

| No. | Halaman | Use case / KF | Aktor | Data yang ditampilkan |
|---:|---|---|---|---|
| 1 | [Login (placeholder; belum menjadi fitur)](./wf-01-login.png) | Tidak ada — autentikasi belum disebut dalam SRS | Belum ditentukan | Tidak membaca atau mengirim data; pemberitahuan bahwa autentikasi belum dirancang |
| 2 | [Beranda](./wf-02-beranda.png) | Titik awal untuk UC-01–UC-05; bukan use case mandiri | Pengelola resep, Pengguna resep | Ringkasan navigasi; tautan ke pencarian dan pencatatan. Tidak menambahkan metrik atau ringkasan data baru |
| 3 | [Daftar dan pencarian resep](./wf-03-daftar-resep.png) | UC-03, UC-04 / KF-02 | Pengguna resep | `resep.id`, `resep.nama`; keadaan tanpa hasil |
| 4 | [Formulir catat resep](./wf-04-form-resep.png) | UC-01, UC-02 / KF-01 | Pengelola resep | `resep.nama`, `bahan.nama`, `resep_bahan.jumlah`, `resep_bahan.satuan`, `langkah_resep.urutan`, `langkah_resep.instruksi` |
| 5 | [Rincian resep](./wf-05-rincian-resep.png) | UC-05 / KF-02 | Pengguna resep | `resep.id`, `resep.nama`, `bahan.nama`, `resep_bahan.jumlah`, `resep_bahan.satuan`, `langkah_resep.urutan`, `langkah_resep.instruksi` |
| 6 | [Daftar bahan](./wf-06-daftar-bahan.png) | Bagian dari alur pencatatan/pembacaan UC-01 dan UC-05 / KF-01, KF-02; halaman entitas `bahan` | Pengelola resep, Pengguna resep | `bahan.id`, `bahan.nama`; pada konteks resep, `resep_bahan.jumlah` dan `resep_bahan.satuan` |
| 7 | [Keadaan validasi dan tanpa hasil](./wf-07-keadaan.png) | Pengecualian UC-02, UC-04 / KF-01, KF-02; keadaan pada formulir dan pencarian, bukan fitur mandiri | Pengelola resep, Pengguna resep | Nama atribut wajib yang belum lengkap; atau kata kunci pencarian dan pesan tanpa hasil |

Semua entitas kamus data terwakili: `resep` pada daftar/rincian/formulir, `bahan` pada daftar bahan, `resep_bahan` pada formulir/rincian, dan `langkah_resep` pada formulir/rincian. Tidak ada use case untuk masuk/login dalam SRS. Login sekarang dibuat sebagai prototipe Jobsheet, tetapi kebutuhan, aktor, hak akses, dan alur autentikasinya tetap harus dikonfirmasi sebelum menjadi fitur produk.

## Hak akses yang dirancang

UC-01 dilakukan oleh Pengelola resep; UC-03–UC-05 oleh Pengguna resep. SRS belum menetapkan apakah Pengelola juga boleh menjadi Pengguna. Implementasi prototipe pada [fitur autentikasi](../../fitur-autentikasi.md) menerapkan matriks latihan, bukan kontrol akses yang telah disetujui klien.
