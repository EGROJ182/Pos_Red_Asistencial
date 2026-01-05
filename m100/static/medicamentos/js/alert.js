document.addEventListener('DOMContentLoaded', function () {
    // Variables
    const contentAlert = document.getElementById("content-alert");
    const alertWrapper = document.getElementById("alert-wrapper");
    let isUserScrolling = false;
    let scrollInterval;
    const scrollSpeed = 18; // Velocidad de desplazamiento (ajustable)
    const autoScrollDelay = 2000; // Tiempo de espera después de interacción manual
    let scrollTimeout;

    // Verificación de elementos
    if (!contentAlert || !alertWrapper) {
        console.error("Los elementos 'content-alert' y 'alert-wrapper' no se encuentran en la vista.");
    } else {
        // Función para desplazamiento automático
        const autoScroll = () => {
            clearInterval(scrollInterval); // Limpia cualquier intervalo previo
            scrollInterval = setInterval(() => {
                if (!isUserScrolling) {
                    // Si llega al final, vuelve al inicio
                    if (contentAlert.scrollLeft >= alertWrapper.scrollWidth - contentAlert.offsetWidth) {
                        contentAlert.scrollLeft = 0;
                    } else {
                        contentAlert.scrollLeft += scrollSpeed;
                    }
                }
            }, 20); // Intervalo entre desplazamientos (ajustable)
        };

        // Función para detener y luego retomar el desplazamiento automático
        const stopAutoScroll = () => {
            isUserScrolling = true; // Marcamos que el usuario está interactuando
            clearTimeout(scrollTimeout);
            clearInterval(scrollInterval); // Detiene el desplazamiento temporalmente

            // Retoma el desplazamiento después de `autoScrollDelay`
            scrollTimeout = setTimeout(() => {
                isUserScrolling = false;
                autoScroll();
            }, autoScrollDelay);
        };

        // Detectar interacción del usuario
        contentAlert.addEventListener("scroll", stopAutoScroll);
        contentAlert.addEventListener("mousedown", stopAutoScroll);
        contentAlert.addEventListener("wheel", stopAutoScroll);
        contentAlert.addEventListener("touchstart", stopAutoScroll);

        // Iniciar el desplazamiento automático
        autoScroll();
    }
});


// document.addEventListener('DOMContentLoaded', function() {
//     // Variables
//     const contentAlert = document.getElementById("content-alert");
//     const alertWrapper = document.getElementById("alert-wrapper");
//     let isUserScrolling = false;
//     let scrollInterval;
//     const scrollSpeed = 18; // Velocidad de desplazamiento (ajustable)
//     const autoScrollDelay = 2000; // Tiempo de espera después de interacción manual

//     // Función para desplazamiento automático
//     const autoScroll = () => {
//         clearInterval(scrollInterval); // Limpia cualquier intervalo previo
//         scrollInterval = setInterval(() => {
//             if (!isUserScrolling) {
//                 // Si llega al final, vuelve al inicio
//                 if (contentAlert.scrollLeft >= alertWrapper.scrollWidth - contentAlert.offsetWidth) {
//                     contentAlert.scrollLeft = 0;
//                 } else {
//                     contentAlert.scrollLeft += scrollSpeed;
//                 }
//             }
//         }, 20); // Intervalo entre desplazamientos (ajustable)
//     };

//     // Función para detener y luego retomar el desplazamiento automático
//     const stopAutoScroll = () => {
//         isUserScrolling = true; // Marcamos que el usuario está interactuando
//         clearTimeout(scrollTimeout);
//         clearInterval(scrollInterval); // Detiene el desplazamiento temporalmente

//         // Retoma el desplazamiento después de `autoScrollDelay`
//         scrollTimeout = setTimeout(() => {
//             isUserScrolling = false;
//             autoScroll();
//         }, autoScrollDelay);
//     };

//     // Variable para gestionar el retardo al retomar el desplazamiento
//     let scrollTimeout;

//     if (!contentAlert || !alertWrapper) {
//         console.error("Los elementos 'content-alert' y 'alert-wrapper' no se encuentran en la vista.");
//     }
//     else {
//         // Detectar interacción del usuario
//         contentAlert.addEventListener("scroll", stopAutoScroll);
//         contentAlert.addEventListener("mousedown", stopAutoScroll);
//         contentAlert.addEventListener("wheel", stopAutoScroll);
//         contentAlert.addEventListener("touchstart", stopAutoScroll);
    
//         // Iniciar el desplazamiento automático
//         autoScroll();
//     }
// });