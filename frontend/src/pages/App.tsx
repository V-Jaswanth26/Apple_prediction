import React, { useState, useEffect } from 'react';
import ChartPage from './ChartPage';
import AnalyticsPage from './AnalyticsPage';
import '../styles/App.css';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chart' | 'analytics'>('chart');

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <h1>🍎 Apple Stock Price Prediction</h1>
        <p>40-Year Historical Data Analysis</p>
      </header>
      
      {/* Prediction */}
      <div className="prediction-banner">
        <h2>Tomorrow's Prediction</h2>
        <div className="loading-prediction">
          Prediction ready
        </div>
      </div>
      
      {/* Tabs */}
      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'chart' ? 'active' : ''}`}
          onClick={() => setActiveTab('chart')}
        >
          📊 Price Chart
        </button>
        
        <button
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Analytics
        </button>
      </div>
      
      {/* Content */}
      <div className="tab-content">
        {activeTab === 'chart' && <ChartPage />}
        {activeTab === 'analytics' && <AnalyticsPage />}
      </div>
    </div>
  );
};

export default App;
