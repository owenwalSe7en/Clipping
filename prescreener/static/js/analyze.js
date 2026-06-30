let pollInterval = null;

function startPolling(analysisId) {
  pollInterval = setInterval(() => pollStatus(analysisId), 2000);
}

async function pollStatus(analysisId) {
  try {
    const res = await fetch(`/api/status/${analysisId}`);
    const data = await res.json();

    const bar = document.getElementById('progress-bar');
    const step = document.getElementById('progress-step');
    const pct = document.getElementById('progress-pct');
    const section = document.getElementById('progress-section');
    const costEl = document.getElementById('analysis-cost');
    const titleEl = document.getElementById('analysis-title');

    if (bar) bar.style.width = data.progress_pct + '%';
    if (step) step.textContent = data.current_step;
    if (pct) pct.textContent = data.progress_pct + '%';
    if (section) section.classList.remove('hidden');
    if (costEl && data.total_cost > 0) costEl.textContent = '$' + data.total_cost.toFixed(4);
    if (titleEl && data.title && data.title !== 'Loading...') titleEl.textContent = data.title;

    if (data.status === 'complete') {
      clearInterval(pollInterval);
      if (section) section.classList.add('hidden');
      window.location.reload();
    } else if (data.status === 'failed') {
      clearInterval(pollInterval);
      if (step) step.textContent = 'Failed: ' + (data.error || 'Unknown error');
      if (bar) bar.classList.replace('bg-accent', 'bg-red-500');
    }
  } catch (e) {
    console.error('Poll error:', e);
  }
}

async function toggleApprove(momentId, btn) {
  try {
    const res = await fetch(`/api/moments/${momentId}/approve`, { method: 'POST' });
    const data = await res.json();
    if (data.approved) {
      btn.textContent = 'Approved';
      btn.className = 'approve-btn px-3 py-1 text-sm rounded transition bg-green-700 text-green-200';
    } else {
      btn.textContent = 'Approve';
      btn.className = 'approve-btn px-3 py-1 text-sm rounded transition bg-gray-700 text-gray-400 hover:bg-green-800 hover:text-green-300';
    }
  } catch (e) {
    console.error('Approve error:', e);
  }
}
