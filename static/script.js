let pnlChart;

async function loadTrades() {
    const res = await fetch('/api/trades');
    const data = await res.json();
    const list = document.getElementById('tradeList');
    list.innerHTML = '';
    const pnlData = [];

    data.forEach(trade => {
        const li = document.createElement('li');
        li.textContent = `${trade.symbol} | ${trade.strategy} | Entry: ${trade.entry} | Result: ${trade.result}`;
        list.appendChild(li);

        const value = parseFloat(trade.result.replace('%', ''));
        if (!isNaN(value)) {
            pnlData.push({ x: trade.entry, y: value });
        }
    });

    updatePnLChart(pnlData);
}

async function loadSignals() {
    const res = await fetch('/api/signals');
    const data = await res.json();
    const list = document.getElementById('signalList');
    list.innerHTML = '';
    data.forEach(signal => {
        const li = document.createElement('li');
        li.textContent = `${signal.time} | ${signal.symbol} | ${signal.reason}`;
        list.appendChild(li);
    });
}

async function loadRisk() {
    const res = await fetch('/api/risk');
    const data = await res.json();
    const list = document.getElementById('riskList');
    list.innerHTML = '';
    data.forEach(risk => {
        const li = document.createElement('li');
        li.textContent = `${risk.symbol} | Risk: ${risk.level} | Confidence: ${risk.confidence}%`;
        list.appendChild(li);
    });
}

async function loadProfitSummary() {
    const res = await fetch('/api/profit');
    const data = await res.json();

    document.getElementById('profit-day').textContent = `Dag: ${data.day}%`;
    document.getElementById('profit-week').textContent = `Vecka: ${data.week}%`;
    document.getElementById('profit-month').textContent = `Månad: ${data.month}%`;
}

async function loadLeaderboard() {
    const res = await fetch('/api/leaderboard');
    const data = await res.json();

    const topStrat = data.strategies[0];
    document.getElementById('top-strategy').textContent =
        `Strategi: ${topStrat.name} (${topStrat.avg}%)`;

    const ul = document.getElementById('top-symbols');
    ul.innerHTML = '';
    data.symbols.forEach(sym => {
        const li = document.createElement('li');
        li.textContent = `${sym.name} | Trades: ${sym.count} | Snitt: ${sym.avg}%`;
        ul.appendChild(li);
    });
}

async function getStatus() {
    const res = await fetch('/api/status');
    const data = await res.json();
    alert(`Status: ${data.status} | Mode: ${data.mode}`);
}

async function toggleMode() {
    const res = await fetch('/api/toggle_mode', { method: 'POST' });
    const data = await res.json();
    alert(`Läge ändrat till: ${data.mode}`);
}

function startNikola() {
    alert('Start-knapp tryckt (placeholder) – implementera API-anrop vid behov.');
}

function stopNikola() {
    alert('Stop-knapp tryckt (placeholder) – implementera API-anrop vid behov.');
}

function exportData() {
    window.location.href = '/api/export';
}

function exportCSV() {
    window.location.href = '/api/export_csv';
}

async function loadSymbolList() {
    const res = await fetch('/api/symbols');
    const data = await res.json();
    const selector = document.getElementById('symbolSelector');

    Object.entries(data).forEach(([exchange, symbols]) => {
        const group = document.createElement('optgroup');
        group.label = exchange.toUpperCase();

        symbols.forEach(sym => {
            const opt = document.createElement('option');
            opt.value = `${exchange}:${sym}`;
            opt.textContent = sym;
            group.appendChild(opt);
        });

        selector.appendChild(group);
    });
}

function updateTradingView() {
    const val = document.getElementById('symbolSelector').value;
    const [exchange, symbol] = val.split(':');
    const iframe = document.querySelector('#tradingview-widget iframe');
    const base = "https://www.tradingview.com/widgetembed/?frameElementId=tv&interval=1&theme=dark&style=1&toolbarbg=F1F3F6&timezone=Etc/UTC&hideideas=1&symbol=";
    iframe.src = `${base}${exchange.toUpperCase()}:${symbol}`;
}

function updatePnLChart(data) {
    if (!document.getElementById('pnlChart')) return;

    if (pnlChart) pnlChart.destroy();

    const ctx = document.getElementById('pnlChart').getContext('2d');
    pnlChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'PnL (%)',
                data: data,
                borderWidth: 2,
                borderColor: 'lime',
                backgroundColor: 'rgba(0,255,0,0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    },
                    ticks: { color: '#aaa' }
                },
                y: {
                    ticks: { color: '#aaa' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#fff' }
                }
            }
        }
    });
}

window.onload = () => {
    loadTrades();
    loadSignals();
    loadRisk();
    loadSymbolList();
    loadProfitSummary();
    loadLeaderboard();
};

setInterval(() => {
    loadTrades();
    loadSignals();
    loadRisk();
    loadProfitSummary();
    loadLeaderboard();
}, 10000);
