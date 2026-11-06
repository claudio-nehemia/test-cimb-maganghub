-- Skema Database Modul Pencatatan Tugas Harian (db_tugas_harian)
-- Dibuat untuk: Modul Pengelolaan Tugas Harian Karyawan Perusahaan

CREATE DATABASE IF NOT EXISTS db_tugas_harian 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE db_tugas_harian;

-- Tabel Utama: tasks
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT 'Judul atau ringkasan tugas',
    description TEXT NULL COMMENT 'Rincian deskripsi pekerjaan',
    assigned_to VARCHAR(100) NOT NULL COMMENT 'Nama staf penanggung jawab tugas',
    department VARCHAR(50) NOT NULL COMMENT 'Divisi/Departemen pelaksana',
    priority ENUM('Rendah', 'Sedang', 'Tinggi') NOT NULL DEFAULT 'Sedang' COMMENT 'Tingkat urgensi tugas',
    status ENUM('Belum Dimulai', 'Sedang Dikerjakan', 'Selesai') NOT NULL DEFAULT 'Belum Dimulai' COMMENT 'Status progres tugas',
    due_date DATE NOT NULL COMMENT 'Batas waktu pengerjaan',
    completed_at DATETIME NULL COMMENT 'Waktu aktual saat tugas ditandai selesai',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_due_date (due_date),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data Awal Perusahaan (Sample Dummy Data)
INSERT INTO tasks (title, description, assigned_to, department, priority, status, due_date, completed_at, created_at)
VALUES 
('Rekonsiliasi Transaksi Harian Cabang', 'Melakukan pengecekan dan pencocokan mutasi kas masuk dan keluar dari 5 kantor cabang utama.', 'Budi Santoso', 'Keuangan', 'Tinggi', 'Sedang Dikerjakan', CURDATE(), NULL, NOW()),
('Pembaruan Patch Keamanan Server Core', 'Menerapkan patch update keamanan OS Linux dan database server staging sebelum rilis production.', 'Claudio Nehemia', 'Teknologi Informasi', 'Tinggi', 'Sedang Dikerjakan', CURDATE(), NULL, NOW()),
('Penyusunan Materi Pelatihan Karyawan Baru', 'Menyusun silabus onboarding dan modul standar operasional prosedur untuk rekrutan divisi operasional.', 'Siti Rahmawati', 'Human Resources', 'Sedang', 'Belum Dimulai', DATE_ADD(CURDATE(), INTERVAL 1 DAY), NULL, NOW()),
('Audit Fisik Inventaris Perangkat IT Kantor', 'Mendata seluruh serial number laptop dinas dan perangkat jaringan di lantai 3 dan 4.', 'Ahmad Fauzi', 'Operasional', 'Rendah', 'Belum Dimulai', DATE_ADD(CURDATE(), INTERVAL 3 DAY), NULL, NOW()),
('Evaluasi Analitik Kampanye Digital Kuartal Ini', 'Menarik data Google Ads, Meta Ads, serta konversi pendaftaran nasabah baru bulan berjalan.', 'Dewi Lestari', 'Pemasaran', 'Sedang', 'Selesai', CURDATE(), NOW(), DATE_SUB(NOW(), INTERVAL 4 HOUR)),
('Review Perjanjian Kerjasama Vendor Pihak Ketiga', 'Memeriksa klausul kerahasiaan data (NDA) dan SLA pada draf kontrak penyedia layanan cloud storage.', 'Hendrik Wijaya', 'Legal & Kepatuhan', 'Tinggi', 'Selesai', DATE_SUB(CURDATE(), INTERVAL 1 DAY), NOW(), DATE_SUB(NOW(), INTERVAL 1 DAY));
