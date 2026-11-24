(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('pai-theme'); } catch (e) { /* storage blocked */ }
  if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;

  var button = document.getElementById('theme');
  if (!button) return;
  button.addEventListener('click', function () {
    var current = root.dataset.theme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = current === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('pai-theme', next); } catch (e) { /* ignore */ }
  });
})();
