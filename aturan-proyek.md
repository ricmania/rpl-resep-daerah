# Aturan Proyek

Dokumen ini mencatat aturan teknis awal untuk aplikasi pengelolaan resep. Struktur dan batasan di bawah adalah rancangan yang belum divalidasi klien.

## Struktur folder

Lihat [rancangan arsitektur](docs/desain/arsitektur.md#struktur-folder-yang-diusulkan) untuk struktur dan tanggung jawab berkas. Struktur tersebut adalah target; berkas aplikasi belum dibuat.

## Akses SQLite

- Hanya `app/models.py` yang boleh membuka koneksi SQLite atau menjalankan SQL aplikasi.
- Routes, layanan bisnis, dan view tidak boleh mengakses SQLite secara langsung.
- Uji skema dapat memakai SQLite langsung untuk memverifikasi kendala basis data.
- Jangan menambahkan berkas basis data lokal `instance/resep.db` ke Git.

## Membuat atau menguji skema

Skema sumber berada di `docs\desain\schema.sql`. Untuk membuat ulang basis data lokal, jalankan dari root proyek:

```powershell
New-Item -ItemType Directory -Force instance | Out-Null
python -c "import sqlite3; from pathlib import Path; c=sqlite3.connect(r'instance\resep.db'); c.execute('PRAGMA foreign_keys = ON'); c.executescript(Path(r'docs\desain\schema.sql').read_text(encoding='utf-8')); c.close()"
```

Perintah tersebut menjalankan `CREATE TABLE` dan karena itu ditujukan untuk basis data baru. Jalankan uji batasan dengan:

```powershell
python tests\cek_skema.py
```

## Konsistensi rancangan

Perubahan tabel harus diselaraskan pada `docs\desain\erd.mmd`, `docs\desain\kamus-data.md`, `docs\desain\normalisasi.md`, dan `docs\desain\schema.sql`. Aturan atribut wajib, pencarian, penghapusan, dan retensi menunggu konfirmasi klien.
