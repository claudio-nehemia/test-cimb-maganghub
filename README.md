# Modul Web Pencatatan Tugas Harian Perusahaan

Aplikasi web modul pencatatan dan pengelolaan tugas harian (*daily task tracking*) yang dirancang untuk mendukung operasional internal perusahaan. Aplikasi ini memfasilitasi monitoring beban kerja karyawan, pencatatan target harian, status perkembangan tugas, hingga pelaporan berkala lintas departemen.

Aplikasi dibangun menggunakan bahasa pemrograman **Python** dengan kerangka kerja **Flask**, serta basis data relasional **MySQL**.

---

## 1. Fitur Utama Aplikasi

1. **Dashboard Metrik & Ringkasan Status**
   - Menampilkan total tugas terdaftar.
   - Perhitungan otomatis tugas belum dimulai, sedang dikerjakan, dan selesai.
   - Indikator persentase penyelesaian tugas (*completion rate*).
   - Deteksi dini tugas yang jatuh tempo hari ini dan tugas yang telah terlewat (*overdue*).

2. **Pengelolaan Tugas Lengkap (CRUD)**
   - **Tambah Tugas Baru:** Mengisi judul, deskripsi rinci, staf penanggung jawab, divisi/departemen, tingkat prioritas, status pengerjaan, dan batas waktu (*due date*).
   - **Tinjau Detail Tugas:** Melihat informasi lengkap riwayat tugas, waktu pembuatan, pembaruan terakhir, dan waktu penyelesaian.
   - **Perbarui Data Tugas:** Mengubah detail tugas serta penyesuaian otomatis timestamp selesai (`completed_at`).
   - **Hapus Data Tugas:** Mekanisme penghapusan aman dilengkapi modal konfirmasi.

3. **Aksi Cepat Status (*Quick Status Toggle*)**
   - Memungkinkan pengawas atau staf mengubah status pengerjaan tugas secara langsung dari tabel dashboard tanpa harus masuk ke halaman edit.

4. **Penyaringan & Pencarian Lanjutan (*Multi-filter & Search*)**
   - Pencarian berdasarkan kata kunci pada judul tugas, deskripsi, maupun nama karyawan.
   - Filter spesifik berdasarkan status, tingkat prioritas, departemen kerja, dan rentang tanggal (Hari Ini, Mendatang, Terlewat).
   - Pengurutan data (*sorting*) berdasarkan batas waktu terdekat, tingkat prioritas, maupun waktu pembuatan.

5. **Ekspor Data Laporan (CSV)**
   - Ekspor seluruh daftar tugas ke dalam format CSV dengan pengkodean UTF-8 BOM, sehingga dapat dibuka langsung dengan rapi pada Microsoft Excel maupun Google Sheets.

---

## 2. Struktur Direktori Proyek

```text
test_cimb/
├── app.py                      # Router utama, logika controller, dan error handling
├── config.py                   # Konfigurasi aplikasi dan variabel lingkungan
├── db.py                       # Handler koneksi MySQL dan inisialisasi tabel otomatis
├── schema.sql                  # Skrip DDL basis data MySQL dan data awal
├── run.py                      # Skrip runner eksekusi server web
├── requirements.txt            # Daftar pustaka / dependensi Python
├── generate_pdf.py             # Generator dokumen spesifikasi teknis format PDF
├── .env.example                # Templat konfigurasi lingkungan
├── .env                        # Konfigurasi aktif lokal
├── templates/
│   ├── base.html               # Layout dasar, navbar, dan struktur halaman
│   ├── index.html              # Tampilan dashboard, metrik, filter, dan tabel
│   ├── form.html               # Tampilan formulir tambah & edit tugas
│   └── detail.html             # Tampilan informasi rinci satu tugas
├── static/
│   ├── css/
│   │   └── style.css           # Berkas CSS kustom tampilan antarmuka
│   └── js/
│       └── script.js           # Berkas JavaScript modal dan interaksi dinamis
└── Dokumentasi_Modul_Tugas_Harian.pdf # Laporan dokumentasi resmi format PDF
```

---

