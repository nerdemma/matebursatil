  // Fetch data from /shares/ and render table (maps API fields to UI)
    let currentCategory = 'ALL';
    let currentSearchQuery = '';
    const sharesBody = document.getElementById('shares-body');
    const statusDiv = document.getElementById('status');
    const searchInput = document.getElementById('searchInput');

    function formatNumber(num) {
      if (num === null || num === undefined || num === '') return '-';
      const n = Number(String(num).replace(/[^0-9\-,.]/g, '').replace(',', '.'));
      if (!isFinite(n)) return String(num);
      return new Intl.NumberFormat('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
    }

    function parseVariation(raw) {
      if (raw === null || raw === undefined) return NaN;
      const s = String(raw).replace('%', '').replace(',', '.').replace('+', '').trim();
      return parseFloat(s);
    }

    function renderRowsFromItems(items) {
      const filtered = items.filter(item => {
        const matchesCategory = currentCategory === 'ALL' || (String(item.category || '').toUpperCase() === currentCategory);
        const q = currentSearchQuery.trim().toLowerCase();
        const matchesSearch = !q || (String(item.ticker || item.ticker).toLowerCase().includes(q)) || (String(item.nombre || item.name || '').toLowerCase().includes(q));
        return matchesCategory && matchesSearch;
      });

      if (!filtered.length) {
        sharesBody.innerHTML = '';
        statusDiv.style.display = 'block';
        statusDiv.innerText = 'No se encontraron resultados para los filtros seleccionados.';
        return;
      }

      statusDiv.style.display = 'none';

      sharesBody.innerHTML = filtered.map(item => {
        const ticker = item.ticker || '-';
        const name = item.nombre || item.name || '-';
        const priceRaw = item.cotizacion ?? item.precio_cierre ?? item.price ?? '-';
        const openRaw = item.precio_apertura ?? item.open ?? '-';
        const lowRaw = item.baja ?? item.low ?? '-';
        const highRaw = item.alta ?? item.high ?? '-';
        const volume = item.volumen ?? item.volume ?? '-';
        const variationRaw = item.variacion ?? item.variacion_pct ?? item.change ?? '0';

        const variationNum = parseVariation(variationRaw);
        const isPositive = isNaN(variationNum) ? true : variationNum >= 0;
        const changeSign = isPositive ? '+' : '';
        const badgeBg = isPositive ? 'bg-mateGreen-bg text-mateGreen' : 'bg-red-500/10 text-red-500';

        return `
          <tr class="tr-hover text-sm">
            <td class="py-4 px-5">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs" style="background-color: var(--badge-bg); color: var(--text-heading); border: 1px solid var(--border-color)">
                  ${String(ticker).substring(0,3)}
                </div>
                <div>
                  <div class="font-bold tracking-tight" style="color: var(--text-heading)">${ticker}</div>
                  <div class="text-xs truncate max-w-[160px] sm:max-w-[220px]" style="color: var(--text-muted)">${name}</div>
                </div>
              </div>
            </td>
            <td class="py-4 px-4 text-right font-bold" style="color: var(--text-heading)">$${formatNumber(priceRaw)}</td>
            <td class="py-4 px-4 text-right"><span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs ${badgeBg}">${changeSign}${isNaN(variationNum) ? String(variationRaw) : variationNum.toFixed(2)}%</span></td>
            <td class="py-4 px-4 text-right hidden sm:table-cell" style="color: var(--text-muted)">$${formatNumber(openRaw)}</td>
            <td class="py-4 px-4 text-right hidden md:table-cell" style="color: var(--text-muted)">$${formatNumber(lowRaw)}</td>
            <td class="py-4 px-4 text-right hidden md:table-cell" style="color: var(--text-muted)">$${formatNumber(highRaw)}</td>
            <td class="py-4 px-4 text-right hidden lg:table-cell font-mono text-xs" style="color: var(--text-muted)">${volume}</td>
            </tr>
        `;
      }).join('');
    }

    async function loadShares() {
      try {
        const q = encodeURIComponent(currentSearchQuery || '');
        const url = q ? `/shares/?q=${q}` : '/shares/';
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('API error');
        const payload = await resp.json();
        const items = payload.items || [];

        // update KPIs if meta exists
        if (payload.meta) {
          const totalEl = document.getElementById('totalCount');
          const updatedEl = document.getElementById('updatedAt');
          if (totalEl) totalEl.textContent = String(payload.meta.totalCount || items.length);
          if (updatedEl && payload.meta.last_updated) updatedEl.textContent = new Date(payload.meta.last_updated).toLocaleString('es-AR');
        }

        renderRowsFromItems(items);
      } catch (err) {
        console.error(err);
        statusDiv.textContent = 'Error al cargar la API de cotizaciones.';
      }
    }

    // Wire search input
    let searchTimeout = null;
    if (searchInput) searchInput.addEventListener('input', (e) => {
      currentSearchQuery = e.target.value;
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(loadShares, 250);
    });

    // Wire filter tabs
    document.querySelectorAll('.filter-tab').forEach(tab => tab.addEventListener('click', (e) => {
      document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('bg-mateGreen', 'text-white', 'shadow-sm'));
      const btn = e.currentTarget;
      btn.classList.add('bg-mateGreen', 'text-white', 'shadow-sm');
      currentCategory = btn.getAttribute('data-category') || 'ALL';
      loadShares();
    }));

    // initial load + periodic refresh
    loadShares();
    setInterval(loadShares, 600000);
  