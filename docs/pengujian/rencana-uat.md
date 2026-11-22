# Rencana UAT — Draf

> Dokumen ini belum menjadi jadwal yang disetujui. Nama peserta, tanggal/jam pasti, tempat, dan durasi harus disepakati dengan klien. Belum ada balasan klien yang tersedia; jangan menandai skenario atau jadwal sebagai disetujui.

## Tujuan

Memastikan alur pencatatan, pencarian, dan membaca resep sesuai cara kerja klien dan kriteria KF-01/KF-02 yang telah dikonfirmasi.

## Peserta dan jadwal

| Butir | Rencana |
|---|---|
| Peserta klien | Pemilik/pengelola resep (nama menunggu konfirmasi) |
| Peserta tim | Fasilitator dan pencatat hasil dari kelompok (nama belum ditetapkan) |
| Waktu | Minggu 14; tanggal dan jam menunggu kesepakatan klien |
| Tempat | Menunggu kesepakatan klien; alternatif ruang kelas atau pertemuan daring |
| Durasi | Usulan 60 menit; menunggu persetujuan klien |
| Status persetujuan | Belum diminta / belum ada balasan yang dicatat |

## Lingkungan dan data

- Jalankan build yang disepakati pada komputer lokal/lingkungan uji terpisah; jangan gunakan data produksi.
- Gunakan data karangan: “Sayur contoh”, “Bahan contoh”, dan instruksi masak sintetis.
- Sebelum UAT, sepakati atribut wajib, aturan pencarian, satuan, dan siapa yang boleh mencatat resep.
- Simpan versi aplikasi/commit, browser, tanggal, dan penguji di lembar hasil.

## Skenario

| ID | KF | Skenario dengan bahasa klien | Hasil yang diharapkan |
|---|---|---|---|
| UAT-01 | KF-01 | “Catat satu resep baru yang biasa dibuat, lengkap dengan bahan dan langkahnya.” | Resep tersimpan dengan isi yang diberikan; klien dapat mengenali nama, bahan, dan urutannya. |
| UAT-02 | KF-01 | “Coba simpan resep, tetapi kosongkan informasi yang sudah kita sepakati wajib.” | Sistem menunjukkan bagian yang belum lengkap dan resep tidak tersimpan. |
| UAT-03 | KF-02 | “Cari resep menggunakan kata yang menurut kita seharusnya cocok.” | Resep yang sesuai tampil berdasarkan aturan pencarian yang disepakati. |
| UAT-04 | KF-02 | “Cari kata yang tidak ada pada resep yang disimpan.” | Sistem menjelaskan bahwa belum ada resep yang cocok; hasil lain tidak disajikan sebagai cocok. |
| UAT-05 | KF-02 | “Buka satu resep yang ditemukan dan periksa bahan serta urutan cara membuatnya.” | Rincian menampilkan resep yang dipilih, bahan, dan langkah secara utuh dan berurutan. |

## Kriteria lulus dan pencatatan

- Klien menyatakan hasil setiap skenario sesuai atau mencatat perbedaan; seluruh lima skenario harus memiliki keputusan.
- Tidak ada data nyata/pribadi yang digunakan. Setiap masalah dicatat dengan ID, langkah, hasil aktual, hasil yang diharapkan, dan tingkat dampak.
- Perubahan aturan (misalnya atribut wajib atau pencarian) dicatat sebagai keputusan/perubahan kebutuhan, bukan cacat, kecuali menyimpang dari kebutuhan yang telah disetujui.
- Setelah sesi, fasilitator mengirim ringkasan hasil dan meminta konfirmasi klien; status UAT tetap “belum disetujui” sampai balasan tercatat.
