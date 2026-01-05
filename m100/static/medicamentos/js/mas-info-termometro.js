document.addEventListener('DOMContentLoaded', () => {
    // Selecciona todas las imágenes de "más información"
    const infoImages = document.querySelectorAll('.option-img');

    // Agrega un evento de clic a cada imagen
    infoImages.forEach(img => {
        img.addEventListener('click', (event) => {
            // Obtén el ID del expediente desde el atributo data-expediente
            const expedienteId = img.getAttribute('data-expediente');

            // Encuentra el contenedor correspondiente
            const infoContainer = document.getElementById(`info-${expedienteId}`);

            // Alterna la visibilidad del contenedor
            if (infoContainer) {
                const isVisible = !infoContainer.classList.contains('hidden');
                infoContainer.classList.toggle('hidden', isVisible); // Oculta si está visible, o muestra si está oculto
                infoContainer.classList.toggle('scale-y-0', isVisible);
                infoContainer.classList.toggle('scale-y-100', !isVisible);
            }
        });
    });
});