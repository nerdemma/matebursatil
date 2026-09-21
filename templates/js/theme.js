  // Theme toggle: restore previous behavior
    (function() {
      const htmlTag = document.documentElement;
      const themeToggleBtn = document.getElementById('themeToggleBtn');
      const sunIcon = document.getElementById('sunIcon');
      const moonIcon = document.getElementById('moonIcon');

      function applyTheme(theme) {
        htmlTag.setAttribute('data-theme', theme);
        if (sunIcon) sunIcon.classList.toggle('hidden', theme !== 'dark');
        if (moonIcon) moonIcon.classList.toggle('hidden', theme !== 'light');
        try { localStorage.setItem('mate_bursatil_theme', theme); } catch(e) {}
      }

      const saved = (function(){
        try { return localStorage.getItem('mate_bursatil_theme'); } catch(e) { return null; }
      })();
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initial = saved || (prefersDark ? 'dark' : 'light');
      applyTheme(initial);

      if (themeToggleBtn) themeToggleBtn.addEventListener('click', () => {
        const current = htmlTag.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
      });
    })();
  