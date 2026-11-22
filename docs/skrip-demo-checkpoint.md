# Skrip demo checkpoint — 5 menit

> Skrip latihan dengan lingkungan dan data uji lokal. Nama anggota belum tercatat pada `docs/kesepakatan-tim.md`; ganti label Penyaji 1/2 setelah kelompok menentukan pembagian.

| Waktu | Penyaji | Demo |
|---|---|---|
| 0:00–0:35 | Penyaji 1 | Jelaskan bahwa aplikasi pada `main` belum menyertakan modul aplikasi; demo berjalan di branch fitur. Tunjukkan tujuan uji dan jangan tampilkan secret. |
| 0:35–1:20 | Penyaji 1 | Masuk memakai akun uji lokal sebagai `pengelola`, tambahkan satu bahan dan catat satu resep. Tunjukkan hasil pada daftar/rincian. |
| 1:20–2:00 | Penyaji 2 | Keluar, masuk sebagai `pengguna`, tampilkan daftar baca-saja; coba buka rute tulis dan tunjukkan halaman 403. |
| 2:00–2:40 | Penyaji 2 | Tunjukkan tes otomatis: guest tidak mengubah data, CSRF tanpa token ditolak 400, dan percobaan login keenam mendapat 429. Jangan mengetik payload serangan. |
| 2:40–3:20 | Penyaji 1 | Tunjukkan tiga header keamanan, contoh log login gagal/akses ditolak yang tidak memuat password, dan konfigurasi production yang menolak debug/Secure yang salah. |
| 3:20–4:00 | Penyaji 1 | Ringkas sepuluh butir kasus sintetis dan lima temuan proyek; jelaskan bahwa `kasus_rentan.py` asli tidak diberikan, jadi tabel bukan hasil analisis file tersebut. |
| 4:00–4:35 | Penyaji 2 | Tunjukkan hasil tes cepat, temuan yang diperbaiki, serta risiko terbuka: persetujuan matriks peran, HTTPS deployment, dan pip-audit. |
| 4:35–5:00 | Keduanya | Sampaikan tindak lanjut dan jawab pertanyaan. Hentikan demo pada menit kelima. |

## Data dan rencana cadangan

- Gunakan basis data uji sementara dan kata sandi karangan yang tidak dipakai di tempat lain.
- Jalankan `python tests/uji_cepat.py` dan `python -m unittest discover -s tests -v` sebelum presentasi.
- Jika aplikasi gagal berjalan, tampilkan keluaran tes yang baru dijalankan dan dokumen laporan; jangan gunakan database produksi atau menampilkan secret.
- Demo tidak menggantikan tinjauan sejawat, UAT, atau persetujuan klien.
