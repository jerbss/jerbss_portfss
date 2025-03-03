document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        themeToggle.classList.add('theme-toggle--toggled');
    }

    themeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        themeToggle.classList.toggle('theme-toggle--toggled');
        
        // Save theme preference
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});