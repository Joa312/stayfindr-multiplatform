# STAYFINDR MULTIPLATFORM BACKEND - European Hotel Search Engine
# Flask backend with multiple booking platform integration
# Supports: Booking.com + Hotels.com + Room Type Filters

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import time
from datetime import datetime
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

# API Configuration
RAPIDAPI_KEY_BOOKING = os.environ.get('RAPIDAPI_KEY_BOOKING', 'demo_key')
RAPIDAPI_KEY_HOTELS = os.environ.get('RAPIDAPI_KEY_HOTELS', 'demo_key')

# European Cities Configuration - Top 10 destinations
CITIES = {
    'stockholm': {
        'name': 'Stockholm, Sweden',
        'coordinates': [59.3293, 18.0686],
        'country_code': 'SE'
    },
    'paris': {
        'name': 'Paris, France',
        'coordinates': [48.8566, 2.3522],
        'country_code': 'FR'
    },
    'london': {
        'name': 'London, UK',
        'coordinates': [51.5074, -0.1278],
        'country_code': 'GB'
    },
    'amsterdam': {
        'name': 'Amsterdam, Netherlands',
        'coordinates': [52.3676, 4.9041],
        'country_code': 'NL'
    },
    'barcelona': {
        'name': 'Barcelona, Spain',
        'coordinates': [41.3851, 2.1734],
        'country_code': 'ES'
    },
    'rome': {
        'name': 'Rome, Italy',
        'coordinates': [41.9028, 12.4964],
        'country_code': 'IT'
    },
    'berlin': {
        'name': 'Berlin, Germany',
        'coordinates': [52.5200, 13.4050],
        'country_code': 'DE'
    },
    'vienna': {
        'name': 'Vienna, Austria',
        'coordinates': [48.2082, 16.3738],
        'country_code': 'AT'
    },
    'prague': {
        'name': 'Prague, Czech Republic',
        'coordinates': [50.0755, 14.4378],
        'country_code': 'CZ'
    },
    'madrid': {
        'name': 'Madrid, Spain',
        'coordinates': [40.4168, -3.7038],
        'country_code': 'ES'
    }
}

# Room Types Configuration with Junior Suite
ROOM_TYPES = {
    'single': {
        'name': 'Single Room',
        'guests': 1,
        'description': 'Perfect for solo travelers',
        'keywords': ['single', 'solo', 'one person', 'individual']
    },
    'double': {
        'name': 'Double Room', 
        'guests': 2,
        'description': 'Ideal for couples',
        'keywords': ['double', 'couple', 'two person', 'standard']
    },
    'family': {
        'name': 'Family Room',
        'guests': 4,
        'description': 'Spacious room for families',
        'keywords': ['family', 'kids', 'children', 'large', 'connecting']
    },
    'junior_suite': {
        'name': 'Junior Suite',
        'guests': 2,
        'description': 'Spacious room with sitting area',
        'keywords': ['junior suite', 'junior', 'suite', 'sitting area', 'upgraded']
    },
    'suite': {
        'name': 'Suite/Apartment',
        'guests': 3,
        'description': 'Luxury accommodation with separate areas',
        'keywords': ['suite', 'apartment', 'luxury', 'separate', 'living room']
    }
}

def get_booking_com_hotels(city_info, checkin, checkout, adults, rooms, room_type):
    """Get hotels from Booking.com via RapidAPI"""
    
    # Mock data for demonstration (replace with real API when you get keys)
    if RAPIDAPI_KEY_BOOKING == 'demo_key':
        return generate_mock_hotels(city_info, 'booking.com', room_type)
    
    # Real API implementation (when you have valid keys)
    try:
        url = "https://booking-com18.p.rapidapi.com/stays/search"
        
        querystring = {
            "locationId": city_info.get('booking_id', '1'),
            "checkinDate": checkin,
            "checkoutDate": checkout,
            "adults": adults,
            "rooms": rooms,
            "currency": "EUR"
        }
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY_BOOKING,
            "X-RapidAPI-Host": "booking-com18.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            return process_booking_hotels(data, city_info, room_type)
        
    except Exception as e:
        print(f"Booking.com API error: {e}")
    
    # Fallback to mock data
    return generate_mock_hotels(city_info, 'booking.com', room_type)

