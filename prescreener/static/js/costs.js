function renderSpendChart(whisper, claude, opusclip) {
  const ctx = document.getElementById('spend-chart');
  if (!ctx) return;

  const total = whisper + claude + opusclip;
  if (total === 0) {
    ctx.parentElement.innerHTML = '<div class="flex items-center justify-center h-full text-gray-500 text-sm">No spending data yet</div>';
    return;
  }

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Whisper', 'Claude', 'OpusClip'],
      datasets: [{
        data: [whisper, claude, opusclip],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(168, 85, 247, 0.8)',
          'rgba(34, 197, 94, 0.8)',
        ],
        borderColor: '#1e293b',
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#9ca3af', padding: 16 },
        },
        tooltip: {
          callbacks: {
            label: (item) => `${item.label}: $${item.raw.toFixed(4)}`,
          },
        },
      },
    },
  });
}

async function logOpusClip() {
  const credits = parseInt(document.getElementById('opus-credits').value);
  const notes = document.getElementById('opus-notes').value;
  const feedback = document.getElementById('opus-feedback');

  if (!credits || credits <= 0) {
    feedback.textContent = 'Enter a positive number of credits.';
    feedback.className = 'text-xs text-red-400';
    feedback.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/costs/opusclip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credits, notes }),
    });
    const data = await res.json();
    feedback.textContent = `Logged ${credits} credits ($${data.amount.toFixed(4)})`;
    feedback.className = 'text-xs text-green-400';
    feedback.classList.remove('hidden');

    document.getElementById('opus-credits').value = '';
    document.getElementById('opus-notes').value = '';

    setTimeout(() => location.reload(), 1500);
  } catch (e) {
    feedback.textContent = 'Error logging credits.';
    feedback.className = 'text-xs text-red-400';
    feedback.classList.remove('hidden');
  }
}
