document.addEventListener('DOMContentLoaded', function() {
    const greetings = [
        "Fala aí!",
        "E aí!",
        "Salve!",
        "Opa!",
        "Beleza?",
        "Oi!"
    ];
    
    const greetingElement = document.getElementById('greeting');
    let currentIndex = 0;
    
    // Adiciona classe inicial
    greetingElement.classList.add('initial');
    
    // Função para verificar o tema atual
    function isDarkMode() {
        return document.body.classList.contains('dark-mode');
    }
    
    // Função para aplicar a classe de gradiente apropriada
    function applyGradientClass() {
        // Remove ambas as classes de gradiente primeiro
        greetingElement.classList.remove('gradient-light', 'gradient-dark');
        // Aplica a classe apropriada baseada no tema
        greetingElement.classList.add(isDarkMode() ? 'gradient-dark' : 'gradient-light');
    }
    
    // Aplica o gradiente inicial
    applyGradientClass();
    
    // Observer para mudanças de tema
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            // Pequeno delay para esperar a mudança de tema acontecer
            setTimeout(applyGradientClass, 100);
        });
    }
    
    // Adicionando as classes hover-darken para todas as imagens que precisam do efeito
    document.querySelectorAll('.d-flex.align-items-center.mb-3 a img').forEach(img => {
        img.classList.add('hover-darken');
    });
    
    // Aguarda 800ms antes de iniciar as animações
    setTimeout(() => {
        // Remove a classe inicial e mostra o primeiro greeting
        greetingElement.classList.remove('initial');
        greetingElement.classList.add('show');
        
        function updateGreeting() {
            greetingElement.classList.remove('show');
            greetingElement.classList.add('fade');
            
            setTimeout(() => {
                currentIndex = (currentIndex + 1) % greetings.length;
                greetingElement.textContent = greetings[currentIndex];
                greetingElement.classList.remove('fade');
                greetingElement.classList.add('show');
                // Reaplica o gradiente depois de mudar o texto
                applyGradientClass();
            }, 300);
        }
        
        // Inicia o ciclo de animações
        setInterval(updateGreeting, 3000);
    }, 800);
    
    // Função para habilitar a ordenação - modificar a parte relevante
    function enableSorting() {
        // Configuração aprimorada do Sortable
        sortable = new Sortable(top3Container, {
            animation: 150,
            delay: 100,
            delayOnTouchOnly: true,
            touchStartThreshold: 5,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            forceFallback: false,
            onStart: function(evt) {
                const item = evt.item;
                item.classList.add('sorting-enabled');
            },
            onEnd: function(evt) {
                const item = evt.item;
                item.classList.remove('sorting-enabled');
                
                // Mostrar botão para salvar apenas se a ordem mudou
                if (evt.oldIndex !== evt.newIndex) {
                    saveOrderBtn.style.display = 'inline-block';
                    reorderBtn.style.display = 'none';
                    
                    // Remover o código que adiciona a classe order-changed
                    // Assim não teremos mais o efeito visual
                }
            }
        });
        
        // Adicionar indicadores visuais que os cards são arrastáveis
        document.querySelectorAll('.top3-item').forEach(item => {
            item.classList.add('sortable-enabled');
        });
        
        // Remover a linha que mostrava as instruções
        // reorderingInfo.style.display = 'block';
    }
});