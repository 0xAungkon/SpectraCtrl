const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const iconPath = document.getElementById('iconPath');
const themeLabel = document.getElementById('themeLabel');
const root = document.documentElement;

function setTheme(mode) {
  if (mode === 'dark') {
    root.style.setProperty('--bg', '#111827');
    root.style.setProperty('--bg-semi', '#1f2937');
    root.style.setProperty('--text-primary', '#f9fafb');
    root.style.setProperty('--text-muted', '#9ca3af');
    root.style.setProperty('--border', '#374151');
    iconPath.setAttribute('d', 'M21.75 15.5A9 9 0 1112.5 2.25 7.5 7.5 0 0021.75 15.5z');
    themeLabel.textContent = 'Dark';
  } else {
    root.style.setProperty('--bg', '#ffffff');
    root.style.setProperty('--bg-semi', '#f9fafb');
    root.style.setProperty('--text-primary', '#111827');
    root.style.setProperty('--text-muted', '#6b7280');
    root.style.setProperty('--border', '#e5e7eb');
    iconPath.setAttribute('d', 'M12 3v1m0 16v1m8.66-12.66l-.71.71M4.05 19.95l-.71.71M21 12h1M2 12H1m16.24 5.66l-.71-.71M5.66 5.66l-.71-.71M12 6a6 6 0 100 12 6 6 0 000-12z');
    themeLabel.textContent = 'Light';
  }
  localStorage.setItem('theme', mode);
}

themeToggle.addEventListener('click', () => {
  const current = localStorage.getItem('theme') === 'dark' ? 'light' : 'dark';
  setTheme(current);
});

const storedTheme = localStorage.getItem('theme') || 'light';
setTheme(storedTheme);
