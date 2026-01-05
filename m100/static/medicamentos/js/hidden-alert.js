document.addEventListener("DOMContentLoaded", function () {
    const contentAlert = document.getElementById("content-alert");
    const closeButton = document.getElementById("close-alert");
    const closeImg = document.getElementById("hidden-alert");
    const openAlert = document.getElementById("open-alert");
    const imgOpenAlert = document.getElementById("img-open-alert");
    const openButton = openAlert ? openAlert.querySelector(".btn-med") : null;
    const openAlert2 = document.getElementById("open-alert2");
    const imgOpenAlert2 = document.getElementById("img-open-alert2");
    const openButton2 = openAlert2 ? openAlert2.querySelector(".btn-med2") : null;
    
    const messageContainer = document.getElementById("banner-animals");

    console.log("messageContainer:", messageContainer);

    if (!contentAlert) {
        console.warn("No se encuentra el elemento 'content-alert' en la vista.");
        return;
    }

    function safeAddListener(element, event, handler) {
        if (element) {
            element.addEventListener(event, handler);
        } else {
            console.warn(`No se encontró el elemento para añadir '${event}'`);
        }
    }

    safeAddListener(closeButton, "click", hideAlert);
    safeAddListener(closeImg, "click", hideAlert);
    safeAddListener(openButton, "click", showAlert);
    safeAddListener(imgOpenAlert, "click", showAlert);
    safeAddListener(openButton2, "click", showAlert);
    safeAddListener(imgOpenAlert2, "click", showAlert);

    function hideAlert() {
        contentAlert.classList.add("hide");
        contentAlert.classList.remove("show");
        openAlert?.classList.remove("hidden");
        openAlert2?.classList.remove("hidden");
        messageContainer?.classList.add("show");
        messageContainer?.classList.remove("hide");

        // MOSTRAR messageContainer
        if (messageContainer) {
            messageContainer.classList.remove("hide");
            messageContainer.classList.add("show");
            console.log("✅ Banner mostrado - clases:", messageContainer.className);
        }
    }

    function showAlert() {
        contentAlert.classList.remove("hide");
        contentAlert.classList.add("show");
        openAlert?.classList.add("hidden");
        openAlert2?.classList.add("hidden");
        messageContainer.classList.remove("show");
        messageContainer.classList.add("hide");

        // OCULTAR messageContainer
        if (messageContainer) {
            messageContainer.classList.remove("show");
            messageContainer.classList.add("hide");
            console.log("❌ Banner ocultado - clases:", messageContainer.className);
        }
    }

    // 🎨 NUEVA FUNCIONALIDAD: SLIDESHOW DE FONDOS
    let backgroundSlideshow = null;
    
    // Generar array de imágenes del 1 al 100 con rutas Django correctas
    const animalImages = [];
    for (let i = 1; i <= 306; i++) {
        // Usar la ruta estática de Django correcta
        animalImages.push(`/static/resources/Animals/${i}.png`);
    }
    
    let currentImageIndex = 0;
    
    console.log(`🦎 ${animalImages.length} imágenes de animales cargadas (1-100):`);
    console.log('Primera imagen:', animalImages[0]); // Debug para verificar ruta

    function changeBackground() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            // 🎨 EFECTO DE TRANSICIÓN SUAVE
            // Primero hacer fade out
            messageContainer.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
            messageContainer.style.opacity = '0.3';
            messageContainer.style.transform = 'scale(0.65)';
            
            // Después de 250ms cambiar la imagen y hacer fade in
            setTimeout(() => {
                // Cambiar la imagen de fondo
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
                messageContainer.style.backgroundSize = '160px 110px';
                messageContainer.style.backgroundRepeat = 'no-repeat';
                messageContainer.style.backgroundPosition = 'right';
                
                // Fade in con efecto
                messageContainer.style.opacity = '1';
                messageContainer.style.transform = 'scale(1)';
                
                console.log(`🎨 Fondo cambiado con efecto a: ${currentImage}`);
            }, 250);
            
            // Avanzar al siguiente índice
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    function startBackgroundSlideshow() {
        // Configurar estilos iniciales para transiciones suaves
        if (messageContainer) {
            messageContainer.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
        }
        
        // Cambiar fondo inmediatamente
        // changeBackground();
        // changeBackgroundGlitch()
        changeBackgroundBlur()
        // changeBackgroundBounce()
        // changeBackgroundSlide()
        
        // Iniciar el intervalo de 10 segundos
        // backgroundSlideshow = setInterval(changeBackground, 10000);
        // backgroundSlideshow = setInterval(changeBackgroundGlitch, 10000);
        backgroundSlideshow = setInterval(changeBackgroundBlur, 10000);
        // backgroundSlideshow = setInterval(changeBackgroundBounce, 10000);
        // backgroundSlideshow = setInterval(changeBackgroundSlide, 10000);
        console.log("🎬 Slideshow de fondos iniciado (cada 10 segundos) con efectos suaves");
    }

    function stopBackgroundSlideshow() {
        if (backgroundSlideshow) {
            clearInterval(backgroundSlideshow);
            backgroundSlideshow = null;
            console.log("⏹️ Slideshow de fondos detenido");
        }
    }

    // 🔧 FUNCIONES MEJORADAS CON CONTROL DE SLIDESHOW
    function hideAlertWithSlideshow() {
        hideAlert();
        
        // Iniciar slideshow cuando se muestra el banner
        if (messageContainer?.classList.contains('show')) {
            startBackgroundSlideshow();
        }
    }

    function showAlertWithSlideshow() {
        showAlert();
        
        // Detener slideshow cuando se oculta el banner
        stopBackgroundSlideshow();
    }

    // 🎭 OPCIÓN 1: Efecto Slide (deslizar)
    function changeBackgroundSlide() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            messageContainer.style.transition = 'transform 0.6s ease-in-out';
            messageContainer.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
                messageContainer.style.transform = 'translateX(-100%)';
                
                setTimeout(() => {
                    messageContainer.style.transform = 'translateX(0)';
                }, 50);
            }, 300);
            
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    // 🌟 OPCIÓN 2: Efecto Zoom + Rotate
    function changeBackgroundZoomRotate() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            messageContainer.style.transition = 'transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 0.5s ease';
            messageContainer.style.opacity = '0';
            messageContainer.style.transform = 'scale(0.8) rotate(5deg)';
            
            setTimeout(() => {
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
                messageContainer.style.opacity = '1';
                messageContainer.style.transform = 'scale(1) rotate(0deg)';
            }, 400);
            
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    // 🎪 OPCIÓN 3: Efecto Bounce
    function changeBackgroundBounce() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            messageContainer.style.transition = 'transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55), opacity 0.3s ease';
            messageContainer.style.opacity = '0.2';
            messageContainer.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
                messageContainer.style.opacity = '1';
                messageContainer.style.transform = 'scale(1)';
            }, 300);
            
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    // 🌀 OPCIÓN 4: Efecto Blur + Scale
    function changeBackgroundBlur() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            messageContainer.style.transition = 'filter 0.5s ease, transform 0.5s ease, opacity 0.5s ease';
            messageContainer.style.filter = 'blur(10px)';
            messageContainer.style.transform = 'scale(0.9)';
            messageContainer.style.opacity = '0.5';
            
            setTimeout(() => {
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
                messageContainer.style.filter = 'blur(0px)';
                messageContainer.style.transform = 'scale(1)';
                messageContainer.style.opacity = '1';
            }, 250);
            
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    // 🎨 OPCIÓN 5: Efecto Glitch/Matrix
    function changeBackgroundGlitch() {
        if (messageContainer && animalImages.length > 0) {
            const currentImage = animalImages[currentImageIndex];
            
            // Primer glitch
            messageContainer.style.transition = 'none';
            messageContainer.style.transform = 'translateX(5px)';
            
            setTimeout(() => {
                messageContainer.style.transform = 'translateX(-3px) scaleX(0.98)';
            }, 100);
            
            setTimeout(() => {
                messageContainer.style.transform = 'translateX(2px)';
                messageContainer.style.backgroundImage = `url('${currentImage}')`;
            }, 200);
            
            setTimeout(() => {
                messageContainer.style.transition = 'transform 0.3s ease';
                messageContainer.style.transform = 'translateX(0) scaleX(1)';
            }, 300);
            
            currentImageIndex = (currentImageIndex + 1) % animalImages.length;
        }
    }

    // 🎯 REEMPLAZAR LOS EVENT LISTENERS CON LAS NUEVAS FUNCIONES
    safeAddListener(closeButton, "click", hideAlertWithSlideshow);
    safeAddListener(closeImg, "click", hideAlertWithSlideshow);
    safeAddListener(openButton, "click", showAlertWithSlideshow);
    safeAddListener(imgOpenAlert, "click", showAlertWithSlideshow);
    safeAddListener(openButton2, "click", showAlertWithSlideshow);
    safeAddListener(imgOpenAlert2, "click", showAlertWithSlideshow);

    // 🚀 OPCIONAL: Iniciar slideshow al cargar la página si el banner está visible
    if (messageContainer?.classList.contains('show')) {
        startBackgroundSlideshow();
    }

    // 🎮 FUNCIONES GLOBALES PARA CONTROL MANUAL (opcional)
    window.startAnimalSlideshow = startBackgroundSlideshow;
    window.stopAnimalSlideshow = stopBackgroundSlideshow;
    // window.nextAnimalBackground = changeBackground;
    // window.nextAnimalBackground = changeBackgroundGlitch;
    window.nextAnimalBackground = changeBackgroundBlur;
    // window.nextAnimalBackground = changeBackgroundBounce;
    // window.nextAnimalBackground = changeBackgroundSlide;
});

// document.addEventListener("DOMContentLoaded", function () {
//     const contentAlert = document.getElementById("content-alert");
//     const closeButton = document.getElementById("close-alert");
//     const closeImg = document.getElementById("hidden-alert");
//     const openAlert = document.getElementById("open-alert");
//     const imgOpenAlert = document.getElementById("img-open-alert");
//     const openButton = openAlert.querySelector(".btn-med");

//     const content = document.getElementById("content-alert");
//     if (!content || content===null) {
//         console.error("No se encuentra el elemento 'content-alert' en la vista.");
//     }
//     else {
//         closeButton.addEventListener("click", hideAlert);
//         closeImg.addEventListener("click", hideAlert);
//         openButton.addEventListener("click", showAlert);
//         imgOpenAlert.addEventListener("click", showAlert);

//         function hideAlert() {
//             contentAlert.classList.add("hide");
//             contentAlert.classList.remove("show");
//             openAlert.classList.remove("hidden");
//         }
    
//         function showAlert() {
//             contentAlert.classList.remove("hide");
//             contentAlert.classList.add("show");
//             openAlert.classList.add("hidden");
//         }
//     }

// });
