/**
 * Beyond Tour — Tourism Analytics Dashboard Controller
 * Renders Chart.js doughnut and bar charts based on regional and category distributions.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (typeof Chart === 'undefined') return;

  const dataElem = document.getElementById('tourism-chart-data');
  const chartData = dataElem ? JSON.parse(dataElem.textContent || '{}') : {};

  const regionCanvas = document.getElementById('regionChart');
  if (regionCanvas) {
    const regionCtx = regionCanvas.getContext('2d');
    new Chart(regionCtx, {
      type: 'doughnut',
      data: {
        labels: ['Kumaon', 'Garhwal'],
        datasets: [{
          data: [chartData.kumaonCount || 0, chartData.garhwalCount || 0],
          backgroundColor: ['#C1622D', '#6B8F71'],
          borderWidth: 0
        }]
      },
      options: {
        plugins: {
          legend: {
            labels: { color: '#F7F3EC' }
          }
        }
      }
    });
  }

  const catCanvas = document.getElementById('categoryChart');
  if (catCanvas) {
    const catCtx = catCanvas.getContext('2d');
    new Chart(catCtx, {
      type: 'bar',
      data: {
        labels: chartData.catLabels || [],
        datasets: [{
          label: 'Destinations',
          data: chartData.catData || [],
          backgroundColor: '#C1622D',
          borderRadius: 6
        }]
      },
      options: {
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { ticks: { color: '#DCD3C4' }, grid: { color: 'rgba(220, 211, 196, 0.1)' } },
          x: { ticks: { color: '#DCD3C4' }, grid: { display: false } }
        }
      }
    });
  }
});
