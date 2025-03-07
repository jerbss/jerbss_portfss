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
            }, 300);
        }
        
        // Inicia o ciclo de animações
        setInterval(updateGreeting, 3000);
    }, 800);
});