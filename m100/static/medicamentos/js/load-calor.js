document.addEventListener('DOMContentLoaded', function() {
    // 1. Verificar el contenedor del mapa
    const mapaDiv = document.getElementById('mapaCalor');
    if (!mapaDiv) {
      console.error("No se encuentra el elemento <div id='mapaCalor'> en la vista.");
      return;
    }
  
    // 2. Verificar que Leaflet esté disponible
    if (typeof L === 'undefined') {
      console.error("Leaflet no se ha cargado correctamente (L es undefined).");
      return;
    }
  
    // 3. Crear el mapa en 'mapaCalor'
    let map = L.map('mapaCalor').setView([4.7110, -74.0721], 6);
  
    // 4. Añadir capa base (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Variable global para “fijar” el departamento
    // Si es null => no hay depto fijo. Si tiene string => es el depto fijo.
    let pinnedDept = null;
  
    // 5. Leer los datos JSON de departamentos desde <script id="mapa_data" type="application/json">
    const dataScript = document.getElementById('mapa_data');
    if (!dataScript) {
      console.warn("No se encontró <script id='mapa_data' type='application/json'> con los datos del mapa.");
      return;
    }
  
    let mapaData;
    try {
       // 1. Convertir el texto en un objeto/array de JSON
      const dataString = document.getElementById('mapa_data').textContent;
      mapaData = JSON.parse(dataString);
      // mapaData debe ser un array: [{departamento: "ANTIOQUIA", total: 123}, ...]
      // console.log("Datos del mapa:", mapaData);
    } catch (error) {
      console.error("Error al parsear el JSON del mapa:", error);
      return;
    }
  
    // 6. Construir diccionario { 'NOMBRE_DEPARTAMENTO': total }
    const dataPorDepartamento = {};
    mapaData.forEach(item => {
    //   const depto = (item.departamento || '').toUpperCase();
      const depto = quitarTildes(item.departamento).toUpperCase();
      dataPorDepartamento[depto] = item.total || 0;
    });
  
    // Función para eliminar tildes y diacríticos
    function quitarTildes(str) {
        return str
        .normalize("NFD")                  // Descompone caracteres latinos con diacríticos
        .replace(/[\u0300-\u036f]/g, "")  // Remueve los diacríticos
        .replace(/[.,]/g, "")           // Elimina comas, puntos
        .replace(/\s+/g, " ")           // Opcional: normaliza espacios
        .trim();
    }
    // 7. Definir escala de colores según valor
    const maxValue = Math.max(...Object.values(dataPorDepartamento));
    function getColor(d) {
      return d > maxValue * 0.8 ? '#800026' :
             d > maxValue * 0.6 ? '#BD0026' :
             d > maxValue * 0.4 ? '#E31A1C' :
             d > maxValue * 0.2 ? '#FC4E2A' :
             d > maxValue * 0.1 ? '#FD8D3C' :
             d > 0            ? '#FEB24C' :
                                '#FFEDA0';
    }
    const topoUrl = window.colombiaTopoURL;
    // 8. Cargar el archivo TopoJSON desde static
    fetch(topoUrl)
      .then(response => response.json())
      .then(topoData => {
        // console.log("TopoData loaded:", topoData);
        // 8.1 Convertir TopoJSON a GeoJSON
        //   - Ajusta 'topoData.objects.colombia' según el nombre real dentro de tu topojson
        // const geojson = topojson.feature(topoData, topoData.objects.colombia);
        // Convertir la capa MGN_ANM_DPTOS a GeoJSON
        const geojson = topojson.feature(topoData, topoData.objects.MGN_ANM_DPTOS);
        // Revisar las propiedades del primer feature para ver cómo se llaman
        // console.log("Un ejemplo de feature:", geojson.features[0]);
  
        // 8.2 Crear capa GeoJSON en Leaflet
        let geoJsonLayer = L.geoJSON(geojson, {
          style: function(feature) {
            // Asumiendo que el departamento está en feature.properties.DPTO
            // const departamento = (feature.properties.DPTO || '').toUpperCase();
            // const valor = dataPorDepartamento[departamento] || 0;
            const rawName = feature.properties.DPTO_CNMBR || '';
            const featureName = quitarTildes(rawName).toUpperCase();
            const valor = dataPorDepartamento[featureName] || 0;
            return {
              fillColor: getColor(valor),
              weight: 1,
              color: 'white',
              fillOpacity: 0.7
            };
          },
          onEachFeature: function(feature, layer) {
            // const departamento = (feature.properties.DPTO || '').toUpperCase();
            // const valor = dataPorDepartamento[departamento] || 0;
            const rawName = feature.properties.DPTO_CNMBR || '';
            const featureName = quitarTildes(rawName).toUpperCase();
            const valor = dataPorDepartamento[featureName] || 0;      
  
             // Muestra info en hover (tooltip)
            layer.bindTooltip(`<strong>${rawName}</strong><br>${valor} prestadores únicos`, {
              sticky: true, // El tooltip sigue al cursor
            });

            // // Popup con info
            layer.bindPopup(`<strong>${rawName}</strong><br>${valor} prestadores únicos`);
  
            // Clic para filtrar (opcional)
            layer.on('mouseover', function() {
              console.log("Departamento Hoveado:", departamento);
              // Aquí podrías llamar a AJAX para filtrar tablas, etc.
              // cargarDatosAjax({ departamento: departamento });
              // Llamamos a la función global que definimos en load-dpto.js
              if (pinnedDept === null && window.mostrarDepartamento) {
                window.mostrarDepartamento(rawName);
                // Cambiar el estilo de la capa
                layer.setStyle({
                  weight: 3,
                  color: 'yellow',
                  fillOpacity: 0.7
                });
              }
  
            });
              
              // Al quitar el mouse (mouseout), regresamos a Bogotá
              layer.on('mouseout', function() {
                console.log("Salio del Departamento:", departamento);
                if (pinnedDept === null && window.mostrarDepartamento) {
                  window.mostrarDepartamento("BOGOTA D.C.");
                  layer.setStyle({
                    weight: 1,
                    color: 'white',
                    fillOpacity: 0.7
                  });
                }
              });
              
              layer.on('click', function() {
                // Si el departamento clickeado es el mismo que ya está fijado, “desfijamos”
                if (pinnedDept === rawName) {
                  pinnedDept = null;
                  console.log("Departamento desfijado, regresando a Bogotá.");
                  layer.closePopup();
                  layer.setStyle({
                    weight: 1,
                    color: 'white',
                    fillOpacity: 0.7
                  });
                } else {
                  // Fijar el nuevo departamento
                  pinnedDept = rawName;
                  console.log("Departamento fijado:", pinnedDept);
                  layer.openPopup();
                  if (window.mostrarDepartamento) {
                    window.mostrarDepartamento(rawName);
                    // Cambiar el estilo de la capa
                    layer.setStyle({
                      weight: 3,
                      color: 'yellow',
                      fillOpacity: 0.7
                    });
                  }
                }
              });
          }
        }).addTo(map);
  
        // 8.3 Ajustar vista al contorno de la capa
        map.fitBounds(geoJsonLayer.getBounds());
      })
      .catch(err => {
        console.error("Error al cargar o procesar el TopoJSON:", err);
      });
  });
