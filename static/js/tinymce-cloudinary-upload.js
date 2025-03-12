(function() {
    // Configuração do plugin de upload para TinyMCE
    function configureCloudinaryUpload(editor) {
        // Substitua a função padrão de upload de mídia
        editor.ui.registry.addButton('customvideoupload', {
            icon: 'video',
            tooltip: 'Upload de Vídeo para Cloudinary',
            onAction: function() {
                // Cria um input de arquivo oculto
                const input = document.createElement('input');
                input.setAttribute('type', 'file');
                input.setAttribute('accept', 'video/*');
                
                // Quando um arquivo é selecionado
                input.onchange = function() {
                    if (input.files && input.files[0]) {
                        const file = input.files[0];
                        
                        // Verificar tamanho do arquivo (máximo 100MB)
                        const maxSize = 100 * 1024 * 1024; // 100MB em bytes
                        if (file.size > maxSize) {
                            editor.notificationManager.open({
                                text: 'O arquivo é muito grande. O tamanho máximo é de 100MB.',
                                type: 'error',
                                timeout: 5000
                            });
                            return;
                        }
                        
                        // Mostrar indicador de progresso
                        const notification = editor.notificationManager.open({
                            text: `Enviando vídeo "${file.name}" para o Cloudinary...`,
                            type: 'info',
                            progressBar: true
                        });
                        
                        // Atualizar o progresso periodicamente para dar feedback visual
                        let progress = 0;
                        const progressInterval = setInterval(function() {
                            progress += 5;
                            if (progress > 90) {
                                clearInterval(progressInterval);
                                return;
                            }
                            notification.progressBar.value(progress);
                        }, 1000);
                        
                        uploadToCloudinary(file, editor, notification, progressInterval);
                    }
                };
                
                input.click();
            }
        });
    }
    
    // Função para fazer upload para o Cloudinary
    function uploadToCloudinary(file, editor, notification, progressInterval) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Enviar para o endpoint de upload do Django que redirecionará para o Cloudinary
        fetch('/api/cloudinary/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Limpar o intervalo de progresso
            clearInterval(progressInterval);
            
            if (data.secure_url) {
                // Garantir que temos 100% no indicador de progresso
                notification.progressBar.value(100);
                
                // Fechar notificação após um curto atraso
                setTimeout(() => {
                    notification.close();
                    
                    // Criar um elemento de vídeo responsivo com proporção adequada
                    const videoHtml = `
                    <div class="video-responsive">
                        <video controls controlsList="nodownload" width="100%" height="auto" preload="metadata">
                            <source src="${data.secure_url}" type="${file.type}">
                            Seu navegador não suporta a tag de vídeo.
                        </video>
                    </div>`;
                    
                    // Inserir o HTML no editor
                    editor.insertContent(videoHtml);
                    
                    // Mostrar notificação de sucesso
                    editor.notificationManager.open({
                        text: 'Vídeo enviado com sucesso!',
                        type: 'success',
                        timeout: 3000
                    });
                }, 500);
            } else {
                handleUploadError(editor, notification, 'Upload falhou. Tente novamente.');
            }
        })
        .catch(error => {
            // Limpar o intervalo de progresso em caso de erro
            clearInterval(progressInterval);
            
            let errorMsg = 'Erro ao enviar vídeo';
            if (error.message) {
                errorMsg += `: ${error.message}`;
            }
            
            // Se a resposta contém um erro mais detalhado
            if (error.response && error.response.json) {
                error.response.json().then(data => {
                    if (data.error) {
                        errorMsg = data.error;
                    }
                    handleUploadError(editor, notification, errorMsg);
                });
            } else {
                handleUploadError(editor, notification, errorMsg);
            }
        });
    }
    
    // Função auxiliar para obter o token CSRF
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Função para tratar erros de upload
    function handleUploadError(editor, notification, message) {
        // Fechar notificação de progresso se ainda estiver aberta
        if (notification) {
            notification.close();
        }
        
        // Mostrar erro
        editor.notificationManager.open({
            text: message,
            type: 'error',
            timeout: 5000
        });
    }
    
    // Registra o plugin no TinyMCE
    tinymce.PluginManager.add('cloudinaryupload', function(editor) {
        configureCloudinaryUpload(editor);
        
        return {
            getMetadata: function() {
                return {
                    name: 'Cloudinary Upload Plugin',
                    url: 'https://github.com/yourusername/tinymce-cloudinary'
                };
            }
        };
    });
})();
