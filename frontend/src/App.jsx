import { useState, useEffect } from 'react'

function App() {
  const [backendStatus, setBackendStatus] = useState('🔄 Connecting...')
  const [hotelResults, setHotelResults] = useState(null)
  const [loading, setLoading] = useState(false)

  // Test backend connection
  useEffect(() => {
    fetch('http://localhost:5000')
      .then(res => res.json())
      .then(data => setBackendStatus(`✅ Backend connected! v${data.version} - ${data.cities} cities`))
      .catch(() => setBackendStatus('❌ Backend offline'))
  }, [])

  const searchHotels = async () => {
    setLoading(true)
    setHotelResults(null)
    
    try {
      const response = await fetch('http://localhost:5000/api/hotels?city=stockholm&checkin=2025-07-15&checkout=2025-07-16&adults=2&rooms=1&room_type=double')
      const data = await response.json()
      setHotelResults(data)
    } catch (err) {
      setHotelResults({ error: 'Search failed', message: err.message })
    } finally {
      setLoading(false)
    }
  }

  const searchParis = async () => {
    setLoading(true)
    setHotelResults(null)
    
    try {
      const response = await fetch('http://localhost:5000/api/hotels?city=paris&checkin=2025-07-15&checkout=2025-07-16&adults=2&rooms=1&room_type=junior_suite')
      const data = await response.json()
      setHotelResults(data)
    } catch (err) {
      setHotelResults({ error: 'Search failed', message: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#2c3e50', marginBottom: '10px' }}>
        🏨 STAYFINDR Multi-Platform
      </h1>
      <p style={{ textAlign: 'center', color: '#7f8c8d', fontSize: '18px', marginBottom: '30px' }}>
        One Search, All Platforms - Europe's Smartest Hotel Aggregator
      </p>
      
      <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '12px', margin: '20px 0', border: '1px solid #e9ecef' }}>
        <h3 style={{ margin: '0 0 10px 0', color: '#495057' }}>Backend Status:</h3>
        <p style={{ margin: 0, fontWeight: '500' }}>{backendStatus}</p>
      </div>

      <div style={{ display: 'flex', gap: '15px', marginBottom: '30px', flexWrap: 'wrap' }}>
        <button 
          onClick={searchHotels}
          disabled={loading}
          style={{ 
            padding: '15px 25px', 
            background: loading ? '#6c757d' : 'linear-gradient(135deg, #667eea, #764ba2)', 
            color: 'white', 
            border: 'none', 
            borderRadius: '10px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
            transition: 'transform 0.2s',
            flex: 1,
            minWidth: '200px'
          }}
          onMouseOver={(e) => !loading && (e.target.style.transform = 'translateY(-2px)')}
          onMouseOut={(e) => (e.target.style.transform = 'translateY(0)')}
        >
          {loading ? '⏳ Searching...' : '🇸🇪 Search Stockholm Hotels (Double Room)'}
        </button>

        <button 
          onClick={searchParis}
          disabled={loading}
          style={{ 
            padding: '15px 25px', 
            background: loading ? '#6c757d' : 'linear-gradient(135deg, #ff9a9e, #fecfef)', 
            color: '#2c3e50', 
            border: 'none', 
            borderRadius: '10px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
            transition: 'transform 0.2s',
            flex: 1,
            minWidth: '200px'
          }}
          onMouseOver={(e) => !loading && (e.target.style.transform = 'translateY(-2px)')}
          onMouseOut={(e) => (e.target.style.transform = 'translateY(0)')}
        >
          {loading ? '⏳ Searching...' : '🇫🇷 Search Paris Hotels (Junior Suite)'}
        </button>
      </div>

      {hotelResults && (
        <div style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '25px', borderRadius: '15px', marginTop: '30px', color: 'white' }}>
          <h3 style={{ margin: '0 0 20px 0', textAlign: 'center' }}>
            🏨 REAL Booking.com Search Results
          </h3>
          
          {hotelResults.hotels ? (
            <div>
              <div style={{ background: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', marginBottom: '20px' }}>
                <p style={{ margin: '5px 0' }}><strong>📍 City:</strong> {hotelResults.city}</p>
                <p style={{ margin: '5px 0' }}><strong>🏨 Found:</strong> {hotelResults.total_found} hotels</p>
                <p style={{ margin: '5px 0' }}><strong>🛏️ Room Type:</strong> {hotelResults.room_filter?.description}</p>
                <p style={{ margin: '5px 0' }}><strong>🌙 Stay:</strong> {hotelResults.pricing?.nights} nights ({hotelResults.search_params?.checkin} to {hotelResults.search_params?.checkout})</p>
                <p style={{ margin: '5px 0' }}><strong>💰 Pricing:</strong> {hotelResults.pricing?.description}</p>
              </div>

              <h4 style={{ marginBottom: '15px' }}>Top Hotels:</h4>
              <div style={{ display: 'grid', gap: '15px' }}>
                {hotelResults.hotels.slice(0, 5).map((hotel, index) => (
                  <div key={index} style={{ 
                    background: 'rgba(255,255,255,0.95)', 
                    color: '#2c3e50',
                    padding: '20px', 
                    borderRadius: '12px', 
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                    transition: 'transform 0.2s'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                      <h4 style={{ margin: 0, color: '#2c3e50', fontSize: '18px' }}>{hotel.name}</h4>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#27ae60' }}>
                          €{hotel.price === 'N/A' ? 'N/A' : hotel.price}
                        </div>
                        <div style={{ fontSize: '12px', color: '#7f8c8d' }}>
                          {hotel.price !== 'N/A' && `for ${hotel.nights} nights`}
                        </div>
                      </div>
                    </div>
                    
                    <p style={{ margin: '8px 0', color: '#7f8c8d', fontSize: '14px' }}>
                      📍 {hotel.address}
                    </p>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '15px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <span style={{ color: '#f39c12', fontWeight: 'bold' }}>
                          ⭐ {hotel.rating}/5
                        </span>
                        {hotel.room_type_match && (
                          <span style={{ 
                            background: '#e8f5e8', 
                            color: '#27ae60', 
                            padding: '4px 8px', 
                            borderRadius: '15px', 
                            fontSize: '12px',
                            fontWeight: 'bold'
                          }}>
                            ✨ Room Match
                          </span>
                        )}
                      </div>
                      
                      <a 
                        href={hotel.booking_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ 
                          background: 'linear-gradient(135deg, #667eea, #764ba2)',
                          color: 'white',
                          padding: '8px 16px',
                          borderRadius: '8px',
                          textDecoration: 'none',
                          fontSize: '14px',
                          fontWeight: 'bold',
                          transition: 'transform 0.2s'
                        }}
                        onMouseOver={(e) => e.target.style.transform = 'translateY(-1px)'}
                        onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
                      >
                        📍 Book on Booking.com
                      </a>
                    </div>
                    
                    {hotel.room_description && (
                      <p style={{ 
                        margin: '10px 0 0 0', 
                        fontSize: '12px', 
                        color: '#6c757d',
                        fontStyle: 'italic',
                        background: '#f8f9fa',
                        padding: '8px',
                        borderRadius: '5px'
                      }}>
                        {hotel.room_description}
                      </p>
                    )}
                  </div>
                ))}
              </div>
              
              {hotelResults.hotels.length > 5 && (
                <p style={{ textAlign: 'center', marginTop: '20px', opacity: 0.8 }}>
                  Showing 5 of {hotelResults.total_found} hotels. API integration working perfectly! 🎉
                </p>
              )}
            </div>
          ) : (
            <div style={{ background: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '10px' }}>
              <h4>Debug Information:</h4>
              <pre style={{ fontSize: '12px', overflow: 'auto', background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px' }}>
                {JSON.stringify(hotelResults, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {!hotelResults && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#7f8c8d' }}>
          <h3>🚀 Ready to search real hotels!</h3>
          <p>Click one of the buttons above to see live Booking.com data with:</p>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li>✅ Real hotel prices and ratings</li>
            <li>✅ Direct booking links to Booking.com</li>
            <li>✅ 29 European cities available</li>
            <li>✅ 5 room types including Junior Suite</li>
            <li>✅ Accurate stay pricing calculation</li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default App