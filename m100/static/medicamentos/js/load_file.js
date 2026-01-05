// Función para enviar el archivo y el formulario al servidor mediante AJAX
function handleFileSelect(event) {
    event.preventDefault(); // Previene el envío del formulario por defecto

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        Swal.fire({
            icon: 'info',
            title: 'Información',
            text: 'Por favor seleccione un Archivo para continuar.',
            confirmButtonText: 'Aceptar'
        });
        return;
    }

    // Mostrar el nombre del archivo
    document.getElementById("file-name").innerHTML = `<span>Archivo seleccionado: ${file.name}</span>`;

    // Crear el objeto FormData para enviar el archivo y los datos del formulario
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fecha_pactada", document.getElementById('fecha_pactada').value);
    // formData.append("nit_proveedor", document.getElementById('nit_proveedor').value);
    formData.append("nombre_del_proveedor_pactado", document.getElementById('nombre_del_proveedor_pactado').value);
    formData.append("numero_acta_inicial", document.getElementById('numero_acta_inicial').value);

    // Mostrar el spinner de carga
    document.getElementById('loading-spinner').classList.remove('hidden');

    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar la petición AJAX
    fetch(loadMedUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken // Django necesita el token CSRF para solicitudes POST
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Ocultar el spinner de carga
        document.getElementById('loading-spinner').classList.add('hidden');

        if (data.error) {
            // Mostrar mensaje de SweetAlert2 en caso de error
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: `${data.error}`,
                confirmButtonText: 'Aceptar'
            });
        } else if (data.success) {
            // Mostrar mensaje de éxito si hay registros cargados
            Swal.fire({
                icon: 'success',
                title: 'Éxito',
                text: `${data.success} registros cargados: ${data.num_records}`,
                confirmButtonText: 'Aceptar'
            });
            document.getElementById('result-query').textContent = data.num_records;
        } else if (data.file_url) {
            // Mostrar mensaje de éxito si se genera un archivo
            Swal.fire({
                icon: 'success',
                title: 'ℹ Acta Cargada ℹ',
                text: `Registros cargados: ${data.num_records}`,
                confirmButtonText: 'Descargar'
            }).then(() => {
                // Redirigir a la URL del archivo después de cerrar la alerta
                window.location.href = data.file_url;
            });
        }
    })
    .catch(error => {
        document.getElementById('loading-spinner').classList.add('hidden');
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: '⚠ Error ⚠',
            text: `Hubo un error al procesar el archivo. Por favor, inténtalo nuevamente.\n${error}`,
            confirmButtonText: 'Aceptar'
        });
    });
}

// Función para manejar el arrastre del archivo
function handleDrop(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    const fileInput = document.getElementById("file-input");

    if (file) {
        // Asignar el archivo arrastrado al input file
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // Mostrar el nombre del archivo
        document.getElementById("file-name").innerHTML = `<span>Archivo seleccionado: ${file.name}</span>`;
    }
}