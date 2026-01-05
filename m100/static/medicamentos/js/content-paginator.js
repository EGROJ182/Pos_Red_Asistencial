const movableDiv = document.getElementById('content-paginator');

let offsetX, offsetY;
let isDragging = false;

movableDiv.addEventListener('mousedown', (e) => {
    isDragging = true;

    // Calcula la posición inicial al hacer clic
    offsetX = e.clientX - movableDiv.getBoundingClientRect().left;
    offsetY = e.clientY - movableDiv.getBoundingClientRect().top;

    movableDiv.style.cursor = 'grabbing'; // Cambia el cursor al arrastrar
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        isDragging = true;
        // Calcula nuevas posiciones
        let newX = e.clientX - offsetX;
        let newY = e.clientY - offsetY;

        // Obtiene dimensiones de la ventana y del div
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const divWidth = movableDiv.offsetWidth;
        const divHeight = movableDiv.offsetHeight;

        // Asegúrate de que el div no salga de los límites de la ventana
        if (newX < 0) newX = 0; // Límite izquierdo
        if (newY < 0) newY = 0; // Límite superior
        if (newX + divWidth > windowWidth) newX = windowWidth - divWidth; // Límite derecho
        if (newY + divHeight > windowHeight) newY = windowHeight - divHeight; // Límite inferior

        // Aplica las nuevas posiciones
        movableDiv.style.left = `${newX}px`;
        movableDiv.style.top = `${newY}px`;
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    movableDiv.style.cursor = 'grab'; // Restablece el cursor
});