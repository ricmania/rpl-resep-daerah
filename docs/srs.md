# Software Requirements Specification (SRS)

> **Status: draf latihan.** Kebutuhan berikut berasal dari usulan pada PRD dan skenario simulasi, bukan hasil validasi klien. Status dan rincian masih perlu dikonfirmasi sebelum menjadi komitmen implementasi.

## 1. Tujuan dan lingkup

Dokumen ini merangkum kebutuhan fungsional awal untuk mencatat, menemukan, dan membaca resep. Kebutuhan Must yang dirujuk pemodelan adalah usulan KF-01 dan KF-02.

## 2. Kebutuhan fungsional

### KF-01 — Mencatat resep

**Prioritas:** Must (usulan)

**Deskripsi:** Pengelola resep dapat mencatat nama resep, bahan, dan langkah. Atribut wajib resep belum ditetapkan.

**Kriteria penerimaan**

1. Given semua atribut yang telah disepakati sebagai wajib sudah diisi, When pengelola menyimpan resep, Then resep tersimpan dengan nilai yang dimasukkan.
2. Given satu atau lebih atribut wajib yang telah disepakati belum diisi, When pengelola mencoba menyimpan resep, Then sistem menunjukkan atribut yang belum lengkap dan tidak menyimpan resep.

### KF-02 — Menemukan dan membaca resep

**Prioritas:** Must (usulan)

**Deskripsi:** Pengguna dapat menemukan resep tersimpan dan membaca rincian nama, bahan, dan langkah. Bidang pencarian dan aturan kecocokan belum ditetapkan.

**Kriteria penerimaan**

1. Given ada resep yang cocok menurut bidang dan aturan pencarian yang disepakati, When pengguna mengirim kata kunci, Then sistem menampilkan resep yang cocok.
2. Given tidak ada resep yang cocok menurut aturan pencarian yang disepakati, When pengguna mengirim kata kunci, Then sistem menampilkan keadaan tanpa hasil.
3. Given resep tersimpan, When pengguna membuka resep tersebut, Then nama, bahan, dan langkah milik resep itu ditampilkan.

## 3. Pemodelan

- [Skenario use case](./uml/skenario-use-case.md) — UC-01 sampai UC-05 untuk kebutuhan Must.
- [Diagram use case (Mermaid)](./uml/use-case.mmd) — ringkasan aktor dan use case.

Pemodelan hanya merinci alur pencatatan, validasi kelengkapan atribut wajib, pencarian, hasil tanpa kecocokan, dan pembacaan rincian. Alur tersebut tercakup oleh KF-01 dan KF-02; pemodelan tidak mengidentifikasi kebutuhan fungsional baru.

## 4. Matriks keterlacakan

| ID kebutuhan | Prioritas | Sumber/kriteria yang ditelusuri | Use case |
|---|---|---|---|
| KF-01 | Must (usulan) | PRD M1; menyimpan resep dengan atribut wajib lengkap; memberi tahu atribut wajib yang belum lengkap dan tidak menyimpan resep. | [UC-01](./uml/skenario-use-case.md#uc-01--mencatat-resep-dengan-informasi-wajib-lengkap), [UC-02](./uml/skenario-use-case.md#uc-02--menangani-resep-dengan-atribut-wajib-belum-lengkap) |
| KF-02 | Must (usulan) | PRD M2; menampilkan resep yang cocok; menampilkan keadaan tanpa hasil; menampilkan nama, bahan, dan langkah resep yang dibuka. | [UC-03](./uml/skenario-use-case.md#uc-03--menemukan-resep-yang-cocok-dengan-kata-kunci), [UC-04](./uml/skenario-use-case.md#uc-04--mendapatkan-keadaan-tanpa-hasil-pencarian), [UC-05](./uml/skenario-use-case.md#uc-05--membaca-rincian-resep-yang-ditemukan) |

## 5. Hal yang perlu dikonfirmasi

- Atribut wajib dan opsional resep.
- Bidang pencarian serta aturan kecocokan kata kunci.
- Pengguna dan hak akses untuk mencatat, mencari, dan membaca resep.
- Persetujuan prioritas Must dan kriteria penerimaan oleh kelompok dan klien.
