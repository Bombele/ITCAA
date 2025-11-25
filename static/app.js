// static/app.js
(function(){
  // Gestion du sélecteur de langue global
  const sel = document.getElementById('langSelect');
  if(sel){
    sel.addEventListener('change', () => {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', sel.value);
      window.location.href = url.toString();
    });
  }

  // Améliorations d’accessibilité: focus visible
  try {
    document.body.addEventListener('keyup', (e) => {
      if(e.key === 'Tab') document.body.classList.add('show-focus');
    });
  } catch {}
})();
