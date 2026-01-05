// Inicializar cuando el DOM esté listo
let medicamentosAPI;
document.addEventListener('DOMContentLoaded', () => {
    medicamentosAPI = new MedicamentosAPI();
});

// medicamentos_api.js
// Gestión de la API de Medicamentos Vigentes

class MedicamentosAPI {
    constructor() {
        this.baseURL = '/api/medicamentos-vigente-api/';
        this.currentPage = 1;
        this.filters = {};
        // this.updatePaginationInfo(data.pagination);
        this.init();
    }

    init() {
        this.loadInitialData();
        this.setupEventListeners();
    }

    async loadInitialData() {
        try {
            // Cargar opciones de filtros
            await this.loadFilterOptions();
            // Cargar datos de medicamentos
            await this.loadMedicamentos();
            // Cargar información complementaria
            await this.loadInfoComplementaria();
        } catch (error) {
            console.error('Error cargando datos iniciales:', error);
            this.showError('Error al cargar los datos iniciales');
        }
    }

    setupEventListeners() {
        // Formulario de búsqueda - CORREGIDO para usar el ID
        const searchForm = document.getElementById('filter-form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                console.log('Form submitted'); // Debug
                this.handleSearch(e.target);
            });
        } else {
            console.error('No se encontró el formulario #filter-form');
        }

        // Botones de paginación
        document.getElementById('btn-page')?.addEventListener('click', (e) => this.loadPage(e));
        document.getElementById('btn-first')?.addEventListener('click', () => this.goToPage(1));
        document.getElementById('btn-previous')?.addEventListener('click', () => this.goToPage(this.currentPage - 1));
        document.getElementById('btn-next')?.addEventListener('click', () => this.goToPage(this.currentPage + 1));
        document.getElementById('btn-last')?.addEventListener('click', () => this.goToPage(this.totalPages));

        // Input de página
        const pageInput = document.getElementById('page');
        if (pageInput) {
            pageInput.addEventListener('input', () => this.updatePageLink());
        }
    }

    async loadFilterOptions() {
        try {
            const response = await fetch(`${this.baseURL}filtros_options/`);
            const data = await response.json();
            
            this.populateSelect('forma_farmaceutica', data.formas_farmaceuticas);
            this.populateSelect('alianza', data.alianzas);
            this.populateSelect('canal', data.canales);
            this.populateSelect('control_especial', data.control_especial);
            this.populateSelect('monopolio', data.monopolios);
            this.populateSelect('acta', data.actas);
            this.populateSelect('nombre_del_proveedor_pactado', data.proveedores);
            this.populateSelect('tipo', data.tipos);
            this.populateSelect('novedad', data.novedades);
        } catch (error) {
            console.error('Error cargando opciones de filtros:', error);
        }
    }

    populateSelect(selectId, options) {
        const select = document.getElementById(selectId);
        if (!select) return;

        // Mantener la opción "Selecciona..."
        const firstOption = select.querySelector('option[value=""]');
        select.innerHTML = '';
        if (firstOption) {
            select.appendChild(firstOption);
        }

        options.forEach(option => {
            if (option) { // Filtrar valores nulos o vacíos
                const optElement = document.createElement('option');
                optElement.value = option;
                optElement.textContent = option;
                select.appendChild(optElement);
            }
        });
    }

    async loadMedicamentos(page = 1) {
        try {
            // Mostrar indicador de carga
            this.showLoading();

            // Construir URL con filtros
            const params = new URLSearchParams({
                page: page,
                page_size: 50,
                ...this.filters
            });

            const response = await fetch(`${this.baseURL}?${params}`);
            const data = await response.json();

            // Actualizar datos
            this.currentPage = data.pagination.current_page;
            this.totalPages = data.pagination.num_pages;
            this.totalCount = data.pagination.count;

            // Renderizar tabla
            this.renderTable(data.results);

            // Actualizar información de paginación
            this.updatePaginationInfo(data.pagination);

            // Actualizar filtros aplicados
            this.updateFiltrosAplicados(data.filtros_aplicados);

            // Ocultar indicador de carga
            this.hideLoading();
        } catch (error) {
            console.error('Error cargando medicamentos:', error);
            this.showError('Error al cargar los medicamentos');
            this.hideLoading();
        }
    }

    renderTable(medicamentos) {
        const tableContainer = document.getElementById('medicamentos-table-container');
        if (!tableContainer) return;

        // Construir HTML de la tabla manteniendo tu estructura exacta
        let tableHTML = `
            <table class="table-auto border-collapse border border-gray-300 text-[14px]">
                <thead class="text-white font-bold text-sm text-center">
                    <tr class="text-center">
                        <th class="sticky top-0 left-0 px-4 py-2 border border-gray-300 bg-[#0b5494c7] z-20">Item</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Tipo</th>
                        <th class="sticky top-0 w-auto min-w-[300px] left-20 px-4 py-2 border border-gray-300 bg-[#0b5494c7] z-20">Descripción del Medicamento</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Marca</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Principio Activo</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Concentración</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Forma Farmacéutica</th>
                        <th class="sticky top-0 w-auto min-w-[150px] left-[380px] px-4 py-2 border border-gray-300 bg-[#0b5494c7] z-20">CUM</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Presentación Comercial</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Registro Sanitario</th>
                        <th class="sticky top-0 w-auto min-w-[200px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Estado del Registro</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">ATC</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Expediente</th>
                        <th class="sticky top-0 w-auto min-w-[100px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Consecutivo</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Codigo CUM Homologo</th>
                        <th class="sticky top-0 w-auto min-w-[100px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Alianza</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Laboratorio Alianza</th>
                        <th class="sticky top-0 w-auto min-w-[100px] left-[529.5px] px-4 py-2 border border-gray-300 bg-[#0b5494c7] z-20">Canal</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Cantidad Minima de Dispensación</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Variable Cantidad Unidad Minima Negociada</th>
                        <th class="sticky top-0 w-auto min-w-[180px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Valor Medicamento Regulado</th>
                        <th class="sticky top-0 w-auto min-w-[180px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Tarifa Pactada por Unidad sin IVA</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Medicamento de Control Especial</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Medicamento Monopolio del Estado</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">NIT del Proveedor</th>
                        <th class="sticky top-0 w-auto min-w-[300px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Razón Social del Proveedor Pactado</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Número del Acta / Inicial</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Fecha Pactada</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Validador Acta Duplicada</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Circular Valor Regulado</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Precio Maximo Final Institucional</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Precio Maximo Final Comercial</th>
                        <th class="sticky top-0 w-auto min-w-[150px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Estado del Invima</th>
                        <th class="sticky top-0 w-auto min-w-[200px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Validador Precio Mismo Canal</th>
                        <th class="sticky top-0 w-auto min-w-[200px] px-4 py-2 border border-gray-300 bg-[#ff7c00] z-10">Precio Regulado Institucional 2022</th>
                        <th class="sticky top-0 w-auto min-w-[200px] px-4 py-2 border border-gray-300 bg-[red] z-10">Novedades</th>
                    </tr>
                </thead>
                <tbody>
        `;

        medicamentos.forEach((med, index) => {
            const itemNumber = (this.currentPage - 1) * 50 + index + 1;
            tableHTML += this.renderRow(med, itemNumber);
        });

        tableHTML += '</tbody></table>';
        tableContainer.innerHTML = tableHTML;
    }

    renderRow(med, itemNumber) {
        return `
            <tr class="bg-white border-b">
                <td class="sticky left-0 z-10 bg-[#cec2c2] px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${itemNumber}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.tipo || ''}</td>
                <td class="sticky left-20 z-10 bg-[#cec2c2] px-4 py-2 border border-gray-300 text-[${med.color}]">${med.descripcion_medicamento || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.marca || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.principio_activo || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.concentracion || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.forma_farmaceutica || ''}</td>
                <td class="sticky left-[380px] z-10 bg-[#cec2c2] px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.cum || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-[${med.color}]">${med.presentacion || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.registro_sanitario || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.estado_registro || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.atc || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.expediente || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.consecutivo || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.codigo_cum_homologo || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.alianza || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.laboratorio_alianza || ''}</td>
                <td class="sticky left-[529.5px] z-10 bg-[#cec2c2] px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.canal || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.cantidad_minima_de_dispensacion || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.variable_cantidad_unidad_minima_negociada || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${this.formatCurrency(med.valor_medicamento_regulado)}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${this.formatCurrency(med.tarifa_pactada_por_unidad_sin_iva)}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.medicamentos_de_control_especial || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.medicamentos_monopolio_del_estado || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.nit_proveedor || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-[${med.color}]">${med.nombre_del_proveedor_pactado || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.numero_acta_inicial || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.fecha_pactada || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.validador_acta_duplicada || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.circular_valor_regulado || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${this.formatCurrency(med.precio_maximo_final_institucional)}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${this.formatCurrency(med.precio_maximo_final_comercial)}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.status_invima || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${med.validador_precio_mismo_canal || ''}</td>
                <td class="px-4 py-2 border border-gray-300 text-center text-[${med.color}]">${this.formatCurrency(med.precio_regulado_institucional_2022)}</td>
                <td class="px-4 py-2 border font-bold border-gray-300 text-center text-[${med.color}]">${med.novedad || ''}</td>
            </tr>
        `;
    }

    formatCurrency(value) {
        if (!value || value === "0") {
            return `$ ${value || '0'}`;
        }
        
        const lowerValue = String(value).toLowerCase();
        if (lowerValue.includes('no esta regulado') || lowerValue.includes('no regulado')) {
            return value;
        }

        // Convertir a número y formatear
        const numValue = parseFloat(String(value).replace(/,/g, ''));
        if (isNaN(numValue)) return value;
        
        return `$ ${numValue.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    handleSearch(form) {
        const formData = new FormData(form);
        this.filters = {};

        // Recoger todos los filtros del formulario
        for (let [key, value] of formData.entries()) {
            if (value && key !== 'page') {
                this.filters[key] = value;
            }
        }

        // Resetear a página 1 y cargar
        this.currentPage = 1;
        this.loadMedicamentos(1);
    }

    updatePaginationInfo(pagination) {
        // Actualizar contador de resultados
        const resultQuery = document.getElementById('result-query');
        console.log("PAGINATION DATA:", pagination);
        resultQuery.innerText = pagination.count;
        if (resultQuery) {
        }

        // Actualizar número de página actual
        const pageNumber = document.getElementById('page-number');
        if (pageNumber) {
            pageNumber.textContent = pagination.current_page;
        }

        // Actualizar input de página
        const pageInput = document.getElementById('page');
        if (pageInput) {
            pageInput.value = pagination.current_page;
            pageInput.max = pagination.num_pages;
            pageInput.setAttribute('data-total-pages', pagination.num_pages);
        }

        // Actualizar labels de página anterior/siguiente
        const previousLabel = document.getElementById('previous');
        const nextLabel = document.getElementById('next');
        
        if (previousLabel && pagination.previous_page) {
            previousLabel.textContent = pagination.previous_page;
        }
        if (nextLabel && pagination.next_page) {
            nextLabel.textContent = pagination.next_page;
        }

        // Actualizar total de páginas
        const totalPagesElements = document.querySelectorAll('.font-semibold');
        totalPagesElements.forEach(el => {
            if (el.textContent && !isNaN(el.textContent.trim())) {
                el.textContent = pagination.num_pages;
            }
        });

        // Habilitar/deshabilitar botones
        this.updatePaginationButtons(pagination);
    }

    updatePaginationButtons(pagination) {
        const btnFirst = document.getElementById('btn-first');
        const btnPrevious = document.getElementById('btn-previous');
        const btnNext = document.getElementById('btn-next');
        const btnLast = document.getElementById('btn-last');

        if (btnFirst) btnFirst.disabled = !pagination.has_previous;
        if (btnPrevious) btnPrevious.disabled = !pagination.has_previous;
        if (btnNext) btnNext.disabled = !pagination.has_next;
        if (btnLast) btnLast.disabled = !pagination.has_next;
    }

    updateFiltrosAplicados(filtros) {
        const filtrosContainer = document.getElementById('query-filters');
        if (filtrosContainer) {
            filtrosContainer.textContent = filtros.length > 0 ? filtros.join(', ') : 'Ningún filtro aplicado';
        }
    }

    goToPage(pageNumber) {
        if (pageNumber < 1 || pageNumber > this.totalPages) return;
        this.loadMedicamentos(pageNumber);
    }

    loadPage(event) {
        event.preventDefault();
        const pageInput = document.getElementById('page');
        const page = parseInt(pageInput.value);
        
        if (page >= 1 && page <= this.totalPages) {
            this.goToPage(page);
        }
    }

    updatePageLink() {
        // Esta función se mantiene para compatibilidad con tu código existente
        // pero ahora no actualiza URL, solo valida el input
        const pageInput = document.getElementById('page');
        if (pageInput) {
            const value = parseInt(pageInput.value);
            const max = parseInt(pageInput.max);
            
            if (value > max) pageInput.value = max;
            if (value < 1) pageInput.value = 1;
        }
    }

    async loadInfoComplementaria() {
        try {
            const response = await fetch(`${this.baseURL}info_complementaria/`);
            const data = await response.json();
            
            // Aquí puedes renderizar la información complementaria
            // según tu estructura actual
            this.renderAlerts(data.alerts);
            // this.renderActas(data.info_actas_m100, data.info_actas_otros);
            // this.renderEstandar(data.estandar, data.tarifario);
            
        } catch (error) {
            console.error('Error cargando información complementaria:', error);
        }
    }

    renderAlerts(alerts) {
        // Renderizar las alertas de vencimientos
        // Mantener tu estructura HTML existente
        console.log('Alerts loaded:', alerts);
        // Implementa aquí la lógica para renderizar las alertas en tu sección de vencimientos
    }

    showLoading() {
        const tableContainer = document.getElementById('medicamentos-table-container');
        if (tableContainer) {
            tableContainer.innerHTML = `
                <div class="flex justify-center items-center h-64">
                    <div class="text-center">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                        <p class="mt-4 text-gray-600">Cargando medicamentos...</p>
                    </div>
                </div>
            `;
        }
    }

    hideLoading() {
        // El loading se oculta automáticamente al renderizar la tabla
    }

    showError(message) {
        const tableContainer = document.getElementById('medicamentos-table-container');
        if (tableContainer) {
            tableContainer.innerHTML = `
                <div class="flex justify-center items-center h-64">
                    <div class="text-center text-red-500">
                        <p class="text-xl font-semibold">⚠ ${message}</p>
                        <button onclick="medicamentosAPI.loadMedicamentos()" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                            Reintentar
                        </button>
                    </div>
                </div>
            `;
        }
    }
}



// Funciones globales para mantener compatibilidad con tu código existente
function loadPage(event) {
    if (medicamentosAPI) {
        medicamentosAPI.loadPage(event);
    }
}

function buttonFirst(event) {
    event.preventDefault();
    if (medicamentosAPI) {
        medicamentosAPI.goToPage(1);
    }
}

function buttonPrevious(event) {
    event.preventDefault();
    if (medicamentosAPI) {
        medicamentosAPI.goToPage(medicamentosAPI.currentPage - 1);
    }
}

function buttonNext(event) {
    event.preventDefault();
    if (medicamentosAPI) {
        medicamentosAPI.goToPage(medicamentosAPI.currentPage + 1);
    }
}

function buttonLast(event) {
    event.preventDefault();
    if (medicamentosAPI) {
        medicamentosAPI.goToPage(medicamentosAPI.totalPages);
    }
}

function updatePageLink() {
    if (medicamentosAPI) {
        medicamentosAPI.updatePageLink();
    }
}