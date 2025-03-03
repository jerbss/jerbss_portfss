document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    themeToggle.addEventListener('change', function() {
        body.classList.toggle('dark-mode');
        if (body.classList.contains('dark-mode')) {
            themeToggle.nextElementSibling.textContent = '☀️';
        } else {
            themeToggle.nextElementSibling.textContent = '🌙';
        }
    });
});