## 3. Perancangan Basis Data

Aplikasi menggunakan basis data bernama `db_tugas_harian` dengan tabel utama `tasks`.

### Struktur Tabel `tasks`

| Nama Kolom | Tipe Data | Keterangan |
| :--- | :--- | :--- |
| `id` | INT AUTO_INCREMENT (PK) | Pengidentifikasi unik tugas |
| `title` | VARCHAR(255) NOT NULL | Judul ringkas pekerjaan |
| `description` | TEXT NULL | Deskripsi detail atau kriteria hasil |
| `assigned_to` | VARCHAR(100) NOT NULL | Nama karyawan / penanggung jawab |
| `department` | VARCHAR(50) NOT NULL | Divisi (TI, Keuangan, Operasional, HR, dll.) |
| `priority` | ENUM('Rendah', 'Sedang', 'Tinggi') | Tingkat urgensi pengerjaan |
| `status` | ENUM('Belum Dimulai', 'Sedang Dikerjakan', 'Selesai') | Status progres pengerjaan |
| `due_date` | DATE NOT NULL | Batas waktu penyelesaian tugas |
| `completed_at`| DATETIME NULL | Waktu aktual tugas ditandai selesai |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Waktu pencatatan data ke sistem |
| `updated_at` | TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Waktu pembaruan data terakhir |

---

## 4. Panduan Instalasi dan Menjalankan Sistem

### A. Prasyarat Sistem
1. Python versi 3.10 atau yang lebih baru.
2. Server MySQL / MariaDB (dapat menggunakan Laragon, XAMPP, atau instalasi mandiri).
3. Web browser modern (Google Chrome, Mozilla Firefox, Microsoft Edge).

### B. Konfigurasi Lingkungan (.env)
Salin berkas `.env.example` menjadi `.env` lalu sesuaikan kredensial MySQL lokal Anda:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=db_tugas_harian

SECRET_KEY=kunci-rahasia-perusahaan-2026
FLASK_DEBUG=True
PORT=5000
```

### C. Persiapan Basis Data MySQL
Pastikan layanan MySQL sudah berjalan pada komputer Anda. Terdapat dua alternatif persiapan database:
1. **Otomatis:** Sistem akan secara otomatis mendeteksi, membuat database `db_tugas_harian`, tabel `tasks`, serta data awal ketika aplikasi pertama kali dijalankan.
2. **Manual:** Anda dapat mengeksekusi berkas `schema.sql` melalui antarmuka MySQL CLI, phpMyAdmin, atau HeidiSQL:
   ```bash
   mysql -u root -p < schema.sql
   ```

### D. Instalasi Dependensi Python
Pasang paket-paket pustaka yang dibutuhkan melalui terminal:
```bash
pip install -r requirements.txt
```

### E. Menjalankan Aplikasi
Eksekusi perintah berikut pada direktori proyek:
```bash
python run.py
```
atau:
```bash
python app.py
```

Setelah server aktif, buka peramban dan akses alamat:
```
http://localhost:5000
```

---

## 5. Ringkasan Endpoint Aplikasi

| Metode | URL | Fungsi / Deskripsi |
| :--- | :--- | :--- |
| `GET` | `/` | Menampilkan dashboard utama, ringkasan metrik, filter, dan tabel tugas |
| `GET` | `/tasks/new` | Menampilkan formulir pencatatan tugas baru |
| `POST` | `/tasks/new` | Memvalidasi dan menyimpan data tugas baru ke basis data |
| `GET` | `/tasks/<id>` | Menampilkan rincian lengkap tugas berdasarkan ID |
| `GET` | `/tasks/<id>/edit` | Menampilkan formulir penyuntingan tugas |
| `POST` | `/tasks/<id>/edit` | Memvalidasi dan menyimpan perubahan data tugas |
| `POST` | `/tasks/<id>/quick-status` | Memperbarui status tugas secara instan dari dashboard |
| `POST` | `/tasks/<id>/delete` | Menghapus catatan tugas dari basis data |
| `GET` | `/export/csv` | Mengunduh seluruh catatan tugas dalam format berkas CSV |
