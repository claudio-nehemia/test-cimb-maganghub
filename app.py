import csv
from io import StringIO
from datetime import datetime, date
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, Response, abort
)
from config import Config
from db import get_db_connection, init_db

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi basis data saat aplikasi dijalankan
with app.app_context():
    init_db()

DEPARTMENTS = [
    'Teknologi Informasi',
    'Keuangan',
    'Operasional',
    'Human Resources',
    'Pemasaran',
    'Legal & Kepatuhan',
    'Manajemen Risiko',
    'Layanan Nasabah'
]

PRIORITIES = ['Rendah', 'Sedang', 'Tinggi']
STATUSES = ['Belum Dimulai', 'Sedang Dikerjakan', 'Selesai']


@app.context_processor
def inject_common_data():
    """Menyediakan variabel global ke seluruh template Jinja2."""
    return {
        'now': datetime.now(),
        'today': date.today(),
        'departments_list': DEPARTMENTS,
        'priorities_list': PRIORITIES,
        'statuses_list': STATUSES
    }


@app.route('/')
def index():
    """Halaman utama: Dashboard metrik, filter, dan daftar tugas harian."""
    search_query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    priority_filter = request.args.get('priority', '').strip()
    dept_filter = request.args.get('department', '').strip()
    date_filter = request.args.get('date_filter', '').strip()
    sort_by = request.args.get('sort', 'due_date').strip()
    order = request.args.get('order', 'asc').strip().lower()

    # Validasi parameter sorting agar aman dari SQL injection
    valid_sort_columns = {
        'due_date': 'due_date',
        'priority': "FIELD(priority, 'Tinggi', 'Sedang', 'Rendah')",
        'status': "FIELD(status, 'Belum Dimulai', 'Sedang Dikerjakan', 'Selesai')",
        'title': 'title',
        'created_at': 'created_at'
    }
    order_clause = 'DESC' if order == 'desc' else 'ASC'
    sort_sql = valid_sort_columns.get(sort_by, 'due_date')

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Mengambil statistik ringkasan tugas
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'Belum Dimulai' THEN 1 ELSE 0 END) AS pending,
                    SUM(CASE WHEN status = 'Sedang Dikerjakan' THEN 1 ELSE 0 END) AS in_progress,
                    SUM(CASE WHEN status = 'Selesai' THEN 1 ELSE 0 END) AS completed,
                    SUM(CASE WHEN due_date = CURDATE() AND status != 'Selesai' THEN 1 ELSE 0 END) AS due_today,
                    SUM(CASE WHEN due_date < CURDATE() AND status != 'Selesai' THEN 1 ELSE 0 END) AS overdue
                FROM tasks
            """)
            stats = cursor.fetchone()
            
            # Hitung persentase tugas selesai
            total_tasks = stats['total'] or 0
            completed_tasks = stats['completed'] or 0
            stats['completion_rate'] = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0

            # 2. Query filter daftar tugas
            conditions = ["1=1"]
            params = []

            if search_query:
                conditions.append("(title LIKE %s OR description LIKE %s OR assigned_to LIKE %s)")
                param_val = f"%{search_query}%"
                params.extend([param_val, param_val, param_val])

            if status_filter and status_filter in STATUSES:
                conditions.append("status = %s")
                params.append(status_filter)

            if priority_filter and priority_filter in PRIORITIES:
                conditions.append("priority = %s")
                params.append(priority_filter)

            if dept_filter and dept_filter in DEPARTMENTS:
                conditions.append("department = %s")
                params.append(dept_filter)

            if date_filter == 'today':
                conditions.append("due_date = CURDATE()")
            elif date_filter == 'overdue':
                conditions.append("due_date < CURDATE() AND status != 'Selesai'")
            elif date_filter == 'upcoming':
                conditions.append("due_date > CURDATE()")

            where_clause = " AND ".join(conditions)
            query = f"""
                SELECT id, title, description, assigned_to, department, 
                       priority, status, due_date, completed_at, created_at
                FROM tasks
                WHERE {where_clause}
                ORDER BY {sort_sql} {order_clause}, id DESC
            """
            cursor.execute(query, params)
            tasks = cursor.fetchall()

    finally:
        conn.close()

    return render_template(
        'index.html',
        tasks=tasks,
        stats=stats,
        filters={
            'q': search_query,
            'status': status_filter,
            'priority': priority_filter,
            'department': dept_filter,
            'date_filter': date_filter,
            'sort': sort_by,
            'order': order
        }
    )


@app.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    """Menampilkan form tambah tugas atau memproses pembuatan tugas baru."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form.get('assigned_to', '').strip()
        department = request.form.get('department', '').strip()
        priority = request.form.get('priority', 'Sedang').strip()
        status = request.form.get('status', 'Belum Dimulai').strip()
        due_date = request.form.get('due_date', '').strip()

        # Validasi input form
        errors = []
        if not title:
            errors.append('Judul tugas wajib diisi.')
        if not assigned_to:
            errors.append('Nama penanggung jawab wajib diisi.')
        if not department:
            errors.append('Divisi / Departemen wajib dipilih.')
        if not due_date:
            errors.append('Batas waktu (tanggal jatuh tempo) wajib diisi.')
        if priority not in PRIORITIES:
            errors.append('Prioritas tugas tidak valid.')
        if status not in STATUSES:
            errors.append('Status tugas tidak valid.')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template(
                'form.html',
                action='create',
                task=request.form
            )

        completed_at = datetime.now() if status == 'Selesai' else None

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tasks 
                    (title, description, assigned_to, department, priority, status, due_date, completed_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (title, description, assigned_to, department, priority, status, due_date, completed_at))
            flash('Tugas harian baru berhasil dicatat dalam sistem.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kendala saat menyimpan data: {str(e)}', 'danger')
            return render_template('form.html', action='create', task=request.form)
        finally:
            conn.close()

    # Form baru
    default_task = {
        'title': '',
        'description': '',
        'assigned_to': '',
        'department': 'Teknologi Informasi',
        'priority': 'Sedang',
        'status': 'Belum Dimulai',
        'due_date': date.today().isoformat()
    }
    return render_template('form.html', action='create', task=default_task)


