document.addEventListener('DOMContentLoaded', function() {
    // Adicionar botão customizado para gerar sumário quando o TinyMCE estiver carregado
    if (typeof tinymce !== 'undefined') {
        tinymce.PluginManager.add('toc', function(editor, url) {
            editor.ui.registry.addButton('toc', {
                text: 'Gerar Sumário',
                tooltip: 'Gerar Sumário',
                onAction: function () {
                    generateTableOfContents(editor);
                }
            });
            
            // Adicionar botão para inserir âncora manual
            editor.ui.registry.addButton('anchormanual', {
                icon: 'bookmark',
                tooltip: 'Inserir Âncora Manual',
                onAction: function() {
                    createManualAnchor(editor);
                }
            });
            
            // Adicionar botão para diagnóstico de âncoras
            editor.ui.registry.addButton('tocdiag', {
                icon: 'search',
                tooltip: 'Diagnosticar Links do Sumário',
                onAction: function() {
                    checkTocLinks(editor);
                }
            });
        });
    }
    
    // Função para criar manualmente uma âncora
    function createManualAnchor(editor) {
        editor.windowManager.open({
            title: 'Inserir Âncora',
            body: {
                type: 'panel',
                items: [
                    {
                        type: 'input',
                        name: 'id',
                        label: 'ID da Âncora',
                        placeholder: 'Digite um ID sem espaços (ex: introducao)'
                    }
                ]
            },
            buttons: [
                {
                    type: 'cancel',
                    text: 'Cancelar'
                },
                {
                    type: 'submit',
                    text: 'Inserir',
                    primary: true
                }
            ],
            onSubmit: function(api) {
                const data = api.getData();
                const id = data.id.trim().toLowerCase().replace(/\s+/g, '-');
                
                if (!id) {
                    editor.notificationManager.open({
                        text: 'Por favor, insira um ID válido para a âncora.',
                        type: 'error'
                    });
                    return;
                }
                
                // Inserir âncora na posição atual do cursor
                const selectedNode = editor.selection.getNode();
                
                // Se for um cabeçalho, adiciona um ID a ele
                if (/^H[1-6]$/.test(selectedNode.nodeName)) {
                    editor.dom.setAttrib(selectedNode, 'id', id);
                    editor.notificationManager.open({
                        text: 'Âncora adicionada ao cabeçalho! Use #' + id + ' para criar um link para esta seção.',
                        type: 'success'
                    });
                } else {
                    // Caso contrário, insere uma etiqueta de span com ID
                    editor.execCommand('mceInsertContent', false, `<span id="${id}"></span>`);
                    editor.notificationManager.open({
                        text: 'Âncora inserida! Use #' + id + ' para criar um link para este local.',
                        type: 'success'
                    });
                }
                
                api.close();
            }
        });
    }
    
    function generateTableOfContents(editor) {
        // Obter o conteúdo atual do editor
        let content = editor.getContent();
        
        // Primeiro vamos limpar IDs duplicados que possam existir
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = content;
        
        // Selecionar todos os cabeçalhos h1, h2, h3, h4
        const headings = tempDiv.querySelectorAll('h1, h2, h3, h4');
        
        if (headings.length === 0) {
            editor.notificationManager.open({
                text: 'Nenhum cabeçalho encontrado. Adicione cabeçalhos (H1-H4) para gerar um sumário.',
                type: 'warning'
            });
            return;
        }
        
        // Criar sumário
        let tocHtml = '<div class="toc-wrapper" style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;">';
        tocHtml += '<h3 style="margin-top: 0;">Índice</h3>';
        tocHtml += '<div style="margin-bottom: 10px;"><small><i class="fas fa-info-circle"></i> Se algum link não funcionar, use o botão "Inserir Âncora Manual" para definir manualmente os IDs.</small></div>';
        tocHtml += '<ul class="toc" style="list-style-type: none; padding-left: 10px;">';
        
        // Array para armazenar os IDs usados para verificar duplicações
        const usedIds = new Set();
        const tocItems = [];
        
        // NOVO: Atribuir IDs diretamente aos elementos no DOM temporário
        headings.forEach((heading, index) => {
            // Obter o texto puro do cabeçalho
            const headingText = heading.textContent.trim();
            
            // Preservar formatações especiais antes de aplicar o ID
            const originalHTML = heading.innerHTML;
            
            // Criar ID baseado no texto do cabeçalho
            let slugId = headingText
                .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // remove acentos
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '') // remove caracteres especiais
                .replace(/\s+/g, '-') // substitui espaços por hífens
                .substring(0, 50); // limita o tamanho
            
            // Garantir unicidade do ID
            let uniqueId = slugId || `toc-heading-${index}`;
            let counter = 1;
            while (usedIds.has(uniqueId)) {
                uniqueId = `${slugId}-${counter}`;
                counter++;
            }
            
            // Armazenar o ID usado
            usedIds.add(uniqueId);
            
            // Aplicar o ID diretamente ao elemento no DOM temporário
            heading.id = uniqueId;
            
            // Armazenar informações para o sumário
            tocItems.push({
                id: uniqueId,
                text: headingText,
                level: parseInt(heading.tagName.substring(1)) // H1 = 1, H2 = 2, etc.
            });
        });
        
        // Adicionar os itens do sumário
        tocItems.forEach(item => {
            const indent = (item.level - 1) * 20; // Indentação baseada no nível do cabeçalho
            tocHtml += `<li style="margin-left: ${indent}px; margin-bottom: 5px;"><a href="#${item.id}" style="text-decoration: none;">${item.text}</a></li>`;
        });
        
        tocHtml += '</ul></div><hr>';
        
        // MELHORADO: Obter o HTML com os IDs já atribuídos
        const updatedContent = tempDiv.innerHTML;
        
        // Primeiro inserir o sumário no início
        editor.setContent(tocHtml + updatedContent);
        
        // Adicionar comportamento de scroll suave para os links de âncora
        const smoothScrollCss = `
        <style>
            html {
                scroll-behavior: smooth;
            }
            
            .toc a {
                color: #007bff;
                transition: color 0.2s;
            }
            
            .toc a:hover {
                color: #0056b3;
                text-decoration: underline !important;
            }
        </style>`;
        
        // Adicionar o estilo ao conteúdo
        const finalContent = editor.getContent();
        if (!finalContent.includes('scroll-behavior: smooth')) {
            editor.setContent(smoothScrollCss + finalContent);
        }
        
        editor.notificationManager.open({
            text: 'Sumário gerado com sucesso! Clique nos itens do sumário para navegar até as seções correspondentes.',
            type: 'success'
        });
        
        // Adicionar dica sobre links que não funcionam
        setTimeout(() => {
            editor.notificationManager.open({
                text: 'Se algum link não funcionar, selecione o cabeçalho e use o botão "Inserir Âncora Manual" para definir um ID manualmente.',
                type: 'info'
            });
        }, 5000);
    }
    
    // NOVO: Função auxiliar para verificar links quebrados no sumário
    function checkTocLinks(editor) {
        const content = editor.getContent();
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = content;
        
        const tocLinks = tempDiv.querySelectorAll('.toc a[href^="#"]');
        const brokenLinks = [];
        
        tocLinks.forEach(link => {
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = tempDiv.querySelector(`#${targetId}`);
            
            if (!targetElement) {
                brokenLinks.push({
                    id: targetId,
                    text: link.textContent
                });
            }
        });
        
        if (brokenLinks.length > 0) {
            let message = 'Os seguintes links do sumário não têm um destino correspondente:<br>';
            brokenLinks.forEach(link => {
                message += `- "${link.text}" (#${link.id})<br>`;
            });
            message += '<br>Use o botão "Inserir Âncora Manual" para adicionar IDs aos cabeçalhos correspondentes.';
            
            editor.notificationManager.open({
                text: message,
                type: 'warning',
                timeout: 10000
            });
        }
    }
});
