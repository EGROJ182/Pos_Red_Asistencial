document.addEventListener('DOMContentLoaded', function () {
  // 1. Obtener el script con los datos del gráfico
  const chartScript = document.getElementById('chart_reps');
  if (!chartScript) {
    console.warn("No se encontró <script id='chart_reps' type='application/json'> con los datos del gráfico.");
    return;
  }

  // 2. Parsear los datos como JSON
  let chartDataReps;
  try {
    chartDataReps = JSON.parse(chartScript.textContent);
    // console.log("Datos del chart:", chartDataReps); // Verificar datos
  } catch (error) {
    console.error("Error al parsear chart_reps:", error);
    return;
  }

  // 3. Verificar estructura esperada
  if (!chartDataReps.labels || !chartDataReps.datasets) {
    console.error("Estructura de datos incorrecta. Debe contener 'labels' y 'datasets'.");
    return;
  }

  // 4. Crear un objeto para almacenar la suma de reps por departamento
  const totalRepsPorDepartamento = {};

  // Inicializar con 0 para cada departamento
  chartDataReps.labels.forEach(label => {
    totalRepsPorDepartamento[label] = 0;
  });

  // 5. Sumar los valores de todos los datasets para cada departamento
  chartDataReps.datasets.forEach(dataset => {
    dataset.data.forEach((value, index) => {
      const depto = chartDataReps.labels[index];
      totalRepsPorDepartamento[depto] += value;
    });
  });

  // 6. Convertir a un array y ordenar de menor a mayor
  const sortedData = Object.entries(totalRepsPorDepartamento)
    .map(([label, value]) => ({ label, value }))
    .sort((a, b) => a.value - b.value) // Orden descendente
    .slice(0, 5); // Tomar el Top 5

  // 7. Extraer etiquetas y valores ordenados
  const topLabels = sortedData.map(item => item.label);
  const topValues = sortedData.map(item => item.value);

  // 8. Generar colores aleatorios
  const backgroundColors = topLabels.map(() => {
    const r = Math.floor(Math.random() * 100) + 100; // Más vibrante
    const g = Math.floor(Math.random() * 100) + 100;
    const b = Math.floor(Math.random() * 100) + 100;
    return `rgba(${r}, ${g}, ${b}, 0.7)`;
  });

  // 9. Obtener el contexto del canvas
  const ctx = document.getElementById('chartTopRepsMenor');
  if (!ctx) {
    console.warn("No se encontró <canvas id='chartTopRepsMenor'> en la plantilla.");
    return;
  }

  // 10. Crear el gráfico de barras horizontales
  const myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topLabels,
      datasets: [{
        label: 'Total Reps',
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
          text: 'Top 5 Departamentos con Menos Reps',
          font: { size: 16 }
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return `📌 ${tooltipItem.label}: ${tooltipItem.raw} reps`;
            }
          }
        }
      }
    }
  });
});
