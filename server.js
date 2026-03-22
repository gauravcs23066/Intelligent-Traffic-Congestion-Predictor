const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/api/predict', (req, res) => {
    const { hour, volume, speed } = req.body;

    // Command to run the simple python script
    const pythonProcess = spawn('python', ['predict.py', hour, volume, speed]);

    let stdoutData = '';
    let stderrData = '';

    pythonProcess.stdout.on('data', (data) => {
        stdoutData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        stderrData += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}: ${stderrData}`);
            return res.status(500).json({ error: 'Prediction failed.' });
        }

        try {
            // Trim any extra whitespace/newlines from the python print output
            const result = JSON.parse(stdoutData.trim());
            if (result.error) {
                return res.status(400).json(result);
            }
            res.json(result);
        } catch (e) {
            console.error("Failed to parse Python output:", stdoutData);
            res.status(500).json({ error: 'Failed to read prediction.' });
        }
    });
});

app.listen(port, () => {
    console.log(`Traffic Predictor running at http://localhost:${port}`);
});
