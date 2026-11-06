import os
from dotenv import load_dotenv

# Memuat konfigurasi dari file .env bila tersedia
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'perusahaan-tugas-harian-secure-key-2026')
    
    # Pengaturan Koneksi Database MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'db_tugas_harian')
    
    # Opsi Server Aplikasi
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PORT = int(os.getenv('PORT', 5000))
