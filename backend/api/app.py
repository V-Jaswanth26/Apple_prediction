from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta

from backend.services.data_collector import AppleStockDataCollector
from backend.core.preprocessor import StockDataPreprocessor
from backend.core.model import LSTMStockPredictor

app = Flask(__name__)
CORS(app)

# Global variables for model and preprocessor
model = None
preprocessor = None
data_collector = None

def initialize_model():
    """
    Initialize the model and preprocessor
    """
    global model, preprocessor, data_collector
    
    try:
        # Initialize components
        data_collector = AppleStockDataCollector()
        preprocessor = StockDataPreprocessor()
        
        # Load the trained model
        model_path = "models/apple_stock_lstm_model.h5"
        if os.path.exists(model_path):
            # Get input shape from data
            data = data_collector.load_data()
            if data is not None:
                data = preprocessor.handle_missing_values(data)
                data = preprocessor.add_technical_indicators(data)
                data = preprocessor.handle_missing_values(data)
                
                # Create a sample sequence to get input shape
                sample_X, _ = preprocessor.create_sequences(data, sequence_length=60)
                input_shape = (sample_X.shape[1], sample_X.shape[2])
                
                # Initialize and load model
                model = LSTMStockPredictor(input_shape)
                model.load_model(model_path)
                
                print("Model and preprocessor initialized successfully")
                return True
            else:
                print("No data available for initialization")
                return False
        else:
            print(f"Model file not found at {model_path}")
            return False
            
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        return False

@app.route('/')
def home():
    """
    Home endpoint
    """
    return jsonify({
        'message': 'Apple Stock Price Prediction API',
        'version': '1.0.0',
        'endpoints': [
            '/predict',
            '/predict_multi',
            '/history',
            '/model_info',
            '/health'
        ]
    })

