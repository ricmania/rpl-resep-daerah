# Pertanyaan konfirmasi aturan data

> **Status: belum diajukan.** Tidak ada jawaban klien yang tersedia. Jangan anggap usulan di bawah sebagai persetujuan atau kebijakan yang sudah berlaku. Catat jawaban setelah konfirmasi pada bagian Riwayat Konfirmasi di [SRS](../srs.md), lalu selaraskan kamus data, ERD, dan skema.

| Topik | Pertanyaan untuk klien | Bagian rancangan yang terpengaruh |
|---|---|---|
| Kelengkapan resep | Saat menyimpan, apakah nama, minimal satu bahan, dan minimal satu langkah semuanya wajib? Bolehkah menyimpan draf yang belum lengkap? | `resep.nama`, jumlah baris `resep_bahan` dan `langkah_resep`; validasi aplikasi |
| Rincian bahan | Apakah jumlah dan satuan perlu dicatat? Bolehkah salah satunya belum diketahui? Pecahan atau nilai nol seperti “secukupnya” bagaimana dicatat? | `resep_bahan.jumlah`, `resep_bahan.satuan`, aturan nilai |
| Bahan berulang | Apakah bahan yang sama boleh dicantumkan lebih dari sekali dalam satu resep (misalnya dipakai pada tahap berbeda)? Bagaimana nama bahan yang sama ditulis/diidentifikasi? | Relasi dan aturan duplikasi `resep_bahan`, keunikan `bahan.nama` |
| Langkah | Apakah langkah harus bernomor dan unik per resep? Apakah langkah boleh diedit, dihapus, atau disisipkan di antara langkah yang ada? | `langkah_resep.urutan` dan perilaku pembaruan |
| Nama resep | Bolehkah dua resep memakai nama yang sama? Jika tidak, apakah keunikannya berlaku tanpa membedakan kapitalisasi atau spasi? | Keunikan dan normalisasi `resep.nama` |
| Pencarian | Bidang apa yang dicari (nama, bahan, atau lainnya), dan apakah kecocokan harus sama persis atau boleh sebagian? | KF-02 dan strategi pencarian |
| Penghapusan dan retensi | Bolehkah resep/bahan dihapus? Jika resep dihapus, apa yang harus terjadi pada bahan dan langkah terkait? Berapa lama data disimpan? | Kebijakan FK, retensi, dan penghapusan |
| Koreksi dan foto | Apakah riwayat koreksi atau foto benar-benar perlu disimpan untuk versi awal? | Cakupan entitas dan kebutuhan lanjutan; belum dimasukkan ke ERD |

Setelah jawaban diterima, catat tanggal, jawaban, dan tindak lanjut pada Riwayat Konfirmasi SRS. Jangan merekam data pribadi atau materi klien yang tidak diperlukan.
