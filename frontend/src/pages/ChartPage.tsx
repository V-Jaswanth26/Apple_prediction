import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';
import '../styles/App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface StockItem {
  date: string;
  close: number;
}

const ChartPage: React.FC = () => {
  const [data, setData] = useState<StockItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('30');

  useEffect(() => {
    fetch("http://127.0.0.1:5000/history")
      .then(res => res.json())
      .then(resData => {
        console.log("API DATA:", resData);

        let extracted: StockItem[] = [];

        if (Array.isArray(resData)) {
          extracted = resData;
        } else if (resData.data && Array.isArray(resData.data)) {
          extracted = resData.data;
        } else if (resData.history && Array.isArray(resData.history)) {
          extracted = resData.history;
        } else {
          console.error("Unexpected API format");
        }

        setData(extracted);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fetch error:", err);
        setLoading(false);
      });
  }, []);

  const refreshData = () => {
    setLoading(true);
    fetch("http://127.0.0.1:5000/history")
      .then(res => res.json())
      .then(resData => {
        let extracted: StockItem[] = [];
        if (Array.isArray(resData)) {
          extracted = resData;
        } else if (resData.data && Array.isArray(resData.data)) {
          extracted = resData.data;
        }
        setData(extracted);
        setLoading(false);
      })
      .catch(err => {
        console.error("Refresh error:", err);
        setLoading(false);
      });
  };

  const filteredData = data.slice(-parseInt(selectedPeriod));

  const chartData = {
    labels: filteredData.map(item => new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: 'Apple Stock Price',
        data: filteredData.map(item => item.close),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 3,
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          font: {
            size: 14,
            weight: 'bold' as const,
          },
          color: '#1e293b',
        }
      },
      title: {
        display: true,
        text: `Apple Stock Price - Last ${selectedPeriod} Days`,
        font: {
          size: 18,
          weight: 'bold' as const,
        },
        color: '#1e293b',
        padding: 20,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
        displayColors: false,
        callbacks: {
          label: function(context: any) {
            return `Price: $${context.parsed.y.toFixed(2)}`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          color: '#64748b',
          font: {
            size: 12,
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          color: '#64748b',
          font: {
            size: 12,
          },
          callback: function(value: any) {
            return '$' + value.toFixed(0);
          }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index' as const,
    },
    elements: {
      point: {
        hoverRadius: 8,
      }
    }
  };

  return (
    <div className="stock-chart">
      <div className="chart-header">
        <h2>📊 Stock Price Chart</h2>
        <div className="chart-info">
          <span className="data-count">{data.length} data points</span>
          <span className="last-updated">
            Last: {data.length > 0 ? new Date(data[data.length - 1].date).toLocaleDateString() : 'N/A'}
          </span>
        </div>
      </div>
      
      {loading ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading chart data...</p>
        </div>
      ) : data.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📊</div>
          <h3>No Data Available</h3>
          <p>Unable to load stock data. Please check your connection and try again.</p>
          <button onClick={refreshData} className="refresh-btn">
            🔄 Refresh Data
          </button>
        </div>
      ) : (
        <div className="chart-content">
          <div className="chart-visualization">
            <div className="chart-placeholder">
              <div className="chart-image-container" style={{ height: '500px', width: '100%' }}>
                <Line data={chartData} options={chartOptions} />
              </div>
            </div>
          </div>
          
          <div className="chart-controls">
            <div className="control-group">
              <label htmlFor="period-select">📅 Time Period:</label>
              <select 
                id="period-select"
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="period-select"
              >
                <option value="7">7 Days</option>
                <option value="30">30 Days</option>
                <option value="90">90 Days</option>
                <option value="180">180 Days</option>
                <option value="365">1 Year</option>
              </select>
            </div>
            
            <div className="control-group">
              <button onClick={refreshData} className="control-btn refresh-btn">
                🔄 Refresh
              </button>
              <button className="control-btn predict-btn">
                🔮 Predict 7 Days
              </button>
              <button className="control-btn predict-btn">
                🔮 Predict 30 Days
              </button>
            </div>
          </div>
          
          <div className="chart-stats">
            <h3>📈 Current Statistics</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Current Price</span>
                <span className="stat-value" style={{
                  background: 'linear-gradient(135deg, #3b82f6, #1e40af)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>
                  ${filteredData.length > 0 ? filteredData[filteredData.length - 1].close.toFixed(2) : 'N/A'}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Period High</span>
                <span className="stat-value positive" style={{
                  background: 'linear-gradient(135deg, #10b981, #059669)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>
                  ${filteredData.length > 0 ? Math.max(...filteredData.map(d => d.close)).toFixed(2) : 'N/A'}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Period Low</span>
                <span className="stat-value negative" style={{
                  background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>
                  ${filteredData.length > 0 ? Math.min(...filteredData.map(d => d.close)).toFixed(2) : 'N/A'}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Average</span>
                <span className="stat-value" style={{
                  background: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>
                  ${filteredData.length > 0 ? 
                    (filteredData.reduce((sum, d) => sum + d.close, 0) / filteredData.length).toFixed(2)
                    : 'N/A'
                  }
                </span>
              </div>
            </div>
          </div>
          
                  </div>
      )}
    </div>
  );
};

export default ChartPage;
