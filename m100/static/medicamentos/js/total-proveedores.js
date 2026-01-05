document.addEventListener('DOMContentLoaded', function () {
    const btnOcultarActas = document.querySelector('.button-pts');
    const actasSection = document.getElementById('section-actas');
    
    // Verifica si el botón existe antes de añadir el listener
    if (btnOcultarActas) {
        btnOcultarActas.addEventListener('click', function () {
            const isHidden = actasSection.style.maxHeight;

            actasSection.style.transition = 'max-height 1s ease';
            if (isHidden) {
                actasSection.style.maxHeight = null; // Colapsa la sección
                animateButtonText(btnOcultarActas, 'Ver PTS');
            } else {
                actasSection.style.maxHeight = actasSection.scrollHeight + "px"; // Expande la sección
                animateButtonText(btnOcultarActas, 'Ocultar PTS');
            }
        });
    } else {
        console.error('El botón de ocultar filtros no se encontró en el DOM.');
    }

    function animateButtonText(button, newText) {
        const oldText = button.textContent;
        button.textContent = ''; // Limpia el texto

        // Crear un contenedor para las letras
        const container = document.createElement('div');
        container.style.display = 'inline-block';

        // Animar cada letra
        oldText.split('').forEach((letter, index) => {
            const span = document.createElement('span');
            span.textContent = letter;
            span.style.opacity = '1';
            span.style.transition = `opacity 0.3s ease ${index * 50}ms`; // Incrementa el delay
            container.appendChild(span);
            span.style.opacity = '0'; // Oculta la letra
        });

        button.appendChild(container);

        // Cambiar el texto después de que se oculten las letras
        setTimeout(() => {
            button.textContent = newText; // Cambia el texto del botón
            container.innerHTML = ''; // Limpia el contenedor de letras
            for (let i = 0; i < newText.length; i++) {
                const newSpan = document.createElement('span');
                newSpan.textContent = newText[i];
                newSpan.style.opacity = '0'; // Inicia oculto
                newSpan.style.transition = `opacity 0.3s ease ${i * 50}ms`; // Incrementa el delay
                container.appendChild(newSpan);
                setTimeout(() => {
                    newSpan.style.opacity = '1'; // Desvanece cada letra
                }, 100); // Espera un poco antes de empezar a mostrar las letras
            }
        }, oldText.length * 50 + 300); // Espera a que todas las letras se oculten
    }
});