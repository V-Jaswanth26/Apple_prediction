# Apple Stock Price Prediction - Project Structure

## Overview
This document outlines the organized folder structure for the Apple Stock Price Prediction project.

## Root Directory Structure

```
apple-stock-prediction/
|
|--- backend/                 # Flask backend API
|--- frontend/               # React frontend application
|--- data/                   # Historical stock data
|--- models/                 # Trained ML models and metrics
|--- notebooks/              # Jupyter notebooks for analysis
|--- docs/                   # Project documentation
|--- scripts/                # Utility scripts
|--- tests/                  # Test suites
|--- config/                 # Configuration files
|--- logs/                   # Application logs
|--- assets/                 # Static assets
|--- docker-compose.yml      # Docker orchestration
|--- requirements.txt        # Python dependencies
|--- README.md              # Project overview
|--- DEPLOYMENT.md          # Deployment guide
```

## Backend Structure (`backend/`)

```
backend/
|
|--- api/                    # API endpoints and routes
|   |--- app.py             # Main Flask application
|   |--- simple_app.py      # Simplified API version
|
|--- core/                   # Core business logic
|   |--- model.py           # LSTM model architecture
|   |--- preprocessor.py    # Data preprocessing pipeline
|
|--- services/              # Business services
|   |--- data_collector.py  # Stock data collection
|   |--- train.py           # Model training pipeline
|   |--- predict.py         # Prediction service
|
|--- utils/                  # Utility functions
|--- Dockerfile             # Docker configuration
|--- __pycache__/           # Python cache files
```

## Frontend Structure (`frontend/`)

```
frontend/
|
|--- public/                 # Static public assets
|--- src/                    # Source code
|   |--- components/         # React components
|   |   |--- StockChart.tsx  # Stock chart component
|   |   |--- Analytics.tsx   # Analytics dashboard
|   |
|   |--- pages/              # Page components
|   |   |--- App.tsx         # Main application component
|   |   |--- index.tsx       # Entry point
|   |
|   |--- hooks/              # Custom React hooks
|   |--- services/           # API service functions
|   |--- utils/              # Utility functions
|   |--- types/              # TypeScript type definitions
|   |--- styles/             # CSS stylesheets
|   |   |--- App.css         # Main application styles
|   |   |--- index.css       # Global styles
|   |
|--- package.json            # Node dependencies
|--- tsconfig.json           # TypeScript configuration
|--- Dockerfile              # Docker configuration
|--- nginx.conf              # Nginx configuration
```

## Data Structure (`data/`)

```
data/
|
|--- apple_stock_data.csv   # 40 years of Apple stock data
```

## Models Structure (`models/`)

```
models/
|
|--- apple_stock_lstm_model.h5    # Trained LSTM model
|--- training_history.json        # Training metrics
|--- evaluation_metrics.json      # Model evaluation results
|--- predictions.png              # Prediction visualizations
|--- training_history.png         # Training history plots
```

## Documentation (`docs/`)

```
docs/
|
|--- PROJECT_STRUCTURE.md         # This file
|--- API_DOCUMENTATION.md         # API endpoints documentation
|--- MODEL_DOCUMENTATION.md       # ML model documentation
```

## Scripts (`scripts/`)

```
scripts/
|
|--- setup.sh                  # Environment setup script
|--- deploy.sh                  # Deployment script
|--- backup.sh                  # Data backup script
```

## Tests (`tests/`)

```
tests/
|
|--- backend/                   # Backend tests
|   |--- test_api.py           # API endpoint tests
|   |--- test_model.py         # Model tests
|
|--- frontend/                  # Frontend tests
|   |--- components/          # Component tests
|   |--- services/            # Service tests
```

## Configuration (`config/`)

```
config/
|
|--- development.json          # Development configuration
|--- production.json           # Production configuration
|--- testing.json               # Testing configuration
```

## Logs (`logs/`)

```
logs/
|
|--- app.log                   # Application logs
|--- error.log                 # Error logs
|--- access.log                # Access logs
```

## Assets (`assets/`)

```
assets/
|
|--- images/                   # Static images
|--- icons/                    # Application icons
|--- fonts/                    # Custom fonts
```

## File Purposes

### Backend Files
- **api/app.py**: Main Flask application with all API endpoints
- **api/simple_app.py**: Simplified version for easier deployment
- **core/model.py**: LSTM neural network architecture and training logic
- **core/preprocessor.py**: Data preprocessing and feature engineering
- **services/data_collector.py**: Yahoo Finance API integration
- **services/train.py**: Model training pipeline
- **services/predict.py**: Prediction service wrapper

### Frontend Files
- **pages/App.tsx**: Main React application component
- **pages/index.tsx**: Application entry point
- **components/StockChart.tsx**: Interactive stock chart component
- **components/Analytics.tsx**: Analytics dashboard component
- **styles/App.css**: Main application styles

### Configuration Files
- **docker-compose.yml**: Multi-container Docker setup
- **requirements.txt**: Python dependencies
- **package.json**: Node.js dependencies
- **tsconfig.json**: TypeScript configuration
- **nginx.conf**: Nginx reverse proxy configuration

## Import Path Updates

After restructuring, the following import paths need to be updated:

### Backend Imports
```python
# Old imports
from data_collector import AppleStockDataCollector
from model import StockPredictor
from preprocessor import StockDataPreprocessor

# New imports
from services.data_collector import AppleStockDataCollector
from core.model import StockPredictor
from core.preprocessor import StockDataPreprocessor
```

### Frontend Imports
```typescript
// Old imports
import StockChart from './components/StockChart';
import Analytics from './components/Analytics';
import './App.css';

// New imports
import StockChart from '../components/StockChart';
import Analytics from '../components/Analytics';
import '../styles/App.css';
```

## Benefits of This Structure

1. **Separation of Concerns**: Clear separation between API, core logic, and services
2. **Scalability**: Easy to add new features without clutter
3. **Maintainability**: Organized structure makes code easier to find and modify
4. **Testing**: Dedicated test directories for comprehensive testing
5. **Documentation**: Centralized documentation for better knowledge sharing
6. **Configuration**: Environment-specific configurations
7. **Logging**: Centralized logging for better debugging

## Next Steps

1. Update all import statements in the codebase
2. Update Docker configurations to reflect new structure
3. Create initialization scripts for new directories
4. Update deployment documentation
5. Add proper __init__.py files for Python packages
