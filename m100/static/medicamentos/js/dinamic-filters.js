let originalData = [];

// Obtener los datos desde el script JSON incrustado en el HTML
try {
    const tableroElement = document.getElementById("tablero_json");
    if (tableroElement) {
        originalData = JSON.parse(tableroElement.textContent);
    }
} catch (error) {
    console.error("Error al parsear los datos del tablero:", error);
}

const appliedFilters = {};

function updateFilters(key, value) {
    if (!appliedFilters[key]) {
        appliedFilters[key] = new Set();
    }
    if (appliedFilters[key].has(value)) {
        appliedFilters[key].delete(value);
        if (appliedFilters[key].size === 0) {
            delete appliedFilters[key];
        }
    } else {
        appliedFilters[key].add(value);
    }
    applyFilters();
}

function applyFilters() {
    const filteredData = originalData.filter(item => {
        return Object.keys(appliedFilters).every(key => {
            return appliedFilters[key].size === 0 || appliedFilters[key].has(item[key]);
        });
    });
    renderTable(filteredData);
    updateCharts(filteredData);
}

function renderTable(data) {
    const tableBody = document.querySelector("#table-body");
    if (!tableBody) return;
    tableBody.innerHTML = "";
    data.forEach(item => {
        const row = document.createElement("tr");
        row.classList.add("table-row");
        row.dataset.filterKey = "nombre"; // Ajusta esto según el campo clave
        row.dataset.filterValue = item.nombre;
        row.innerHTML = `
            <td>${item.nombre}</td>
            <td>${item.tipo_proveedor}</td>
            <td>${item.numero_contrato}</td>
        `;
        tableBody.appendChild(row);
    });
    attachTableRowListeners();
}

function updateCharts(data) {
    console.log("Actualizando gráficos con", data);
    // Aquí va la lógica para actualizar los gráficos.
}

function attachTableRowListeners() {
    document.querySelectorAll(".table-row").forEach(row => {
        row.addEventListener("click", function () {
            const key = this.dataset.filterKey;
            const value = this.dataset.filterValue;
            updateFilters(key, value);
        });
    });
}

// Event listeners para los gráficos
document.querySelectorAll(".chart-element").forEach(element => {
    element.addEventListener("click", function () {
        const key = this.dataset.filterKey;
        const value = this.dataset.filterValue;
        updateFilters(key, value);
    });
});

// Renderizar la tabla al inicio
renderTable(originalData);
