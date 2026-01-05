document.addEventListener("DOMContentLoaded", function() {
    viewsButtonsPage();
});

function buttonFirst(event) {
    event.preventDefault(); 

    const contenedor = document.getElementById('medicamentos-table-container');
    contenedor.innerHTML = '<div class="flex justify-center items-center h-64"><div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>';

    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', 1);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePage(1, totalPages);
        // document.getElementById('medicamentos-table-container').innerHTML = data.html;

        // Actualizar la tabla principal
        actualizarTablaPrincipal(data.prestadores);
        
        // Generar los paneles modales para sedes y servicios
        generarPanelesModales(data.data);
        
        // Registrar el evento de cambio de página para análisis
        // console.log(`Página cambiada a: ${data.pagination.current_page}`);
    })
    .catch(error => {
        console.error('Error al cargar la página:', error);
        contenedor.innerHTML = `
            <div class="flex flex-col items-center justify-center h-64">
                <p class="text-red-500 font-semibold mb-2">Error al cargar los datos</p>
                <p class="text-gray-600 mb-4">Intente nuevamente</p>
                <button id="retry-button" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                    Reintentar
                </button>
            </div>
        `;
    });
    
}

function buttonLast(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    
    // Establece el número de página en la URL
    url.searchParams.set('page', totalPages);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        validatePage(totalPages, totalPages);
        // document.getElementById('medicamentos-table-container').innerHTML = data.html;

        // Actualizar la tabla principal
        actualizarTablaPrincipal(data.prestadores);
        
        // Generar los paneles modales para sedes y servicios
        generarPanelesModales(data.data);
        
        // Registrar el evento de cambio de página para análisis
        // console.log(`Página cambiada a: ${data.pagination.current_page}`);
    })
    .catch(error => {
        console.error('Error al cargar la página:', error);
        contenedor.innerHTML = `
            <div class="flex flex-col items-center justify-center h-64">
                <p class="text-red-500 font-semibold mb-2">Error al cargar los datos</p>
                <p class="text-gray-600 mb-4">Intente nuevamente</p>
                <button id="retry-button" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                    Reintentar
                </button>
            </div>
        `;
    });
    
}

function buttonNext(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    let next = document.querySelector('#next').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', next);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        // document.getElementById('medicamentos-table-container').innerHTML = data.html;

        // Actualizar la tabla principal
        actualizarTablaPrincipal(data.prestadores);
        
        // Generar los paneles modales para sedes y servicios
        generarPanelesModales(data.data);

        validatePage(parseInt(next), parseInt(totalPages));
        
        // Registrar el evento de cambio de página para análisis
        // console.log(`Página cambiada a: ${data.pagination.current_page}`);
    })
    .catch(error => {
        console.error('Error al cargar la página:', error);
        contenedor.innerHTML = `
            <div class="flex flex-col items-center justify-center h-64">
                <p class="text-red-500 font-semibold mb-2">Error al cargar los datos</p>
                <p class="text-gray-600 mb-4">Intente nuevamente</p>
                <button id="retry-button" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                    Reintentar
                </button>
            </div>
        `;
    });
    
}

function buttonPrevious(event) {
    event.preventDefault(); 
    // const pageLink = document.getElementById('pageLink');
    let page = document.getElementById('page');
    const url = new URL(window.location.href);
    const totalPages = page.getAttribute('data-total-pages');
    let previous = document.querySelector('#previous').textContent;
    
    // Establece el número de página en la URL
    url.searchParams.set('page', previous);
    
    // Realiza la solicitud AJAX
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(response => response.json())
    .then(data => {
        // console.log(data); // Verificar la respuesta
        // document.getElementById('medicamentos-table-container').innerHTML = data.html;

        // Actualizar la tabla principal
        actualizarTablaPrincipal(data.prestadores);
        
        // Generar los paneles modales para sedes y servicios
        generarPanelesModales(data.data);
        
        validatePage(previous, totalPages);

        // Registrar el evento de cambio de página para análisis
        // console.log(`Página cambiada a: ${data.pagination.current_page}`);
    })
    .catch(error => {
        console.error('Error al cargar la página:', error);
        contenedor.innerHTML = `
            <div class="flex flex-col items-center justify-center h-64">
                <p class="text-red-500 font-semibold mb-2">Error al cargar los datos</p>
                <p class="text-gray-600 mb-4">Intente nuevamente</p>
                <button id="retry-button" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                    Reintentar
                </button>
            </div>
        `;
    });        
}

