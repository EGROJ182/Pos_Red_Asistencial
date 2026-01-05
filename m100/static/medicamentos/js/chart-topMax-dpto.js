document.addEventListener('DOMContentLoaded', function () {
  // 1. Obtener el script con los datos del gráfico
  const chartScript = document.getElementById('chart_data');
  const total_pc = document.getElementById('total_pc');

  if (!chartScript) {
    console.warn("No se encontró <script id='chart_data' type='application/json'> con los datos del gráfico.");
    return;
  }

  // 2. Parsear los datos como JSON
  let chartData;
  try {
    chartData = JSON.parse(chartScript.textContent);
    // console.log("Datos del chart:", chartData); // Verificar datos
  } catch (error) {
    console.error("Error al parsear chart_data:", error);
    return;
  }

  // 3. Verificar estructura esperada
  if (!chartData.data || !chartData.labels) {
    console.error("Estructura de datos incorrecta. Debe contener 'labels' y 'value'.");
    return;
  }

  // 4. Ordenar los datos de mayor a menor y tomar el top 5
  const sortedData = chartData.labels.map((label, index) => ({
    label,
    value: chartData.data[index]
  }))
  .sort((a, b) => b.value - a.value) // Ordenar de mayor a menor
  .slice(0, 5); // Tomar los 5 primeros

  // Extraer etiquetas y valores ordenados
  const topLabels = sortedData.map(item => item.label);
  const topValues = sortedData.map(item => item.value);

  const prestadores = topValues.reduce((acc, val) => acc + val, 0);

  // 5. Generar colores aleatorios para las barras
  const backgroundColors = topLabels.map(() => {
    const r = Math.floor(Math.random() * 200);
    const g = Math.floor(Math.random() * 200);
    const b = Math.floor(Math.random() * 200);
    return `rgba(${r}, ${g}, ${b}, 0.6)`;
  });

  // 9. Obtener el contexto del canvas
  const ctx = document.getElementById('chartTopMayorDpto');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartTopMayorDpto'> en la plantilla.");
    return;
  }

  // 10. Crear el gráfico de barras horizontales
  const myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topLabels,
      datasets: [{
        label: `Cantidad de Prestadores ${prestadores} de ${total_pc.textContent} (${total_pc.textContent ? ((prestadores || 0) / total_pc.textContent * 100).toFixed(2) : 0}%)`,
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
          text: 'Top 5 Departamentos con mayor cantidad de Prestadores',
          font: { size: 16 }
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `📌 ${tooltipItem.label}: ${tooltipItem.raw} Prestadores`;
            }
          }
        }
      }
    }
  });
});
