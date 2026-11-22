# Rencana Sprint 2 — Minggu 11–12

## Tujuan sprint

Menerapkan antarmuka resep sesuai wireframe Jobsheet 7, menguji alur pencatatan/pembacaan, menyepakati kebutuhan autentikasi dan peran sebelum mengimplementasikannya, lalu menyelesaikan tinjauan kode dan checkpoint Minggu 12.

## Rencana kerja

| Minggu | Fokus | Hasil kerja | Kriteria selesai |
|---|---|---|---|
| 11 | Validasi rancangan dan penyelarasan antarmuka | Cocokkan daftar resep, form catat resep, rincian resep, validasi, dan keadaan tanpa hasil dengan `docs/desain/wireframe/`. Catat keputusan prototipe versus keputusan klien. | Setiap layar pada cakupan sprint punya menu, aksi, dan area pesan yang konsisten; setiap kriteria penerimaan yang disetujui memiliki uji. |
| 11 | Validasi resep dan penyimpanan | Uji nama, daftar bahan, jumlah/satuan opsional, langkah berurutan, masukan kosong/tidak valid, serta rollback transaksi. | Form menampilkan isian kembali setelah gagal; data valid disimpan utuh; tidak ada data parsial saat gagal. |
| 11–12 | Penemuan kebutuhan autentikasi/peran | Tanyakan siapa pengguna sebenarnya, apakah dua peran diperlukan, batas akses, cara login yang diizinkan, dan kebutuhan sesi. Login pada wireframe saat ini hanya placeholder. | Keputusan dan pertanyaan terbuka dicatat; tidak ada autentikasi atau pembatasan akses yang diklaim tanpa persetujuan. |
| 12 | Implementasi antarmuka yang disetujui | Sesuaikan template dan navigasi ke wireframe; implementasikan autentikasi/peran hanya setelah kebutuhan dan aturan akses disetujui. | Uji alur peran mencakup akses yang diizinkan dan ditolak; sesi tidak mengekspos kredensial atau rahasia di repositori. Jika keputusan belum tersedia, autentikasi tetap pekerjaan tertunda. |
| 12 | Code review, regresi, dan checkpoint | Tinjau diff melalui PR, perbaiki temuan, jalankan skrip uji cepat dan seluruh uji, demo alur dari daftar ke rincian. | PR mendapat peninjau dan persetujuan; semua uji lulus; checkpoint Minggu 12 mencatat fitur selesai, bukti uji, temuan review, serta keputusan/risiko tersisa. |

## Strategi pengujian dan peninjauan

- Jalankan `python tests/uji_cepat.py` untuk pemeriksaan alur singkat pada database sementara.
- Jalankan `python -m unittest discover -s tests -v` dan `python tests/cek_skema.py` sebelum PR dan setelah perubahan tinjauan.
- Uji manual keadaan kosong, data valid, setiap validasi, serta navigasi balik pada ukuran layar desktop dan sempit.
- Peninjau selain pembuat memeriksa kesesuaian wireframe, validasi, parameter SQL, transaksi, dan tidak adanya perubahan di luar ruang lingkup.

## Ketergantungan dan risiko

- Prioritas KF-01/KF-02 dan kriteria wajib di PRD masih usulan; aturan prototipe nama + satu bahan + satu langkah bukan persetujuan klien.
- Autentikasi dan kewenangan tidak didefinisikan dalam SRS. Jangan menambah login placeholder sebagai kontrol keamanan.
- Pencarian KF-02 masih memerlukan kesepakatan bidang dan aturan pencocokan.
- Kapasitas dan pembagian kerja anggota belum ditetapkan pada kesepakatan tim; penanggung jawab perlu ditunjuk sebelum Sprint 2 dimulai.

## Bahan Pertemuan 11

Wireframe Jobsheet 7 telah ditinjau kembali: [form catat resep](./desain/wireframe/wf-04-form-resep.png) menempatkan nama, baris bahan, langkah berurutan, aksi simpan/kembali, dan area pesan; [keadaan validasi/tanpa hasil](./desain/wireframe/wf-07-keadaan.png) menunjukkan pesan tanpa kehilangan jalur kembali; [daftar/pencarian](./desain/wireframe/wf-03-daftar-resep.png) dan [rincian resep](./desain/wireframe/wf-05-rincian-resep.png) menjadi target tahap KF-02.
