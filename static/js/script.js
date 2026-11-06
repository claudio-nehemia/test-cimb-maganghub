/**
 * Modul Pencatatan Tugas Harian Perusahaan
 * Script Interaktivitas Frontend
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto dismiss alert setelah 6 detik
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });
});

/**
 * Membuka modal konfirmasi hapus tugas dan mengatur action form
 * @param {number|string} taskId 
 * @param {string} taskTitle 
 */
function confirmDelete(taskId, taskTitle) {
    const deleteModalEl = document.getElementById('deleteModal');
    if (!deleteModalEl) return;

    const modalTitleEl = document.getElementById('deleteTaskTitle');
    const deleteFormEl = document.getElementById('deleteForm');

    if (modalTitleEl) {
        modalTitleEl.textContent = `"${taskTitle}" (ID: #${taskId})`;
    }

    if (deleteFormEl) {
        deleteFormEl.action = `/tasks/${taskId}/delete`;
    }

    const modalInstance = new bootstrap.Modal(deleteModalEl);
    modalInstance.show();
}
