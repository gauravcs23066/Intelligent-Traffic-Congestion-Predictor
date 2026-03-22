document.getElementById('predictForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI Elements
    const submitBtn = document.getElementById('submitBtn');
    const resultCard = document.getElementById('resultCard');
    const errorBox = document.getElementById('errorBox');
    const statusBox = document.getElementById('statusBox');
    const resultStatus = document.getElementById('resultStatus');

    // Form Values
    const hour = parseInt(document.getElementById('hour').value);
    const volume = parseInt(document.getElementById('volume').value);
    const speed = parseInt(document.getElementById('speed').value);

    // Reset UI
    submitBtn.disabled = true;
    submitBtn.textContent = 'Running Model...';
    errorBox.style.display = 'none';
    resultCard.style.display = 'none';
    statusBox.className = 'status-box';

    // Reset bars
    ['Clear', 'Moderate', 'Congested'].forEach(state => {
        document.getElementById(`bar${state}`).style.width = '0%';
        document.getElementById(`prob${state}`).textContent = '0%';
    });

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hour, volume, speed })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Prediction request failed');
        }

        // Show Results
        resultCard.style.display = 'block';

        // Set Status Text and Color
        resultStatus.textContent = data.status;
        statusBox.className = `status-box status-${data.status.toLowerCase()}`;

        // Animate Probability Bars
        setTimeout(() => {
            const states = ['Clear', 'Moderate', 'Congested'];
            data.probabilities.forEach((prob, index) => {
                if (states[index]) {
                    const percentage = (prob * 100).toFixed(1);
                    document.getElementById(`bar${states[index]}`).style.width = `${percentage}%`;
                    document.getElementById(`prob${states[index]}`).textContent = `${percentage}%`;
                }
            });
        }, 100);

    } catch (error) {
        errorBox.textContent = `Error: ${error.message}`;
        errorBox.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Run Prediction';
    }
});
