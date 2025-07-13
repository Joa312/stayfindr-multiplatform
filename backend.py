# STAYFINDR MULTI-PLATFORM BACKEND - European Hotel Aggregator
# Flask backend with Booking.com + Hotels.com integration
# TRUE AGGREGATOR: Compare prices across multiple platforms!

import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import time
from datetime import datetime
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

# RapidAPI Configuration
BOOKING_RAPIDAPI_KEY = "e1d84ea6ffmsha47402150e4b4a7p1ad726jsn90c5c8f86999"
BOOKING_RAPIDAPI_HOST = "booking-com18.p.rapidapi.com"

# Hotels.com API Configuration
HOTELS_RAPIDAPI_KEY = "ae6d44ef88mshd1dc5c75449a1b6p154a82jsne83e2399cc75"
HOTELS_RAPIDAPI_HOST = "hotels4.p.rapidapi.com"

# European Cities Configuration - 29 major destinations
CITIES = {
    'stockholm': {
        'name': 'Stockholm, Sweden',
        'coordinates': [59.3293, 18.0686],
        'search_query': 'Stockholm Sweden'
    },
    'paris': {
        'name': 'Paris, France', 
        'coordinates': [48.8566, 2.3522],
        'search_query': 'Paris France'
    },
    'london': {
        'name': 'London, UK',
        'coordinates': [51.5074, -0.1278],
        'search_query': 'London United Kingdom'
    },
    'amsterdam': {
        'name': 'Amsterdam, Netherlands',
        'coordinates': [52.3676, 4.9041],
        'search_query': 'Amsterdam Netherlands'
    },
    'barcelona': {
        'name': 'Barcelona, Spain',
        'coordinates': [41.3851, 2.1734],
        'search_query': 'Barcelona Spain'
    },
    'rome': {
        'name': 'Rome, Italy',
        'coordinates': [41.9028, 12.4964],
        'search_query': 'Rome Italy'
    },
    'berlin': {
        'name': 'Berlin, Germany',
        'coordinates': [52.5200, 13.4050],
        'search_query': 'Berlin Germany'
    },
    'copenhagen': {
        'name': 'Copenhagen, Denmark',
        'coordinates': [55.6761, 12.5683],
        'search_query': 'Copenhagen Denmark'
    },
    'vienna': {
        'name': 'Vienna, Austria',
        'coordinates': [48.2082, 16.3738],
        'search_query': 'Vienna Austria'
    },
    'prague': {
        'name': 'Prague, Czech Republic',
        'coordinates': [50.0755, 14.4378],
        'search_query': 'Prague Czech Republic'
    }
}

# Country codes for Booking.com URLs based on city
COUNTRY_CODES = {
    'stockholm': 'sv', 'oslo': 'no', 'helsinki': 'fi', 'copenhagen': 'dk',
    'paris': 'fr', 'lyon': 'fr', 'nice': 'fr',
    'london': 'en-gb', 'edinburgh': 'en-gb',
    'amsterdam': 'nl', 'brussels': 'nl',
    'barcelona': 'es', 'madrid': 'es', 'palma': 'es', 'ibiza': 'es',
    'rome': 'it', 'milano': 'it', 'florence': 'it',
    'berlin': 'de', 'munich': 'de',
    'vienna': 'de', 'zurich': 'de',
    'prague': 'cs', 'warsaw': 'pl', 'budapest': 'hu',
    'dublin': 'en-gb', 'lisbon': 'pt', 'athens': 'el', 'santorini': 'el'
}

# Room Type Configuration with Junior Suite
ROOM_TYPES = {
    'single': {
        'name': 'Single Room',
        'description': 'Single Room - Perfect for solo travelers',
        'guests': 1,
        'keywords': ['single', 'solo', 'individual', 'one person'],
        'booking_param': 'single'
    },
    'double': {
        'name': 'Double Room',
        'description': 'Double Room - Ideal for couples',
        'guests': 2,
        'keywords': ['double', 'twin', 'couple', 'two beds', 'king'],
        'booking_param': 'double'
    },
    'family': {
        'name': 'Family Room',
        'description': 'Family Room - Great for families with children',
        'guests': 4,
        'keywords': ['family', 'quad', 'children', 'kids', 'connecting'],
        'booking_param': 'family'
    },
    'junior_suite': {
        'name': 'Junior Suite',
        'description': 'Junior Suite - Spacious room with sitting area',
        'guests': 2,
        'keywords': ['junior suite', 'junior', 'suite', 'sitting area', 'upgraded', 'spacious'],
        'booking_param': 'junior_suite'
    },
    'suite': {
        'name': 'Suite/Apartment',
        'description': 'Suite/Apartment - Luxury accommodation with separate living area',
        'guests': 3,
        'keywords': ['suite', 'apartment', 'luxury', 'separate', 'living area', 'premium'],
        'booking_param': 'suite'
    }
}

# Test endpoint
@app.route('/test')
def test():
    return jsonify({
        'status': 'STAYFINDR Multiplatform Backend Online!',
        'platforms': ['Booking.com', 'Hotels.com'],
        'cities': len(CITIES),
        'room_types': len(ROOM_TYPES)
    })

if __name__ == '__main__':
    print("🚀 Starting STAYFINDR Multi-Platform Backend...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
