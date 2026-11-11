# Jurnal Kritik User Story

## Catatan sesi

- **Jenis masukan:** Kritik AI terhadap draf latihan user story Persona 1.
- **Dasar penilaian:** Simulasi Persona 1 pada `catatanwawancara.md`, bukan hasil wawancara nyata.
- **Keputusan umum:** Seluruh 12 story tetap berstatus `[Asumsi]`; jangan gunakan sebagai kebutuhan klien yang telah disepakati sebelum dikonfirmasi.

## Kritik dan keputusan

| Area yang dikritik | Kritik AI | Keputusan |
|---|---|---|
| Keabsahan sumber | Sumber yang tersedia merupakan simulasi, bukan catatan wawancara nyata. | Menambahkan peringatan di catatan dan user story. Semua story diberi penanda `[Asumsi]` dan menunjuk ID S1–S6. |
| Story US-02 | Resep dari chat belum tentu perlu diintegrasikan langsung dengan chat; simulasi hanya menyebut resep dikirim lewat chat. | Membatasi story pada memasukkan rincian resep yang diterima, bukan integrasi aplikasi chat. Konfirmasi alur sebenarnya saat wawancara. |
| Story US-03 | Website adalah solusi yang dibayangkan persona, bukan kebutuhan yang sudah dikonfirmasi. | Merumuskan story sebagai kumpulan resep terpusat tanpa mewajibkan website tertentu. |
| Story US-04 dan US-05 | Kata kunci pencarian dan daftar resep adalah cara pemenuhan yang belum ditetapkan. | Mempertahankan keduanya sebagai asumsi terpisah untuk diuji; tanyakan bagaimana persona biasanya mencari dan menemukan resep. |
| Story US-07 dan US-08 | Mencatat koreksi dan melihat takaran terkini dapat tumpang tindih. | Memisahkan sementara tindakan memperbarui dan kebutuhan membaca hasilnya. Gabungkan jika wawancara menunjukkan pengguna tidak membedakan keduanya. |
| Story US-09 dan US-10 | Mengaitkan foto dan melihat foto merupakan tindakan berbeda, tetapi belum diketahui apakah keduanya diperlukan. | Mempertahankan sebagai asumsi yang dapat diuji; konfirmasi bagaimana foto disimpan, dicari, dan dipasangkan dengan resep. |
| Story US-11 dan US-12 | Penghitungan ulang takaran mengasumsikan resep memiliki jumlah sajian awal, pengguna memasukkan jumlah tujuan, serta aturan perhitungan tertentu. | Menandai asumsi dan memakai kriteria rumus eksplisit agar dapat diuji. Konfirmasi jumlah sajian, satuan, pembulatan, dan perilaku yang diharapkan sebelum implementasi. |
| Kriteria penerimaan | Kriteria perlu dapat diuji dan menyatakan kondisi, tindakan, serta hasil. | Setiap story memiliki dua skenario Given–When–Then. Periksa kembali istilah dan aturan setelah memperoleh jawaban nyata dari klien. |
| Pedoman wawancara | Belum ada hasil wawancara untuk menilai pertanyaan mana yang kurang berguna. | Tidak mengubah `pedoman-wawancara.md` berdasarkan simulasi. Setelah wawancara, catat pertanyaan yang tidak menghasilkan contoh atau informasi relevan, lalu revisi pedoman berdasarkan bukti tersebut. |

## Tindak lanjut sebelum menetapkan kebutuhan

1. Lakukan wawancara nyata dan rapikan catatan pada `catatanwawancara.md`, dengan memisahkan fakta, asumsi, dan hal yang perlu dikonfirmasi.
2. Tanyakan proses mencari resep, pencatatan koreksi, penyimpanan foto, dan kebutuhan penyesuaian takaran berdasarkan contoh nyata.
3. Perbarui atau hapus story yang tidak didukung catatan nyata; hilangkan `[Asumsi]` hanya setelah klien mengonfirmasi kebutuhan terkait.
