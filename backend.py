# STAYFINDR BACKEND - European Hotel Search Engine
# Flask backend with booking-com18 API - WORKING VERSION
# Uses YOUR verified working endpoint

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

# API Configuration
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY_BOOKING', 'e1d84ea6ffmsha47402150e4b4a7p1ad726jsn90c5c8f86999')

# European Cities with destination IDs
CITIES = {
    'stockholm': {
        'name': 'Stockholm, Sweden',
        'coordinates': [59.3293, 18.0686],
        'dest_id': '20088325',  # Your verified working ID
        'country_code': 'se'
    },
    'paris': {
        'name': 'Paris, France', 
        'coordinates': [48.8566, 2.3522],
        'dest_id': '20024809',
        'country_code': 'fr'
    },
    'london': {
        'name': 'London, UK',
        'coordinates': [51.5074, -0.1278],
        'dest_id': '20023181',
        'country_code': 'gb'
    },
    'amsterdam': {
        'name': 'Amsterdam, Netherlands',
        'coordinates': [52.3676, 4.9041],
        'dest_id': '20023999',
        'country_code': 'nl'
    },
    'barcelona': {
        'name': 'Barcelona, Spain',
        'coordinates': [41.3851, 2.1734],
        'dest_id': '20023707',
        'country_code': 'es'
    }
}

def search_real_hotels(dest_id, checkin, checkout, adults, rooms):
    """Search hotels using YOUR WORKING booking-com18 endpoint"""
    
    url = "https://booking-com18.p.rapidapi.com/web/stays/search"
    
    params = {
        "destId": dest_id,
        "destType": "city",
        "checkIn": checkin,
        "checkOut": checkout,
        "adults": adults,
        "rooms": rooms,
        "currency": "EUR"
    }
    
    headers = {
        "x-rapidapi-host": "booking-com18.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    print(f"🔄 API Call: {url}")
    print(f"📊 Params: {params}")
    print(f"🔑 Key: {RAPIDAPI_KEY[:20]}...")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print(f"📈 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response keys: {list(data.keys())}")
            
            if data.get('status') and data.get('data'):
                # Success - extract hotels
                hotel_data = data['data']
                
                # Handle different structures
                hotels = []
                if isinstance(hotel_data, list):
                    hotels = hotel_data
                elif isinstance(hotel_data, dict):
                    for key in ['properties', 'hotels', 'results', 'items']:
                        if key in hotel_data:
                            hotels = hotel_data[key]
                            break
                
                print(f"🏨 Found {len(hotels)} hotels")
                return hotels[:25]
            else:
                print(f"❌ API returned errors: {data.get('errors', 'Unknown error')}")
                return []
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

def process_hotels(hotels, city_info):
    """Process hotel data"""
    processed = []
    
    for i, hotel in enumerate(hotels):
        # Extract hotel info
        name = hotel.get('name') or hotel.get('hotel_name') or f"Hotel_{i}"
        price = hotel.get('price') or hotel.get('rate') or 'N/A'
        rating = hotel.get('rating') or hotel.get('review_score', 4.0)
        
        # Coordinates
        lat = hotel.get('latitude') or hotel.get('lat')
        lng = hotel.get('longitude') or hotel.get('lng')
        
        if lat and lng:
            coordinates = [float(lat), float(lng)]
        else:
            base_lat, base_lng = city_info['coordinates']
            coordinates = [base_lat + (i * 0.002), base_lng + (i * 0.002)]
        
        # Create booking URL
        hotel_id = hotel.get('id') or hotel.get('hotel_id') or f"hotel_{i}"
        booking_url = f"https://www.booking.com/hotel/{city_info['country_code']}/hotel-{hotel_id}.html"
        
        processed_hotel = {
            'id': hotel_id,
            'name': name,
            'address': hotel.get('address', city_info['name']),
            'coordinates': coordinates,
            'price': price,
            'rating': float(rating) if rating else 4.0,
            'booking_url': booking_url,
            'platform': 'booking.com',
            'currency': 'EUR',
            'source': 'REAL_API'
        }
        
        processed.append(processed_hotel)
    
    return processed

@app.route('/')
def home():
    return jsonify({
        "name": "STAYFINDR Backend - WORKING VERSION",
        "status": "Online",
        "api_endpoint": "booking-com18.p.rapidapi.com/web/stays/search",
        "cities": len(CITIES),
        "message": "Using YOUR verified working endpoint!"
    })

@app.route('/test')
def test():
    return jsonify({
        "status": "STAYFINDR Backend Online",
        "api_key_active": bool(RAPIDAPI_KEY and len(RAPIDAPI_KEY) > 10),
        "working_endpoint": "booking-com18.p.rapidapi.com/web/stays/search",
        "cities": len(CITIES),
        "test_ready": True
    })

@app.route('/test-simple')
def test_simple():
    """Simple test of working endpoint"""
    
    url = "https://booking-com18.p.rapidapi.com/web/stays/search"
    params = {
        "destId": "20088325",  # Stockholm
        "destType": "city",
        "checkIn": "2025-07-15",   # FIXED: Use valid future date
        "checkOut": "2025-07-16"   # FIXED: Use valid future date
    }
    headers = {
        "x-rapidapi-host": "booking-com18.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "status": "SUCCESS!",
                "status_code": response.status_code,
                "has_data": bool(data.get('data')),
                "has_errors": bool(data.get('errors')),
                "response_keys": list(data.keys()),
                "sample_response": str(data)[:1000]
            })
        else:
            return jsonify({
                "status": "FAILED",
                "status_code": response.status_code,
                "error": response.text[:300]
            })
    except Exception as e:
        return jsonify({
            "status": "EXCEPTION",
            "error": str(e)
        })

@app.route('/api/hotels')
def get_hotels():
    """Get real hotels using working endpoint"""
    
    city = request.args.get('city', 'stockholm')
    checkin = request.args.get('checkin', '2025-07-15')   # FIXED: Default to valid date
    checkout = request.args.get('checkout', '2025-07-16') # FIXED: Default to valid date
    adults = request.args.get('adults', '2')
    rooms = request.args.get('rooms', '1')
    
    if city not in CITIES:
        return jsonify({'error': f'City {city} not supported'}), 400
    
    city_info = CITIES[city]
    
    print(f"🔍 Searching: {city_info['name']}")
    print(f"📅 Dates: {checkin} to {checkout}")
    
    # Call real API
    hotels_data = search_real_hotels(
        city_info['dest_id'],
        checkin,
        checkout, 
        adults,
        rooms
    )
    
    if not hotels_data:
        return jsonify({
            'error': 'No hotels found - check /test-simple for API status',
            'city': city_info['name'],
            'hotels': [],
            'total_found': 0,
            'data_source': 'FAILED_REAL_API'
        }), 404
    
    # Process hotels
    processed_hotels = process_hotels(hotels_data, city_info)
    
    return jsonify({
        'city': city_info['name'],
        'hotels': processed_hotels,
        'total_found': len(processed_hotels),
        'search_params': {
            'checkin': checkin,
            'checkout': checkout,
            'adults': adults,
            'rooms': rooms
        },
        'data_source': 'REAL_BOOKING_API',
        'api_endpoint': 'booking-com18.p.rapidapi.com/web/stays/search'
    })

if __name__ == '__main__':
    print("🚀 Starting STAYFINDR Backend - WORKING VERSION")
    print(f"🔑 API Key: {RAPIDAPI_KEY[:20]}..." if RAPIDAPI_KEY else "❌ NO API KEY")
    print("🏨 Using YOUR verified working endpoint!")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
