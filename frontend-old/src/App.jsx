// STAYFINDR Multi-Platform Frontend
import { useState, useEffect } from 'react';

function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [searchResult, setSearchResult] = useState(null);

  // Test backend connection
  useEffect(() => {
    fetch('http://localhost:5000')
      .then(res => res.json())
      .then(data => setApiStatus(data))
      .catch(err => console.error('Backend connection failed:', err));
  }, []);

  const testSearch = () => {
    fetch('http://localhost:5000/api/hotels/search?city=stockholm&checkin=2025-07-15&checkout=2025-07-17')
      .then(res => res.json())
      .then(data => setSearchResult(data))
      .catch(err => console.error('Search failed:', err));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🏨 STAYFINDR Multi-Platform</h1>
      <p>One Search, All Platforms</p>
      
      <div style={{ marginBottom: '20px', padding: '15px', background: '#f0f0f0', borderRadius: '8px' }}>
        <h3>Backend Status:</h3>
        {apiStatus ? (
          <div>
            <p>✅ {apiStatus.message}</p>
            <p>Version: {apiStatus.version}</p>
            <p>Platforms: {Object.entries(apiStatus.platforms).map(([name, enabled]) => 
              `${name}: ${enabled ? '✅' : '❌'}`).join(', ')}</p>
          </div>
        ) : (
          <p>🔄 Connecting to backend...</p>
        )}
      </div>

      <button 
        onClick={testSearch}
        style={{ 
          padding: '10px 20px', 
          background: '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        🔍 Test Hotel Search
      </button>

      {searchResult && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#e8f5e8', borderRadius: '8px' }}>
          <h3>Search Result:</h3>
          <pre>{JSON.stringify(searchResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;