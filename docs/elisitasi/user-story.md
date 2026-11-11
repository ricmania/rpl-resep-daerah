# User Story — Draf Latihan Persona 1

> **Status:** Draf latihan, bukan kebutuhan hasil wawancara nyata. Saat ini `catatanwawancara.md` hanya berisi draf pesan izin dan simulasi Persona 1. Semua story di bawah ditandai `[Asumsi]` dan harus dikonfirmasi kepada calon klien sebelum dianggap sebagai kebutuhan.

## Rumusan kebutuhan sementara

Berikut interpretasi sementara dari simulasi Persona 1, bukan kebutuhan klien yang telah divalidasi:

- **[Asumsi]** Menghimpun rincian resep yang saat ini dicatat di media berbeda. Sumber: S1 dan S3.
- **[Asumsi]** Menemukan dan membaca kembali resep yang sudah dicatat dengan lebih mudah. Sumber: S2 dan S3.
- **[Asumsi]** Mencatat koreksi takaran pada resep dan memeriksa takaran yang tersimpan. Sumber: S4.
- **[Asumsi]** Mencocokkan foto hasil masakan dengan resep terkait. Sumber: S5.
- **[Asumsi]** Menyesuaikan takaran resep untuk jumlah sajian yang berbeda. Sumber: S6.

## Daftar user story

### US-01 — [Asumsi] Mencatat informasi resep

Sebagai pengelola dokumentasi resep, saya ingin mencatat nama resep, bahan, dan langkahnya agar informasi resep tersimpan sebagai satu catatan.

**Kriteria penerimaan**

1. Given nama, bahan, dan langkah resep telah diisi, When pengelola menyimpan resep, Then satu catatan resep tersimpan dengan informasi yang dimasukkan.
2. Given nama, bahan, atau langkah resep belum diisi, When pengelola mencoba menyimpan resep, Then sistem menunjukkan informasi yang belum diisi dan resep tidak tersimpan.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S1 (simulasi; belum dikonfirmasi).

### US-02 — [Asumsi] Mencatat resep baru yang diterima lewat chat

Sebagai pengelola dokumentasi resep, saya ingin memasukkan rincian resep baru yang diterima lewat chat ke catatan resep agar resep tersebut tidak hanya berada di percakapan.

**Kriteria penerimaan**

1. Given pengelola memiliki rincian resep baru dari chat, When ia memasukkan dan menyimpan rincian tersebut, Then catatan resep baru tersedia di kumpulan resep.
2. Given rincian resep dari chat telah disimpan, When pengelola membuka catatan itu, Then rincian yang dimasukkan dapat dibaca kembali.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S1 (simulasi; belum dikonfirmasi).

### US-03 — [Asumsi] Menghimpun resep dalam satu kumpulan

Sebagai pengelola dokumentasi resep, saya ingin melihat resep yang sudah dicatat dalam satu kumpulan agar tidak perlu mencarinya di beberapa media.

**Kriteria penerimaan**

1. Given resep telah disimpan, When pengelola membuka kumpulan resep, Then resep tersebut muncul dalam kumpulan.
2. Given resep dicatat dari sumber yang berbeda, When pengelola membuka kumpulan resep, Then semua resep yang tersimpan muncul di kumpulan yang sama.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S1 dan S3 (simulasi; S3 mengusulkan website).

### US-04 — [Asumsi] Mencari resep

Sebagai pengelola dokumentasi resep, saya ingin mencari resep dengan kata kunci agar lebih mudah menemukan resep yang tersimpan.

**Kriteria penerimaan**

1. Given kumpulan resep memiliki resep yang cocok dengan kata kunci, When pengelola mencari menggunakan kata kunci tersebut, Then resep yang cocok ditampilkan.
2. Given tidak ada resep yang cocok dengan kata kunci, When pengelola melakukan pencarian, Then sistem menunjukkan bahwa tidak ada resep yang cocok.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S2 dan S3 (simulasi; belum dikonfirmasi).

### US-05 — [Asumsi] Menelusuri kumpulan resep

Sebagai pengelola dokumentasi resep, saya ingin melihat daftar resep yang tersimpan agar dapat memilih resep yang ingin saya periksa.

**Kriteria penerimaan**

1. Given ada resep yang tersimpan, When pengelola membuka daftar resep, Then daftar menampilkan resep-resep tersebut.
2. Given daftar resep ditampilkan, When pengelola memilih satu resep, Then catatan resep yang dipilih terbuka.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S2 dan S3 (simulasi; daftar sebagai cara penelusuran adalah asumsi).

### US-06 — [Asumsi] Membaca rincian resep

Sebagai pengelola dokumentasi resep, saya ingin melihat bahan dan langkah resep dalam satu catatan agar dapat memeriksa informasi resep.

