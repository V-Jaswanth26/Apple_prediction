import React, { useState, useEffect } from 'react';
import '../styles/App.css';

interface StockItem {
  date: string;
  close: number;
}

const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<StockItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/history")
      .then(res => res.json())
      .then(resData => {
        let extracted: StockItem[] = [];

        if (Array.isArray(resData)) extracted = resData;
        else if (resData.data) extracted = resData.data;
        else if (resData.history) extracted = resData.history;

        setData(extracted);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const metrics = (() => {
    if (data.length === 0) return null;

    const prices = data.map(d => d.close);
    const current = prices[prices.length - 1];
    const max = Math.max(...prices);
    const min = Math.min(...prices);
    const avg = prices.reduce((a, b) => a + b, 0) / prices.length;

    return {
      current,
      max,
      min,
      avg,
      volatility: ((max - min) / avg * 100).toFixed(2)
    };
  })();

  return (
    <div className="analytics-container">

      {/* Header */}
      <h2 className="page-title">📈 Apple Analytics</h2>

      {loading ? (
        <div className="loading-box">Loading...</div>
      ) : metrics ? (
        <>
          {/* 🔥 FIXED GRID */}
          <div className="analytics-grid">

            <div className="card blue">
              <h4>Current Price</h4>
              <p className="value">${metrics.current.toFixed(2)}</p>
            </div>

            <div className="card green">
              <h4>High</h4>
              <p className="value">${metrics.max.toFixed(2)}</p>
            </div>

            <div className="card orange">
              <h4>Low</h4>
              <p className="value">${metrics.min.toFixed(2)}</p>
            </div>

            <div className="card purple">
              <h4>Average</h4>
              <p className="value">${metrics.avg.toFixed(2)}</p>
            </div>

            <div className="card red">
              <h4>Volatility</h4>
              <p className="value">{metrics.volatility}%</p>
            </div>

            <div className="card gray">
              <h4>Total Records</h4>
              <p className="value">{data.length}</p>
            </div>

          </div>

          {/* Insights */}
          <div className="insights-box">
            <h3>📊 Insights</h3>
            <p>
              Over <b>{data.length}</b> trading days, price ranged between
              <b> ${metrics.min.toFixed(2)}</b> and
              <b> ${metrics.max.toFixed(2)}</b>.
            </p>
            <p>
              Market volatility is <b>{metrics.volatility}%</b>.
            </p>
          </div>
        </>
      ) : (
        <div className="loading-box">No data available</div>
      )}

    </div>
  );
};

export default AnalyticsPage;