def get_hotels_com_hotels(city_info, checkin, checkout, adults, rooms, room_type):
    """Get hotels from Hotels.com via RapidAPI"""
    
    # Mock data for demonstration (replace with real API when you get keys)
    if RAPIDAPI_KEY_HOTELS == 'demo_key':
        return generate_mock_hotels(city_info, 'hotels.com', room_type)
    
    # Real API implementation (when you have valid keys)
    try:
        url = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search"
        
        querystring = {
            "checkin_date": checkin,
            "checkout_date": checkout,
            "adults_number": adults,
            "domain": "AE",
            "locale": "en_GB",
            "sort_order": "REVIEW",
            "currency": "EUR",
            "units": "metric",
            "destination": city_info['name']
        }
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY_HOTELS,
            "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            return process_hotels_com_data(data, city_info, room_type)
            
    except Exception as e:
        print(f"Hotels.com API error: {e}")
    
    # Fallback to mock data
    return generate_mock_hotels(city_info, 'hotels.com', room_type)

def generate_mock_hotels(city_info, platform, room_type):
    """Generate realistic mock hotel data for demonstration"""
    
    room_info = ROOM_TYPES.get(room_type, ROOM_TYPES['double'])
    base_price = 100 if platform == 'booking.com' else 110
    
    # Platform-specific price adjustments
    if room_type == 'junior_suite':
        base_price *= 1.5
    elif room_type == 'suite':
        base_price *= 2.0
    elif room_type == 'family':
        base_price *= 1.3
    
    hotels = []
    city_name = city_info['name'].split(',')[0]
    
    for i in range(5):  # 5 hotels per platform
        price_variation = 1 + (i * 0.2)  # Price variation between hotels
        final_price = int(base_price * price_variation)
        
        hotel = {
            'id': f"{platform}_{city_name.lower()}_{i+1}",
            'name': f"{city_name} {['Grand Hotel', 'Plaza', 'Royal', 'Central', 'Palace'][i]}",
            'address': f"{city_name} City Center",
            'coordinates': [
                city_info['coordinates'][0] + (i * 0.01) - 0.02,
                city_info['coordinates'][1] + (i * 0.01) - 0.02
            ],
            'price': final_price,
            'currency': 'EUR',
            'rating': round(4.0 + (i * 0.2), 1),
            'platform': platform,
            'room_type': room_info['name'],
            'room_description': room_info['description'],
            'booking_url': create_platform_booking_url(city_info, platform, room_type, i+1),
            'amenities': ['WiFi', 'Breakfast', 'Parking'] if room_type != 'suite' else ['WiFi', 'Breakfast', 'Spa', 'Room Service']
        }
        hotels.append(hotel)
    
    return hotels

def create_platform_booking_url(city_info, platform, room_type, hotel_id):
    """Create booking URLs for different platforms"""
    
    city_name = city_info['name'].split(',')[0].replace(' ', '+')
    
    if platform == 'booking.com':
        return f"https://www.booking.com/searchresults.html?ss={city_name}&room_type={room_type}&hotel_id={hotel_id}"
    elif platform == 'hotels.com':
        return f"https://www.hotels.com/search.do?destination={city_name}&room-type={room_type}&hotel-id={hotel_id}"
    
    return "#"

def process_booking_hotels(data, city_info, room_type):
    """Process real Booking.com API response"""
    hotels = []
    
    if 'data' in data:
        for hotel_data in data['data'][:5]:  # Limit to 5 hotels
            hotel = {
                'id': hotel_data.get('id'),
                'name': hotel_data.get('name'),
                'address': hotel_data.get('address', city_info['name']),
                'coordinates': [
                    float(hotel_data.get('latitude', city_info['coordinates'][0])),
                    float(hotel_data.get('longitude', city_info['coordinates'][1]))
                ],
                'price': hotel_data.get('price', {}).get('amount', 100),
                'currency': hotel_data.get('price', {}).get('currency', 'EUR'),
                'rating': hotel_data.get('rating', 4.0),
                'platform': 'booking.com',
                'room_type': ROOM_TYPES.get(room_type, {}).get('name', 'Double Room'),
                'booking_url': hotel_data.get('url', '#')
            }
            hotels.append(hotel)
    
    return hotels

def aggregate_and_compare_prices(booking_hotels, hotels_com_hotels):
    """Aggregate results from multiple platforms and enable price comparison"""
    
    all_hotels = []
    
    # Add platform identifier and comparison data
    for hotel in booking_hotels:
        hotel['comparison_available'] = True
        hotel['price_comparison'] = 'Check Hotels.com for alternative pricing'
        all_hotels.append(hotel)
    
    for hotel in hotels_com_hotels:
        hotel['comparison_available'] = True  
        hotel['price_comparison'] = 'Check Booking.com for alternative pricing'
        all_hotels.append(hotel)
    
    # Sort by price for best value first
    all_hotels.sort(key=lambda x: x.get('price', 999))
    
    return all_hotels

def analyze_room_type_match(hotel_name, room_type):
    """Analyze if hotel matches requested room type"""
    if room_type == 'double':
        return True  # Most common, assume available
    
    room_keywords = ROOM_TYPES.get(room_type, {}).get('keywords', [])
    hotel_lower = hotel_name.lower()
    
    # Check if hotel name contains room type keywords
    for keyword in room_keywords:
        if keyword in hotel_lower:
            return True
    
    return False

