import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface AnalyticsData {
  current_price: number;
  price_52w_high: number;
  price_52w_low: number;
  ma_50: number;
  ma_200: number;
  volatility: number;
  current_rsi?: number;
  price_vs_ma50: number;
  price_vs_ma200: number;
  last_updated: string;
}

const Analytics: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get('http://localhost:5000/analytics');
      setAnalytics(response.data);
    } catch (err) {
      setError('Failed to fetch analytics data');
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!analytics) {
    return <div className="loading">No analytics data available</div>;
  }

  return (
    <div className="analytics">
      <h2>Stock Analytics & Insights</h2>
      
      <div className="analytics-grid">
        <div className="analytics-card">
          <h3>Current Price</h3>
          <div className="metric-value">${analytics.current_price.toFixed(2)}</div>
        </div>
        
        <div className="analytics-card">
          <h3>52-Week Range</h3>
          <div className="metric-range">
            <div className="range-high">High: ${analytics.price_52w_high.toFixed(2)}</div>
            <div className="range-low">Low: ${analytics.price_52w_low.toFixed(2)}</div>
          </div>
        </div>
        
        <div className="analytics-card">
          <h3>Moving Averages</h3>
          <div className="metric-values">
            <div className="ma-item">
              <span className="ma-label">MA 50:</span>
              <span className="ma-value">${analytics.ma_50.toFixed(2)}</span>
            </div>
            <div className="ma-item">
              <span className="ma-label">MA 200:</span>
              <span className="ma-value">${analytics.ma_200.toFixed(2)}</span>
            </div>
          </div>
        </div>
        
        <div className="analytics-card">
          <h3>Price vs MA</h3>
          <div className="metric-values">
            <div className="vs-item">
              <span className="vs-label">vs MA 50:</span>
              <span className={`vs-value ${analytics.price_vs_ma50 >= 0 ? 'positive' : 'negative'}`}>
                {analytics.price_vs_ma50 >= 0 ? '+' : ''}{analytics.price_vs_ma50.toFixed(2)}%
              </span>
            </div>
            <div className="vs-item">
              <span className="vs-label">vs MA 200:</span>
              <span className={`vs-value ${analytics.price_vs_ma200 >= 0 ? 'positive' : 'negative'}`}>
                {analytics.price_vs_ma200 >= 0 ? '+' : ''}{analytics.price_vs_ma200.toFixed(2)}%
              </span>
            </div>
          </div>
        </div>
        
        <div className="analytics-card">
          <h3>Volatility</h3>
          <div className="metric-value">{analytics.volatility.toFixed(2)}%</div>
          <div className="metric-description">Annualized volatility</div>
        </div>
        
        {analytics.current_rsi && (
          <div className="analytics-card">
            <h3>RSI</h3>
            <div className="metric-value">{analytics.current_rsi.toFixed(2)}</div>
            <div className={`rsi-indicator ${
              analytics.current_rsi > 70 ? 'overbought' : 
              analytics.current_rsi < 30 ? 'oversold' : 'neutral'
            }`}>
              {analytics.current_rsi > 70 ? 'Overbought' : 
               analytics.current_rsi < 30 ? 'Oversold' : 'Neutral'}
            </div>
          </div>
        )}
      </div>
      
      <div className="analytics-insights">
        <h3>Technical Analysis Insights</h3>
        <ul>
          <li>
            <strong>Trend Analysis:</strong> {
              analytics.current_price > analytics.ma_50 && analytics.ma_50 > analytics.ma_200 
                ? 'Strong Uptrend (Price > MA50 > MA200)' 
                : analytics.current_price > analytics.ma_50 
                  ? 'Uptrend (Price > MA50)' 
                  : 'Downtrend (Price < MA50)'
            }
          </li>
          <li>
            <strong>Volatility:</strong> {
              analytics.volatility > 30 
                ? 'High volatility expected' 
                : analytics.volatility > 20 
                  ? 'Moderate volatility' 
                  : 'Low volatility'
            }
          </li>
          {analytics.current_rsi && (
            <li>
              <strong>RSI Signal:</strong> {
                analytics.current_rsi > 70 
                  ? 'Stock may be overbought - consider taking profits' 
                  : analytics.current_rsi < 30 
                    ? 'Stock may be oversold - potential buying opportunity' 
                    : 'RSI is in neutral zone'
              }
            </li>
          )}
          <li>
            <strong>Price Position:</strong> Current price is {
              analytics.current_price >= analytics.price_52w_high * 0.95 
                ? 'near 52-week high levels' 
                : analytics.current_price <= analytics.price_52w_low * 1.05 
                  ? 'near 52-week low levels' 
                  : 'in the middle of 52-week range'
            }
          </li>
        </ul>
      </div>
      
      <div className="last-updated">
        Last updated: {new Date(analytics.last_updated).toLocaleString()}
      </div>
    </div>
  );
};

export default Analytics;
