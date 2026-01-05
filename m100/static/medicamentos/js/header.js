document.addEventListener("DOMContentLoaded", function () {
  // Ocultar el header al hacer scroll
    const header = document.querySelector(".main-header");
    let lastScrollTop = 0;
  
    window.addEventListener("scroll", function () {
      let scrollTop = window.scrollY || document.documentElement.scrollTop;
  
      if (scrollTop > lastScrollTop) {
        // Scroll hacia abajo -> Oculta el header
        header.classList.add("-translate-y-full");
      } else {
        // Scroll hacia arriba -> Muestra el header
        header.classList.remove("-translate-y-full");
      }
  
      lastScrollTop = scrollTop;
    });
  
    // Mostrar el header al hacer hover en la parte superior
    document.body.addEventListener("mousemove", function (event) {
      if (event.clientY < 50) {
        header.classList.remove("-translate-y-full");
      }
    });
  });
  