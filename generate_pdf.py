"""
Script Pembuat Dokumen Dokumentasi Format PDF
Format: Formal Standard Paper (Times New Roman, Hitam, Tanpa Footer)
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)


def build_pdf(filename="Dokumentasi_Modul_Tugas_Harian.pdf"):
    # Dokumen A4 dengan margin standar formal
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()

    # Tipografi Times New Roman & Warna Hitam Penuh
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.black,
        alignment=1, # Rata tengah formal
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        textColor=colors.black,
        alignment=1,
        spaceAfter=14
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.black
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=colors.black,
        alignment=4, # Rata kiri-kanan (Justify)
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=colors.black,
        leftIndent=15,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.black
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.black,
        alignment=1 # Center header
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        textColor=colors.black
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        textColor=colors.black,
        alignment=1
    )

    elements = []

    # =========================================================================
    # JUDUL DOKUMEN & INFORMASI AWAL
    # =========================================================================
    elements.append(Paragraph("DOKUMENTASI SPESIFIKASI TEKNIS & PANDUAN IMPLEMENTASI", title_style))
    elements.append(Paragraph("MODUL WEB PENCATATAN TUGAS HARIAN PERUSAHAAN", title_style))
    elements.append(Paragraph("Aplikasi Pengelolaan Tugas Operasional Berbasis Python Flask & Database MySQL", subtitle_style))
    elements.append(Spacer(1, 8))

    meta_data = [
        [Paragraph("Nama Modul", meta_style), Paragraph(": Modul Web Pencatatan Tugas Harian (Daily Task Tracker)", meta_style)],
        [Paragraph("Bahasa / Framework", meta_style), Paragraph(": Python 3.13 / Flask 3.1", meta_style)],
        [Paragraph("Basis Data", meta_style), Paragraph(": MySQL 8.0 (Driver: PyMySQL)", meta_style)],
        [Paragraph("Pengembang", meta_style), Paragraph(": Claudio Nehemia Panggabean (NIM: 41522010144)", meta_style)],
        [Paragraph("Status Evaluasi", meta_style), Paragraph(": Rilis Final untuk Pengujian Fungsional", meta_style)],
        [Paragraph("Tanggal", meta_style), Paragraph(f": {datetime.now().strftime('%d %B %Y')}", meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[4.2 * cm, 12.3 * cm])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 12))

    # =========================================================================
    # BAB 1: PENDAHULUAN
    # =========================================================================
    elements.append(Paragraph("1.0 PENDAHULUAN", h1_style))
    
    elements.append(Paragraph("1.1 Latar Belakang Kebutuhan", h2_style))
    elements.append(Paragraph(
        "Aktivitas operasional harian pada lingkungan perusahaan menuntut koordinasi kerja yang jelas, "
        "terdokumentasi, dan terukur. Tanpa sistem pencatatan yang terintegrasi, tugas-tugas harian antarstaf "
        "rentan mengalami keterlambatan penyelesaian, tumpang tindih penanggung jawab, serta menyulitkan pihak "
        "manajemen dalam mengevaluasi progres kerja divisi secara objektif. Oleh karena itu, modul web pencatatan "
        "tugas harian ini dikembangkan sebagai media pencatatan mandiri yang terpusat, cepat, dan mudah diakses.",
        body_style
    ))

    elements.append(Paragraph("1.2 Maksud dan Tujuan", h2_style))
    elements.append(Paragraph("Pengembangan modul web ini memiliki tujuan pokok sebagai berikut:", body_style))
    elements.append(Paragraph("1. Menyediakan modul web terpusat untuk mendokumentasikan setiap penugasan harian karyawan.", bullet_style))
    elements.append(Paragraph("2. Mengelola status perkembangan pekerjaan secara transparan (Belum Dimulai, Sedang Dikerjakan, Selesai).", bullet_style))
    elements.append(Paragraph("3. Mengelompokkan tugas berdasarkan divisi/departemen kerja, tingkat prioritas, dan batas waktu penyelesaian.", bullet_style))
    elements.append(Paragraph("4. Menyajikan ringkasan metrik statistik (rasio penyelesaian tugas dan deteksi tugas lewat batas waktu/overdue).", bullet_style))
    elements.append(Paragraph("5. Memfasilitasi ekspor rekapitulasi data tugas ke dalam format berkas CSV yang kompatibel dengan Microsoft Excel.", bullet_style))

    elements.append(Paragraph("1.3 Ruang Lingkup Sistem", h2_style))
    elements.append(Paragraph(
        "Sistem dirancang sebagai modul operasional berbasis web yang dapat dijalankan pada jaringan lokal (intranet) "
        "maupun cloud. Pengelolaan data mencakup operasi pembuatan tugas baru, pembaruan data, peninjauan rincian, "
        "pengubahan status cepat, penghapusan data dengan konfirmasi keamanan, serta penyaringan data terpadu.",
        body_style
    ))

    # =========================================================================
    # BAB 2: ARSITEKTUR DAN TEKNOLOGI
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("2.0 ARSITEKTUR DAN SPESIFIKASI TEKNOLOGI", h1_style))
    
    elements.append(Paragraph("2.1 Komponen Sistem", h2_style))
    elements.append(Paragraph(
        "Arsitektur modul menggunakan pola Model-View-Controller (MVC) ringan yang diakomodasi secara terstruktur "
        "pada kerangka kerja Python Flask:",
        body_style
    ))

    tech_data = [
        [Paragraph("Komponen", table_header_style), Paragraph("Teknologi yang Digunakan", table_header_style), Paragraph("Keterangan dan Peran Sistem", table_header_style)],
        [Paragraph("Backend", table_cell_style), Paragraph("Python 3.13 & Flask 3.1", table_cell_style), Paragraph("Pemroses logika bisnis, perutean HTTP, validasi form, dan templating Jinja2.", table_cell_style)],
        [Paragraph("Basis Data", table_cell_style), Paragraph("MySQL 8.0 (PyMySQL)", table_cell_style), Paragraph("Penyimpanan relasional dengan transaksi ACID dan pengindeksan performa.", table_cell_style)],
        [Paragraph("Frontend", table_cell_style), Paragraph("HTML5, CSS3, Bootstrap 5.3", table_cell_style), Paragraph("Antarmuka pengguna responsif dengan struktur rapi dan navigasi intuitif.", table_cell_style)],
        [Paragraph("Simbol / Ikon", table_cell_style), Paragraph("Font Awesome 6", table_cell_style), Paragraph("Ikon visual untuk status pengerjaan, prioritas, dan aksi tombol.", table_cell_style)],
        [Paragraph("Konfigurasi", table_cell_style), Paragraph("python-dotenv", table_cell_style), Paragraph("Pengelolaan variabel lingkungan (.env) agar kredensial database terisolasi aman.", table_cell_style)]
    ]
    t_tech = Table(tech_data, colWidths=[2.5 * cm, 4.8 * cm, 9.2 * cm])
    t_tech.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_tech)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("2.2 Struktur Berkas Proyek", h2_style))
    elements.append(Paragraph(
        "Struktur direktori disusun secara modular untuk memudahkan pemeliharaan kode:",
        body_style
    ))
    tree_text = (
        "test_cimb/<br/>"
        "&nbsp;&nbsp;[+] app.py : Controller utama, routing HTTP, logika kalkulasi statistik<br/>"
        "&nbsp;&nbsp;[+] config.py : Pemetaan konfigurasi server dan kredensial database dari .env<br/>"
        "&nbsp;&nbsp;[+] db.py : Konektor PyMySQL dan inisialisasi tabel otomatis<br/>"
        "&nbsp;&nbsp;[+] schema.sql : Berkas skrip SQL DDL tabel tasks dan data sampel awal<br/>"
        "&nbsp;&nbsp;[+] run.py : Berkas runner untuk mengeksekusi server web lokal<br/>"
        "&nbsp;&nbsp;[+] requirements.txt : Daftar dependensi pustaka Python<br/>"
        "&nbsp;&nbsp;[+] templates/ : Templat antarmuka (base.html, index.html, form.html, detail.html)<br/>"
        "&nbsp;&nbsp;[+] static/ : Berkas statis CSS (desain) dan JavaScript (interaktivitas modal)"
    )
    elements.append(Paragraph(tree_text, code_style))

    # =========================================================================
    # BAB 3: PERANCANGAN BASIS DATA
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("3.0 PERANCANGAN BASIS DATA (DATABASE DESIGN)", h1_style))
    elements.append(Paragraph(
        "Basis data yang digunakan bernama <b>db_tugas_harian</b> dengan set karakter <b>utf8mb4</b> "
        "dan engine penyimpanan <b>InnoDB</b>. Seluruh entitas tugas dicatat dalam tabel <b>tasks</b>.",
        body_style
    ))

    elements.append(Paragraph("3.1 Kamus Data Tabel 'tasks'", h2_style))
    db_schema = [
        [Paragraph("Nama Kolom", table_header_style), Paragraph("Tipe Data", table_header_style), Paragraph("Null / Default", table_header_style), Paragraph("Keterangan Fungsi", table_header_style)],
        [Paragraph("id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL, PK, AI", table_cell_style), Paragraph("Nomor identitas unik setiap tugas.", table_cell_style)],
        [Paragraph("title", table_cell_style), Paragraph("VARCHAR(255)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Judul pokok instruksi pekerjaan.", table_cell_style)],
        [Paragraph("description", table_cell_style), Paragraph("TEXT", table_cell_style), Paragraph("NULL", table_cell_style), Paragraph("Rincian detail spesifikasi pekerjaan.", table_cell_style)],
        [Paragraph("assigned_to", table_cell_style), Paragraph("VARCHAR(100)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Nama karyawan / staf penanggung jawab.", table_cell_style)],
        [Paragraph("department", table_cell_style), Paragraph("VARCHAR(50)", table_cell_style), Paragraph("NOT NULL, INDEX", table_cell_style), Paragraph("Divisi kerja pelaksana tugas.", table_cell_style)],
        [Paragraph("priority", table_cell_style), Paragraph("ENUM('Rendah','Sedang','Tinggi')", table_cell_style), Paragraph("DEFAULT 'Sedang', INDEX", table_cell_style), Paragraph("Tingkat kepentingan atau urgensi tugas.", table_cell_style)],
        [Paragraph("status", table_cell_style), Paragraph("ENUM('Belum Dimulai','Sedang Dikerjakan','Selesai')", table_cell_style), Paragraph("DEFAULT 'Belum Dimulai', INDEX", table_cell_style), Paragraph("Status tahapan pengerjaan tugas saat ini.", table_cell_style)],
        [Paragraph("due_date", table_cell_style), Paragraph("DATE", table_cell_style), Paragraph("NOT NULL, INDEX", table_cell_style), Paragraph("Batas akhir penyelesaian tugas.", table_cell_style)],
        [Paragraph("completed_at", table_cell_style), Paragraph("DATETIME", table_cell_style), Paragraph("NULL", table_cell_style), Paragraph("Waktu presisi saat tugas ditandai selesai.", table_cell_style)],
        [Paragraph("created_at", table_cell_style), Paragraph("TIMESTAMP", table_cell_style), Paragraph("CURRENT_TIMESTAMP", table_cell_style), Paragraph("Waktu pencatatan tugas ke dalam database.", table_cell_style)],
        [Paragraph("updated_at", table_cell_style), Paragraph("TIMESTAMP", table_cell_style), Paragraph("ON UPDATE CURRENT_TIMESTAMP", table_cell_style), Paragraph("Waktu pembaruan data terakhir.", table_cell_style)]
    ]
    t_schema = Table(db_schema, colWidths=[2.5 * cm, 4.3 * cm, 4.0 * cm, 5.7 * cm])
    t_schema.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(t_schema)

    elements.append(Paragraph("3.2 Optimasi Pengindeksan (Indexing)", h2_style))
    elements.append(Paragraph(
        "Kolom status, priority, due_date, dan department dipasangi indeks sekunder (B-Tree index). "
        "Optimasi ini memastikan bahwa operasi filtering komposit, pengurutan waktu, dan kalkulasi agregat "
        "tetap berkinerja tinggi saat volume data mencapai ribuan baris tugas.",
        body_style
    ))

    # =========================================================================
    # BAB 4: FITUR DAN ALUR KERJA SISTEM
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("4.0 FITUR DAN ALUR KERJA SISTEM", h1_style))

    elements.append(Paragraph("4.1 Dashboard dan Panel Metrik", h2_style))
    elements.append(Paragraph(
        "Halaman utama menyajikan ringkasan statistik yang diperbarui secara langsung dari basis data: "
        "Total Tugas, Tugas Belum Dimulai, Tugas Sedang Dikerjakan, Tugas Selesai, dan persentase ketuntasan. "
        "Sistem juga mendeteksi otomatis jika ada tugas yang jatuh tempo pada hari peninjauan atau tugas yang "
        "telah melewati batas waktu (overdue), ditandai dengan panel peringatan visual.",
        body_style
    ))

    elements.append(Paragraph("4.2 Operasi CRUD dan Aksi Cepat Status", h2_style))
    elements.append(Paragraph("1. Tambah Tugas Baru: Mengisi judul, deskripsi, nama staf, departemen, prioritas, status awal, dan batas waktu.", bullet_style))
    elements.append(Paragraph("2. Tinjau Detail: Melihat rincian instruksi lengkap beserta timestamp pembuatan dan penyelesaian.", bullet_style))
    elements.append(Paragraph("3. Sunting Tugas: Memperbarui parameter tugas apabila terjadi perubahan penugasan atau perpanjangan batas waktu.", bullet_style))
    elements.append(Paragraph("4. Aksi Cepat Status: Mengubah status tugas secara instan dari tabel utama tanpa harus membuka formulir edit penuh.", bullet_style))
    elements.append(Paragraph("5. Hapus Aman: Dilengkapi kotak dialog konfirmasi guna memvalidasi tindakan penghapusan.", bullet_style))

    elements.append(Paragraph("4.3 Penyaringan Data dan Ekspor Laporan CSV", h2_style))
    elements.append(Paragraph(
        "Sistem mendukung pencarian multi-kriteria berbasis kata kunci pada judul/staf, pemfilteran berdasarkan "
        "status pengerjaan, divisi kerja, dan kategori tanggal. Seluruh data yang tersaring dapat diunduh kapan saja "
        "dalam bentuk berkas CSV yang telah dilengkapi penanda UTF-8 BOM agar rapi saat dibuka pada Excel.",
        body_style
    ))

    # =========================================================================
    # BAB 5: PANDUAN INSTALASI & HASIL PENGUJIAN
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("5.0 PANDUAN INSTALASI DAN HASIL PENGUJIAN", h1_style))

    elements.append(Paragraph("5.1 Prosedur Instalasi dan Eksekusi Server", h2_style))
    elements.append(Paragraph(
        "1. Pastikan server MySQL lokal (Laragon/XAMPP/MySQL Service) telah aktif.<br/>"
        "2. Buat atau sesuaikan berkas .env dengan kredensial user dan password MySQL Anda.<br/>"
        "3. Pasang dependensi pustaka Python: <code>pip install -r requirements.txt</code><br/>"
        "4. Jalankan aplikasi melalui skrip runner: <code>python run.py</code><br/>"
        "5. Buka peramban web dan akses alamat: <b>http://localhost:5000</b>.",
        body_style
    ))

    elements.append(Paragraph("5.2 Hasil Pengujian Fungsional (Black-box Testing)", h2_style))
    elements.append(Paragraph(
        "Pengujian fungsional telah dilakukan terhadap seluruh fitur modul dengan rincian berikut:",
        body_style
    ))

    test_data = [
        [Paragraph("No", table_header_style), Paragraph("Skenario Pengujian", table_header_style), Paragraph("Masukan Data Uji", table_header_style), Paragraph("Hasil yang Diharapkan", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("1", table_cell_center), Paragraph("Akses Halaman Utama", table_cell_style), Paragraph("GET /", table_cell_style), Paragraph("Dashboard metrik dan tabel daftar tugas tampil lengkap.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("2", table_cell_center), Paragraph("Pencatatan Tugas Baru", table_cell_style), Paragraph("Formulir valid terisi", table_cell_style), Paragraph("Data tersimpan ke MySQL dan redirect ke dashboard.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("3", table_cell_center), Paragraph("Validasi Form Kosong", table_cell_style), Paragraph("Judul dikosongkan", table_cell_style), Paragraph("Sistem menolak dan menampilkan pesan error validasi.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("4", table_cell_center), Paragraph("Ubah Status Instan", table_cell_style), Paragraph("Status -> 'Selesai'", table_cell_style), Paragraph("Status terbarui dan kolom completed_at terisi waktu kini.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("5", table_cell_center), Paragraph("Penyaringan Multi-Filter", table_cell_style), Paragraph("Status & Departemen", table_cell_style), Paragraph("Hanya baris tugas yang cocok yang ditampilkan pada tabel.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("6", table_cell_center), Paragraph("Penghapusan Tugas", table_cell_style), Paragraph("Konfirmasi modal ID", table_cell_style), Paragraph("Data terhapus secara permanen dari tabel basis data.", table_cell_style), Paragraph("BERHASIL", table_cell_center)],
        [Paragraph("7", table_cell_center), Paragraph("Ekspor Berkas CSV", table_cell_style), Paragraph("GET /export/csv", table_cell_style), Paragraph("Berkas CSV terunduh dengan format UTF-8 rapi.", table_cell_style), Paragraph("BERHASIL", table_cell_center)]
    ]
    t_test = Table(test_data, colWidths=[0.9 * cm, 3.8 * cm, 3.4 * cm, 6.4 * cm, 2.0 * cm])
    t_test.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(t_test)

    # =========================================================================
    # BAB 6: DAFTAR ENDPOINT SISTEM
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("6.0 DAFTAR ENDPOINT SISTEM (HTTP ROUTING)", h1_style))

    endpoint_data = [
        [Paragraph("Metode", table_header_style), Paragraph("Rute URL", table_header_style), Paragraph("Deskripsi Fungsi dan Perilaku Sistem", table_header_style)],
        [Paragraph("GET", table_cell_center), Paragraph("/", table_cell_style), Paragraph("Menampilkan antarmuka dashboard, rekapitulasi statistik, serta tabel tugas.", table_cell_style)],
        [Paragraph("GET", table_cell_center), Paragraph("/tasks/new", table_cell_style), Paragraph("Menampilkan formulir pencatatan tugas harian baru.", table_cell_style)],
        [Paragraph("POST", table_cell_center), Paragraph("/tasks/new", table_cell_style), Paragraph("Memvalidasi dan menyimpan data tugas baru ke basis data MySQL.", table_cell_style)],
        [Paragraph("GET", table_cell_center), Paragraph("/tasks/&lt;id&gt;", table_cell_style), Paragraph("Menampilkan rincian lengkap tugas beserta riwayat waktu pengerjaan.", table_cell_style)],
        [Paragraph("GET", table_cell_center), Paragraph("/tasks/&lt;id&gt;/edit", table_cell_style), Paragraph("Menampilkan formulir pengubahan data tugas yang telah tersimpan.", table_cell_style)],
        [Paragraph("POST", table_cell_center), Paragraph("/tasks/&lt;id&gt;/edit", table_cell_style), Paragraph("Menyimpan pembaruan data tugas ke dalam basis data MySQL.", table_cell_style)],
        [Paragraph("POST", table_cell_center), Paragraph("/tasks/&lt;id&gt;/quick-status", table_cell_style), Paragraph("Mengubah status pengerjaan secara instan langsung dari tabel dashboard.", table_cell_style)],
        [Paragraph("POST", table_cell_center), Paragraph("/tasks/&lt;id&gt;/delete", table_cell_style), Paragraph("Menghapus data tugas dari basis data setelah melalui konfirmasi modal.", table_cell_style)],
        [Paragraph("GET", table_cell_center), Paragraph("/export/csv", table_cell_style), Paragraph("Mengekspor seluruh data tugas harian ke berkas CSV standar Microsoft Excel.", table_cell_style)]
    ]
    t_endpoint = Table(endpoint_data, colWidths=[1.8 * cm, 4.4 * cm, 10.3 * cm])
    t_endpoint.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(t_endpoint)

    # =========================================================================
    # BAB 7: PENUTUP
    # =========================================================================
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("7.0 KESIMPULAN", h1_style))
    elements.append(Paragraph(
        "Modul Web Pencatatan Tugas Harian Perusahaan telah berhasil direalisasikan sesuai seluruh ketentuan "
        "teknis yang dipersyaratkan. Penggunaan bahasa pemrograman Python dengan kerangka kerja Flask menghasilkan "
        "aplikasi yang ringan, mudah dikembangkan, dan terstruktur. Dukungan basis data MySQL menjamin integritas "
        "dan persistensi data tugas harian operasional perusahaan secara andal.",
        body_style
    ))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "Demikian dokumen teknis ini disusun sebagai panduan implementasi dan laporan hasil pengujian sistem.",
        body_style
    ))

    # Bangun dokumen PDF tanpa footer canvas
    doc.build(elements)
    print(f"[+] Dokumen PDF berhasil dibuat: {filename}")


if __name__ == '__main__':
    build_pdf()
