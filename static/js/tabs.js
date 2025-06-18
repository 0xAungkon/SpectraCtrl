const tabs = document.querySelectorAll('#sidebar-tabs a');

const panels = {
  share: document.getElementById('share-panel'),
  player: document.getElementById('player-panel'),
  connections: document.getElementById('connections-panel'),
  about: document.getElementById('about-panel'),
};

function onTabClick(type = 'tab', id = null) {
  if(type === 'monitor' || type === 'window') {
    const playerTab = document.getElementById('tab-player');
    playerTab.click(); // activate player tab

    const streamImg = document.getElementById('stream');
    if (id) {
      streamImg.src = `/stream?id=${id}&type=${type}`;
      streamImg.onerror = () => { streamImg.src = '/static/images/error.jpg'; };
    }
  }
}


tabs.forEach(tab => {
  tab.addEventListener('click', e => {
    e.preventDefault();
    const selectedTab = tab.dataset.tab;
    tabs.forEach(t => {
      t.classList.toggle('active', t === tab);
      t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
      t.tabIndex = t === tab ? 0 : -1;
    });
    Object.entries(panels).forEach(([key, panel]) => {
      panel.hidden = key !== selectedTab;
    });
    window.location.hash = selectedTab;
    if(selectedTab != 'player') {
        const streamImg = document.getElementById('stream');
        streamImg.src = ''; // clear stream when switching tabs
    }
  });
});


window.addEventListener('DOMContentLoaded', () => {

  const hash = window.location.hash.slice(1);
  if (hash) {
    const targetTab = Array.from(tabs).find(t => t.dataset.tab === hash);
    if (targetTab) targetTab.click();
  }

  window.setTimeout(() => {
    document.querySelector('body').classList.remove('opacity-0');
  }, 100); // wait for DOM to settle
});