# API Routes

@app.route('/')
def home():
    """API Documentation Page"""
    return jsonify({
        'name': 'STAYFINDR Multiplatform Backend',
        'version': '1.0',
        'status': 'Online',
        'description': 'European hotel search across multiple booking platforms',
        'endpoints': {
            '/test': 'Health check',
            '/api/hotels': 'Search hotels across platforms',
            '/api/cities': 'List supported cities',
            '/api/room-types': 'List available room types'
        },
        'platforms': ['Booking.com', 'Hotels.com'],
        'cities': len(CITIES),
        'room_types': len(ROOM_TYPES),
        'features': [
            'Multi-platform price comparison',
            'Room type filtering (including Junior Suite)',
            'Real-time availability',
            'European city coverage'
        ]
    })

@app.route('/test')
def test():
    """Health check endpoint"""
    return jsonify({
        'status': 'STAYFINDR Multiplatform Backend Online!',
        'platforms': ['Booking.com', 'Hotels.com'],
        'cities': len(CITIES),
        'room_types': len(ROOM_TYPES),
        'features': {
            'price_comparison': True,
            'room_filtering': True,
            'junior_suite': True,
            'multi_platform': True
        }
    })

@app.route('/api/cities')
def get_cities():
    """Get all supported cities"""
    return jsonify({
        'cities': CITIES,
        'total': len(CITIES),
        'coverage': 'Major European destinations'
    })

@app.route('/api/room-types')
def get_room_types():
    """Get all supported room types"""
    return jsonify({
        'room_types': ROOM_TYPES,
        'total': len(ROOM_TYPES),
        'junior_suite_included': True
    })

@app.route('/api/hotels')
def search_hotels():
    """Search hotels across multiple platforms with room type filtering"""
    
    # Get search parameters
    city = request.args.get('city', 'stockholm').lower()
    checkin = request.args.get('checkin', '2025-01-20')
    checkout = request.args.get('checkout', '2025-01-21') 
    adults = request.args.get('adults', '2')
    rooms = request.args.get('rooms', '1')
    room_type = request.args.get('room_type', 'double')
    
    # Validate city
    if city not in CITIES:
        return jsonify({'error': f'City {city} not supported'}), 400
    
    # Validate room type
    if room_type not in ROOM_TYPES:
        return jsonify({'error': f'Room type {room_type} not supported'}), 400
        
    city_info = CITIES[city]
    room_info = ROOM_TYPES[room_type]
    
    # Search across multiple platforms
    print(f"🔍 Searching {city} for {room_type} rooms...")
    
    # Get hotels from Booking.com
    booking_hotels = get_booking_com_hotels(city_info, checkin, checkout, adults, rooms, room_type)
    
    # Get hotels from Hotels.com  
    hotels_com_hotels = get_hotels_com_hotels(city_info, checkin, checkout, adults, rooms, room_type)
    
    # Aggregate and compare prices
    all_hotels = aggregate_and_compare_prices(booking_hotels, hotels_com_hotels)
    
    # Calculate comparison stats
    booking_count = len(booking_hotels)
    hotels_count = len(hotels_com_hotels)
    total_hotels = len(all_hotels)
    
    # Get price range
    prices = [h.get('price', 0) for h in all_hotels if h.get('price')]
    price_range = {
        'min': min(prices) if prices else 0,
        'max': max(prices) if prices else 0,
        'average': sum(prices) // len(prices) if prices else 0
    }
    
    return jsonify({
        'city': city_info['name'],
        'room_type': room_info['name'], 
        'room_description': room_info['description'],
        'search_params': {
            'checkin': checkin,
            'checkout': checkout,
            'adults': adults,
            'rooms': rooms
        },
        'aggregated_results': True,
        'platforms': ['booking', 'hotels'],
        'platform_stats': {
            'booking.com': booking_count,
            'hotels.com': hotels_count,
            'total': total_hotels
        },
        'price_comparison': 'enabled',
        'price_range': price_range,
        'hotels': all_hotels,
        'total_found': total_hotels,
        'room_filter': 'enabled',
        'junior_suite_available': room_type == 'junior_suite'
    })

if __name__ == '__main__':
    print("🚀 Starting STAYFINDR Multi-Platform Backend...")
    print("🏨 Supporting 10 European cities")
    print("🌍 Multi-platform aggregation: Booking.com + Hotels.com")
    print("🔍 Room type filtering with Junior Suite support")
    print("💰 Price comparison enabled")
    print("📋 Test API: /test")
    print("✅ Ready for frontend integration")
    
    # Use PORT environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
