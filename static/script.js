document.addEventListener('DOMContentLoaded', () => {
  // DOM references
  const urlGroup   = document.getElementById('urlGroup');
  const queryBox   = document.getElementById('query');
  const loader     = document.getElementById('loader');
  const slider     = document.getElementById('numResults');
  const label      = document.getElementById('numResultsLabel');
  let lastRecommendations = [];

  // === THEME TOGGLE ===
  document.getElementById('themeToggle')?.addEventListener('click', () => {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });

  // === Load saved theme on startup ===
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  // === MODE SWITCH (URL vs QUERY) ===
  document.querySelectorAll('input[name="mode"]').forEach(radio =>
    radio.addEventListener('change', () => {
      if (radio.value === 'url' && radio.checked) {
        urlGroup.style.display = 'flex';
        queryBox.rows = 6;
      }
      if (radio.value === 'query' && radio.checked) {
        urlGroup.style.display = 'none';
        queryBox.rows = 12;
      }
    })
  );
  // Trigger mode setup on load
  document.querySelector('input[name="mode"]:checked')?.dispatchEvent(new Event('change'));

  // === EXTRACT KEYWORDS FROM URL ===
  document.getElementById('extractBtn')?.addEventListener('click', () => {
    const url = document.getElementById('jobUrl').value.trim();
    try {
      const match = new URL(url).pathname.match(/\/(?:jobs\/view|jobs|job)\/([^/?]+)/i);
      if (match) {
        const keywords = match[1].toLowerCase().split('-').slice(0, 5).join(' ');
        queryBox.value = keywords;
      } else {
        alert("Could not extract keywords from that URL.");
      }
    } catch {
      alert("Invalid URL.");
    }
  });

  // === MAIN RECOMMENDATION ACTION ===
  document.getElementById('btn')?.addEventListener('click', async () => {
    const query = queryBox.value.trim();
    if (!query) return;

    const results = document.getElementById('results');
    loader.style.display = 'inline';
    results.innerHTML = '';

    try {
      const res = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      lastRecommendations = data.recommendations || [];
      renderRecommendations();
    } catch (err) {
      console.error(err);
      alert("Error fetching recommendations.");
    } finally {
      loader.style.display = 'none';
    }
  });

  // === DROPDOWN ===
  const menuBtn = document.getElementById('menuBtn');
  const dropdown = menuBtn?.closest('.dropdown');
  menuBtn?.addEventListener('click', e => {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });
  document.addEventListener('click', () => {
    dropdown?.classList.remove('open');
  });

  // Help/About actions
  document.getElementById('helpBtn')?.addEventListener('click', e => {
    e.preventDefault();
    alert('Show help content here');
  });

  document.getElementById('aboutBtn')?.addEventListener('click', e => {
    e.preventDefault();
    alert('Show about content here');
  });

  // === RENDERING FUNCTION ===
  function renderRecommendations() {
    const results = document.getElementById('results');
    results.innerHTML = '';
  
    const max = parseInt(slider?.value || '5', 10);
    lastRecommendations.slice(0, max).forEach((r, i) => {
      const div = document.createElement('div');
      div.className = 'rec';
  
      div.innerHTML = `
        <strong>${i + 1}. ${r.name}</strong><br>
        <button class="glass-button" onclick="window.open('${r.url}', '_blank')">Assessment</button><br>
        <p><strong>Score:</strong> ${r.relevance?.toFixed(3) || 'N/A'}<br>
        <strong>Duration:</strong> ${r.duration || 'N/A'} min<br>
        <strong>Remote:</strong> ${r.remote_testing}, <strong>Adaptive:</strong> ${r.adaptive_irt}<br>
        <strong>Types:</strong> ${r.test_type?.join(', ') || 'N/A'}</p>
      `;
      results.appendChild(div);
    });
  }
  
});


function showToast(msg, duration = 3000) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, duration);
}
const slider = document.getElementById('numResults');
const label = document.getElementById('numResultsLabel');

slider?.addEventListener('input', () => {
  label.textContent = slider.value;
  renderRecommendations(); // this re-renders results based on new k
});
