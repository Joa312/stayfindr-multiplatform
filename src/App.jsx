import React, { useState, useEffect } from 'react'

function App() {
  const [backendStatus, setBackendStatus] = useState('🔄 Connecting...')
  const [hotelResults, setHotelResults] = useState(null)

  // Test backend connection
  useEffect(() => {
    fetch('http://localhost:5000')
      .then(res => res.json())
      .then(data => setBackendStatus('✅ Backend connected!'))
      .catch(() => setBackendStatus('❌ Backend offline'))
  }, [])

  const searchHotels = () => {
    fetch('http://localhost:5000/api/hotels/search?city=stockholm')
      .then(res => res.json())
      .then(data => setHotelResults(data))
      .catch(err => setHotelResults({ error: 'Search failed' }))
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🏨 STAYFINDR Multi-Platform</h1>
      <p>One Search, All Platforms</p>
      
      <div style={{ background: '#f0f0f0', padding: '15px', borderRadius: '8px', margin: '20px 0' }}>
        <h3>Backend Status:</h3>
        <p>{backendStatus}</p>
      </div>

      <button 
        onClick={searchHotels}
        style={{ 
          padding: '10px 20px', 
          background: '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '5px',
          cursor: 'pointer',
          fontSize: '16px'
        }}
      >
        🔍 Search Hotels (Stockholm)
      </button>

      {hotelResults && (
        <div style={{ background: '#e8f5e8', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
          <h3>Search Results:</h3>
          <pre>{JSON.stringify(hotelResults, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App