@app.route('/tasks/<int:task_id>')
def task_detail(task_id):
    """Menampilkan rincian lengkap suatu tugas."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()
            if not task:
                abort(404)
    finally:
        conn.close()

    return render_template('detail.html', task=task)


@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Menampilkan form edit tugas atau memperbarui data tugas."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()
            if not task:
                abort(404)

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            assigned_to = request.form.get('assigned_to', '').strip()
            department = request.form.get('department', '').strip()
            priority = request.form.get('priority', 'Sedang').strip()
            status = request.form.get('status', 'Belum Dimulai').strip()
            due_date = request.form.get('due_date', '').strip()

            errors = []
            if not title:
                errors.append('Judul tugas wajib diisi.')
            if not assigned_to:
                errors.append('Nama penanggung jawab wajib diisi.')
            if not department:
                errors.append('Divisi / Departemen wajib dipilih.')
            if not due_date:
                errors.append('Batas waktu wajib diisi.')
            if priority not in PRIORITIES:
                errors.append('Prioritas tugas tidak valid.')
            if status not in STATUSES:
                errors.append('Status tugas tidak valid.')

            if errors:
                for err in errors:
                    flash(err, 'danger')
                return render_template('form.html', action='edit', task=request.form, task_id=task_id)

            # Pengaturan waktu selesai secara logis
            if status == 'Selesai' and task['status'] != 'Selesai':
                completed_at = datetime.now()
            elif status != 'Selesai':
                completed_at = None
            else:
                completed_at = task['completed_at']

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE tasks 
                    SET title = %s, description = %s, assigned_to = %s, 
                        department = %s, priority = %s, status = %s, 
                        due_date = %s, completed_at = %s
                    WHERE id = %s
                """, (title, description, assigned_to, department, priority, status, due_date, completed_at, task_id))
            
            flash('Pembaruan data tugas berhasil disimpan.', 'success')
            return redirect(url_for('task_detail', task_id=task_id))

    finally:
        conn.close()

    return render_template('form.html', action='edit', task=task, task_id=task_id)


@app.route('/tasks/<int:task_id>/quick-status', methods=['POST'])
def quick_status(task_id):
    """Aksi cepat mengubah status tugas (misal langsung tandai selesai)."""
    new_status = request.form.get('status', '').strip()
    if new_status not in STATUSES:
        flash('Status tugas tidak valid.', 'danger')
        return redirect(request.referrer or url_for('index'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if new_status == 'Selesai':
                cursor.execute("""
                    UPDATE tasks 
                    SET status = %s, completed_at = NOW() 
                    WHERE id = %s
                """, (new_status, task_id))
            else:
                cursor.execute("""
                    UPDATE tasks 
                    SET status = %s, completed_at = NULL 
                    WHERE id = %s
                """, (new_status, task_id))
        flash(f'Status tugas #{task_id} berhasil diperbarui menjadi "{new_status}".', 'success')
    finally:
        conn.close()

    return redirect(request.referrer or url_for('index'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Menghapus data tugas dari database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        flash(f'Tugas #{task_id} telah berhasil dihapus.', 'info')
    finally:
        conn.close()

    return redirect(url_for('index'))


@app.route('/export/csv')
def export_csv():
    """Mengekspor daftar tugas ke dalam format file CSV."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, assigned_to, department, 
                       priority, status, due_date, completed_at, created_at
                FROM tasks 
                ORDER BY due_date ASC, id ASC
            """)
            tasks = cursor.fetchall()
    finally:
        conn.close()

    si = StringIO()
    writer = csv.writer(si, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    # Header Kolom
    writer.writerow([
        'ID Tugas', 'Judul Tugas', 'Deskripsi', 'Penanggung Jawab', 
        'Divisi', 'Prioritas', 'Status', 'Batas Waktu', 'Waktu Selesai', 'Waktu Dibuat'
    ])
    
    # Isi Data
    for t in tasks:
        writer.writerow([
            t['id'],
            t['title'],
            t['description'] or '',
            t['assigned_to'],
            t['department'],
            t['priority'],
            t['status'],
            t['due_date'].strftime('%Y-%m-%d') if t['due_date'] else '',
            t['completed_at'].strftime('%Y-%m-%d %H:%M:%S') if t['completed_at'] else '-',
            t['created_at'].strftime('%Y-%m-%d %H:%M:%S') if t['created_at'] else ''
        ])

    # Tambahkan UTF-8 BOM agar terbaca sempurna di Microsoft Excel
    output = '\ufeff' + si.getvalue()
    filename = f"daftar_tugas_harian_{date.today().strftime('%Y%m%d')}.csv"

    return Response(
        output,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', not_found=True), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', server_error=True), 500


if __name__ == '__main__':
    print(f"[*] Aplikasi Manajemen Tugas Harian berjalan di http://localhost:{Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
