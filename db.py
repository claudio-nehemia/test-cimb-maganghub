import pymysql
from pymysql.cursors import DictCursor
from config import Config

def get_db_connection():
    """
    Membuka dan mengembalikan koneksi baru ke basis data MySQL.
    Menggunakan DictCursor agar hasil query dikembalikan dalam bentuk dictionary.
    """
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=True
    )

def init_db():
    """
    Menginisialisasi basis data dan tabel tasks jika belum ada.
    Membuat database jika belum dibuat, lalu membuat tabel tugas.
    """
    try:
        # Koneksi awal ke server MySQL tanpa memilih database terlebih dahulu
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
        with conn.cursor() as cursor:
            # Pastikan database dibuat
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(f"USE `{Config.DB_NAME}`;")
            
            # Buat tabel tasks jika belum ada
            create_table_query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NULL,
                assigned_to VARCHAR(100) NOT NULL,
                department VARCHAR(50) NOT NULL,
                priority ENUM('Rendah', 'Sedang', 'Tinggi') NOT NULL DEFAULT 'Sedang',
                status ENUM('Belum Dimulai', 'Sedang Dikerjakan', 'Selesai') NOT NULL DEFAULT 'Belum Dimulai',
                due_date DATE NOT NULL,
                completed_at DATETIME NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_status (status),
                INDEX idx_priority (priority),
                INDEX idx_due_date (due_date),
                INDEX idx_department (department)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            cursor.execute(create_table_query)
            
            # Periksa apakah tabel kosong, jika iya masukkan data awal
            cursor.execute("SELECT COUNT(*) AS total FROM tasks;")
            count = cursor.fetchone()['total']
            if count == 0:
                seed_query = """
                INSERT INTO tasks (title, description, assigned_to, department, priority, status, due_date, completed_at)
                VALUES 
                ('Rekonsiliasi Transaksi Harian Cabang', 'Melakukan pengecekan dan pencocokan mutasi kas masuk dan keluar dari 5 kantor cabang utama.', 'Budi Santoso', 'Keuangan', 'Tinggi', 'Sedang Dikerjakan', CURDATE(), NULL),
                ('Pembaruan Patch Keamanan Server Core', 'Menerapkan patch update keamanan OS Linux dan database server staging sebelum rilis production.', 'Claudio Nehemia', 'Teknologi Informasi', 'Tinggi', 'Sedang Dikerjakan', CURDATE(), NULL),
                ('Penyusunan Materi Pelatihan Karyawan Baru', 'Menyusun silabus onboarding dan modul standar operasional prosedur untuk rekrutan divisi operasional.', 'Siti Rahmawati', 'Human Resources', 'Sedang', 'Belum Dimulai', DATE_ADD(CURDATE(), INTERVAL 1 DAY), NULL),
                ('Audit Fisik Inventaris Perangkat IT Kantor', 'Mendata seluruh serial number laptop dinas dan perangkat jaringan di lantai 3 dan 4.', 'Ahmad Fauzi', 'Operasional', 'Rendah', 'Belum Dimulai', DATE_ADD(CURDATE(), INTERVAL 3 DAY), NULL),
                ('Evaluasi Analitik Kampanye Digital Kuartal Ini', 'Menarik data Google Ads, Meta Ads, serta konversi pendaftaran nasabah baru bulan berjalan.', 'Dewi Lestari', 'Pemasaran', 'Sedang', 'Selesai', CURDATE(), NOW()),
                ('Review Perjanjian Kerjasama Vendor Pihak Ketiga', 'Memeriksa klausul kerahasiaan data (NDA) dan SLA pada draf kontrak penyedia layanan cloud storage.', 'Hendrik Wijaya', 'Legal & Kepatuhan', 'Tinggi', 'Selesai', DATE_SUB(CURDATE(), INTERVAL 1 DAY), NOW());
                """
                cursor.execute(seed_query)
        conn.close()
        return True, "Basis data dan tabel berhasil diverifikasi."
    except Exception as e:
        return False, str(e)
