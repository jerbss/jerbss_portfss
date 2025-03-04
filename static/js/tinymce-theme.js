document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Function to update TinyMCE theme
    function updateTinyMCETheme(isDarkMode) {
        if (typeof tinymce !== 'undefined') {
            try {
                // Get all TinyMCE editors
                const editors = tinymce.get();
                
                if (editors && editors.length > 0) {
                    editors.forEach(editor => {
                        // Remove existing editor
                        const editorId = editor.id;
                        const content = editor.getContent();
                        const editorElement = document.getElementById(editorId);
                        
                        tinymce.execCommand('mceRemoveEditor', false, editorId);
                        
                        // Create new config with updated theme
                        const newConfig = {
                            selector: `#${editorId}`,
                            menubar: 'file edit view insert format tools table help',
                            plugins: 'advlist autolink lists link image charmap searchreplace visualblocks code fullscreen insertdatetime media table wordcount help',
                            toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | code',
                            skin: isDarkMode ? 'oxide-dark' : 'oxide',
                            content_css: isDarkMode ? 'dark' : 'default',
                            content_style: isDarkMode 
                                ? 'body { background-color: #1a1a1a; color: #e1e1e1; } a { color: #58a6ff; }'
                                : 'body { background-color: #ffffff; color: #000000; } a { color: #0d6efd; }',
                            relative_urls: false,
                            remove_script_host: false,
                            convert_urls: false
                        };
                        
                        // Initialize the editor again with new settings
                        setTimeout(() => {
                            tinymce.init(newConfig).then(editors => {
                                if (editors[0]) {
                                    editors[0].setContent(content);
                                }
                            });
                        }, 100);
                    });
                }
            } catch(e) {
                console.log("Error updating TinyMCE theme:", e);
            }
        }
    }
    
    // Listen for theme toggle
    themeToggle.addEventListener('click', function() {
        // Check if body has dark-mode class after toggle
        setTimeout(function() {
            const isDarkMode = document.body.classList.contains('dark-mode');
            updateTinyMCETheme(isDarkMode);
        }, 300);
    });
    
    // Set initial theme
    const isDarkMode = document.body.classList.contains('dark-mode');
    if (isDarkMode) {
        setTimeout(function() {
            updateTinyMCETheme(true);
        }, 1000); // Wait a bit longer for initial load
    }
});