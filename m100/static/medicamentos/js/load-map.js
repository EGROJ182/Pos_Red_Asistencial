document.addEventListener('DOMContentLoaded', function() {
    const mapaDiv = document.getElementById('map');
    if (!mapaDiv) {
      console.error("No se encuentra el elemento <div id='map'> en la vista.");
      return;
    }
  
    // 2. Verificar que Leaflet esté disponible
    if (typeof L === 'undefined') {
      console.error("Leaflet no se ha cargado correctamente (L es undefined).");
      return;
    }
    // Verificar si map existe
    if (document.getElementById('map')) {
        // Verificar si Leaflet está cargado
        if (typeof L !== 'undefined') {
            // Crear el mapa centrado en un punto por defecto
            let map = L.map('map').setView([4.7110, -74.0721], 13); // Coordenadas de Bogotá
            // console.log(map);

            // Agregar un "tile layer" al mapa (usamos OpenStreetMap en este caso)
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // Obtener el contenido del <script type="application/json">
            const mapa_data = document.querySelector('script[type="application/json"]').textContent;
            // console.log(mapa_data);  // Verifica que contiene un JSON válido

            // Intentar parsear el JSON
            try {
                const parsedData = JSON.parse(mapa_data);
                // console.log(parsedData);  // Verifica que los datos son los esperados

                // Agregar los marcadores al mapa
                parsedData.forEach(function(departamento) {
                    let lat = parseFloat(departamento.lat);
                    let lng = parseFloat(departamento.lng);

                    // Crear el marcador
                    let marker = L.marker([lat, lng]).addTo(map);

                    // Crear contenido para la ventana emergente
                    let popupContent = `<h4>${departamento.departamento}</h4>`;
                    departamento.proveedores.forEach(function(proveedor) {
                        popupContent += `<p><strong>${proveedor.nombre}</strong><br>${proveedor.direccion}<br>Tipo: ${proveedor.tipo_proveedor}</p>`;
                    });

                    // Asignar la ventana emergente al marcador
                    marker.bindPopup(popupContent);

                });
            } catch (error) {
                console.error("Error al parsear JSON: ", error);
            }
        } else {
            console.error("Leaflet no se ha cargado correctamente.");
        }   
    }
    else {
        console.error("No se encuentra map en la vista.");
    }
});