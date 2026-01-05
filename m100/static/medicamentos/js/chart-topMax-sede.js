document.addEventListener('DOMContentLoaded', function () {
  // 1. Obtener el script con los datos del gráfico
  const chartScript = document.getElementById('chart_data_sedes');
  const chartTS = document.getElementById('total_sedes');
  if (!chartScript) {
    console.warn("No se encontró <script id='chart_data_sedes' type='application/json'> con los datos del gráfico.");
    return;
  }

  // 2. Parsear los datos como JSON
  let chartDataSedes;
  try {
    chartDataSedes = JSON.parse(chartScript.textContent);
    console.log("Datos del chart :", chartDataSedes); // Verificar datos
  } catch (error) {
    console.error("Error al parsear chart_sedes:", error);
    return;
  }

  // 3. Verificar estructura esperada
  if (!chartDataSedes.data || !chartDataSedes.labels) {
    console.error("Estructura de datos incorrecta. Debe contener 'labels' y 'value'.");
    return;
  }

  // 4. Ordenar los datos de mayor a menor y tomar el top 5
  const sortedData = chartDataSedes.labels.map((label, index) => ({
    label,
    value: chartDataSedes.data[index]
  }))
  .sort((a, b) => b.value - a.value) // Ordenar de mayor a menor
  .slice(0, 5); // Tomar los 5 primeros

  // Extraer etiquetas y valores ordenados
  const topLabels = sortedData.map(item => item.label);
  const topValues = sortedData.map(item => item.value);

  // 5. Generar colores aleatorios para las barras
  const backgroundColors = topLabels.map(() => {
    const r = Math.floor(Math.random() * 200);
    const g = Math.floor(Math.random() * 200);
    const b = Math.floor(Math.random() * 200);
    return `rgba(${r}, ${g}, ${b}, 0.6)`;
  });

  // 9. Obtener el contexto del canvas
  const ctx = document.getElementById('chartTopSedeMayor');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartTopSedeMayor'> en la plantilla.");
    return;
  }

  const totalSedes = topValues.reduce((acc, val) => acc + val, 0);

  // 10. Crear el gráfico de barras horizontales
  const myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topLabels,
      datasets: [{
        label: `Total Sedes ${totalSedes} de ${chartTS.textContent} (${chartTS.textContent ? ((totalSedes || 0) / chartTS.textContent * 100).toFixed(2) : 0}%)`,
        data: topValues,
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(c => c.replace('0.7', '1')),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        x: { beginAtZero: true }
      },
      plugins: {
        title: {
          display: true,
          text: 'Top 5 Departamentos con Más Sedes',
          font: { size: 16 }
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `📌 ${tooltipItem.label}: ${tooltipItem.raw} Sedes`;
            }
          }
        }
      }
    }
  });
});