// load-dpto.js
document.addEventListener('DOMContentLoaded', function() {
  // 1) Crear el segundo mapa
  window.mapDpto = L.map('mapaDpto').setView([4.7110, -74.0721], 7);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(window.mapDpto);

  const dataScript = document.getElementById('mapa_data_dos');
  let deptData = {};
  if (dataScript) {
    try {
      deptData = JSON.parse(dataScript.textContent); 
      // console.log(deptData)

      // Crear un nuevo objeto con las llaves normalizadas
      const newDeptData = {};
      for (let nd in deptData) {
        // Normalizar la clave 'nd'
        const normKey = quitarTildes(nd).toUpperCase();

        // Copiar el contenido
        newDeptData[normKey] = deptData[nd];
      }

      // Reemplazar el objeto original por el nuevo
      deptData = newDeptData;

      // deptData => { "ANTIOQUIA": {"prestadores":..., "sedes":..., "reps":...}, ... }
    } catch (err) {
      console.error("Error al parsear mapa_data_dos:", err);
    }
  }

  // 2) Cargar el TopoJSON (o GeoJSON) de los departamentos
  //    Ajusta la ruta según tu archivo real:
  fetch("/static/geojson/colombia.topojson")
    .then(res => res.json())
    .then(topoData => {
      // Suponiendo que la capa se llama MGN_ANM_DPTOS
      // (mira el console.log para confirmarlo)

      const geojson = topojson.feature(topoData, topoData.objects.MGN_ANM_DPTOS);
      // Guardamos la lista de features en una variable global
      window.geojsonDptos = geojson;

      // Por defecto, mostramos Bogotá
      mostrarDepartamento("BOGOTA D.C.");
    })
    .catch(err => {
      console.error("Error en load-dpto.js al cargar TopoJSON:", err);
    });
// });

/**
 * Función global que filtra y dibuja un único departamento
 * en el mapaDpto.
 */
window.mostrarDepartamento = function(deptoName) {
  if (!window.geojsonDptos) return;

  // Eliminar capa anterior, si existe
  if (window.layerDpto) {
    window.mapDpto.removeLayer(window.layerDpto);
  }

  // Filtrar las features para quedarnos solo con el depto
  const features = window.geojsonDptos.features.filter(f => {
    // Ajusta la propiedad según tu TopoJSON:
    // p.ej. f.properties.DPTO_CNMBR, f.properties.NOMBRE_DPT, etc.
    const nombre = quitarTildes(f.properties.DPTO_CNMBR || '').toUpperCase();
    const buscado = quitarTildes(deptoName).toUpperCase();
    return nombre === buscado;
  });

  // Crear la nueva capa con las features filtradas
  window.layerDpto = L.geoJSON(
    { type: "FeatureCollection", features: features },
    {
      style: { color: 'darkblue', weight: 2, fillOpacity: 0.3 }
    }
  ).addTo(window.mapDpto);

  // Ajustar el zoom a ese departamento
  if (features.length > 0) {
    window.mapDpto.fitBounds(window.layerDpto.getBounds());
  }

  // 4) Mostrar datos del departamento en un popup (opcional)
  const dptoKey = quitarTildes(deptoName).toUpperCase(); 
  // Buscar en deptData
  let info = deptData[dptoKey];
  if (!info) {
    info = { prestadores: 0, sedes: 0, reps: 0 };
  }

  let html_temp = ""
  const cobertura = info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0;

  if (parseFloat(cobertura) >= 80){
    html_temp = `
      <strong>${deptoName} <img src="${logoUrl}" alt="Logo" class="logo-img h-[15px] w-[15px]"></strong>
      <strong>Red Asistencial Positiva</strong><br>
      Número de Prestadores: ${info.prestadores || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios || 0}<br>
      <spam style="color:green; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes || 0}<br>
      Códigos REPS Habilitados: ${info.reps || 0}<br>
      ------------------------------------------------------------<br>
      <strong>REPS</strong><br>
      Número de Prestadores: ${info.prestadores_reps || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios_reps || 0}<br>
      <spam style="color:black; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios_reps || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes_reps || 0}<br>
      Códigos REPS Habilitados: ${info.reps_reps || 0}<br>
    `;
  }
  else if (parseFloat(cobertura) >= 60){
    html_temp = `
      <strong>${deptoName} <img src="${logoUrl}" alt="Logo" class="logo-img h-[15px] w-[15px]"></strong>
      <strong>Red Asistencial Positiva</strong><br>
      Número de Prestadores: ${info.prestadores || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios || 0}<br>
      <spam style="color:rgba(218, 165, 32, 0.76); font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes || 0}<br>
      Códigos REPS Habilitados: ${info.reps || 0}<br>
      ------------------------------------------------------------<br>
      <strong>REPS</strong><br>
      Número de Prestadores: ${info.prestadores_reps || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios_reps || 0}<br>
      <spam style="color:black; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios_reps || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes_reps || 0}<br>
      Códigos REPS Habilitados: ${info.reps_reps || 0}<br>
    `;
  }
  else if (parseFloat(cobertura) >= 40){
    html_temp = `
      <strong>${deptoName} <img src="${logoUrl}" alt="Logo" class="logo-img h-[15px] w-[15px]"></strong>
      <strong>Red Asistencial Positiva</strong><br>
      Número de Prestadores: ${info.prestadores || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios || 0}<br>
      <spam style="color:orange; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes || 0}<br>
      Códigos REPS Habilitados: ${info.reps || 0}<br>
      ------------------------------------------------------------<br>
      <strong>REPS</strong><br>
      Número de Prestadores: ${info.prestadores_reps || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios_reps || 0}<br>
      <spam style="color:black; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios_reps || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes_reps || 0}<br>
      Códigos REPS Habilitados: ${info.reps_reps || 0}<br>
    `;
  }
  else if (parseFloat(cobertura) >= 20){
    html_temp = `
      <strong>${deptoName} <img src="${logoUrl}" alt="Logo" class="logo-img h-[15px] w-[15px]"></strong>
      <strong>Red Asistencial Positiva</strong><br>
      Número de Prestadores: ${info.prestadores || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios || 0}<br>
      <spam style="color:rgb(243, 16, 8); font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes || 0}<br>
      Códigos REPS Habilitados: ${info.reps || 0}<br>
      ------------------------------------------------------------<br>
      <strong>REPS</strong><br>
      Número de Prestadores: ${info.prestadores_reps || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios_reps || 0}<br>
      <spam style="color:black; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios_reps || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes_reps || 0}<br>
      Códigos REPS Habilitados: ${info.reps_reps || 0}<br>
    `;
  }
  else {
    html_temp = `
      <strong>${deptoName} <img src="${logoUrl}" alt="Logo" class="logo-img h-[15px] w-[15px]"></strong>
      <strong>Red Asistencial Positiva</strong><br>
      Número de Prestadores: ${info.prestadores || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios || 0}<br>
      <spam style="color:red; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes || 0}<br>
      Códigos REPS Habilitados: ${info.reps || 0}<br>
      ------------------------------------------------------------<br>
      <strong>REPS</strong><br>
      Número de Prestadores: ${info.prestadores_reps || 0}<br>
      Número de Municipios con Cobertura: ${info.municipios_reps || 0}<br>
      <spam style="color:black; font-weight: bold;">% Cobertura Departamental:  ${info.dane ? ((info.municipios_reps || 0) / info.dane * 100).toFixed(2) : 0}%</spam><br>
      Total Municipios DANE: ${info.dane || 0}<br>
      N° Sedes de Atención: ${info.sedes_reps || 0}<br>
      Códigos REPS Habilitados: ${info.reps_reps || 0}<br>
    `;
  }
  // Construir HTML
  const infoHtml = html_temp;

  // Para mostrarlo en la capa. Si son multipolígonos, puedes bindear a la primera feature
  window.layerDpto.eachLayer(function(layer) {
    layer.bindPopup(infoHtml).openPopup();
  });
};

/**
 * Función para eliminar tildes (Á->A, É->E, etc.)
 */
function quitarTildes(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[.,]/g, "")           // Elimina comas, puntos
    .replace(/\s+/g, " ")           // Opcional: normaliza espacios
    .trim();
  }
});