document.addEventListener("DOMContentLoaded", function () {
  const details = document.querySelector("details");

  if (!details) {
      console.error("Elemento <details> no encontrado.");
  } else {
      const content = details.querySelector(".historico");

      if (!content) {
          console.error("Elemento '.historico' no encontrado dentro de <details>.");
      } else {
          details.addEventListener("toggle", () => {
              if (details.open) {
                  content.style.height = content.scrollHeight + "px";
              } else {
                  content.style.height = "0";
              }
          });

          content.addEventListener("transitionend", () => {
              if (details.open) {
                  content.style.height = "auto";
              }
          });
      }
  }
});




// document.addEventListener("DOMContentLoaded", function () {
//     const details = document.querySelector("details");
//     if (details) { // Verifica si el elemento existe
//       const content = details.querySelector(".historico");
  
//       details.addEventListener("toggle", () => {
//         if (details.open) {
//           content.style.height = content.scrollHeight + "px";
//         } else {
//           content.style.height = "0";
//         }
//       });
  
//       content.addEventListener("transitionend", () => {
//         if (details.open) {
//           content.style.height = "auto";
//         }
//       });
//     } else {
//       console.error("Elemento <details> no encontrado.");
//     }
//   });