const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.json({
        message: '🏨 STAYFINDR Test API',
        version: 'TEST',
        status: 'working'
    });
});

app.get('/api/hotels', (req, res) => {
    res.json({
        city: 'Stockholm, Sweden',
        hotels: [
            {
                name: 'Test Hotel 1',
                price: 120,
                rating: 4.2,
                platform: 'booking.com'
            },
            {
                name: 'Test Hotels.com Hotel',
                price: 95,
                rating: 4.0,
                platform: 'hotels.com'
            }
        ],
        platforms: {
            'booking.com': 1,
            'hotels.com': 1
        }
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Test backend running on port ${PORT}`);
});