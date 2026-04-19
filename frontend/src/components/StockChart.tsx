import React, { useState, useEffect, useCallback } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface StockData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  ma_10?: number;
  ma_50?: number;
  ma_200?: number;
  rsi?: number;
}

interface PredictionData {
  date: string;
  predicted_price: number;
}

const StockChart: React.FC = () => {
  const [historicalData, setHistoricalData] = useState<StockData[]>([]);
  const [predictions, setPredictions] = useState<PredictionData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [daysToShow, setDaysToShow] = useState(365);

  const fetchHistoricalData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(`https://apple-prediction-spyn.onrender.com/history?days=${daysToShow}`);
      setHistoricalData(response.data.data);
    } catch (err) {
      setError('Failed to fetch historical data');
      console.error('Error fetching historical data:', err);
    } finally {
      setLoading(false);
    }
  }, [daysToShow]);

  const fetchPredictions = useCallback(async (days: number = 7) => {
    try {
      const response = await axios.post('https://apple-prediction-spyn.onrender.com/predict_multi', { days });
      setPredictions(response.data.predictions);
    } catch (err) {
      setError('Failed to fetch predictions');
      console.error('Error fetching predictions:', err);
    }
  }, []);

  useEffect(() => {
    fetchHistoricalData();
  }, [fetchHistoricalData]);

  const chartData = {
    labels: [
      ...historicalData.map((item: StockData) => item.date),
      ...predictions.map((item: PredictionData) => item.date)
    ],
    datasets: [
      {
        label: 'Close Price',
        data: historicalData.map((item: StockData) => item.close),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
      {
        label: 'MA 50',
        data: historicalData.map((item: StockData) => item.ma_50 || null),
        borderColor: 'rgb(255, 206, 86)',
        backgroundColor: 'rgba(255, 206, 86, 0.2)',
        tension: 0.1,
        hidden: false,
      },
      {
        label: 'MA 200',
        data: historicalData.map((item: StockData) => item.ma_200 || null),
        borderColor: 'rgb(153, 102, 255)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        tension: 0.1,
        hidden: false,
      },
      {
        label: 'Predictions',
        data: [
          ...Array(historicalData.length - 1).fill(null),
          historicalData[historicalData.length - 1]?.close || null,
          ...predictions.map((item: PredictionData) => item.predicted_price)
        ],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderDash: [5, 5],
        tension: 0.1,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Apple Stock Price Prediction',
      },
    },
    scales: {
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        title: {
          display: true,
          text: 'Price ($)',
        },
      },
      x: {
        type: 'category' as const,
        display: true,
        title: {
          display: true,
          text: 'Date',
        },
      },
    },
  };

  if (loading) {
    return <div className="loading">Loading chart data...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="stock-chart">
      <div className="chart-controls">
        <div className="control-group">
          <label htmlFor="days-select">Historical Days:</label>
          <select
            id="days-select"
            value={daysToShow}
            onChange={(e) => setDaysToShow(Number(e.target.value))}
          >
            <option value={30}>30 Days</option>
            <option value={90}>90 Days</option>
            <option value={180}>180 Days</option>
            <option value={365}>1 Year</option>
            <option value={730}>2 Years</option>
          </select>
        </div>
        
        <div className="control-group">
          <button onClick={() => fetchPredictions(1)}>Predict 1 Day</button>
          <button onClick={() => fetchPredictions(7)}>Predict 7 Days</button>
          <button onClick={() => fetchPredictions(30)}>Predict 30 Days</button>
        </div>
      </div>
      
      <div className="chart-container">
        <Line data={chartData} options={options} />
      </div>
      
      {predictions.length > 0 && (
        <div className="predictions-summary">
          <h3>Prediction Summary</h3>
          <p>Trend: <strong>{predictions[predictions.length - 1]?.predicted_price > predictions[0]?.predicted_price ? 'UP' : 'DOWN'}</strong></p>
          <p>Start Price: ${predictions[0]?.predicted_price?.toFixed(2)}</p>
          <p>End Price: ${predictions[predictions.length - 1]?.predicted_price?.toFixed(2)}</p>
          <p>Change: ${((predictions[predictions.length - 1]?.predicted_price || 0) - (predictions[0]?.predicted_price || 0)).toFixed(2)}</p>
        </div>
      )}
    </div>
  );
};

export default StockChart;
