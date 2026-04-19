import React from 'react';
import ReactDOM from 'react-dom/client';
import '../styles/index.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="app-header">
        <h1>🍎 Apple Stock Price Prediction</h1>
        <p>40-Year Historical Data Analysis with LSTM Deep Learning</p>
      </header>
      
      <div className="prediction-banner">
        <h2>Tomorrow's Prediction</h2>
        <div className="loading-prediction">Loading prediction...</div>
      </div>

      <div className="tab-navigation">
        <button className="tab-button active">📊 Price Chart</button>
        <button className="tab-button">📈 Analytics</button>
      </div>

      <div className="tab-content">
        <div>Chart component will be here</div>
      </div>

      <footer className="app-footer">
        <p>
          <strong>Disclaimer:</strong> This is for educational purposes only. 
          Stock predictions are not financial advice. Always consult with qualified 
          financial advisors before making investment decisions.
        </p>
      </footer>
    </div>
  );
};

export default App;
