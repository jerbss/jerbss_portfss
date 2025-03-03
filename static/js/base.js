document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-toggle');
    const themeStatus = document.querySelector('.theme-status');
    const body = document.body;
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Function to update accessibility attributes
    function updateThemeAccessibility(isDark) {
        themeToggle.setAttribute('aria-pressed', isDark ? 'true' : 'false');
        themeStatus.textContent = isDark ? 'escuro' : 'claro';
        themeToggle.setAttribute('title', `Mudar para tema ${isDark ? 'claro' : 'escuro'}`);
    }

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        themeToggle.classList.add('theme-toggle--toggled');
        updateThemeAccessibility(true);
    } else {
        updateThemeAccessibility(false);
    }

    // Handle keyboard navigation
    themeToggle.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            this.click();
        }
    });

    themeToggle.addEventListener('click', function() {
        const isDark = !body.classList.contains('dark-mode');
        body.classList.toggle('dark-mode');
        themeToggle.classList.toggle('theme-toggle--toggled');
        
        // Update accessibility attributes
        updateThemeAccessibility(isDark);
        
        // Save theme preference
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    // Back to top button
    const backToTopBtn = document.querySelector('.position-fixed .btn-primary');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
});