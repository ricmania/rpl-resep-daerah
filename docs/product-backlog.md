> Backlog tentatif dari PRD latihan; prioritas dan kriteria perlu disetujui kelompok/klien. Atribut wajib resep, bidang pencarian, serta aturan kecocokan belum ditetapkan.

| Sprint | ID kebutuhan | Tugas | Alasan / ketergantungan |
|---|---|---|---|
| 1 | KF-01 (Must — usulan) | Konfirmasi atribut resep yang wajib dan opsional bersama kelompok/klien. | Menjadi dasar penyimpanan dan validasi; belum diputuskan pada PRD. |
| 1 | KF-01 (Must — usulan) | Siapkan input untuk nama resep, bahan, dan langkah sesuai atribut yang disepakati. | Mewujudkan kebutuhan mencatat resep tanpa menetapkan atribut bisnis tambahan. |
| 1 | KF-01 (Must — usulan) | Simpan resep dengan atribut wajib yang telah disepakati. | Memenuhi kriteria resep tersimpan dengan nilai yang dimasukkan. |
| 1 | KF-01 (Must — usulan) | Tolak penyimpanan saat atribut wajib belum lengkap dan tunjukkan isian yang kurang. | Memenuhi skenario validasi KF-01; tidak menyimpan data parsial. |
| 1 | KF-01 (Must — usulan) | Uji penyimpanan berhasil dan atribut wajib belum lengkap. | Memastikan kedua skenario KF-01 dapat diperiksa. |
| 2 | KF-02 (Must — usulan) | Konfirmasi bidang pencarian dan aturan kecocokan. | PRD belum menetapkan apa yang dicari atau definisi kecocokan. |
| 2 | KF-02 (Must — usulan) | Tampilkan resep yang cocok dengan kata kunci menurut aturan yang disepakati. | Memenuhi skenario hasil pencarian. |
| 2 | KF-02 (Must — usulan) | Tampilkan keadaan tanpa hasil ketika tidak ada resep yang cocok. | Memenuhi skenario pencarian tanpa hasil. |
| 2 | KF-02 (Must — usulan) | Tampilkan nama, bahan, dan langkah saat resep dibuka. | Memenuhi skenario membaca rincian resep. |
| 2 | KF-02 (Must — usulan) | Uji hasil cocok, tanpa hasil, dan rincian resep. | Memastikan skenario KF-02 dapat diperiksa. |
| 3 | KF-03 (Should — usulan) | Konfirmasi siapa yang boleh mengoreksi takaran dan apakah nilai lama perlu disimpan. | Kewenangan dan riwayat koreksi masih menjadi pertanyaan terbuka. |
| 3 | KF-03 (Should — usulan) | Simpan serta tampilkan kembali takaran resep yang dikoreksi sesuai keputusan. | Bergantung pada resep yang dapat dibuka dan aturan yang disepakati. |
| 3 | KF-03 (Should — usulan) | Uji penyimpanan dan pembacaan kembali takaran yang dikoreksi. | Memastikan skenario KF-03 dapat diperiksa. |
| 3 | KF-04 (Should — usulan) | Konfirmasi cara penyimpanan foto, batas berkas, dan hak akses. | Mekanisme foto belum ditetapkan pada PRD. |
| 3 | KF-04 (Should — usulan) | Kaitkan foto pilihan dengan resep dan tampilkan hanya foto resep tersebut. | Bergantung pada keputusan cara penyimpanan dan resep yang tersedia. |
| 3 | KF-04 (Should — usulan) | Uji pengaitan dan penampilan foto pada resep terkait. | Memastikan skenario KF-04 dapat diperiksa. |

**Fitur yang dikerjakan pada branch ini:** KF-01, pencatatan resep. Aturan prototipe yang dipilih pengguna adalah nama wajib, minimal satu bahan, dan minimal satu langkah; ini belum menjadi persetujuan klien. KF-02 tetap menunggu kesepakatan bidang dan aturan pencarian.

Urutan KF-02 bergantung pada data KF-01. KF-03 dan KF-04 bergantung pada resep yang dapat dibuka dan konfirmasi aturan bisnisnya.