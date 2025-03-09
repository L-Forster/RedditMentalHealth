import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDisorders, setSelectedDisorders] = useState([
    'depression', 'schizophrenia', 'npd', 'adhd', 'bipolar', 'aspd'
  ]);

  const toggleDisorder = (disorder) => {
    if (selectedDisorders.includes(disorder)) {
      setSelectedDisorders(selectedDisorders.filter(d => d !== disorder));
    } else {
      setSelectedDisorders([...selectedDisorders, disorder]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username) {
      setError("Please enter a username");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const analysisResults = [];

      // Only analyze selected disorders
      for (const disorder of selectedDisorders) {
        const response = await fetch('http://localhost:5000/api/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            subreddit: disorder,
            username: username,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || `Error analyzing ${disorder}`);
        }

        // Extract probability value
        let probability = 0;
        if (typeof data.result === 'number') {
          probability = data.result;
        } else if (Array.isArray(data.result) && data.result.length > 1) {
          probability = data.result[1];
        }

        // Add to results for display
        analysisResults.push({
          name: disorder,
          probability: probability,
          displayName: disorder.charAt(0).toUpperCase() + disorder.slice(1),
          color: probability > 0.6 ? '#FF0000' : '#008080' // Red if > 0.6, Teal otherwise
        });
      }

      // Sort results by name
      analysisResults.sort((a, b) => a.name.localeCompare(b.name));
      setResults(analysisResults);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const availableDisorders = [
    { id: 'bipolar', label: 'Bipolar' },
    { id: 'depression', label: 'Depression' },
    { id: 'aspd', label: 'aspd' },
    { id: 'schizophrenia', label: 'Schizophrenia' },
    { id: 'npd', label: 'NPD' },
    { id: 'bipolar', label: 'bipolar' }
  ];
    // 'depression', 'schizophrenia', 'npd', 'adhd', 'bipolar', 'aspd'

  return (
    <div className="App">
      <header className="App-header">
        <h1>Reddit Mental Health Analyzer</h1>
      </header>
      <main>
        <section className="disorder-selection">
          <h2>Select Disorders to Analyze</h2>
          <div className="disorder-checkboxes">
            {availableDisorders.map(disorder => (
              <div key={disorder.id} className="disorder-checkbox">
                <input
                  type="checkbox"
                  id={`disorder-${disorder.id}`}
                  checked={selectedDisorders.includes(disorder.id)}
                  onChange={() => toggleDisorder(disorder.id)}
                />
                <label htmlFor={`disorder-${disorder.id}`}>{disorder.label}</label>
              </div>
            ))}
          </div>
        </section>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Reddit Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter Reddit username"
              required
            />
          </div>

          <button type="submit" disabled={loading || selectedDisorders.length === 0}>
            {loading ? 'Analyzing...' : 'Analyze User'}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {loading && <div className="loading">Analyzing user data across selected disorders...</div>}

        {results && (
          <div className="results">
            <h2>Analysis Results for u/{username}</h2>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart
                  data={results}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="displayName" angle={-45} textAnchor="end" />
                  <YAxis
                    label={{ value: 'Probability', angle: -90, position: 'insideLeft' }}
                    domain={[0, 1]}
                  />
                  <Tooltip formatter={(value) => `${(value * 100).toFixed(2)}%`} />
                  <Legend />
                  <Bar
                    dataKey="probability"
                    name="Probability Score"
                    fill={(entry) => entry.color}
                    isAnimationActive={true}
                  >
                    {results.map((entry, index) => (
                      <Bar
                        key={`bar-${index}`}
                        dataKey="probability"
                        name={entry.displayName}
                        fill={entry.color}
                        data={[entry]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
export default App;