async function loadSymbols() {
    const response = await fetch('/data/symbol_whitelist.json');
    const whitelist = await response.json();

    const exchangeSelect = document.getElementById('exchange-select');
    const symbolSelect = document.getElementById('symbol-select');

    exchangeSelect.addEventListener('change', () => {
        const selectedExchange = exchangeSelect.value;
        const symbols = whitelist[selectedExchange];
        symbolSelect.innerHTML = ''; // Töm

        symbols.forEach(symbol => {
            const option = document.createElement('option');
            option.value = symbol;
            option.textContent = symbol;
            symbolSelect.appendChild(option);
        });
    });

    // Auto-trigger for first load
    exchangeSelect.dispatchEvent(new Event('change'));
}
window.onload = loadSymbols;
