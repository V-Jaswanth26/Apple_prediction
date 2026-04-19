# Apple Stock Price Prediction (40-Year Time Series Analysis)

## Overview
Deep learning-based forecasting system for Apple Inc. stock prices using ~40 years of historical data with a modern, organized project structure.

## Features
- Historical data analysis (40 years of Apple stock data)
- LSTM-based time series prediction with 17 technical indicators
- Multi-timeframe forecasting (next day, week, month)
- Interactive visualization dashboard with Chart.js
- Modern React frontend with TypeScript
- RESTful API with Flask
- Docker containerization for easy deployment

## Tech Stack
- **Machine Learning**: TensorFlow, LSTM, Scikit-learn
- **Backend**: Flask, Flask-CORS
- **Frontend**: React, TypeScript, Chart.js
- **Data Source**: Yahoo Finance API
- **Deployment**: Docker, Docker Compose, Nginx

## Project Structure
```
apple-stock-prediction/
|
|--- backend/                 # Flask backend API
|   |--- api/                # API endpoints and routes
|   |   |--- app.py         # Main Flask application
|   |   |--- simple_app.py   # Simplified API version
|   |--- core/               # Core business logic
|   |   |--- model.py       # LSTM model architecture
|   |   |--- preprocessor.py # Data preprocessing pipeline
|   |--- services/           # Business services
|   |   |--- data_collector.py # Stock data collection
|   |   |--- train.py        # Model training pipeline
|   |   |--- predict.py      # Prediction service
|   |--- utils/              # Utility functions
|
|--- frontend/               # React frontend application
|   |--- src/
|   |   |--- components/     # React components
|   |   |   |--- StockChart.tsx # Stock chart component
|   |   |   |--- Analytics.tsx  # Analytics dashboard
|   |   |--- pages/          # Page components
|   |   |   |--- App.tsx     # Main application component
|   |   |   |--- index.tsx   # Entry point
|   |   |--- hooks/          # Custom React hooks
|   |   |--- services/       # API service functions
|   |   |--- utils/          # Utility functions
|   |   |--- types/          # TypeScript type definitions
|   |   |--- styles/         # CSS stylesheets
|
|--- data/                   # Historical stock data
|   |--- apple_stock_data.csv # 40 years of Apple stock data
|
|--- models/                 # Trained ML models and metrics
|   |--- apple_stock_lstm_model.h5 # Trained LSTM model
|   |--- training_history.json     # Training metrics
|   |--- evaluation_metrics.json   # Model evaluation results
|
|--- docs/                   # Project documentation
|   |--- PROJECT_STRUCTURE.md     # Detailed structure documentation
|   |--- DEPLOYMENT.md            # Deployment guide
|
|--- scripts/                # Utility scripts
|   |--- setup.sh               # Environment setup
|   |--- deploy.sh              # Deployment automation
|
|--- tests/                  # Test suites
|--- config/                 # Configuration files
|--- logs/                   # Application logs
|--- assets/                 # Static assets
|--- docker-compose.yml      # Docker orchestration
|--- requirements.txt        # Python dependencies
```

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone and setup
git clone <repository-url>
cd apple-stock-prediction

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start with Docker Compose
docker-compose up --build
```

### Option 2: Manual Setup
```bash
# Backend setup
cd backend
pip install -r ../requirements.txt
python api/simple_app.py

# Frontend setup (in another terminal)
cd frontend
npm install
npm start
```

## Usage
1. **Data Collection**: Automatically fetches 40 years of Apple stock data
2. **Model Training**: LSTM model trained on historical data with technical indicators
3. **Start Backend**: Flask API runs on http://localhost:5000
4. **Start Frontend**: React app runs on http://localhost:3000
5. **Access Application**: Open http://localhost:3000 in your browser

## API Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Next day prediction
- `POST /predict_multi` - Multi-day predictions
- `GET /history` - Historical data
- `GET /analytics` - Analytics and insights

## Model Features
- **Input Features**: 17 technical indicators (OHLCV, MA, RSI, MACD, Bollinger Bands, Stochastic)
- **Architecture**: 3-layer LSTM with Batch Normalization and Dropout
- **Sequence Length**: 60 days
- **Training Data**: 10,011 samples from 40 years of historical data
- **Performance**: MSE: 0.254, MAE: 0.443, RMSE: 0.504

## Development
```bash
# Run tests
cd backend && python -m pytest ../tests/
cd frontend && npm test

# Development mode
docker-compose -f docker-compose.yml up --build

# Production deployment
./scripts/deploy.sh production
```

## Important Disclaimer
This is a prediction aid, not financial advice. Stock markets are inherently unpredictable and external factors (news, economy, global events) are not included in this model. Always do your own research before making investment decisions.

## Evaluation Metrics
- **Mean Squared Error (MSE)**: 0.254
- **Root Mean Squared Error (RMSE)**: 0.504
- **Mean Absolute Error (MAE)**: 0.443

## Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Detailed folder organization
- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [API Documentation](docs/API_DOCUMENTATION.md) - API endpoint details

## Contributing
1. Follow the established folder structure
2. Update import paths when adding new files
3. Add tests for new features
4. Update documentation as needed
