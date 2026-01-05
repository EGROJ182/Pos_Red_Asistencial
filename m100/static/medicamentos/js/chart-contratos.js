document.addEventListener('DOMContentLoaded', function() {
  // 1. Tomar el <script id="chartData">
  const chartScript = document.getElementById('chart_contratos');
  if (!chartScript) {
    console.warn("No se encontró <script id='chartContratos' type='application/json'> con los datos del gráfico.");
    return;
  }

  // 2. Parsear el contenido como JSON
  let chartData;
  try {
    chartData = JSON.parse(chartScript.textContent);
    // chartData = { labels: [...], data: [...] }
    // console.log("Datos del chart:", chartData);
  } catch (error) {
    console.error("Error al parsear chart_contratos:", error);
    return;
  }

  // 3. Obtener el contexto del canvas
  const ctx = document.getElementById('chartPrestadoresContrato');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartPrestadoresContrato'> en la plantilla.");
    return;
  }

  // 4. Generar colores aleatorios para cada departamento (opcional)
  // const backgroundColors = chartData.labels.map(() => {
  //   const r = Math.floor(Math.random() * 200);
  //   const g = Math.floor(Math.random() * 200);
  //   const b = Math.floor(Math.random() * 200);
  //   return `rgba(${r}, ${g}, ${b}, 0.6)`;
  // });

  // Generar colores en tonos de azul desde oscuro a claro
  const backgroundColors = chartData.labels.map((_, index, array) => {
    const total = array.length;
    const intensity = Math.floor(35 + (index / total) * 180); // Ahora va de 75 (oscuro) a 255 (claro)
    return `rgba(${intensity}, ${intensity}, 155, 0.9)`; // Mantiene el azul fuerte y varía la intensidad
  });

  // 5. Crear el gráfico de torta con Chart.js
  const myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: chartData.labels,
      datasets: [{
        data: chartData.data,
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(c => c.replace('0.6', '1')),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              // Cálculo de porcentaje
              const dataset = context.dataset.data;
              const total = dataset.reduce((a, b) => a + b, 0);
              const value = context.raw;
              const pct = ((value / total) * 100).toFixed(1) + '%';
              return `${context.label}: ${value} (${pct})`;
            }
          }
        },
        // Leyenda con hover + mostrar valores al lado del nombre
        legend: {
          position: 'right',
          labels: {
            // Personalizar las etiquetas de la leyenda
            generateLabels: function (chart) {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                const dataset = data.datasets[0];
                return data.labels.map(function (label, i) {
                  const background = dataset.backgroundColor[i];
                  const value = dataset.data[i];
                  return {
                    // Texto en la leyenda: "Departamento X 300 prestadores"
                    text: `${label} ${value}`,
                    fillStyle: background,
                    hidden: isNaN(value) || value === null,
                    index: i
                  };
                });
              }
              return [];
            }
          },
          // Eventos de hover en la leyenda
          onHover: (event, legendItem, legend) => {
            // Al pasar el mouse sobre un label en la leyenda
            const chart = legend.chart;
            const { index } = legendItem;

            // Localizar la posición (x,y) del slice en el canvas
            const meta = chart.getDatasetMeta(0);
            const slice = meta.data[index];
            if (!slice) return;

            // Activar el tooltip sobre ese slice
            chart.tooltip.setActiveElements(
              [{ datasetIndex: 0, index }], 
              { x: slice.x, y: slice.y }
            );

            // Marcar el slice como "hover" (cambia el estilo)
            chart.setActiveElements([{ datasetIndex: 0, index }]);
            chart.update();
          },
          onLeave: (event, legendItem, legend) => {
            // Al quitar el mouse de la leyenda
            const chart = legend.chart;

            // Desactivar tooltip y hover
            chart.tooltip.setActiveElements([], { x: 0, y: 0 });
            chart.setActiveElements([]);
            chart.update();
          }
        }
      }
    }
  });
});