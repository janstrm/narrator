document.getElementById('start-capture').addEventListener('click', () => {
    fetch('/start_capture', { method: 'POST' })
        .then(response => response.json())
        .then(data => logMessage('capture-log-output', 'Capture started.'));
});

document.getElementById('stop-capture').addEventListener('click', () => {
    fetch('/stop_capture', { method: 'POST' })
        .then(response => response.json())
        .then(data => logMessage('capture-log-output', 'Capture stopped.'));
});

document.getElementById('start-narrating').addEventListener('click', () => {
    fetch('/start_narrating', { method: 'POST' })
        .then(response => response.json())
        .then(data => logMessage('narration-log-output', 'Narration started.'));
});

document.getElementById('stop-narrating').addEventListener('click', () => {
    fetch('/stop_narrating', { method: 'POST' })
        .then(response => response.json())
        .then(data => logMessage('narration-log-output', 'Narration stopped.'));
});

document.getElementById('shutdown-server').addEventListener('click', () => {
    fetch('/shutdown', { method: 'POST' })
        .then(response => response.text())
        .then(data => {
            logMessage('capture-log-output', data);
            logMessage('narration-log-output', data);
        });
});

function logMessage(elementId, message) {
    const logElement = document.getElementById(elementId);
    logElement.innerHTML += `<p>${message}</p>`;
    logElement.scrollTop = logElement.scrollHeight;
}

function fetchLogs() {
    fetch('/logs')
        .then(response => response.json())
        .then(data => {
            const captureLog = data.capture;
            const narrationLog = data.narration;
            updateLog('capture-log-output', captureLog);
            updateLog('narration-log-output', narrationLog);
        });
}

function updateLog(elementId, messages) {
    const logElement = document.getElementById(elementId);
    logElement.innerHTML = '';
    messages.forEach(message => {
        logElement.innerHTML += `<p>${message}</p>`;
    });
    logElement.scrollTop = logElement.scrollHeight;
}

// Fetch logs every 2 seconds
setInterval(fetchLogs, 2000);
