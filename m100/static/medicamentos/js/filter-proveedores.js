document.addEventListener("DOMContentLoaded", function () {
    let header = document.querySelector(".main-header");
    header.style.display = "none";

    let menuInput = document.getElementById("nombre_proveedores");
    let menuOkInput = document.getElementById("numero_proveedores");
    let menuInput2 = document.getElementById("nombre");
    let menuOkInput2 = document.getElementById("serv_nombre");

    function checkAndShowHeader() {
        let menu = menuInput.value.trim().toLowerCase();
        let menuOk = menuOkInput.value.trim().toLowerCase();
        let menu2 = menuInput2.value.trim().toLowerCase();
        let menuOk2 = menuOkInput2.value.trim().toLowerCase();

        // Mostrar el header solo si ambos son "menu"
        if (menu === "ver" && menuOk === "menu" || menu2 === "ver" && menuOk2 === "menu") {
            header.style.display = "block";
            console.log("Header visible");
        } else {
            header.style.display = "none";
        }
    }
    // Ejecutar cuando los inputs cambien
    menuInput.addEventListener("input", checkAndShowHeader);
    menuOkInput.addEventListener("input", checkAndShowHeader);
    menuInput2.addEventListener("input", checkAndShowHeader);
    menuOkInput2.addEventListener("input", checkAndShowHeader);

    const filters = document.querySelectorAll("#nombre_proveedores, #nit_proveedores, #numero_proveedores"); // Ajusta los IDs de los inputs
    const tableContainer = document.getElementById("proveedores-table-container");

    function filterTable() {
        const searchValues = Array.from(filters).map(input => input.value.trim().toLowerCase());

        const rows = tableContainer.querySelectorAll("tbody tr");

        rows.forEach(row => {
            const rowText = Array.from(row.querySelectorAll("td"))
                .map(td => td.textContent.trim().toLowerCase())
                .join(" ");

            // Verifica si todas las búsquedas coinciden con el contenido de la fila
            const matchesAllFilters = searchValues.every(value => rowText.includes(value));

            row.style.display = matchesAllFilters ? "" : "none";
        });
    }

    filters.forEach(input => {
        input.addEventListener("input", filterTable);
    });
});
