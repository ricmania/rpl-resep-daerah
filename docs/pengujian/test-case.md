# Matriks Kebutuhan dan Test Case

> **Cakupan terbatas pada bukti di branch ini.** PRD tidak tersedia di workspace dan `main` belum memiliki aplikasi (`app.py`, `models.py`, `services.py`, maupun `tests/uji_cepat.py`). SRS hanya menyebut KF-01 dan KF-02. Karena itu enam KF tidak dapat diturunkan tanpa mengarang kebutuhan, dan pengujian otomatis di sini hanya memeriksa DDL SQLite. Uji antarmuka/alur KF-01 dan KF-02 tetap tertunda sampai implementasi tersedia.

## 1. Matriks keterlacakan

| KF | Sumber dan kriteria penerimaan | Kriteria yang diuji di branch ini | Test case |
|---|---|---|---|
| KF-01 — Mencatat resep | SRS §2: resep tersimpan dengan nilai yang dimasukkan; atribut wajib yang belum diisi diberitahukan dan tidak disimpan. Atribut wajib masih menunggu konfirmasi. | Integritas baris resep/bahan/langkah dan batas skema yang tertulis di `docs/desain/schema.sql`; belum membuktikan alur form. | TC-01–TC-22 |
| KF-02 — Menemukan dan membaca resep | SRS §2: hasil sesuai aturan pencarian yang disepakati, keadaan tanpa hasil, dan rincian nama/bahan/langkah. Aturan pencarian belum ditetapkan. | Belum dapat diuji: tidak ada aplikasi, query/model pencarian, atau tampilan pada `main`. | TC-23–TC-25 (tertunda) |

**Kesenjangan:** target enam KF dari lembar kerja tidak dapat dipenuhi dari SRS yang tersedia. KF-01 dan KF-02 adalah satu-satunya KF teridentifikasi; autentikasi/CSRF bukan KF dalam SRS ini. Mohon lampirkan PRD atau daftar KF yang telah disetujui sebelum perluasan matriks.

## 2. Partisi dan batas

| Isian / aturan sumber | Partisi valid | Partisi tidak valid | Nilai batas yang diuji |
|---|---|---|---|
| `resep.nama`, `bahan.nama`, `langkah_resep.instruksi` — `TEXT NOT NULL` dan tidak boleh kosong menurut DDL | Teks nonkosong | NULL, kosong, spasi saja, atau BLOB | String nonkosong vs kosong/spasi |
| `resep_bahan.jumlah` — opsional, jika ada maka `> 0` menurut DDL; bukan aturan KF terkonfirmasi | NULL atau bilangan positif | Nol, negatif, teks nonangka | -0.01, 0, 0.01 |
| `langkah_resep.urutan` — `INTEGER > 0` menurut DDL | Bilangan bulat positif | Negatif, nol, pecahan, teks | -1, 0, 1; pecahan 1.5 |

## 3. Test case

Kolom aktual/status diisi hanya setelah perintah uji dijalankan. `Otomatis` berarti uji terhadap skema SQLite sementara, bukan bukti bahwa UI atau aplikasi telah berfungsi.

