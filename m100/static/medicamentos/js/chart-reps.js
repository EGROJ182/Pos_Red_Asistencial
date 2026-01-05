document.addEventListener('DOMContentLoaded', function () {
  // 1. Obtener los datos desde el script JSON
  const chartScript = document.getElementById('chart_reps');
  if (!chartScript) {
    console.warn("No se encontró <script id='chart_reps' type='application/json'> con los datos del gráfico.");
    return;
  }

  let chartDataReps;
  try {
    chartDataReps = JSON.parse(chartScript.textContent);
  } catch (error) {
    console.error("Error al parsear chart_reps:", error);
    return;
  }

  // 2. Verificar si Chart.js está cargado
  if (typeof Chart === "undefined") {
    console.error("Chart.js no está disponible. Asegúrate de incluir el script.");
    return;
  }

  // 3. Obtener el contexto del canvas
  const ctx = document.getElementById('chartRepsDepartamento');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartRepsDepartamento'> en la plantilla.");
    return;
  }

  // 4. Crear el gráfico de barras apiladas horizontales con Chart.js
  new Chart(ctx, {
    type: 'bar',
    data: {
      // Departamentos en "labels" => eje Y
      // datasets => tipos de servicio
      labels: chartDataReps.labels,
      datasets: chartDataReps.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      // indexAxis: 'y' => barras horizontales
      indexAxis: 'y',
      plugins: {
      // Configurar la leyenda para hover
        legend: {
          position: 'top',
          onHover: (event, legendItem, legend) => {
            // Al pasar el mouse sobre un label de la leyenda
            const chart = legend.chart;
            const { index } = legendItem; // índice del dataset
            const meta = chart.getDatasetMeta(index);
            
            // Construir un array con todos los elementos (barras) de ese dataset
            const activeElements = meta.data.map((_, i) => ({
              datasetIndex: index,
              index: i
            }));

            // 1) Resaltar visualmente las barras
            chart.setActiveElements(activeElements);

            // 2) Mostrar tooltip en las barras
            if (activeElements.length > 0) {
              // Tomar la posición de la primera barra para mostrar el tooltip
              const { x, y } = meta.data[0];
              chart.tooltip.setActiveElements(activeElements, { x, y });
            }
            chart.update();
          },
          onLeave: (event, legendItem, legend) => {
            // Al quitar el mouse de la leyenda
            const chart = legend.chart;

            // Desactivar el hover y tooltip en las barras
            chart.setActiveElements([]);
            chart.tooltip.setActiveElements([]);
            chart.update();
          }
        },
        // Tooltip normal cuando pasas el mouse por la barra
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `${tooltipItem.dataset.label}: ${tooltipItem.raw} reps`;
            }
          }
        }
      },
      scales: {
        x: {
          // Apilado en eje X
          stacked: true,
          beginAtZero: true
        },
        y: {
          // Apilado en eje Y
          stacked: true
        }
      }
    }
  });
});