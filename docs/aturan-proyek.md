# Aturan Proyek

## 1. Stack

- Bahasa pemrograman: Python 3.14; versi minimum yang didukung Python 3.10.
- Framework web: Flask.
- Basis data: SQLite.
- Paket/dependensi lain hanya boleh ditambahkan setelah disetujui kelompok.

## 2. Struktur folder

```text
app.py          Titik masuk aplikasi
templates/      Template halaman
static/         Berkas statis, seperti CSS, JavaScript, dan gambar
tests/          Uji otomatis
docs/           Dokumentasi proyek
```

Jangan menambahkan atau memindahkan struktur utama tanpa persetujuan kelompok.

## 3. Konvensi

- Gunakan bahasa Indonesia untuk komentar dan pesan yang ditampilkan kepada pengguna.
- Gunakan `snake_case` untuk variabel dan fungsi Python, `PascalCase` untuk kelas, serta nama berkas/folder huruf kecil dengan tanda hubung bila diperlukan.
- Satu commit berisi satu fitur atau satu perubahan yang saling terkait; tulis pesan commit yang menjelaskan perubahan.
- Ikuti aturan Git dalam [kesepakatan-tim.md](./kesepakatan-tim.md): gunakan branch `fitur-...`, `perbaikan-...`, atau `docs-...`; jangan push langsung ke `main`; ajukan Pull Request dan minta tinjauan minimal satu anggota lain sebelum merge.
- **Aturan penggunaan AI:** setiap penggunaan AI dicatat di Jurnal Vibe Coding; jangan masukkan data pribadi klien, kata sandi, atau kunci ke AI; tinjau kode hasil AI sebelum di-commit.

## 4. Larangan

- Jangan menambah paket atau dependensi tanpa persetujuan kelompok.
- Jangan menyimpan rahasia, seperti kata sandi, token, atau kunci, di dalam kode maupun repositori.
- Jangan mengubah berkas di luar lingkup tugas yang disepakati.
- Jangan menghapus, melemahkan, atau mengubah uji hanya agar perubahan terlihat lulus.
- Jangan melewati proses branch dan Pull Request yang ditetapkan dalam kesepakatan tim.

## 5. Cara menjalankan dan menguji

Jalankan perintah dari direktori utama proyek setelah struktur aplikasi tersedia:

```powershell
python app.py
```

Jalankan uji otomatis dengan `unittest` bawaan Python:

```powershell
python -m unittest discover -s tests
```

Jika cara menjalankan aplikasi atau pengujian berubah, perbarui bagian ini dan beri tahu kelompok melalui Pull Request.