document.addEventListener('DOMContentLoaded', function () {
    const btnOcultarActas = document.querySelector('.button-vencimientos');
    const actasSection = document.getElementById('section-vencimientos');
    
    // Verifica si el botón existe antes de añadir el listener
    if (btnOcultarActas) {
        btnOcultarActas.addEventListener('click', function () {
            const isHidden = actasSection.style.maxHeight;

            actasSection.style.transition = 'max-height 1s ease';
            if (isHidden) {
                actasSection.style.maxHeight = null; // Colapsa la sección
            } else {
                actasSection.style.maxHeight = actasSection.scrollHeight + "px"; // Expande la sección
            }
        });
    } else {
        console.error('El botón de ocultar filtros no se encontró en el DOM.');
    }
});