| ID | KF | Teknik / partisi | Data / langkah ringkas | Hasil yang diharapkan | Hasil aktual | Status |
|---|---|---|---|---|---|---|
| TC-01 | KF-01 | Normal | Simpan resep dengan nama `Sayur contoh`. | Baris tersimpan dan nilainya sama. | Tersimpan; database berada di `tmp_path`. | Lulus |
| TC-02 | KF-01 | Pelanggaran | Simpan nama resep `""`. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-03 | KF-01 | Pelanggaran | Simpan nama resep berisi spasi saja. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-04 | KF-01 | Pelanggaran | Simpan nama resep NULL. | Ditolak oleh `NOT NULL`. | Ditolak `IntegrityError`. | Lulus |
| TC-05 | KF-01 | Normal | Simpan bahan dengan nama nonkosong. | Baris bahan tersimpan. | Bahan `Bayam` tersimpan. | Lulus |
| TC-06 | KF-01 | Pelanggaran | Simpan nama bahan kosong. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-07 | KF-01 | Pelanggaran | Simpan nama bahan berisi spasi saja. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-08 | KF-01 | Pelanggaran | Simpan nama bahan NULL. | Ditolak oleh `NOT NULL`. | Ditolak `IntegrityError`. | Lulus |
| TC-09 | KF-01 | Batas bawah | Simpan jumlah bahan `-0.01`. | Ditolak karena jumlah harus positif. | Ditolak `IntegrityError`. | Lulus |
| TC-10 | KF-01 | Batas | Simpan jumlah bahan `0`. | Ditolak karena batasnya `> 0`. | Ditolak `IntegrityError`. | Lulus |
| TC-11 | KF-01 | Batas atas partisi invalid | Simpan jumlah bahan `0.01`. | Diterima dan tersimpan sebagai nilai numerik positif. | Diterima sebagai nilai numerik. | Lulus |
| TC-12 | KF-01 | Partisi opsional | Simpan jumlah NULL. | Diterima karena kolom opsional. | Diterima sebagai NULL. | Lulus |
| TC-13 | KF-01 | Pelanggaran tipe | Simpan jumlah `abc`. | Ditolak; jumlah bukan angka. | Ditolak setelah perbaikan D-01 (`cb4c41e`). | Lulus |
| TC-14 | KF-01 | Pelanggaran | Simpan satuan kosong. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-15 | KF-01 | Pelanggaran | Simpan satuan berisi spasi saja. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-16 | KF-01 | Pelanggaran tipe | Simpan BLOB sebagai satuan. | Ditolak; kolom teks hanya menerima teks. | Ditolak setelah perbaikan D-03 (`bd2a535`). | Lulus |
| TC-17 | KF-01 | Batas bawah | Simpan urutan langkah `-1`. | Ditolak karena urutan harus positif. | Ditolak `IntegrityError`. | Lulus |
| TC-18 | KF-01 | Batas | Simpan urutan langkah `0`. | Ditolak; nilai minimum valid adalah 1. | Ditolak `IntegrityError`. | Lulus |
| TC-19 | KF-01 | Batas tipe | Simpan urutan langkah `1.5`. | Ditolak; urutan harus bilangan bulat. | Ditolak setelah perbaikan D-02 (`0161824`). | Lulus |
| TC-20 | KF-01 | Pelanggaran tipe | Simpan urutan langkah `abc`. | Ditolak; urutan harus bilangan bulat. | Ditolak setelah perbaikan D-02 (`0161824`). | Lulus |
| TC-21 | KF-01 | Pelanggaran | Simpan instruksi langkah kosong/spasi saja. | Ditolak oleh batasan skema. | Ditolak `IntegrityError`. | Lulus |
| TC-22 | KF-01 | Pelanggaran tipe | Simpan BLOB sebagai instruksi. | Ditolak; instruksi harus teks. | Ditolak setelah perbaikan D-03 (`bd2a535`). | Lulus |
| TC-23 | KF-02 | Jalur normal | Cari resep cocok melalui formulir aplikasi. | Daftar menampilkan hasil yang cocok menurut aturan final. | — | Tertunda: aplikasi/aturan pencarian tidak tersedia |
| TC-24 | KF-02 | Jalur tanpa hasil | Cari kata kunci yang tidak cocok. | Aplikasi menampilkan keadaan tanpa hasil. | — | Tertunda: aplikasi/aturan pencarian tidak tersedia |
| TC-25 | KF-02 | Jalur normal | Buka resep dengan beberapa bahan/langkah. | Rincian menampilkan resep terpilih dan langkah berurutan. | — | Tertunda: aplikasi tidak tersedia |

Komposisi: **25 test case**; sedikitnya 6 pemeriksaan batas, 6 pelanggaran, dan 3 jalur normal. 22 pemeriksaan skema otomatis; 3 alur KF-02 tertunda. Eksekusi terakhir `pytest -q tests`: **33 kasus lulus, 0 gagal**, tersebar pada 12 fungsi uji (parametrisasi dihitung sebagai kasus). Semua case mengacu ke KF yang ada.

## 4. Catatan draf dan pemeriksaan

- Draf uji ini mengikuti SRS dan DDL yang tersedia, bukan PRD yang tidak ada. Tidak ditambahkan kebutuhan toko, harga, login, atau CSRF.
- SQLite memakai tipe dinamis; deklarasi `REAL`, `INTEGER`, dan `TEXT` saja belum membuktikan semua nilai tersimpan memiliki kelas tipe yang tepat. TC-13, TC-16, TC-19, TC-20, dan TC-22 secara khusus memeriksa batasan tersebut.
- Fixture pytest membuat database di `tmp_path`, bukan di file database aplikasi.
- Fixture akun dan client/CSRF tidak dibuat karena branch `main` tidak berisi aplikasi atau rute HTTP.
- Mutasi manual pada skema membuktikan regresi tertangkap: menghapus pemeriksaan tipe jumlah membuat 1 uji gagal; menghapus pemeriksaan tipe urutan membuat 2 uji gagal; menghapus pemeriksaan tipe nama membuat 1 uji gagal. Setiap mutasi dikembalikan sebelum validasi akhir.
- `tests/uji_cepat.py` tidak tersedia pada `main`; perintah yang diminta gagal saat mencari file. `tests/cek_skema.py` tersedia dan keempat pelanggaran yang diperiksanya ditolak.
