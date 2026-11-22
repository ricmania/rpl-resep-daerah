# Rencana Sprint 2 — Minggu 11–12

## Tujuan sprint

Menerapkan antarmuka resep sesuai wireframe Jobsheet 7, menguji alur pencatatan/pembacaan, mengerjakan siklus autentikasi Jobsheet sebagai prototipe latihan, lalu menyelesaikan tinjauan kode dan checkpoint Minggu 12. Autentikasi/peran belum disetujui klien dan tidak mengubah status kebutuhan pada SRS.

## Rencana kerja

| Minggu | Fokus | Hasil kerja | Kriteria selesai |
|---|---|---|---|
| 11 | Validasi rancangan dan penyelarasan antarmuka | Cocokkan daftar resep, form catat resep, rincian resep, validasi, dan keadaan tanpa hasil dengan `docs/desain/wireframe/`. Catat keputusan prototipe versus keputusan klien. | Setiap layar pada cakupan sprint punya menu, aksi, dan area pesan yang konsisten; setiap kriteria penerimaan yang disetujui memiliki uji. |
| 11 | Validasi resep dan penyimpanan | Uji nama, daftar bahan, jumlah/satuan opsional, langkah berurutan, masukan kosong/tidak valid, serta rollback transaksi. | Form menampilkan isian kembali setelah gagal; data valid disimpan utuh; tidak ada data parsial saat gagal. |
| 11–12 | Penemuan kebutuhan autentikasi/peran | Tanyakan siapa pengguna sebenarnya, apakah dua peran diperlukan, batas akses, cara login yang diizinkan, dan kebutuhan sesi. Login pada wireframe masih placeholder kebutuhan. | Keputusan dan pertanyaan terbuka dicatat; implementasi latihan tidak dianggap persetujuan klien. |
| 12 | Antarmuka dan siklus autentikasi Jobsheet | Template induk, CSS bersama, login/logout, dua peran baca/tulis, CSRF, validasi dua lapis, pembatasan login, log keamanan, dan header/config production diterapkan pada branch latihan. | 41 tes aplikasi dan 11 skenario uji cepat lulus; uji manual browser dan review sejawat masih harus dilakukan. |
| 12 | Code review, regresi, dan checkpoint | Tinjau diff melalui PR, perbaiki temuan, jalankan skrip uji cepat dan seluruh uji, demo alur dua peran dan fitur inti. | PR mendapat peninjau dan persetujuan; checkpoint mencatat bukti tes, temuan review, dan risiko tersisa. |

## Strategi pengujian dan peninjauan

- Jalankan `python tests/uji_cepat.py` untuk pemeriksaan alur singkat pada database sementara.
- Jalankan `python -m unittest discover -s tests -v` dan `python tests/cek_skema.py` sebelum PR dan setelah perubahan tinjauan.
- Uji manual keadaan kosong, data valid, setiap validasi, serta navigasi balik pada ukuran layar desktop dan sempit.
- Peninjau selain pembuat memeriksa kesesuaian wireframe, validasi, parameter SQL, transaksi, dan tidak adanya perubahan di luar ruang lingkup.

## Ketergantungan dan risiko

- Prioritas KF-01/KF-02 dan kriteria wajib di PRD masih usulan; aturan prototipe nama + satu bahan + satu langkah bukan persetujuan klien.
- Autentikasi dan kewenangan tidak didefinisikan dalam SRS. Matriks `pengelola` (tulis) dan `pengguna` (baca) adalah asumsi Jobsheet, bukan ketetapan klien.
- Pencarian KF-02 masih memerlukan kesepakatan bidang dan aturan pencocokan.
- Kapasitas dan pembagian kerja anggota belum ditetapkan pada kesepakatan tim; penanggung jawab perlu ditunjuk sebelum Sprint 2 dimulai.

## Bahan Pertemuan 11

Wireframe Jobsheet 7 telah ditinjau kembali: [form catat resep](./desain/wireframe/wf-04-form-resep.png) menempatkan nama, baris bahan, langkah berurutan, aksi simpan/kembali, dan area pesan; [keadaan validasi/tanpa hasil](./desain/wireframe/wf-07-keadaan.png) menunjukkan pesan tanpa kehilangan jalur kembali; [daftar/pencarian](./desain/wireframe/wf-03-daftar-resep.png) dan [rincian resep](./desain/wireframe/wf-05-rincian-resep.png) menjadi target tahap KF-02.

## Checkpoint Minggu 12

**Demo prototipe 5 menit**

1. Masuk sebagai `pengelola`, tambahkan bahan dan catat resep.
2. Tunjukkan daftar/rincian resep dan pesan berhasil.
3. Keluar, masuk sebagai `pengguna`, baca daftar, lalu buktikan aksi tulis ditolak di server dengan 403.
4. Tunjukkan bahwa kredensial disimpan sebagai hash dan tes cepat mencetak `SEMUA UJI LULUS`.

**Belum selesai / tindak lanjut**

- Minta persetujuan klien atas autentikasi, aktor, matriks izin, dan kebutuhan KF.
- Pembatasan lima percobaan login per pasangan alamat/username selama lima menit sudah diterapkan untuk prototipe; evaluasi ambang dan penyimpanan terdistribusi bila aplikasi di-deploy multi-instance.
- Lakukan review sejawat atas CSRF dan seluruh kontrol akses.
- Uji manual keyboard, keterlihatan fokus, label, pesan, serta tampilan lebar sekitar 360 px; catat hasil aktual.
- Uji konfigurasi HTTPS/cookie pada deployment; jangan memakai konfigurasi tes.

## Sprint 3 — Minggu 13–14 (rencana)

| Target | Rencana kerja | Kriteria selesai |
|---|---|---|
| Pengujian | Susun sedikitnya 20 test case, dengan sedikitnya 8 uji otomatis yang mencakup alur utama, validasi, akses, sesi, CSRF, batas login, dan error. | Semua uji otomatis lulus; hasil manual dan regresi tercatat. |
| UAT | Jalankan UAT dengan klien memakai data karangan; catat skenario, hasil, umpan balik, dan keputusan perubahan. | UAT ditinjau klien; kebutuhan/peran yang belum disetujui diberi status terbuka. |
| Rilis v1.0 | Tinjau temuan keamanan terbuka, pemindaian dependensi, konfigurasi HTTPS, dokumentasi penggunaan, dan persetujuan rilis. | Tidak ada temuan kritis/tinggi terbuka yang tidak diterima secara eksplisit; release notes dan tag v1.0 disiapkan setelah persetujuan. |

Target ini adalah rencana, bukan klaim UAT atau rilis yang sudah dilakukan.
