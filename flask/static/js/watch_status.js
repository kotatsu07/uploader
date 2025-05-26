function fetchWatchStatus() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            const statusText = document.getElementById('watch-status');
            statusText.textContent = data.is_watching ? "監視中" : "停止中";
            statusText.style.color = data.is_watching ? "green" : "red";
        });
}

function startWatchStatusUpdate() {
    setInterval(fetchWatchStatus, 5000);
}
