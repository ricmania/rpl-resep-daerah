# Rencana Uji

> **Status: rencana, belum dieksekusi.** Workspace belum berisi aplikasi yang dapat diuji. Sumber yang tersedia adalah SRS dan skenario use case; PRD disebut dalam jobsheet tetapi tidak tersedia. KF-01 dan KF-02 adalah kebutuhan Must (usulan); tidak ada kebutuhan Should pada SRS saat ini.

## 1. Tujuan

Memeriksa secara terukur bahwa penyimpanan resep, validasi atribut wajib, pencarian, keadaan tanpa hasil, dan pembacaan rincian memenuhi kriteria penerimaan KF-01/KF-02. Uji antarmuka dilakukan setelah aplikasi tersedia. Hasil pengujian harus dicatat dengan status, bukti, dan versi yang diuji; tabel di bawah adalah rancangan test case, bukan hasil lulus.

## 2. Ruang lingkup

- **Termasuk:** KF-01 (UC-01, UC-02) dan KF-02 (UC-03, UC-04, UC-05), prioritas Must usulan.
- **Belum ada:** KF Should; jangan menambah fitur atau test case untuk kebutuhan yang belum tercantum.
- **Di luar cakupan fungsional:** login/autentikasi (tidak ada KF atau UC terkait), unggah foto, riwayat koreksi, penghitungan ulang takaran. Semua belum ditetapkan sebagai fitur.
- **Asumsi rancangan yang harus dikonfirmasi:** `nama` nonblank; `jumlah` yang diisi harus lebih besar dari 0 (`REAL` pada draf skema). SRS belum menentukan aturan bisnis tersebut, presisi angka, satuan, atribut wajib, atau semantik pencarian. Kasus yang menguji asumsi ini harus ditahan atau diperbarui setelah konfirmasi.

## 3. Strategi

- **Black-box manual:** jalankan alur pada browser dari perspektif aktor; bandingkan nilai, pesan, keadaan tanpa hasil, dan data tersimpan dengan kriteria penerimaan.
- **Otomatis dasar:** gunakan uji unit untuk validasi masukan/aturan inti dan uji integrasi SQLite untuk batasan `CHECK`, `NOT NULL`, `UNIQUE`, serta FK. Uji skema yang tersedia memeriksa empat pelanggaran database, tetapi tidak menggantikan pengujian aplikasi atau UAT.
- **UAT dengan klien:** setelah aturan wajib, pencarian, satuan, dan akses dikonfirmasi; jalankan skenario anonim/sintetis bersama klien dan catat persetujuan atau perubahan.
- **Partisi/nilai batas:** gunakan data valid dan invalid serta nilai pada kedua sisi batas `jumlah > 0` hanya sebagai rancangan sementara berdasarkan DDL saat ini; konfirmasikan aturan sebelum UAT.

## 4. Lingkungan dan data uji

- Browser desktop modern dan perangkat pengembangan kelompok; versi OS/browser dicatat saat eksekusi.
- Basis data SQLite lokal terisolasi yang dibuat dari `docs/desain/schema.sql`; foreign key diaktifkan.
- Hanya data karangan, misalnya resep “Contoh sayur”, bahan “Contoh daun”, jumlah `0`, `-0.01`, atau `0.01`; tidak menggunakan data pribadi maupun data klien.
- Gunakan build/commit yang sama untuk seluruh penguji dan catat hash/versinya pada laporan hasil.

## 5. Kriteria lulus

- Semua test case Must yang sudah memiliki aturan terkonfirmasi lulus; semua test case tertunda dicatat alasannya dan tidak dihitung sebagai bukti lulus.
- TC-01 menyimpan nilai yang dimasukkan; TC-02 menampilkan atribut wajib yang kurang dan tidak menyimpan; TC-04/TC-05 menunjukkan hasil sesuai aturan pencarian yang disetujui; TC-06 menampilkan nama, bahan, dan langkah dari resep terpilih.
- Kasus nilai batas yang telah disetujui menunjukkan nilai tepat di bawah/pada/di atas ambang diperlakukan konsisten dengan aturan final.
- Tidak ada hasil gagal tanpa tiket/perbaikan atau keputusan tertulis. Semua TC harus memiliki status dan bukti sebelum menyatakan rilis lulus.

## 6. Pembagian tugas

Nama anggota belum dicantumkan pada kesepakatan tim. Tetapkan orang sebelum eksekusi; jangan menganggap peran di bawah telah ditugaskan.

| Tanggung jawab | Penugasan |
|---|---|
| Menjalankan uji black-box UC-01/UC-02 | Belum ditetapkan |
| Menjalankan uji black-box UC-03–UC-05 | Belum ditetapkan |
| Menjalankan/meninjau uji otomatis dasar | Belum ditetapkan |
| Mengatur dan mencatat UAT dengan klien | Belum ditetapkan |

## 7. Daftar test case (draf)

`Pending konfirmasi` berarti ekspektasi masih mengandalkan aturan rancangan yang belum disetujui. Prasyarat “atribut wajib” dan “aturan pencarian” harus diisi dari hasil konfirmasi, bukan ditebak penguji.