@app.route('/health')
def health_check():
    """
    Health check endpoint
    """
    status = 'healthy' if model is not None else 'unhealthy'
    
    return jsonify({
        'status': status,
        'model_loaded': model is not None,
        'preprocessor_loaded': preprocessor is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/model_info')
def model_info():
    """
    Get model information
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    # Load evaluation metrics if available
    metrics_path = "../models/evaluation_metrics.json"
    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
    
    return jsonify({
        'model_type': 'LSTM',
        'input_shape': model.input_shape,
        'sequence_length': model.input_shape[0],
        'num_features': model.input_shape[1],
        'evaluation_metrics': metrics,
        'training_data': '40 years of Apple stock data (1986-2026)'
    })

@app.route('/history')
def get_history():
    """
    Get historical stock data
    """
    try:
        # Get query parameters
        days = request.args.get('days', 365, type=int)
        
        # Load data
        data = data_collector.load_data()
        if data is None:
            return jsonify({'error': 'No historical data available'}), 404
        
        # Filter to requested number of days
        if len(data) > days:
            data = data.tail(days)
        
        # Convert to JSON format
        history_data = []
        for _, row in data.iterrows():
            history_data.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume']),
                'ma_10': float(row['MA_10']) if pd.notna(row['MA_10']) else None,
                'ma_50': float(row['MA_50']) if pd.notna(row['MA_50']) else None,
                'ma_200': float(row['MA_200']) if pd.notna(row['MA_200']) else None,
                'rsi': float(row['RSI']) if pd.notna(row['RSI']) else None
            })
        
        return jsonify({
            'data': history_data,
            'total_records': len(history_data),
            'date_range': {
                'start': history_data[0]['date'] if history_data else None,
                'end': history_data[-1]['date'] if history_data else None
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict next day's stock price
    """
    try:
        if model is None or preprocessor is None:
            initialize_model()
        
        # Get data from request (optional, if not provided use latest data)
        request_data = request.get_json()
        
        # Load latest data
        data = data_collector.load_data()
        if data is None:
            return jsonify({'error': 'No data available for prediction'}), 404
        
        # Preprocess data
        data = preprocessor.handle_missing_values(data)
        data = preprocessor.add_technical_indicators(data)
        data = preprocessor.handle_missing_values(data)
        
        # Get last 60 days for prediction
        last_60_days = data.tail(60)
        
        # Create prediction input
        prediction_input = preprocessor.create_prediction_input(last_60_days, sequence_length=60)
        
        # Make prediction
        prediction = model.predict(prediction_input)
        
        # Inverse transform to get actual price
        predicted_price = preprocessor.inverse_transform_predictions(
            prediction, prediction_input.shape[2]
        )[0]
        
        # Get current price for comparison
        current_price = float(data['Close'].iloc[-1])
        
        return jsonify({
            'predicted_price': round(predicted_price, 2),
            'current_price': round(current_price, 2),
            'price_change': round(predicted_price - current_price, 2),
            'price_change_percent': round(((predicted_price - current_price) / current_price) * 100, 2),
            'prediction_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_multi', methods=['POST'])
def predict_multi():
    """
    Predict multiple future days (1, 7, 30 days)
    """
    try:
        if model is None or preprocessor is None:
            initialize_model()
        
        # Get number of days from request
        request_data = request.get_json()
        days_to_predict = request_data.get('days', 7) if request_data else 7
        
        # Validate days_to_predict
        if days_to_predict not in [1, 7, 30]:
            return jsonify({'error': 'Days to predict must be 1, 7, or 30'}), 400
        
        # Load latest data
        data = data_collector.load_data()
        if data is None:
            return jsonify({'error': 'No data available for prediction'}), 404
        
        # Preprocess data
        data = preprocessor.handle_missing_values(data)
        data = preprocessor.add_technical_indicators(data)
        data = preprocessor.handle_missing_values(data)
        
        # Get last 60 days for prediction
        last_60_days = data.tail(60)
        
        # Create prediction input
        prediction_input = preprocessor.create_prediction_input(last_60_days, sequence_length=60)
        
        # Get the actual sequence for multi-day prediction
        features = last_60_days[preprocessor.feature_columns].values
        scaled_features = preprocessor.scaler.transform(features)
        last_sequence = scaled_features[-60:]
        
        # Make multi-day predictions
        predictions = model.predict_next_days(
            last_sequence, 
            days_to_predict, 
            preprocessor.scaler
        )
        
        # Create response with dates
        current_date = datetime.now()
        prediction_data = []
        
        for i, pred_price in enumerate(predictions):
            future_date = current_date + timedelta(days=i+1)
            prediction_data.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_price': round(float(pred_price), 2)
            })
        
        # Calculate overall trend
        if len(predictions) > 1:
            trend = 'up' if predictions[-1] > predictions[0] else 'down'
            total_change = predictions[-1] - predictions[0]
            total_change_percent = (total_change / predictions[0]) * 100
        else:
            trend = 'neutral'
            total_change = 0
            total_change_percent = 0
        
        return jsonify({
            'predictions': prediction_data,
            'days_predicted': days_to_predict,
            'trend': trend,
            'total_change': round(float(total_change), 2),
            'total_change_percent': round(float(total_change_percent), 2),
            'base_price': round(float(data['Close'].iloc[-1]), 2),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def get_analytics():
    """
    Get analytics and insights
    """
    try:
        # Load data
        data = data_collector.load_data()
        if data is None:
            return jsonify({'error': 'No data available'}), 404
        
        # Calculate basic statistics
        current_price = float(data['Close'].iloc[-1])
        price_52w_high = float(data['Close'].tail(252).max())  # 52 weeks = 252 trading days
        price_52w_low = float(data['Close'].tail(252).min())
        
        # Calculate moving averages
        ma_50 = float(data['Close'].tail(50).mean())
        ma_200 = float(data['Close'].tail(200).mean())
        
        # Calculate volatility (last 30 days)
        daily_returns = data['Close'].pct_change().tail(30)
        volatility = float(daily_returns.std() * np.sqrt(252))  # Annualized volatility
        
        # RSI current value
        current_rsi = float(data['RSI'].iloc[-1]) if pd.notna(data['RSI'].iloc[-1]) else None
        
        return jsonify({
            'current_price': round(current_price, 2),
            'price_52w_high': round(price_52w_high, 2),
            'price_52w_low': round(price_52w_low, 2),
            'ma_50': round(ma_50, 2),
            'ma_200': round(ma_200, 2),
            'volatility': round(volatility * 100, 2),  # As percentage
            'current_rsi': round(current_rsi, 2) if current_rsi else None,
            'price_vs_ma50': round(((current_price - ma_50) / ma_50) * 100, 2),
            'price_vs_ma200': round(((current_price - ma_200) / ma_200) * 100, 2),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize model before starting the server
    if initialize_model():
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to initialize model. Exiting...")
