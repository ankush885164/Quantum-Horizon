
    // Master Holdings Data
    const HOLDINGS = [
      {
        symbol: "NVDA",
        name: "NVIDIA Corporation",
        sector: "Technology",
        market: "US",
        price: 128.40,
        shares: 8500,
        cost: 88.20,
        dayPl: +44450.00,
        dayReturn: +4.25,
        sma20: 121.15,
        sma50: 114.80,
        rsi: 64.2,
        vol: 18.4,
        color: "#00f0ff"
      },
      {
        symbol: "RELIANCE.NS",
        name: "Reliance Industries Ltd",
        sector: "Energy",
        market: "NSE",
        price: 1360.20,
        shares: 125000,
        cost: 1180.50,
        dayPl: +328000.00,
        dayReturn: +2.14,
        sma20: 1320.40,
        sma50: 1280.10,
        rsi: 58.7,
        vol: 14.1,
        color: "#ffd166"
      },
      {
        symbol: "MSFT",
        name: "Microsoft Corporation",
        sector: "Technology",
        market: "US",
        price: 448.20,
        shares: 7200,
        cost: 382.50,
        dayPl: +57600.00,
        dayReturn: +1.82,
        sma20: 440.10,
        sma50: 431.50,
        rsi: 61.0,
        vol: 12.8,
        color: "#38bdf8"
      },
      {
        symbol: "TCS.NS",
        name: "Tata Consultancy Services",
        sector: "Technology",
        market: "NSE",
        price: 2349.40,
        shares: 85000,
        cost: 2150.00,
        dayPl: +142000.00,
        dayReturn: +0.84,
        sma20: 2310.20,
        sma50: 2280.00,
        rsi: 54.5,
        vol: 11.9,
        color: "#818cf8"
      },
      {
        symbol: "AAPL",
        name: "Apple Inc.",
        sector: "Technology",
        market: "US",
        price: 224.50,
        shares: 12000,
        cost: 175.40,
        dayPl: +30600.00,
        dayReturn: +1.15,
        sma20: 220.80,
        sma50: 215.20,
        rsi: 59.2,
        vol: 13.5,
        color: "#c084fc"
      },
      {
        symbol: "HDFCBANK.NS",
        name: "HDFC Bank Ltd",
        sector: "Financials",
        market: "NSE",
        price: 1742.60,
        shares: 190000,
        cost: 1540.20,
        dayPl: +420000.00,
        dayReturn: +1.45,
        sma20: 1710.00,
        sma50: 1675.00,
        rsi: 57.8,
        vol: 13.9,
        color: "#00f0ff"
      },
      {
        symbol: "BTC-USD",
        name: "Bitcoin Core Treasury",
        sector: "Financials",
        market: "CRYPTO",
        price: 63240.00,
        shares: 45.0,
        cost: 51200.00,
        dayPl: +88200.00,
        dayReturn: +3.15,
        sma20: 61200.00,
        sma50: 58400.00,
        rsi: 66.4,
        vol: 28.5,
        color: "#f59e0b"
      },
      {
        symbol: "ASML",
        name: "ASML Holding NV",
        sector: "Semiconductors",
        market: "US",
        price: 920.00,
        shares: 1500,
        cost: 690.00,
        dayPl: -6250.00,
        dayReturn: -0.45,
        sma20: 935.00,
        sma50: 915.00,
        rsi: 48.2,
        vol: 21.0,
        color: "#f43f5e"
      }
    ];

    let activeSymbol = "NVDA";
    let activeCurrency = "USD";
    const FX_RATES = { "USD": 1.0, "INR": 84.42, "EUR": 0.92, "GBP": 0.79 };
    const FX_SYMS = { "USD": "$", "INR": "₹", "EUR": "€", "GBP": "£" };

    let isFiltersOpen = true;
    let liveSimulationInterval = null;

    let pbiChart = null;
    let pbiDonut = null;
    let techBenchmarkChart = null;
    let rsiBarChart = null;
    let volBarChart = null;

    // Toast Utility
    function triggerPBIToast(title, message) {
      const container = document.getElementById("pbi-toast-container");
      const toast = document.createElement("div");
      toast.className = "pointer-events-auto flex items-center gap-2.5 p-3 rounded-lg bg-pbi-surface border border-pbi-accent text-white shadow-xl max-w-xs text-xs";
      toast.innerHTML = `
        <div class="w-6 h-6 rounded bg-[#f2c811] text-black font-bold flex items-center justify-center shrink-0 text-[10px]">PBI</div>
        <div class="flex flex-col">
          <span class="font-bold text-white">${title}</span>
          <span class="text-[10px] text-[#94a3b8]">${message}</span>
        </div>
      `;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 250);
      }, 3500);
    }

    // Toggle Filters Pane
    function toggleFiltersPane() {
      const pane = document.getElementById("filters-pane");
      const toggleText = document.getElementById("filters-toggle-text");
      isFiltersOpen = !isFiltersOpen;

      if (isFiltersOpen) {
        pane.style.display = "flex";
        pane.style.width = "16rem";
        toggleText.innerText = "Filters (4)";
        triggerPBIToast("Filters Pane", "Opened Filter Drawer.");
      } else {
        pane.style.display = "none";
        toggleText.innerText = "Show Filters";
        triggerPBIToast("Filters Pane", "Collapsed. Maximum Canvas Enabled.");
      }
    }

    // Generate Dynamic Historical Series for any asset
    function generateStockHistory(symbol, basePrice, days=60) {
      const labels = [];
      const prices = [];
      const sma20 = [];
      const sma50 = [];
      const bUpper = [];
      const bLower = [];
      const volumes = [];

      let cur = basePrice * 0.88;
      const today = new Date();

      for (let i = days; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(today.getDate() - i);
        labels.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));

        const noise = (Math.sin(i * 0.3) * 0.015) + (Math.cos(i * 0.1) * 0.01) + 0.002;
        cur = cur * (1 + noise);
        if (i === 0) cur = basePrice; // anchor to exact live price
        prices.push(parseFloat(cur.toFixed(2)));

        // Volume
        volumes.push(Math.round(800000 + Math.random() * 2500000));
      }

      // Calculate SMAs
      for (let i = 0; i < prices.length; i++) {
        // SMA 20
        if (i >= 19) {
          const slice20 = prices.slice(i - 19, i + 1);
          const avg20 = slice20.reduce((a, b) => a + b, 0) / 20;
          sma20.push(parseFloat(avg20.toFixed(2)));
          // Bollinger Bands
          const std = Math.sqrt(slice20.map(x => Math.pow(x - avg20, 2)).reduce((a, b) => a + b) / 20);
          bUpper.push(parseFloat((avg20 + 2 * std).toFixed(2)));
          bLower.push(parseFloat((avg20 - 2 * std).toFixed(2)));
        } else {
          sma20.push(prices[i]);
          bUpper.push(prices[i] * 1.04);
          bLower.push(prices[i] * 0.96);
        }

        // SMA 50
        if (i >= 49) {
          const slice50 = prices.slice(i - 49, i + 1);
          sma50.push(parseFloat((slice50.reduce((a, b) => a + b, 0) / 50).toFixed(2)));
        } else {
          sma50.push(prices[Math.max(0, i - 5)]);
        }
      }

      return { labels, prices, sma20, sma50, bUpper, bLower, volumes };
    }

    // Initialize Main Chart.js Visual
    function initMainChart() {
      const ctx = document.getElementById('pbiChartCanvas').getContext('2d');
      const hist = generateStockHistory(activeSymbol, HOLDINGS.find(h => h.symbol === activeSymbol).price, 60);

      pbiChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: hist.labels,
          datasets: [
            {
              label: 'Close Price',
              data: hist.prices,
              borderColor: '#00f0ff',
              borderWidth: 2.5,
              backgroundColor: 'rgba(0, 240, 255, 0.12)',
              fill: true,
              tension: 0.25,
              yAxisID: 'y'
            },
            {
              label: '20-Day SMA',
              data: hist.sma20,
              borderColor: '#fbbf24',
              borderWidth: 2,
              borderDash: [4, 2],
              pointRadius: 0,
              fill: false,
              tension: 0.2,
              yAxisID: 'y'
            },
            {
              label: '50-Day SMA',
              data: hist.sma50,
              borderColor: '#ec4899',
              borderWidth: 1.8,
              borderDash: [5, 3],
              pointRadius: 0,
              fill: false,
              tension: 0.2,
              yAxisID: 'y'
            },
            {
              label: 'Bollinger Upper',
              data: hist.bUpper,
              borderColor: 'rgba(192, 132, 252, 0.45)',
              borderWidth: 1,
              pointRadius: 0,
              fill: false,
              hidden: true,
              yAxisID: 'y'
            },
            {
              label: 'Bollinger Lower',
              data: hist.bLower,
              borderColor: 'rgba(192, 132, 252, 0.45)',
              borderWidth: 1,
              pointRadius: 0,
              fill: false,
              hidden: true,
              yAxisID: 'y'
            },
            {
              type: 'bar',
              label: 'Trading Volume',
              data: hist.volumes,
              backgroundColor: 'rgba(99, 102, 241, 0.35)',
              borderRadius: 2,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(10, 14, 28, 0.95)',
              titleColor: '#00f0ff',
              bodyColor: '#e6fffa',
              borderColor: 'rgba(129, 140, 248, 0.3)',
              borderWidth: 1,
              padding: 10,
              titleFont: { family: 'JetBrains Mono', size: 12 },
              bodyFont: { family: 'JetBrains Mono', size: 11 },
              callbacks: {
                label: function(context) {
                  const sym = FX_SYMS[activeCurrency];
                  const label = context.dataset.label || '';
                  if (label === 'Trading Volume') {
                    return ` Volume: ${(context.raw / 1000000).toFixed(2)}M`;
                  }
                  return ` ${label}: ${sym}${context.raw.toLocaleString()}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(129, 140, 248, 0.12)' },
              ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8 }
            },
            y: {
              type: 'linear',
              position: 'left',
              grid: { color: 'rgba(129, 140, 248, 0.12)' },
              ticks: {
                color: '#94a3b8',
                font: { family: 'JetBrains Mono', size: 10 },
                callback: v => FX_SYMS[activeCurrency] + v.toLocaleString()
              }
            },
            y1: {
              type: 'linear',
              position: 'right',
              grid: { display: false },
              ticks: { display: false },
              max: Math.max(...hist.volumes) * 3
            }
          }
        }
      });
    }

    // Initialize Donut Chart
    function initDonutChart() {
      const ctx = document.getElementById('pbiDonutCanvas').getContext('2d');
      pbiDonut = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Technology & AI', 'Financial Services', 'Energy & Refining', 'Semiconductors'],
          datasets: [{
            data: [42.0, 24.0, 18.0, 16.0],
            backgroundColor: ['#818cf8', '#00f0ff', '#fbbf24', '#ec4899'],
            borderColor: '#0e142c',
            borderWidth: 3,
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(10, 14, 28, 0.95)',
              titleColor: '#00f0ff',
              bodyColor: '#fff',
              borderColor: 'rgba(129, 140, 248, 0.3)',
              borderWidth: 1,
              callbacks: {
                label: ctx => ` ${ctx.label}: ${ctx.raw}% Allocation`
              }
            }
          },
          onClick: (evt, activeElements) => {
            if (activeElements.length > 0) {
              const idx = activeElements[0].index;
              const sectors = ['Technology', 'Financials', 'Energy', 'Semiconductors'];
              filterBySector(sectors[idx]);
            }
          }
        }
      });
    }

    // Update Main Visual when selecting a holding
    function focusOnHolding(symbol) {
      activeSymbol = symbol;
      const h = HOLDINGS.find(item => item.symbol === symbol);
      if (!h) return;

      document.getElementById('slicer-symbol').value = symbol;
      document.getElementById('main-chart-title').innerText = `Interactive Trajectory: ${h.symbol} (${h.name})`;
      document.getElementById('active-focus-label').innerText = `${h.symbol} • ${h.name.toUpperCase()}`;

      // Update Chart Data
      const hist = generateStockHistory(h.symbol, h.price, 60);
      pbiChart.data.labels = hist.labels;
      pbiChart.data.datasets[0].data = hist.prices;
      pbiChart.data.datasets[0].borderColor = h.color;
      pbiChart.data.datasets[1].data = hist.sma20;
      pbiChart.data.datasets[2].data = hist.sma50;
      pbiChart.data.datasets[3].data = hist.bUpper;
      pbiChart.data.datasets[4].data = hist.bLower;
      pbiChart.data.datasets[5].data = hist.volumes;
      pbiChart.update();

      // Update Bottom Telemetry
      const sym = FX_SYMS[activeCurrency];
      document.getElementById('tele-price').innerText = `${sym}${h.price.toFixed(2)}`;
      document.getElementById('tele-sma20').innerText = `${sym}${h.sma20.toFixed(2)}`;
      document.getElementById('tele-sma50').innerText = `${sym}${h.sma50.toFixed(2)}`;
      document.getElementById('tele-signal').innerText = h.sma20 > h.sma50 ? "Bullish (SMA20 > SMA50)" : "Bearish Momentum";
      document.getElementById('tele-signal').style.color = h.sma20 > h.sma50 ? "var(--tw-colors-pbi-accent, #00ff9d)" : "var(--tw-colors-pbi-rose, #ff4d6d)";

      // Highlight Table Row
      renderMatrixTable();

      triggerPBIToast("Focus Updated", `Visuals sliced to ${h.symbol} (${h.name}).`);
    }

    // Toggle Technical Overlays
    function toggleChartDataset(index, isVisible) {
      if (pbiChart) {
        pbiChart.data.datasets[index].hidden = !isVisible;
        pbiChart.update();
      }
    }

    function toggleBollingerBands(isVisible) {
      if (pbiChart) {
        pbiChart.data.datasets[3].hidden = !isVisible;
        pbiChart.data.datasets[4].hidden = !isVisible;
        pbiChart.update();
        triggerPBIToast("Bollinger Bands", isVisible ? "Displayed on Chart." : "Hidden.");
      }
    }

    // Timeframe Slicing
    function onTimeframeChange(period, btn) {
      document.querySelectorAll('#timeframe-group button').forEach(b => {
        b.className = "px-2 py-0.5 rounded text-[10px] text-[#94a3b8] hover:text-white";
      });
      btn.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-pbi-accent text-black shadow-sm";

      let days = 60;
      if (period === '1M') days = 22;
      else if (period === '3M') days = 65;
      else if (period === '1Y') days = 250;
      else if (period === 'ALL') days = 360;

      const h = HOLDINGS.find(item => item.symbol === activeSymbol) || HOLDINGS[0];
      const hist = generateStockHistory(h.symbol, h.price, days);

      pbiChart.data.labels = hist.labels;
      pbiChart.data.datasets[0].data = hist.prices;
      pbiChart.data.datasets[1].data = hist.sma20;
      pbiChart.data.datasets[2].data = hist.sma50;
      pbiChart.data.datasets[3].data = hist.bUpper;
      pbiChart.data.datasets[4].data = hist.bLower;
      pbiChart.data.datasets[5].data = hist.volumes;
      pbiChart.update();

      triggerPBIToast("Time Window Sliced", `Evaluated historical measures for ${period} window.`);
    }

    // Render Matrix Table
    function renderMatrixTable() {
      const tbody = document.getElementById('matrix-tbody');
      const sym = FX_SYMS[activeCurrency];

      tbody.innerHTML = HOLDINGS.map(h => {
        const isSelected = h.symbol === activeSymbol;
        const totalVal = h.shares * h.price;
        const posClass = h.dayReturn >= 0 ? 'data-bar-pos text-pbi-accent' : 'data-bar-neg text-pbi-rose';
        const crossBadge = h.sma20 > h.sma50 
          ? '<span class="px-1.5 py-0.2 rounded bg-pbi-accent/15 text-pbi-accent text-[9px] font-bold">Bullish Cross</span>' 
          : '<span class="px-1.5 py-0.2 rounded bg-pbi-rose/15 text-pbi-rose text-[9px] font-bold">Bearish</span>';

        return `
          <tr class="hover:bg-pbi-surface/80 transition-colors cursor-pointer ${isSelected ? 'pbi-active-row' : ''}" onclick="focusOnHolding('${h.symbol}')">
            <td class="py-2 px-2.5 font-bold" style="color:${h.color};">${h.symbol}</td>
            <td class="py-2 px-2.5 font-sans font-semibold text-white">${h.name}</td>
            <td class="py-2 px-2.5 text-[#94a3b8]">${h.sector}</td>
            <td class="py-2 px-2.5 text-right font-bold text-white">${sym}${h.price.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-right">
              <div class="${posClass} px-1.5 py-0.2 inline-block font-bold">
                ${h.dayReturn >= 0 ? '+' : ''}${h.dayReturn.toFixed(2)}%
              </div>
            </td>
            <td class="py-2 px-2.5 text-right text-pbi-gold">${sym}${h.sma20.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-right text-pbi-cyan">${sym}${h.sma50.toFixed(2)}</td>
            <td class="py-2 px-2.5 text-center text-white font-bold">${h.rsi.toFixed(1)}</td>
            <td class="py-2 px-2.5 text-center">${crossBadge}</td>
            <td class="py-2 px-2.5 text-center">
              <button onclick="event.stopPropagation(); focusOnHolding('${h.symbol}');" class="px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-accent hover:text-black text-pbi-mint font-bold text-[10px] border border-pbi-border transition-all">
                Select
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    // Slicer Handlers
    function onSymbolSlicerChange(val) {
      if (val === 'ALL') {
        activeSymbol = "NVDA";
        focusOnHolding("NVDA");
        document.getElementById('active-focus-label').innerText = "ALL CORE ASSETS (8)";
      } else {
        focusOnHolding(val);
      }
    }

    function onMarketSlicerChange(val) {
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const sym = r.querySelector('td').innerText.trim();
        const h = HOLDINGS.find(item => item.symbol === sym);
        if (val === 'ALL' || h.market === val) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings`;
      triggerPBIToast("Market Sliced", `Filtered to ${val} market segment.`);
    }

    function filterBySector(sec) {
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const sym = r.querySelector('td').innerText.trim();
        const h = HOLDINGS.find(item => item.symbol === sym);
        if (h.sector === sec) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings (${sec})`;
      const firstInSec = HOLDINGS.find(h => h.sector === sec);
      if (firstInSec) focusOnHolding(firstInSec.symbol);
      triggerPBIToast("Sector Sliced", `Filtered to ${sec}.`);
    }

    function filterMatrix() {
      const q = document.getElementById('matrix-search').value.toLowerCase().trim();
      const rows = document.querySelectorAll('#matrix-tbody tr');
      let count = 0;
      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        if (!q || text.includes(q)) {
          r.style.display = '';
          count++;
        } else {
          r.style.display = 'none';
        }
      });
      document.getElementById('matrix-count-badge').innerText = `${count} Holdings`;
    }

    function resetAllSelections() {
      document.getElementById('slicer-symbol').value = 'ALL';
      document.getElementById('slicer-market').value = 'ALL';
      document.getElementById('matrix-search').value = '';
      const rows = document.querySelectorAll('#matrix-tbody tr');
      rows.forEach(r => r.style.display = '');
      document.getElementById('matrix-count-badge').innerText = `8 Core Holdings`;
      focusOnHolding('NVDA');
      document.getElementById('active-focus-label').innerText = "ALL CORE ASSETS (8)";
      triggerPBIToast("Reset Complete", "All visual selections cleared.");
    }

    function setCurrency(curr) {
      activeCurrency = curr;
      ['USD', 'INR', 'EUR', 'GBP'].forEach(c => {
        const b = document.getElementById(`btn-curr-${c}`);
        if (c === curr) b.className = "px-2 py-0.5 rounded bg-pbi-accent text-black font-bold";
        else b.className = "px-2 py-0.5 rounded text-[#94a3b8] hover:text-white";
      });

      const sym = FX_SYMS[curr];
      const rate = FX_RATES[curr];
      document.getElementById('kpi-nav-val').innerText = `${sym}${(14842920.45 * rate).toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      document.getElementById('kpi-gain-val').innerText = `+${sym}${(3210480.00 * rate).toLocaleString('en-US', {maximumFractionDigits: 2})}`;
      renderMatrixTable();
      focusOnHolding(activeSymbol);
      triggerPBIToast("Currency Converted", `${curr} (${sym})`);
    }

    // Report Tab Switcher
    function switchReportTab(tabId) {
      ['exec', 'tech', 'risk'].forEach(t => {
        document.getElementById(`page-${t}`).classList.add('hidden');
        const btn = document.getElementById(`tab-btn-${t}`);
        btn.className = "px-3 py-1 rounded-t text-[#94a3b8] hover:text-white flex items-center gap-1 transition-colors cursor-pointer";
      });

      document.getElementById(`page-${tabId}`).classList.remove('hidden');
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      activeBtn.className = "px-3 py-1 rounded-t bg-pbi-surface text-pbi-gold font-bold flex items-center gap-1 border-t-2 border-t-pbi-gold cursor-pointer";

      const pageNames = { 'exec': 'Page 1 of 3 (Executive)', 'tech': 'Page 2 of 3 (Technicals)', 'risk': 'Page 3 of 3 (Risk & DAX)' };
      document.getElementById('page-counter').innerText = pageNames[tabId];

      if (tabId === 'tech' && !techBenchmarkChart) initTechPageCharts();
      triggerPBIToast("Tab Switched", activeBtn.innerText.trim());
    }

    // Page 2: Technicals Charts
    function initTechPageCharts() {
      // Comparison Benchmark
      const ctx1 = document.getElementById('techBenchmarkCanvas').getContext('2d');
      const dates = Array.from({length: 30}, (_, i) => `Day ${i+1}`);
      techBenchmarkChart = new Chart(ctx1, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            { label: 'NVDA', data: dates.map((_, i) => 100 + i * 1.5 + Math.sin(i) * 3), borderColor: '#00f0ff', tension: 0.2 },
            { label: 'BTC-USD', data: dates.map((_, i) => 100 + i * 0.8 + Math.cos(i) * 5), borderColor: '#c084fc', tension: 0.2 },
            { label: 'RELIANCE.NS', data: dates.map((_, i) => 100 + i * 0.5 + Math.sin(i * 0.5) * 2), borderColor: '#ffd166', tension: 0.2 },
            { label: 'S&P 500 Benchmark', data: dates.map((_, i) => 100 + i * 0.3), borderColor: '#ec4899', borderDash: [4, 4], tension: 0.2 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } } } },
          scales: {
            x: { grid: { color: 'rgba(22, 50, 58, 0.4)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(22, 50, 58, 0.4)' }, ticks: { color: '#94a3b8', callback: v => v + '%' } }
          }
        }
      });

      // RSI Horizontal Bar Chart
      const ctx2 = document.getElementById('rsiBarCanvas').getContext('2d');
      rsiBarChart = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: HOLDINGS.map(h => h.symbol),
          datasets: [{
            label: 'RSI (14)',
            data: HOLDINGS.map(h => h.rsi),
            backgroundColor: HOLDINGS.map(h => h.rsi >= 70 ? '#ff4d6d' : (h.rsi <= 30 ? '#00f5d4' : '#00ff9d')),
            borderRadius: 3
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: 'rgba(22, 50, 58, 0.4)' } },
            y: { ticks: { color: '#fff', font: { family: 'JetBrains Mono', size: 10 } } }
          }
        }
      });

      // Volatility Bar Chart
      const ctx3 = document.getElementById('volBarCanvas').getContext('2d');
      volBarChart = new Chart(ctx3, {
        type: 'bar',
        data: {
          labels: HOLDINGS.map(h => h.symbol),
          datasets: [{
            label: '30D Vol %',
            data: HOLDINGS.map(h => h.vol),
            backgroundColor: '#38bdf8',
            borderRadius: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#fff', font: { family: 'JetBrains Mono', size: 9 } } },
            y: { ticks: { color: '#94a3b8', callback: v => v + '%' }, grid: { color: 'rgba(22, 50, 58, 0.4)' } }
          }
        }
      });
    }

    // Page 3: DAX Evaluator
    const DAX_CATALOG = {
      "SHARPE": {
        output: "2.41 (Annualized Sharpe Ratio)",
        formula: "DIVIDE([Portfolio Unrealized ROI %] / 100 - 0.0425, [Realized Volatility 30D] / 100, 2.41)",
        code: `// Power BI DAX Definition\n[Sharpe Ratio] = \nVAR RiskFreeRate = 0.0425\nVAR AnnualReturn = [Portfolio Unrealized ROI %] / 100\nVAR AnnualVol = [Realized Volatility 30D] / 100\nRETURN\n    DIVIDE(AnnualReturn - RiskFreeRate, AnnualVol, 2.41)`
      },
      "GOLDEN_CROSS": {
        output: "Bullish Cross Signal (SMA 20 > SMA 50 across 7 of 8 holdings)",
        formula: "IF([SMA 20] > [SMA 50], "Bullish Golden Cross", "Bearish Death Cross")",
        code: `// Power BI DAX Definition\n[MA Cross Signal] = \nVAR Sma20Val = [SMA 20]\nVAR Sma50Val = [SMA 50]\nRETURN\n    IF(ISBLANK(Sma20Val) || ISBLANK(Sma50Val), "Neutral",\n       IF(Sma20Val > Sma50Val, "Bullish Golden Cross", "Bearish Cross"))`
      },
      "UNREALIZED_ROI": {
        output: "+27.64% (Portfolio Total Inception Return)",
        formula: "DIVIDE([Total Unrealized Gain], [Total Portfolio Value] - [Total Unrealized Gain], 0) * 100",
        code: `// Power BI DAX Definition\n[Portfolio Unrealized ROI %] = \nVAR Gains = SUM(Fact_PortfolioPositions[unrealized_gain])\nVAR Cost = SUM(Fact_PortfolioPositions[total_value]) - Gains\nRETURN\n    DIVIDE(Gains, Cost, 0) * 100`
      },
      "BETA": {
        output: "0.94 (Systematic Beta vs S&P 500 Index)",
        formula: "DIVIDE(COVARIANCE.S(Fact_StockAnalytics[return], Benchmark[return]), VARIANCE.S(Benchmark[return]))",
        code: `// Power BI DAX Definition\n[Portfolio Beta] = \nVAR Covar = COVARIANCE.S(Fact_StockAnalytics[daily_return_pct], Benchmark_SPX[daily_return_pct])\nVAR BenchVar = VARIANCE.S(Benchmark_SPX[daily_return_pct])\nRETURN\n    DIVIDE(Covar, BenchVar, 0.94)`
      },
      "VAR_95": {
        output: "$240,000.00 (95% 1-Day Maximum Value at Risk)",
        formula: "[Total Portfolio Value] * 1.645 * ([Realized Volatility 30D] / SQRT(252))",
        code: `// Power BI DAX Definition\n[Value at Risk 95%] = \nVAR ZScore = 1.645\nVAR DailyVol = [Realized Volatility 30D] / SQRT(252)\nRETURN\n    [Total Portfolio Value] * ZScore * DailyVol`
      }
    };

    function runDAXEvaluation() {
      const key = document.getElementById('dax-selector').value;
      const data = DAX_CATALOG[key];
      if (data) {
        document.getElementById('dax-eval-output').innerText = data.output;
        document.getElementById('dax-eval-formula').innerText = `Formula: ${data.formula}`;
        document.getElementById('dax-code-preview').innerText = data.code;
        document.getElementById('dax-eval-time').innerText = `Evaluated in ${(Math.random() * 0.8 + 0.3).toFixed(1)}ms`;
        triggerPBIToast("DAX Query Executed", `Computed ${key} measure.`);
      }
    }

    // Stress Testing
    function onStressShock(val) {
      const pct = parseFloat(val);
      document.getElementById('shock-display').innerText = `Market Shock: ${pct >= 0 ? '+' : ''}${pct}%`;
      const baseNav = 14842920.45;
      const nextNav = baseNav * (1 + (pct * 0.94 / 100));
      const impact = nextNav - baseNav;

      document.getElementById('stress-nav').innerText = `$${(nextNav / 1000000).toFixed(2)}M`;
      document.getElementById('stress-impact').innerText = `${impact >= 0 ? '+' : ''}$${(impact / 1000).toFixed(1)}K (${pct}%)`;
      document.getElementById('stress-impact').style.color = impact >= 0 ? '#00ff9d' : '#ff4d6d';
      document.getElementById('stress-status').innerText = pct <= -15 ? 'Capital Buffer Alert' : 'Nominal Tier-1';
      document.getElementById('stress-status').style.color = pct <= -15 ? '#ffd166' : '#00ff9d';
    }

    // Live Streaming Simulation Toggle
    function toggleLiveSimulation() {
      const btn = document.getElementById('btn-live-toggle');
      const icon = document.getElementById('live-icon');
      const text = document.getElementById('live-text');
      const status = document.getElementById('sync-status');

      if (!liveSimulationInterval) {
        // Start Live Streaming Ticks
        liveSimulationInterval = setInterval(() => {
          // Jiggle prices slightly
          HOLDINGS.forEach(h => {
            const delta = (Math.random() * 0.6 - 0.28);
            h.price = Math.max(10, h.price + delta);
            h.dayReturn += (delta * 0.05);
          });
          focusOnHolding(activeSymbol);
          status.innerText = `Tick: ${new Date().toLocaleTimeString()}`;
        }, 3000);

        icon.innerText = "pause";
        text.innerText = "Live Ticks: ON";
        btn.className = "px-2 py-0.5 rounded bg-pbi-accent text-black font-bold text-[11px] font-mono flex items-center gap-1 shadow-sm";
        triggerPBIToast("Live Streaming Active", "Streaming simulated DirectQuery market ticks every 3s.");
      } else {
        // Stop Live Ticks
        clearInterval(liveSimulationInterval);
        liveSimulationInterval = null;
        icon.innerText = "play_arrow";
        text.innerText = "Live Ticks: Off";
        btn.className = "px-2 py-0.5 rounded bg-pbi-surface hover:bg-pbi-card border border-pbi-border text-[11px] font-mono text-pbi-accent flex items-center gap-1";
        status.innerText = "DirectQuery Paused";
        triggerPBIToast("Streaming Paused", "DirectQuery sync paused.");
      }
    }

    function refreshDataModel() {
      const icon = document.getElementById('refresh-icon');
      icon.classList.add('animate-spin');
      setTimeout(() => {
        icon.classList.remove('animate-spin');
        focusOnHolding(activeSymbol);
        triggerPBIToast("Data Refreshed", "Re-queried Databricks Delta Gold layers.");
      }, 600);
    }

    function exportFilteredData() {
      const csvContent = "data:text/csv;charset=utf-8,Symbol,Name,Sector,Market,Price,SharesHeld,CostBasis,DayReturnPct,SMA20,SMA50,RSI\n" +
        HOLDINGS.map(h => `${h.symbol},${h.name},${h.sector},${h.market},${h.price},${h.shares},${h.cost},${h.dayReturn},${h.sma20},${h.sma50},${h.rsi}`).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "PowerBI_Export_Holdings.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      triggerPBIToast("Export Complete", "Downloaded PowerBI_Export_Holdings.csv.");
    }

    // Initialize Everything
    window.addEventListener('DOMContentLoaded', () => {
      renderMatrixTable();
      initMainChart();
      initDonutChart();
      focusOnHolding('NVDA');
    });
  