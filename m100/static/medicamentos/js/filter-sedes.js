document.addEventListener("DOMContentLoaded", function () {
    const filters = document.querySelectorAll("#codigo_sedes, #nombre_sedes, #numero_sedes, #dpto_sedes, #municipio_sedes"); // Ajusta los IDs de los inputs
    const tableContainer = document.getElementById("sedes-table-container");

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
