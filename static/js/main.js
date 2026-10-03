// Genel yardımcı fonksiyonlar

console.log('Randevu Sistemi yüklendi ✓');

// Aktif menü vurgusu
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && path.startsWith(href)) item.classList.add('active');
    });
});