| ID | KF | Prasyarat / data uji | Langkah | Hasil yang diharapkan | Teknik / status |
|---|---|---|---|---|---|
| TC-01 | KF-01 | Atribut wajib sudah disepakati; data sintetis memenuhi aturan | Isi nama, bahan, dan langkah; simpan; baca kembali data yang tersimpan | Resep tersimpan tepat dengan nilai yang dimasukkan | Partisi valid; menunggu kesepakatan atribut |
| TC-02 | KF-01 | Satu atribut yang telah disepakati sebagai wajib dikosongkan | Kirim penyimpanan | Sistem menunjukkan nama atribut yang belum lengkap; tidak ada resep baru tersimpan | Partisi invalid; Must |
| TC-03 | KF-01 | Nama hanya berisi spasi | Coba simpan resep | Jika aturan nonblank disetujui: simpan ditolak, pesan menunjuk nama, tidak ada baris resep baru | Partisi invalid; asumsi draf, pending konfirmasi |
| TC-04 | KF-02 | Resep sintetis cocok berdasarkan bidang/aturan pencarian yang sudah disepakati | Cari istilah yang cocok | Hasil mencakup resep yang cocok; hasil tidak cocok tidak disajikan sebagai kecocokan | Partisi valid; menunggu aturan pencarian |
| TC-05 | KF-02 | Tidak ada resep sintetis cocok dengan kata kunci menurut aturan yang disepakati | Cari kata kunci tanpa kecocokan | Keadaan tanpa hasil terlihat; tidak ada resep ditampilkan sebagai hasil cocok | Partisi tanpa kecocokan; Must |
| TC-06 | KF-02 | Satu hasil pencarian memiliki nama, bahan, dan beberapa langkah berurutan | Buka hasil tersebut | Rincian menunjukkan nama dan bahan milik resep itu serta seluruh instruksi dalam urutan `langkah_resep.urutan` | Partisi valid; Must |
| TC-07 | KF-01 | Aturan draf `jumlah` harus `> 0`; masukkan `-0.01` | Simpan rincian bahan dengan jumlah `-0.01` | Jika aturan disetujui: ditolak; tidak ada jumlah negatif tersimpan | Nilai batas di bawah 0; asumsi draf, pending konfirmasi |
| TC-08 | KF-01 | Aturan draf `jumlah` harus `> 0`; masukkan `0` | Simpan rincian bahan dengan jumlah `0` | Jika aturan disetujui: ditolak pada batas 0; tidak ada baris jumlah nol tersimpan | Nilai batas tepat 0; asumsi draf, pending konfirmasi |
| TC-09 | KF-01 | Aturan draf `jumlah` harus `> 0`; masukkan `0.01` | Simpan rincian bahan dengan jumlah `0.01` | Jika aturan disetujui dan presisi mengizinkan: diterima dan nilai terbaca kembali sebagai `0.01` | Nilai batas di atas 0; asumsi draf, pending konfirmasi |

## 8. Matriks keterlacakan KF → use case → halaman → test case

| KF | Use case | Halaman | Prioritas | Test case |
|---|---|---|---|---|
| KF-01 | UC-01 | [wf-04-form-resep](../desain/wireframe/wf-04-form-resep.png) | Must (usulan) | TC-01, TC-07–TC-09 |
| KF-01 | UC-02 | [wf-04-form-resep](../desain/wireframe/wf-04-form-resep.png), [wf-07-keadaan](../desain/wireframe/wf-07-keadaan.png) | Must (usulan) | TC-02, TC-03 |
| KF-02 | UC-03 | [wf-03-daftar-resep](../desain/wireframe/wf-03-daftar-resep.png) | Must (usulan) | TC-04 |
| KF-02 | UC-04 | [wf-03-daftar-resep](../desain/wireframe/wf-03-daftar-resep.png), [wf-07-keadaan](../desain/wireframe/wf-07-keadaan.png) | Must (usulan) | TC-05 |
| KF-02 | UC-05 | [wf-05-rincian-resep](../desain/wireframe/wf-05-rincian-resep.png) | Must (usulan) | TC-06 |

TC-07–TC-09 menguji aturan batas teknis `resep_bahan.jumlah` pada rancangan kamus/skema; karena atribut dan ambangnya belum tercantum dalam KF, kasus tersebut bukan kriteria penerimaan Must yang tervalidasi. Tidak ada test case tanpa KF: semua kasus ditautkan ke KF-01 atau KF-02. Halaman login placeholder tidak memiliki test case fungsional karena tidak ada KF autentikasi.

## 9. Catatan pemeriksaan draf AI

Kesalahan utama yang perlu dihindari adalah mengimpor contoh toko dari jobsheet ke proyek resep atau mengarang ambang bisnis yang tidak tercantum pada SRS. Karena PRD tidak ada pada workspace, semua test case diturunkan dari kriteria KF di SRS; pengujian jumlah `> 0` secara eksplisit ditandai sebagai asumsi draf yang menunggu konfirmasi.

## 10. Hasil eksekusi

Belum ada aplikasi untuk menjalankan test case antarmuka. Eksekusi uji batasan DDL yang terpisah tercatat pada `python tests\cek_skema.py`; hasil tersebut hanya membuktikan penolakan pelanggaran skema di SQLite, bukan kelulusan test case aplikasi di atas.
