"""
Script Utama Menjalankan Aplikasi Web Manajemen Tugas Harian
"""
import sys
from app import app
from config import Config

if __name__ == '__main__':
    print("=" * 60)
    print(" MODUL PENCATATAN TUGAS HARIAN PERUSAHAAN")
    print(f" Status: Server aktif berjalan di http://localhost:{Config.PORT}")
    print(f" Database: MySQL ({Config.DB_USER}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME})")
    print(" Tekan CTRL + C untuk menghentikan server.")
    print("=" * 60)
    try:
        app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
    except KeyboardInterrupt:
        print("\n[!] Server dimatikan oleh pengguna.")
        sys.exit(0)
