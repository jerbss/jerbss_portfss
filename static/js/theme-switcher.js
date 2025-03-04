/* filepath: /c:/PROJETO/jerbss_portfss/static/js/theme-switcher.js */
// ...existing code...

function updateTinyMCETheme(isDarkMode) {
    if (typeof tinymce !== 'undefined') {
        tinymce.editors.forEach(editor => {
            editor.setContent(editor.getContent()); // Refresh content
            editor.ui.registry.getAll().icons = {}; // Clear icon cache
            
            // Update editor theme
            editor.settings.skin = isDarkMode ? 'oxide-dark' : 'oxide';
            editor.settings.content_css = isDarkMode ? 'dark' : 'default';
            editor.settings.content_style = isDarkMode 
                ? 'body { background-color: #1a1a1a; color: #e1e1e1; }'
                : 'body { background-color: #ffffff; color: #000000; }';
            
            // Reload the editor
            editor.reload();
        });
    }
}

// Add to your existing theme toggle function
function toggleTheme() {
    // ...existing theme toggle code...
    
    const isDarkMode = document.body.classList.contains('dark-mode');
    updateTinyMCETheme(isDarkMode);
}