function validatePage(page, totalPages) {
    if (parseInt(page) >= parseInt(totalPages)) {
        document.getElementById('page-number').innerText = totalPages;
        document.getElementById('next').innerText = totalPages;
        document.getElementById('previous').innerText = totalPages-1;
        // document.getElementById('page').value = totalPages;
        document.getElementById('btn-next').style.display = "none";
        document.getElementById('btn-last').style.display = "none";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
    else if (parseInt(page) <= 1) {
        document.getElementById('page-number').innerText = 1;
        document.getElementById('next').innerText = 2;
        document.getElementById('previous').innerText = 1;
        // document.getElementById('page').value = 1;
        document.getElementById('btn-previous').style.display = "none";
        document.getElementById('btn-first').style.display = "none";
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
    }
    else {
        document.getElementById('previous').innerText = parseInt(page)-1;
        document.getElementById('next').innerText = parseInt(page)+1;
        document.getElementById('page-number').innerText = page;
        // document.getElementById('page').value = parseInt(page);
        document.getElementById('btn-next').style.display = "block";
        document.getElementById('btn-first').style.display = "block";
        document.getElementById('btn-last').style.display = "block";
        document.getElementById('btn-previous').style.display = "block";
    }
}

function viewsButtonsPage() {
    const result = document.getElementById('result-query').textContent;
    if(parseInt(result)<21) {
        document.getElementById('page').disabled = true;
        document.getElementById('btn-next').style.display = 'none';
        document.getElementById('btn-last').style.display = 'none';
        document.getElementById('btn-first').style.display = 'none';
        document.getElementById('btn-previous').style.display = 'none';
        document.getElementById('btn-page').style.display = 'none';
    }
    else{
        document.getElementById('page').disabled = false;
        document.getElementById('btn-first').style.display = 'none';
        document.getElementById('btn-previous').style.display = 'none';
        document.getElementById('btn-next').style.display = 'block';
        document.getElementById('btn-last').style.display = 'block';
        document.getElementById('btn-page').style.display = 'block';
    }
}


// Función para actualizar la tabla principal con los nuevos datos
function actualizarTablaPrincipal(prestadores) {
    const contenedor = document.getElementById('medicamentos-table-container');
    
    // Crear el encabezado
    let html = `
    <div class="sticky top-0 bg-[#f3f4f562] z-20 flex justify-between border-b border-gray-300 text-center font-bold min-w-[1024px]">
        <p class="w-[5%] py-2">#</p>
        <p class="w-[20%] py-2">NIT</p>
        <p class="w-[50%] py-2">Razón Social</p>
        <p class="w-[25%] py-2">Estado</p>
    </div>
    `;
    
    // Si no hay prestadores, mostrar mensaje
    if (!prestadores || prestadores.length === 0) {
        html += `
        <div class="flex items-center border-b border-gray-300 text-center min-w-[1024px]">
            <p class="w-full py-4 text-center text-gray-500 italic">No se encontraron prestadores con los filtros aplicados</p>
        </div>
        `;
    } else {
        // Generar filas para cada prestador
        prestadores.forEach((prestador, index) => {
            html += `
            <div class="flex items-center border-b border-gray-300 text-center min-w-[1024px] hover:bg-[#4aa5ff62] hover:font-semibold transition-colors duration-300 relative">
                <!-- Número de fila -->
                <div class="w-[5%] flex justify-between py-2 border-r border-gray-300 relative group">
                    <p class="w-full py-2">${index + 1}</p>
                    <div class="absolute z-50 hidden group-hover:block bg-gray-100 shadow-lg rounded-lg text-[#333] font-bold px-2 py-2 border border-gray-300 group-hover:scale-y-100 transition-all duration-300 ease-in-out scale-y-0 origin-top"
                        style="top: 0; left: 140%; transform: translateX(-50%);">
                        <!-- Contenedor imagen sedes -->
                        <div class="flex w-[50px] justify-center">
                            <img src="/static/resources/info2.gif" alt="img-info" class="toggle-sedes h-10 cursor-pointer" data-nit="${prestador.nit}">
                        </div>
                    </div>
                </div>
                
                <!-- Datos del prestador en la tabla principal -->
                <p class="w-[20%] py-2 border-r border-gray-300 hover-trigger">${prestador.nit}</p>
                <div class="w-[50%] flex justify-center py-2 border-r border-gray-300 relative group">
                    <p class="w-full py-2 text-[#333]">${prestador.nombre}</p>
                    <!-- Contador de sedes -->
                    <div class="absolute z-50 items-center hidden w-[250px] group-hover:block bg-gray-100 shadow-lg rounded-lg text-[#333] font-bold px-4 py-2 border border-gray-300 group-hover:scale-y-100 transition-all duration-300 ease-in-out scale-y-0 origin-top"
                        style="top: -30px; left: 50%; transform: translateX(-50%);">
                        Cantidad de Sedes: ${prestador.cantidad_sedes || 0}
                    </div>
                </div>
                <div class="w-[25%] flex justify-center py-2 relative group">
                    <p class="w-full py-2 text-[#333]">${prestador.nit || 'Activo'}</p>
                    <div class="absolute z-50 items-center hidden w-[250px] group-hover:block bg-gray-100 shadow-lg rounded-lg text-[#333] font-bold px-4 py-2 border border-gray-300 group-hover:scale-y-100 transition-all duration-300 ease-in-out scale-y-0 origin-top"
                        style="top: -30px; left: 50%; transform: translateX(-50%);">
                        Contratos: ${prestador.nit || 0}
                    </div>
                </div>
            </div>
            `;
        });
    }
    
    // Actualizar el contenido del contenedor
    contenedor.innerHTML = html;
}

// Función para generar los paneles modales
function generarPanelesModales(prestadores) {
    // Primero eliminamos todos los paneles modales existentes
    document.querySelectorAll('.informacion').forEach(panel => {
        panel.remove();
    });
    
    // Crear el contenedor para los paneles modales si no existe
    let contenedorModales = document.getElementById('contenedor-modales');
    if (!contenedorModales) {
        contenedorModales = document.createElement('div');
        contenedorModales.id = 'contenedor-modales';
        document.body.appendChild(contenedorModales);
    } else {
        // Limpiar el contenedor existente
        contenedorModales.innerHTML = '';
    }
    
    // Verificar si hay prestadores
    if (!prestadores || prestadores.length === 0) {
        return;
    }
    
    let htmlModales = '';
    
    // Generar los paneles de sedes para cada prestador
    prestadores.forEach(prestador => {
        // Panel modal para las sedes del prestador
        htmlModales += `
        <div id="sedes-${prestador.nit}" class="informacion fixed inset-0 z-[9999] hidden flex-col bg-white shadow-2xl rounded-3xl text-[#333] p-6 border-2 border-blue-500 m-auto max-w-[90%] max-h-[90%] overflow-auto">
            <!-- Barra de título para sedes -->
            <div class="flex justify-between items-center mb-4 bg-white sticky top-0 z-[10000] pb-2 border-b-2 border-blue-300">
                <div class="flex w-[115px] justify-start space-x-2 text-black items-center">
                    <img src="/static/resources/x.gif" alt="img-close" class="close-sedes rounded-xl h-10 cursor-pointer" data-nit="${prestador.nit}">
                    <p class="close-sedes cursor-pointer font-semibold" data-nit="${prestador.nit}">Cerrar</p>
                </div>
                
                <div class="flex-grow text-center text-blue-600 font-bold">
                    <p class="option-img">Sedes de ${prestador.nombre} - ${prestador.nit}</p>
                </div>
                
                <div class="w-[115px]"></div>
            </div>

            <!-- Contenido de sedes -->
            <div class="w-full">
                <!-- Encabezados tabla sedes -->
                <div class="sticky top-16 bg-white flex justify-between text-center font-bold min-w-[1024px] border-b border-gray-300">
                    <p class="w-[3%] py-2">#</p>
                    <p class="w-[10%] py-2">Código H-S</p>
                    <p class="w-[20%] py-2">Departamento</p>
                    <p class="w-[20%] py-2">Municipio</p>
                    <p class="w-[15%] py-2">Dirección</p>
                    <p class="w-[10%] py-2">Télefono</p>
                    <p class="w-[22%] py-2">Email</p>
                </div>
        `;
                
        // Generar filas para cada sede
        if (prestador.sedes && prestador.sedes.length > 0) {
            prestador.sedes.forEach((sede, index) => {
                htmlModales += `
                <div class="flex items-center border-b border-gray-300 text-center min-w-[1024px] hover:bg-[#4aa5ff62] hover:font-semibold transition-colors duration-300 relative">
                    <!-- Número de fila -->
                    <div class="w-[3%] flex justify-between py-2 border-r border-gray-300 relative group">
                        <p class="w-full py-2">${index + 1}</p>
                        <div class="absolute z-50 hidden group-hover:block bg-gray-100 shadow-lg rounded-lg text-[#333] font-bold px-2 py-2 border border-gray-300 group-hover:scale-y-100 transition-all duration-300 ease-in-out scale-y-0 origin-top"
                        style="top: 0; left: 140%; transform: translateX(-50%);">
                            <!-- Botón para ver servicios -->
                            <div class="flex w-[50px] justify-center">
                                <img src="/static/resources/info2.gif" alt="img-info" class="toggle-servicios h-10 cursor-pointer" data-sede-id="${sede.codigo_de_habilitacion}-${sede.numero_sede}">
                            </div>
                        </div>
                    </div>
                    <p class="w-[10%] py-2 border-r border-gray-300">${sede.codigo_de_habilitacion}-${sede.numero_sede}</p>
                    <p class="w-[20%] py-2 border-r border-gray-300">${sede.departamento}</p>
                    <p class="w-[20%] py-2 border-r border-gray-300">${sede.municipio}</p>
                    <p class="w-[15%] py-2 border-r border-gray-300">${sede.direccion}</p>
                    <p class="w-[10%] py-2 border-r border-gray-300">${sede.telefono}</p>
                    <p class="w-[22%] py-2 border-gray-300">${sede.email}</p>
                </div>`;
                
                // Generar el panel de servicios para esta sede
                htmlModales += `
                <div id="servicios-${sede.codigo_de_habilitacion}-${sede.numero_sede}" 
                    class="informacion fixed inset-0 z-[9999] hidden flex-col bg-white shadow-2xl rounded-3xl text-[#333] p-6 border-2 border-orange-500 m-auto max-w-[90%] max-h-[90%] overflow-auto">
                    
                    <!-- Barra de título para servicios -->
                    <div class="flex justify-between items-center mb-4 bg-white sticky top-0 z-[10000] pb-2 border-b-2 border-orange-300">
                        <div class="flex w-[115px] justify-start space-x-2 text-black items-center">
                            <img src="/static/resources/x.gif" alt="img-close" class="close-servicios rounded-xl h-10 cursor-pointer" 
                                data-sede-id="${sede.codigo_de_habilitacion}-${sede.numero_sede}">
                            <p class="close-servicios cursor-pointer font-semibold" 
                                data-sede-id="${sede.codigo_de_habilitacion}-${sede.numero_sede}">Cerrar</p>
                        </div>
                        
                        <div class="flex-grow text-center text-orange-600 font-bold">
                            <p class="option-img">Servicios de la Sede: ${sede.sede_nombre || ''} 
                                (${sede.codigo_de_habilitacion} # ${sede.numero_sede})</p>
                        </div>
                        
                        <div class="w-[115px]"></div>
                    </div>
                    
                    <!-- Contenido de servicios -->
                    <div class="w-full">
                        <!-- Encabezados tabla servicios -->
                        <div class="sticky top-16 bg-white flex justify-between text-center font-bold min-w-[1024px] border-b border-gray-300">
                            <p class="w-[5%] py-2">#</p>
                            <p class="w-[15%] py-2">Código</p>
                            <p class="w-[40%] py-2">Servicio</p>
                            <p class="w-[10%] py-2">Grupo Cod.</p>
                            <p class="w-[20%] py-2">Grupo</p>
                            <p class="w-[10%] py-2">Complejidad</p>
                        </div>`;
                
                // Generar filas para cada servicio
                if (sede.servicios && sede.servicios.length > 0) {
                    sede.servicios.forEach((servicio, idx) => {
                        htmlModales += `
                        <div class="flex items-center border-b border-gray-300 text-center min-w-[1024px] hover:bg-[#4aa5ff62] hover:font-semibold transition-colors duration-300 relative">
                            <p class="w-[5%] py-2 border-r border-gray-300">${idx + 1}</p>
                            <p class="w-[15%] py-2 border-r border-gray-300">${servicio.serv_codigo}</p>
                            <p class="w-[40%] py-2 border-r border-gray-300">${servicio.serv_nombre}</p>
                            <p class="w-[10%] py-2 border-r border-gray-300">${servicio.grse_codigo}</p>
                            <p class="w-[20%] py-2 border-r border-gray-300">${servicio.grse_nombre}</p>
                            <p class="w-[10%] py-2 border-r border-gray-300">${servicio.complejidades}</p>
                        </div>`;
                    });
                } else {
                    htmlModales += `
                    <div class="flex items-center text-center bg-white">
                        <p class="w-full py-2 text-center text-gray-500 italic">No hay servicios registrados para esta sede</p>
                    </div>`;
                }
                
                htmlModales += `
                    </div>
                </div>`;
            });
        } else {
            htmlModales += `
            <div class="flex items-center text-center bg-white">
                <p class="w-full py-2 text-center text-gray-500 italic">No hay sedes registradas para este prestador</p>
            </div>`;
        }
        
        htmlModales += `
            </div>
        </div>`;
    });
    
    // Agregar los paneles modales al contenedor
    contenedorModales.innerHTML = htmlModales;
}