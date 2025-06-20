
let tradeAmountLocked = false;

let activeMarkets = JSON.parse(localStorage.getItem("activeMarkets")) || {
    crypto: true,
    forex: true,
    binary: true
};

function toggleMarket(type) {
    activeMarkets[type] = !activeMarkets[type];
    localStorage.setItem("activeMarkets", JSON.stringify(activeMarkets));
    updateToggleStyles();
    fetch("/api/update_markets", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(activeMarkets)
    });
}

function updateToggleStyles() {
    ["crypto", "forex", "binary"].forEach(type => {
        const circle = document.getElementById("circle-" + type);
        circle.style.backgroundColor = activeMarkets[type] ? "green" : "transparent";
    });
}

function sendCommand(cmd) {
    if (cmd === 'simulering') cmd = 'demo';
    fetch(`/api/control/${cmd}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            updateStatusCircle(data.mode || {});
        });
}

function updateStatusCircle(mode) {
    document.getElementById("circle-live").className = "circle";
    document.getElementById("circle-simulering").className = "circle";
    document.getElementById("circle-stoppad").className = "circle";
    if (mode.status === "running" && mode.demo === false) {
        document.getElementById("circle-live").classList.add("status-live");
    } else if (mode.status === "running" && mode.demo === true) {
        document.getElementById("circle-simulering").classList.add("status-simulering");
    } else {
        document.getElementById("circle-stoppad").classList.add("status-stoppad");
    }
}

function updateAmount() {
    if (tradeAmountLocked) return;
    const sekAmount = parseInt(document.getElementById("amountSlider").value);
    const currency = document.getElementById("currency").value;
    fetch(`/api/update_trade_amount`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: sekAmount, currency: currency })
    });
}

function lockTradeAmount() {
    tradeAmountLocked = !tradeAmountLocked;
    document.getElementById("lock-indicator").style.backgroundColor = tradeAmountLocked ? "green" : "transparent";
}

function fetchData() {
    const currency = document.getElementById("currency").value;
    fetch(`/api/data?currency=${currency}`)
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("liveTradesTable").getElementsByTagName("tbody")[0];
            table.innerHTML = "";
            data.live_trades.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${row.symbol}</td>
                    <td>${row.strategy || ''}</td>
                    <td>${row.entry_price || ''}</td>
                    <td>${row.amount || ''}</td>
                    <td>${row.confidence || ''}</td>
                    <td>${row.profit || ''}</td>
                    <td>${row.invest || ''}</td>
                    <td>${row.pnl_pct || ''}</td>
                `;
                table.appendChild(tr);
            });

            const aiTable = document.getElementById("aiSignalsTable").getElementsByTagName("tbody")[0];
            aiTable.innerHTML = "";
            data.ai_signals.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${row.platform}</td>
                    <td>${row.symbol}</td>
                    <td>${row.strategy}</td>
                    <td>${row.risk}</td>
                    <td>${row.confidence}</td>
                    <td>${row.amount}</td>
                    <td>${row.eta}</td>
                `;
                aiTable.appendChild(tr);
            });

            document.getElementById("profit-label").textContent = data.pnl_type;
            document.getElementById("profit-amount").textContent = `${data.total_profit.toFixed(2)} kr`;
            document.getElementById("profitData").innerHTML =
                `Profit: ${data.total_profit} ${currency}<br>` +
                `Loss: ${data.total_loss} ${currency}<br>` +
                `NET: ${(data.total_profit + data.total_loss).toFixed(2)} ${currency}`;

            const brokerList = document.getElementById("broker-balances");
            brokerList.innerHTML = "";
            for (const [broker, accounts] of Object.entries(data.balances)) {
                const tooltip = accounts.map(acc => `${acc.currency}: ${acc.balance}`).join(" | ");
                const li = document.createElement("li");
                li.textContent = broker;
                li.title = tooltip;
                brokerList.appendChild(li);
            }

            const list = document.getElementById("topStrategiesList");
            list.innerHTML = "";
            data.top_strategies.forEach(item => {
                list.innerHTML += `<li>${item.strategy} (${item.count})</li>`;
            });

            document.getElementById("deriv-loginid").textContent = data.deriv.loginid || "–";
            document.getElementById("deriv-type").textContent = data.deriv.mode === "Demo" ? "Demo" : "Live";
            document.getElementById("deriv-balance").textContent = `${data.deriv.balance} ${data.deriv.currency}`;
        });

    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            document.getElementById("nikola-status-circle").style.backgroundColor =
                data.status === "running" ? "green" : "red";
        });
}

function fetchDerivStatus() {
    fetch("/api/deriv_status")
        .then(response => response.json())
        .then(data => {
            let msg = '';
            for (let key in data) {
                const acc = data[key];
                msg += `${key} (${acc.loginid})\nBalans: ${acc.balance} ${acc.currency}\nTyp: ${acc.is_virtual ? 'Demo' : 'Live'}\n\n`;
            }
            alert(msg.trim());
        })
        .catch(err => alert("Fel vid hämtning av Deriv-status: " + err));
}

function manualExport() {
    fetch("/api/export_balances")
        .then(res => res.json())
        .then(data => alert("✅ " + data.msg))
        .catch(err => alert("❌ Fel vid export: " + err));
}

updateToggleStyles();
fetchData();
setInterval(fetchData, 7000);
