// server.js
const express = require('express');
const gsmarena = require('gsmarena-api');
const app = express();

// Route 1: Search for a device name and get its ID
app.get('/search', async (req, res) => {
    try {
        const devices = await gsmarena.search.search(req.query.q);
        res.json(devices);
    } catch (e) {
        res.status(500).json({error: e.message});
    }
});

// Route 2: Get the full technical specs using the device ID
app.get('/device', async (req, res) => {
    try {
        const device = await gsmarena.catalog.getDevice(req.query.id);
        res.json(device);
    } catch (e) {
        res.status(500).json({error: e.message});
    }
});

app.listen(3000, () => console.log('GSMArena Microservice running on port 3000'));