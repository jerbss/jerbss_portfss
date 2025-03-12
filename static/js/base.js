document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-toggle');
    const themeStatus = document.querySelector('.theme-status');
    const body = document.body;
    
    // Adicionado código para detectar a direção da rolagem
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    // Função para controlar a visibilidade da navbar baseada na rolagem
    function handleNavbarVisibility() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Se estiver no topo da página, sempre manter a navbar visível
        if (scrollTop <= 100) {
            navbar.classList.remove('navbar-hidden');
            return;
        }
        
        // Detecta a direção da rolagem
        if (scrollTop > lastScrollTop) {
            // Rolagem para baixo - esconder a navbar
            navbar.classList.add('navbar-hidden');
        } else {
            // Rolagem para cima - mostrar a navbar
            navbar.classList.remove('navbar-hidden');
        }
        
        lastScrollTop = scrollTop;
    }
    
    // Adiciona o listener para o evento de rolagem (com debounce para performance)
    let scrollTimer;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(handleNavbarVisibility, 10);
    });
    
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
    
    function toggleBackToTopButton() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    }

    // Listen for scroll events
    window.addEventListener('scroll', toggleBackToTopButton);
    
    // Check initial scroll position
    toggleBackToTopButton();
});