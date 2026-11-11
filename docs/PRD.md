# PRD — Aplikasi Pengelolaan Resep Daerah

> **Status: draf latihan untuk ditinjau.** Belum ada catatan wawancara nyata; SRS dan product backlog juga belum terisi. Isi dan urutan prioritas di bawah merupakan usulan dari simulasi Persona 1, bukan keputusan klien atau komitmen implementasi. Konfirmasikan dengan kelompok dan klien sebelum membuat kode.

## 1. Ringkasan produk dan tujuan

Draf ini menggambarkan aplikasi untuk mencatat dan menemukan resep, serta menghubungkan foto dengan resep. Arah latihan ini berangkat dari simulasi tentang catatan resep di beberapa media dan kesulitan menemukan resep lama; tujuan dan bentuk produk masih perlu divalidasi dengan klien.

## 2. Pengguna dan peran

Peran berikut adalah hipotesis kerja, bukan hak akses yang telah disepakati.

| Peran sementara | Kegiatan yang diusulkan                                            |
| --------------- | ------------------------------------------------------------------ |
| Pengelola resep | Mencatat dan memperbarui resep serta mengaitkan foto dengan resep. |
| Pembaca resep   | Melihat, mencari, dan membaca resep.                               |

Apakah aplikasi berbentuk web, apakah perlu dua peran berbeda, dan batas aksesnya masih terbuka.

## 3. Fitur berdasarkan prioritas usulan

Prioritas berikut adalah pengelompokan untuk latihan saja. Klien dan kelompok belum menyetujuinya; urutan ini tidak boleh dianggap sebagai ruang lingkup implementasi final.

### Must — usulan untuk divalidasi

**M1. Mencatat resep** — Pengelola dapat mencatat nama resep, bahan, dan langkah. Daftar atribut wajib belum disepakati.

- **Given** semua atribut yang telah disepakati sebagai wajib sudah diisi, **When** pengelola menyimpan resep, **Then** resep tersimpan dengan nilai yang dimasukkan.
- **Given** satu atau lebih atribut wajib yang telah disepakati belum diisi, **When** pengelola mencoba menyimpan resep, **Then** sistem menunjukkan atribut yang belum lengkap dan tidak menyimpan resep.

**M2. Menemukan dan membaca resep** — Pengguna dapat menemukan resep tersimpan dan membaca rincian nama, bahan, dan langkah. Bidang yang dicari dan aturan kecocokan belum ditetapkan.

- **Given** ada resep yang cocok menurut bidang dan aturan pencarian yang nantinya disepakati, **When** pengguna mengirim kata kunci, **Then** sistem menampilkan resep yang cocok.
- **Given** tidak ada resep yang cocok menurut aturan pencarian yang disepakati, **When** pengguna mengirim kata kunci, **Then** sistem menampilkan keadaan tanpa hasil.
- **Given** resep tersimpan, **When** pengguna membuka resep tersebut, **Then** nama, bahan, dan langkah milik resep itu ditampilkan.

### Should — usulan untuk divalidasi

**S1. Memperbarui takaran resep** — Pengelola dapat menyimpan koreksi takaran pada resep.

- **Given** pengelola memasukkan koreksi takaran pada resep, **When** ia menyimpan perubahan, **Then** nilai takaran yang baru tersimpan pada resep itu.
- **Given** perubahan takaran telah tersimpan, **When** resep dibuka kembali, **Then** takaran terbaru ditampilkan.

**S2. Mengaitkan foto dengan resep** — Pengelola dapat mengaitkan foto yang dipilih dengan resep.

- **Given** pengelola memilih resep dan sebuah foto, **When** ia menyimpan kaitan tersebut, **Then** foto tercatat sebagai milik resep yang dipilih.
- **Given** foto telah dikaitkan dengan resep, **When** pengguna membuka resep itu, **Then** foto yang ditampilkan berasal dari kaitan resep tersebut.

## 4. Data awal

Entitas berikut adalah rancangan awal untuk dibahas, bukan skema yang telah disetujui. ERD lengkap direncanakan kemudian.

| Entitas sementara | Atribut kandidat                               |
| ----------------- | ---------------------------------------------- |
| Resep             | ID, nama, waktu dibuat/diubah.                 |
| Bahan resep       | ID resep, nama bahan, jumlah, satuan.          |
| Langkah resep     | ID resep, urutan, uraian.                      |
| Foto resep        | ID resep, rujukan berkas, keterangan opsional. |

Keharusan atribut, format/ukuran foto, penyimpanan berkas, dan kebutuhan riwayat perubahan belum diputuskan.

## 5. Di luar lingkup implementasi draf

- **Could — kandidat, belum diprioritaskan:** Penghitungan ulang takaran untuk jumlah sajian berbeda. Ini hanya ide dari simulasi; kebutuhan dan aturan hitung belum dikonfirmasi.
- **Integrasi chat:** Belum didefinisikan sebagai fitur dalam draf ini. Ini bukan keputusan Won’t; perlu ditanyakan apakah integrasi dibutuhkan atau pencatatan manual sudah cukup.

Tidak ada keputusan Won’t dari klien yang tercatat saat ini.

## 6. Pertanyaan terbuka untuk klien dan kelompok

1. Apakah produk yang dibutuhkan berupa aplikasi web? Siapa pengguna sebenarnya, dan apakah ada peran serta batas akses yang berbeda?
2. Apakah usulan prioritas Must/Should di atas sesuai? Fitur mana yang benar-benar harus dikerjakan pada versi ini?
3. Informasi apa yang wajib dan opsional pada resep, termasuk jumlah sajian, jumlah bahan, dan satuan?
4. Bidang resep apa yang harus dicari, bagaimana aturan kecocokan, dan informasi apa yang ditampilkan pada hasil?
5. Siapa yang boleh mengoreksi takaran? Apakah nilai lama atau riwayat perubahan perlu dipertahankan?
6. Apakah foto perlu diunggah atau cukup dirujuk? Format/ukuran apa yang didukung, dan siapa yang boleh melihat atau mengubahnya?
7. Apakah penghitungan ulang takaran diperlukan? Jika ya, apa aturan jumlah sajian, satuan, dan pembulatan?
8. Apakah integrasi chat diperlukan, atau cukup mencatat resep yang diterima melalui chat?
9. Apakah ada fitur yang secara eksplisit tidak akan dikerjakan (Won’t) pada versi ini?
