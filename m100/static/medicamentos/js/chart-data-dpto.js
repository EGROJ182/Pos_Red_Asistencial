document.addEventListener('DOMContentLoaded', function() {
  const chartScript = document.getElementById('chart_data');
  if (!chartScript) {
    console.warn("No se encontró <script id='chartData' type='application/json'> con los datos del gráfico.");
    return;
  }

  let chartData;
  try {
    chartData = JSON.parse(chartScript.textContent);
  } catch (error) {
    console.error("Error al parsear chart_data:", error);
    return;
  }

  const ctx = document.getElementById('chartPrestadoresDepartamento');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartPrestadoresDepartamento'> en la plantilla.");
    return;
  }

  // Ordenar los datos de mayor a menor
  const sortedData = chartData.labels
    .map((label, index) => ({ label, value: chartData.data[index] }))
    .sort((a, b) => b.value - a.value); // Orden descendente

  const labelsSorted = sortedData.map(item => item.label);
  const dataSorted = sortedData.map(item => item.value);

  // Generar colores aleatorios después de ordenar
  // const backgroundColors = labelsSorted.map(() => {
  //   const r = Math.floor(Math.random() * 200);
  //   const g = Math.floor(Math.random() * 200);
  //   const b = Math.floor(Math.random() * 200);
  //   return `rgba(${r}, ${g}, ${b}, 0.6)`;
  // });

  // Generar colores en tonos de azul desde oscuro a claro
  const backgroundColors = labelsSorted.map((_, index, array) => {
    const total = array.length;
    const intensity = Math.floor(35 + (index / total) * 180); // Ahora va de 75 (oscuro) a 255 (claro)
    return `rgba(155, ${intensity}, ${intensity}, 0.9)`; // Mantiene el azul fuerte y varía la intensidad
  });

  const myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labelsSorted,
      datasets: [{
        data: dataSorted,
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
              const dataset = context.dataset.data;
              const total = dataset.reduce((a, b) => a + b, 0);
              const value = context.raw;
              const pct = ((value / total) * 100).toFixed(1) + '%';
              return `${context.label}: ${value} (${pct})`;
            }
          }
        },
        legend: {
          position: 'right',
          labels: {
            generateLabels: function (chart) {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                const dataset = data.datasets[0];
                return data.labels.map(function (label, i) {
                  const background = dataset.backgroundColor[i];
                  const value = dataset.data[i];
                  return {
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
          onHover: (event, legendItem, legend) => {
            const chart = legend.chart;
            const { index } = legendItem;
            const meta = chart.getDatasetMeta(0);
            const slice = meta.data[index];
            if (!slice) return;

            chart.tooltip.setActiveElements(
              [{ datasetIndex: 0, index }], 
              { x: slice.x, y: slice.y }
            );

            chart.setActiveElements([{ datasetIndex: 0, index }]);
            chart.update();
          },
          onLeave: (event, legendItem, legend) => {
            const chart = legend.chart;
            chart.tooltip.setActiveElements([], { x: 0, y: 0 });
            chart.setActiveElements([]);
            chart.update();
          }
        }
      }
    }
  });
});