**Kriteria penerimaan**

1. Given catatan resep memiliki bahan dan langkah, When pengelola membuka catatan, Then bahan dan langkah ditampilkan bersama resep tersebut.
2. Given pengelola membuka resep yang berbeda, When rincian ditampilkan, Then bahan dan langkah yang terlihat berasal dari resep yang dipilih.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S1 (simulasi; belum dikonfirmasi).

### US-07 — [Asumsi] Mencatat koreksi takaran

Sebagai pengelola dokumentasi resep, saya ingin memperbarui takaran yang telah dikoreksi agar catatan resep mencerminkan koreksi tersebut.

**Kriteria penerimaan**

1. Given catatan resep memiliki takaran yang perlu dikoreksi, When pengelola memasukkan takaran koreksi dan menyimpan perubahan, Then catatan resep menyimpan takaran yang baru.
2. Given takaran koreksi telah disimpan, When pengelola membuka kembali resep, Then takaran yang ditampilkan sama dengan takaran koreksi.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S4 (simulasi; belum dikonfirmasi).

### US-08 — [Asumsi] Memeriksa takaran resep setelah koreksi

Sebagai pengelola dokumentasi resep, saya ingin dapat memeriksa takaran yang saat ini tercatat agar tidak mengandalkan pesan koreksi yang terpisah.

**Kriteria penerimaan**

1. Given takaran resep telah diperbarui, When pengelola melihat rincian resep, Then takaran yang ditampilkan adalah takaran terkini yang tersimpan.
2. Given takaran resep belum diperbarui, When pengelola melihat rincian resep, Then sistem menampilkan takaran yang saat ini tersimpan tanpa mengubahnya.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S4 (simulasi; belum dikonfirmasi; batas antara US-07 dan US-08 perlu divalidasi).

### US-09 — [Asumsi] Menghubungkan foto dengan resep

Sebagai pengelola dokumentasi resep, saya ingin mengaitkan foto hasil masakan dengan resep yang sesuai agar keduanya mudah dicocokkan.

**Kriteria penerimaan**

1. Given resep telah tersimpan dan pengelola memilih foto, When pengelola mengaitkan foto dengan resep tersebut, Then foto tersimpan sebagai bagian dari resep yang dipilih.
2. Given foto telah dikaitkan dengan satu resep, When pengelola membuka resep lain, Then foto tersebut tidak ditampilkan sebagai foto resep lain yang tidak dipilih.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S5 (simulasi; belum dikonfirmasi).

### US-10 — [Asumsi] Melihat foto dari catatan resep

Sebagai pengelola dokumentasi resep, saya ingin melihat foto yang terkait dengan resep agar dapat mencocokkan foto dan resep.

**Kriteria penerimaan**

1. Given resep memiliki foto terkait, When pengelola membuka resep, Then foto terkait dapat dilihat dari catatan resep tersebut.
2. Given resep tidak memiliki foto terkait, When pengelola membuka resep, Then sistem tidak menampilkan foto dari resep lain sebagai foto resep tersebut.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S5 (simulasi; belum dikonfirmasi).

### US-11 — [Asumsi] Menentukan jumlah sajian tujuan

Sebagai pengguna resep, saya ingin memasukkan jumlah sajian yang diinginkan agar takaran resep dapat disesuaikan.

**Kriteria penerimaan**

1. Given resep memiliki jumlah sajian awal, When pengguna memasukkan jumlah sajian tujuan yang valid, Then jumlah sajian tujuan digunakan untuk penyesuaian takaran.
2. Given jumlah sajian tujuan kosong atau bukan bilangan positif, When pengguna meminta penyesuaian, Then sistem meminta jumlah sajian yang valid dan tidak menampilkan hasil penyesuaian.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S6 (simulasi; input jumlah sajian adalah asumsi yang perlu dikonfirmasi).

### US-12 — [Asumsi] Menghitung ulang takaran berdasarkan jumlah sajian

Sebagai pengguna resep, saya ingin takaran dihitung ulang berdasarkan jumlah sajian tujuan agar dapat menggunakan resep dengan jumlah sajian berbeda.

**Kriteria penerimaan**

1. Given resep memiliki takaran awal dan jumlah sajian awal, When pengguna meminta takaran untuk jumlah sajian tujuan, Then setiap takaran dihitung dengan rumus takaran awal × jumlah sajian tujuan ÷ jumlah sajian awal.
2. Given jumlah sajian tujuan sama dengan jumlah sajian awal, When pengguna meminta penghitungan ulang, Then setiap takaran hasil sama dengan takaran awal.

**Sumber:** [catatanwawancara.md](./catatanwawancara.md), Lampiran latihan Persona 1, S6 (simulasi; rumus dan aturan pembulatan belum dikonfirmasi).
