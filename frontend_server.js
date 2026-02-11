const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));

// Serve the test page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_chatbot.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Test server running at http://localhost:${PORT}`);
    console.log('Make sure backend is running at http://localhost:8000');
});