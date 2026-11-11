# Skenario Use Case

> Skenario ini diturunkan dari kriteria Must pada PRD yang dibahas sebelumnya: KF-01 (mencatat resep) dan KF-02 (menemukan serta membaca resep). Prioritas dan kebutuhan masih usulan untuk divalidasi; skenario tidak menetapkan atribut wajib atau aturan pencarian yang belum disepakati.

## UC-01 — Mencatat resep dengan informasi wajib lengkap

**Aktor dan KF**
- Aktor utama: Pengelola resep
- KF yang dipenuhi: KF-01 — Mencatat resep (Must, usulan)

**Prasyarat**
- Pengelola resep sedang menggunakan aplikasi.
- Atribut wajib resep telah disepakati.

**Alur utama**
1. Pengelola resep memilih tindakan untuk mencatat resep.
2. Sistem menampilkan isian resep.
3. Pengelola resep mengisi nama, bahan, langkah, dan atribut wajib lain yang telah disepakati.
4. Sistem menerima isian resep.
5. Pengelola resep meminta sistem menyimpan resep.
6. Sistem menyimpan resep dengan nilai yang dimasukkan.

**Alur alternatif**
- Pada langkah 3, pengelola resep mengisi hanya atribut wajib yang telah ditetapkan. Sistem tetap menyimpan resep dengan nilai tersebut.

**Pengecualian**
- Pada langkah 3, satu atau lebih atribut wajib belum diisi. Sistem menunjukkan atribut yang belum lengkap dan tidak menyimpan resep.

**Pascakondisi**
- Berhasil: resep tersimpan dengan nilai yang dimasukkan.
- Tidak berhasil: resep tidak tersimpan jika atribut wajib belum lengkap.

## UC-02 — Menangani resep dengan atribut wajib belum lengkap

**Aktor dan KF**
- Aktor utama: Pengelola resep
- KF yang dipenuhi: KF-01 — Mencatat resep (Must, usulan)

**Prasyarat**
- Pengelola resep sedang menggunakan aplikasi.
- Atribut wajib resep telah disepakati.

**Alur utama**
1. Pengelola resep membuka isian untuk mencatat resep.
2. Sistem menampilkan isian resep.
3. Pengelola resep mengisi resep dengan setidaknya satu atribut wajib kosong, lalu meminta sistem menyimpan.
4. Sistem menunjukkan atribut yang belum lengkap dan tidak menyimpan resep.

**Alur alternatif**
- Setelah pemberitahuan, pengelola resep melengkapi semua atribut wajib dan meminta penyimpanan kembali. Sistem menyimpan resep dengan nilai yang dimasukkan.

**Pengecualian**
- Pengelola resep menutup atau meninggalkan isian tanpa melengkapi satu atau lebih atribut wajib. Resep tetap tidak tersimpan.

**Pascakondisi**
- Resep tidak tersimpan selama atribut wajib belum lengkap; jika dilengkapi dan disimpan kembali, resep tersimpan.

## UC-03 — Menemukan resep yang cocok dengan kata kunci

**Aktor dan KF**
- Aktor utama: Pengguna resep
- KF yang dipenuhi: KF-02 — Menemukan dan membaca resep (Must, usulan)

**Prasyarat**
- Ada resep tersimpan.
- Bidang dan aturan pencarian telah disepakati.

**Alur utama**
1. Pengguna resep memasukkan kata kunci pencarian.
2. Sistem menerima kata kunci.
3. Pengguna resep mengirim permintaan pencarian.
4. Sistem menampilkan resep yang cocok menurut bidang dan aturan pencarian yang disepakati.

**Alur alternatif**
- Pengguna resep mengganti kata kunci dengan kata kunci lain yang cocok. Sistem menampilkan resep yang cocok dengan kata kunci baru tersebut.

**Pengecualian**
- Tidak ada resep yang cocok dengan kata kunci. Sistem menampilkan keadaan tanpa hasil.

**Pascakondisi**
- Resep yang cocok ditampilkan, atau keadaan tanpa hasil ditampilkan jika tidak ada kecocokan.

## UC-04 — Mendapatkan keadaan tanpa hasil pencarian

**Aktor dan KF**
- Aktor utama: Pengguna resep
- KF yang dipenuhi: KF-02 — Menemukan dan membaca resep (Must, usulan)

**Prasyarat**
- Bidang dan aturan pencarian telah disepakati.
- Kata kunci yang dikirim tidak cocok dengan resep tersimpan.

**Alur utama**
1. Pengguna resep memasukkan kata kunci.
2. Sistem menerima kata kunci.
3. Pengguna resep mengirim permintaan pencarian.
4. Sistem memeriksa resep berdasarkan bidang dan aturan yang disepakati.
5. Sistem tidak menemukan resep yang cocok.
6. Sistem menampilkan keadaan tanpa hasil.

**Alur alternatif**
- Pengguna resep mengirim kata kunci berbeda yang cocok dengan resep tersimpan. Sistem menampilkan resep yang cocok.

**Pengecualian**
- Pencarian tidak menghasilkan kecocokan. Sistem menampilkan keadaan tanpa hasil dan tidak menampilkan resep sebagai hasil cocok.

**Pascakondisi**
- Keadaan tanpa hasil ditampilkan; atau, bila kata kunci alternatif cocok, resep yang cocok ditampilkan.

## UC-05 — Membaca rincian resep yang ditemukan

**Aktor dan KF**
- Aktor utama: Pengguna resep
- KF yang dipenuhi: KF-02 — Menemukan dan membaca resep (Must, usulan)

**Prasyarat**
- Resep tersimpan dengan nama, bahan, dan langkah.
- Pengguna resep telah menemukan resep melalui daftar atau hasil pencarian.

**Alur utama**
1. Pengguna resep memilih resep yang ditemukan.
2. Sistem membuka rincian resep yang dipilih.
3. Pengguna resep melihat rincian resep.
4. Sistem menampilkan nama, bahan, dan langkah milik resep tersebut.

**Alur alternatif**
- Pengguna resep memilih resep lain yang tersimpan dari daftar atau hasil pencarian. Sistem menampilkan rincian resep yang dipilih tersebut.

**Pengecualian**
- Tidak ada resep yang cocok saat pengguna mencari resep untuk dibuka. Sistem menampilkan keadaan tanpa hasil; rincian resep tidak dibuka.

**Pascakondisi**
- Berhasil: rincian nama, bahan, dan langkah resep yang dipilih ditampilkan.
- Tidak ada kecocokan: keadaan tanpa hasil ditampilkan dan tidak ada rincian resep yang dibuka.