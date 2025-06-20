const API_URL = '/fetch';

async function fetchData() {
  const res = await fetch(API_URL, { headers: { accept: 'application/json' } });
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

function createMonitorCard(monitor) {
  return `
    <article class="glass-card p-5 cursor-pointer select-text" tabindex="0" role="button" aria-label="Monitor ${monitor.monitor_id}" data-type="monitor" data-id="${monitor.monitor_id}">
      <h3 class="text-lg font-semibold text-var(--text-primary) truncate" data-tooltip="${monitor.monitor_id}">${monitor.monitor_id}</h3>
      <p class="mt-1 text-sm text-var(--text-muted) font-mono">Resolution: ${monitor.resolution}</p>
      <p class="text-sm text-var(--text-muted) font-mono">Aspect Ratio: ${monitor.aspect_ratio.toFixed(2)}</p>
    </article>
  `;
}

function createWindowCard(win) {
  return `
    <article class="glass-card p-5 cursor-pointer select-text" tabindex="0" role="button" aria-label="Window ${win.window_name}" data-type="window" data-id="${win.window_id}">
      <h3 class="text-base font-semibold text-var(--text-primary) truncate" data-tooltip="${win.window_name}">${win.window_name}</h3>
      <p class="mt-1 text-xs text-var(--text-muted) font-mono">App: ${win.application}</p>
      <p class="text-xs text-var(--text-muted) font-mono">Resolution: ${win.resolution}</p>
      <p class="text-xs text-var(--text-muted) font-mono">Aspect Ratio: ${win.aspect_ratio.toFixed(2)}</p>
      <p class="text-xs mt-2 text-gray-400 font-mono truncate" data-tooltip="Window ID: ${win.window_id}">ID: ${win.window_id}</p>
    </article>
  `;
}

function onItemClick(type, id) {
    window.location.hash = `${type}-${id}`;
    const playerTab = document.getElementById('tab-player');
    playerTab.click(); // activate player tab

    const streamImg = document.getElementById('stream');
    const steam_overlay = document.getElementById('steam_overlay');
    const stream_message = steam_overlay.querySelector('p');
    if (id) {
        steam_overlay.classList.add('hidden');
        const steaming_url=`/stream?id=${id}&type=${type}`;

        streamImg.src = steaming_url;
        localStorage.setItem('streaming_url', steaming_url);
        
        streamImg.onerror = () => { 
            steam_overlay.classList.remove('hidden');
            stream_message.textContent = `Failed to load ${type} stream.`;
        };
    }
}

async function render() {
  try {
    // Fetch data and render monitors and windows
    const data = await fetchData();
    const monitorsEl = document.getElementById('monitors');
    const windowsEl = document.getElementById('windows');
    monitorsEl.innerHTML = data.monitors.map(createMonitorCard).join('');
    windowsEl.innerHTML = data.windows.map(createWindowCard).join('');

    // Add click and keyboard event listeners to each item
    [...monitorsEl.children, ...windowsEl.children].forEach(el => {
      el.addEventListener('click', () => onItemClick(el.dataset.type, el.dataset.id));
      el.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onItemClick(el.dataset.type, el.dataset.id);
        }
      });
    });
  } catch {
    // Handle errors gracefully
    document.getElementById('monitors').innerHTML = '<p class="text-red-600 font-semibold">Failed to load monitors.</p>';
    document.getElementById('windows').innerHTML = '<p class="text-red-600 font-semibold">Failed to load windows.</p>';
  }

    // Fullscreen toggle
    document.getElementById('fullscreenBtn').addEventListener('click', () => {
        const el = document.getElementById('stream_cn');
        if (!document.fullscreenElement) {
            el.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    });
}

// Initial render
render();
window.setInterval(render, 5000); // Refresh every 5 seconds