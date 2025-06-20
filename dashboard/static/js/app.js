
const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
  log("WebSocket ansluten.");
});

socket.on("status_update", data => {
  log("Status uppdaterad: " + data.status);
  document.getElementById("status").innerText = data.status;
});

socket.on("trade_executed", data => {
  log("Ny trade: " + data.symbol + " " + data.result);
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${data.time}</td>
    <td>${data.symbol}</td>
    <td>${data.strategy}</td>
    <td>${data.result}</td>
  `;
  document.querySelector("#tradeTable tbody").prepend(row);

  // uppdatera senaste trade
  document.getElementById("latestTrade").innerText = `${data.symbol} ${data.result} ${data.time}`;
});

function startBot() {
  fetch('/start_bot').then(() => log('Bot startad'));
}

function stopBot() {
  fetch('/stop_bot').then(() => log('Bot stoppad'));
}

function toggleDemoLive() {
  const modeBtn = document.getElementById('modeToggle');
  modeBtn.innerText = modeBtn.innerText === 'Demo' ? 'Live' : 'Demo';
}

function toggleAutoTrade() {
  const checked = document.getElementById('autoTradeToggle').checked;
  log('Auto-trade: ' + (checked ? 'På' : 'Av'));
}

function manualTrade() {
  const amount = document.getElementById('manualAmount').value;
  const currency = document.getElementById('currencySelect').value;
  fetch('/manual_trade', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount, currency })
  }).then(() => log(`Manuell trade skickad: ${amount} ${currency}`));
}

function exportTrades() {
  fetch('/export_trades')
    .then(res => res.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'trades.csv';
      a.click();
    });
}

function log(message) {
  const logOutput = document.getElementById('logOutput');
  const now = new Date().toLocaleTimeString();
  logOutput.textContent += `[${now}] ${message}\n`;
  logOutput.scrollTop = logOutput.scrollHeight;
}

window.onload = function () {
  new TradingView.widget({
    autosize: true,
    symbol: "BINANCE:BTCUSDT",
    interval: "15",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    container_id: "tv1"
  });
  new TradingView.widget({
    autosize: true,
    symbol: "BINANCE:ETHUSDT",
    interval: "15",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    container_id: "tv2"
  });
  new TradingView.widget({
    autosize: true,
    symbol: "FOREXCOM:EURUSD",
    interval: "15",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    container_id: "tv3"
  });
  new TradingView.widget({
    autosize: true,
    symbol: "NASDAQ:AAPL",
    interval: "15",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    container_id: "tv4"
  });
};
