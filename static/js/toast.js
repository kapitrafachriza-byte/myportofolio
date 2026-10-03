/**
 * Utility functions for Toast Notifications, CSRF Cookie Extraction, and XSS Escaping.
 * Digunakan secara global di seluruh halaman portofolio (Tutorial & Tugas 5).
 */

/**
 * Mengambil nilai cookie berdasarkan nama (misalnya 'csrftoken').
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Mengamankan string teks dari serangan Cross-Site Scripting (XSS).
 * Mengubah karakter &, <, >, ", dan ' menjadi HTML entities yang aman.
 */
function escapeHtml(unsafe) {
    return String(unsafe ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

/**
 * Menampilkan pesan toast notification di layar.
 * Menggunakan textContent untuk memastikan pesan bebas dari injeksi HTML/XSS.
 * @param {string} title - Judul notifikasi
 * @param {string} message - Pesan penjelasan
 * @param {'success'|'error'|'info'} type - Tipe toast untuk styling warna
 */
function showToast(title, message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        container.setAttribute('aria-live', 'polite');
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const titleEl = document.createElement('strong');
    titleEl.className = 'toast-title';
    titleEl.textContent = title;

    const messageEl = document.createElement('p');
    messageEl.className = 'toast-message';
    messageEl.textContent = message;

    toast.appendChild(titleEl);
    toast.appendChild(messageEl);
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
