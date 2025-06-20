document.getElementById("manualTradeForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    exchange: document.getElementById("exchange").value,
    symbol: document.getElementById("symbol").value,
    amount: parseFloat(document.getElementById("amount").value),
    risk: parseFloat(document.getElementById("risk").value),
    leverage: parseFloat(document.getElementById("leverage").value),
  };

  const res = await fetch("/manual_trade", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();
  document.getElementById("manualTradeResult").innerText = result.message || "Trade skickad!";
});
