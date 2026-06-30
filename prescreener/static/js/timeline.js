let timelineChart = null;

async function loadTimeline(analysisId) {
  try {
    const res = await fetch(`/api/timeline/${analysisId}`);
    const data = await res.json();
    if (data.moments && data.moments.length > 0) {
      renderTimeline(data);
    }
  } catch (e) {
    console.error('Timeline load error:', e);
  }
}

function renderTimeline(data) {
  const ctx = document.getElementById('timeline-chart');
  if (!ctx) return;

  const section = document.getElementById('timeline-section');
  if (section) section.classList.remove('hidden');

  const durationMin = data.duration_seconds / 60;
  const moments = data.moments;

  const colorMap = {
    red: 'rgba(239, 68, 68, 0.8)',
    orange: 'rgba(249, 115, 22, 0.8)',
    yellow: 'rgba(234, 179, 8, 0.7)',
    gray: 'rgba(107, 114, 128, 0.5)',
  };

  const labels = moments.map(m => m.start / 60);
  const barColors = moments.map(m => colorMap[m.color] || colorMap.gray);
  const scores = moments.map(m => m.virality_score);

  timelineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: scores,
        backgroundColor: barColors,
        borderColor: barColors,
        borderWidth: 1,
        borderRadius: 3,
        barThickness: 12,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => {
              const m = moments[items[0].dataIndex];
              return `${m.start_display} – ${m.end_display} (${Math.round(m.duration)}s)`;
            },
            label: (item) => {
              const m = moments[item.dataIndex];
              return [
                `Score: ${m.virality_score}/10`,
                `${m.category.replace('_', ' ')}`,
                m.reason,
              ];
            },
          },
        },
      },
      scales: {
        x: {
          type: 'linear',
          min: 0,
          max: durationMin,
          title: {
            display: true,
            text: 'Time (minutes)',
            color: '#9ca3af',
          },
          ticks: { color: '#6b7280' },
          grid: { color: 'rgba(75, 85, 99, 0.3)' },
          offset: false,
        },
        y: {
          min: 0,
          max: 10,
          title: {
            display: true,
            text: 'Virality Score',
            color: '#9ca3af',
          },
          ticks: {
            color: '#6b7280',
            stepSize: 2,
          },
          grid: { color: 'rgba(75, 85, 99, 0.3)' },
        },
      },
      onClick: (event, elements) => {
        if (elements.length > 0) {
          const m = moments[elements[0].index];
          const card = document.getElementById(`moment-${m.id}`);
          if (card) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.classList.add('border-accent');
            setTimeout(() => card.classList.remove('border-accent'), 2000);
          }
        }
      },
    },
  });
}
