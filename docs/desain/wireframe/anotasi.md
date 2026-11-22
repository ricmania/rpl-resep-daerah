# Anotasi wireframe

Nomor anotasi pada gambar bersesuaian dengan nomor pada tabel. Menu, judul/identitas halaman, dan area pesan diletakkan konsisten di setiap layar. Pesan tetap disediakan meskipun halaman tidak memuat aksi penyimpanan. Isian angka dibatasi dan instruksi menyatakan aturan; warna bukan satu-satunya pembeda pesan.

## Pemetaan elemen per layar

| Wireframe | Nomor | Elemen | Data / aksi | Aturan / pesan | Prinsip |
|---|---:|---|---|---|---|
| Semua halaman | — | Menu navigasi di header | Beranda, cari resep, catat resep, bahan, akun* | Urutan dan label konsisten; kontrol akses belum ditetapkan | Konsistensi, navigasi jelas |
| Semua halaman | 5 | Area pesan | Status aksi terakhir | Pesan keberhasilan atau kesalahan tampil sebagai teks | Umpan balik |
| wf-01-login | 1 | Pemberitahuan login | Tidak ada data akun | “Autentikasi belum ditentukan; jangan masukkan kredensial.” | Pencegahan galat, privasi |
| wf-01-login | 2 | Penjelasan placeholder | Tidak ada kolom akun atau kata sandi | “Autentikasi belum ditentukan” | Kejelasan, privasi |
| wf-01-login | 3 | Tombol kembali | Menuju beranda | “Lanjut ke rancangan beranda (alur placeholder)” | Umpan balik, kontrol pengguna |
| wf-02-beranda | 1 | Ringkasan menu | Pencarian, catat, bahan | Label dan urutan sama di semua halaman | Konsistensi |
| wf-02-beranda | 2 | Tautan pencarian | Membuka daftar resep | Membuka alur KF-02 | Navigasi |
| wf-02-beranda | 3 | Tautan catat resep | Membuka formulir | Ditujukan untuk Pengelola resep; akses belum ditegakkan | Navigasi, kesesuaian aktor |
| wf-03-daftar-resep | 1 | Isian kata kunci | Kata kunci untuk KF-02 | Aturan bidang dan kecocokan menunggu konfirmasi; jangan menyiratkan cakupan pencarian tertentu | Pencegahan galat, istilah jelas |
| wf-03-daftar-resep | 2 | Tombol cari | Meminta pencarian | Kesalahan/kegagalan pencarian disampaikan di area pesan | Umpan balik |
| wf-03-daftar-resep | 3 | Daftar hasil | `resep.id`, `resep.nama` | Tampilkan hanya resep cocok menurut aturan yang kelak disepakati | Keterlihatan status |
| wf-03-daftar-resep | 4 | Tautan rincian | Membuka resep terpilih | Tampilkan identitas resep agar pilihan jelas | Kontrol pengguna |
| wf-04-form-resep | 1 | Isian nama | `resep.nama` | Wajib bisnis menunggu kesepakatan; jika kosong, jelaskan bagian yang perlu dilengkapi | Pencegahan galat |
| wf-04-form-resep | 2 | Daftar bahan | `bahan.nama`, `resep_bahan.jumlah`, `resep_bahan.satuan` | `jumlah` angka positif bila dicantumkan menurut draf skema; presisi/unit belum disepakati | Pencegahan galat |
| wf-04-form-resep | 3 | Langkah berurutan | `langkah_resep.urutan`, `langkah_resep.instruksi` | Nomor urut positif; pesan menunjukkan langkah yang belum lengkap | Pengelompokan, pencegahan galat |
| wf-04-form-resep | 4 | Tombol simpan | Menyimpan resep | Jangan memberi sukses jika gagal; tampilkan atribut yang belum lengkap dan jangan menyimpan | Umpan balik |
| wf-05-rincian-resep | 1 | Identitas resep | `resep.id`, `resep.nama` | Tampilkan resep yang sedang dibuka | Keterlihatan status |
| wf-05-rincian-resep | 2 | Rincian bahan | `bahan.nama`, `resep_bahan.jumlah`, `resep_bahan.satuan` | Nilai opsional yang tidak diketahui tidak ditampilkan seolah-olah diketahui | Akurasi |
| wf-05-rincian-resep | 3 | Rincian langkah | `langkah_resep.urutan`, `langkah_resep.instruksi` | Urutkan menurut `urutan` | Konsistensi |
| wf-05-rincian-resep | 4 | Tombol kembali | Kembali ke daftar hasil | Tidak mengubah data resep | Kontrol pengguna |
| wf-06-daftar-bahan | 1 | Daftar bahan | `bahan.id`, `bahan.nama` | Tidak mengasumsikan nama bahan unik sebelum dikonfirmasi | Akurasi |
| wf-06-daftar-bahan | 2 | Tombol kembali | Kembali ke beranda | Tidak mengubah data resep tanpa aksi eksplisit | Kontrol pengguna |
| wf-07-keadaan | 1 | Pesan validasi | Nama atribut wajib yang kosong | Jangan menyimpan resep; jelaskan isian yang perlu diperbaiki | Pencegahan galat, umpan balik |
| wf-07-keadaan | 2 | Pesan tanpa hasil | Kata kunci pencarian | “Tidak ada resep yang cocok”; jangan tampilkan daftar hasil seolah ada kecocokan | Umpan balik |
| wf-07-keadaan | 3 | Tautan tindakan lanjutan | Perbaiki form atau ubah kata kunci | Sediakan jalan kembali yang jelas | Kontrol pengguna |

## Pemeriksaan prinsip dan contoh sebelum–sesudah

- **Konsistensi:** setiap gambar memakai menu dan area pesan yang sama; aksi utama berada pada area isi dan dinamai dengan kata kerja.
- **Umpan balik:** simpan, pencarian, validasi, dan keadaan tanpa hasil semuanya memiliki pesan yang terlihat.
- **Pencegahan galat:** jumlah disajikan sebagai angka dengan aturan positif dari draf skema; aturan itu masih harus dikonfirmasi. Tidak ada placeholder nilai turunan seperti total.
- **Keterbacaan:** nama menu dan judul berupa teks; pesan tidak dibedakan melalui warna saja.

| Sebelum | Sesudah | Prinsip |
|---|---|---|
| Kolom `jumlah` berupa teks bebas sehingga masukan seperti “dua” mungkin terkirim. | Kolom jumlah diberi label angka dan petunjuk “lebih dari 0 bila diisi”; pesan validasi disediakan. | Pencegahan galat dan umpan balik; ambang berasal dari draf skema dan menunggu konfirmasi. |
