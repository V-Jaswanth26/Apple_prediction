import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta

from services.data_collector import AppleStockDataCollector
from core.preprocessor import StockDataPreprocessor
from core.model import LSTMStockPredictor

class StockPredictionService:
    def __init__(self):
        self.data_collector = AppleStockDataCollector()
        self.preprocessor = StockDataPreprocessor()
        self.model = None
        self.is_initialized = False
        
    def initialize(self):
        """
        Initialize the prediction service
        """
        try:
            # Load the trained model
            model_path = "../models/apple_stock_lstm_model.h5"
            if not os.path.exists(model_path):
                print(f"Model file not found at {model_path}")
                return False
            
            # Load data to get input shape
            data = self.data_collector.load_data()
            if data is None:
                print("No data available for initialization")
                return False
            
            # Preprocess data to get the correct shape
            data = self.preprocessor.handle_missing_values(data)
            data = self.preprocessor.add_technical_indicators(data)
            data = self.preprocessor.handle_missing_values(data)
            
            # Create a sample sequence to get input shape
            sample_X, _ = self.preprocessor.create_sequences(data, sequence_length=60)
            input_shape = (sample_X.shape[1], sample_X.shape[2])
            
            # Initialize and load model
            self.model = LSTMStockPredictor(input_shape)
            
            # Try to load the model with error handling
            try:
                self.model.load_model(model_path)
                self.is_initialized = True
                print("Model loaded successfully")
                return True
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                # Try alternative loading method
                try:
                    import tensorflow as tf
                    self.model.model = tf.keras.models.load_model(model_path, compile=False)
                    self.model.model.compile(optimizer='adam', loss='mse')
                    self.is_initialized = True
                    print("Model loaded with alternative method")
                    return True
                except Exception as e2:
                    print(f"Alternative loading also failed: {str(e2)}")
                    return False
                    
        except Exception as e:
            print(f"Error initializing service: {str(e)}")
            return False
    
    def predict_next_day(self):
        """
        Predict next day's stock price
        """
        if not self.is_initialized:
            return {'error': 'Service not initialized'}
        
        try:
            # Load latest data
            data = self.data_collector.load_data()
            if data is None:
                return {'error': 'No data available for prediction'}
            
            # Preprocess data
            data = self.preprocessor.handle_missing_values(data)
            data = self.preprocessor.add_technical_indicators(data)
            data = self.preprocessor.handle_missing_values(data)
            
            # Get last 60 days for prediction
            last_60_days = data.tail(60)
            
            # Create prediction input
            prediction_input = self.preprocessor.create_prediction_input(last_60_days, sequence_length=60)
            
            # Make prediction
            prediction = self.model.predict(prediction_input)
            
            # Inverse transform to get actual price
            predicted_price = self.preprocessor.inverse_transform_predictions(
                prediction, prediction_input.shape[2]
            )[0]
            
            # Get current price for comparison
            current_price = float(data['Close'].iloc[-1])
            
            return {
                'predicted_price': round(predicted_price, 2),
                'current_price': round(current_price, 2),
                'price_change': round(predicted_price - current_price, 2),
                'price_change_percent': round(((predicted_price - current_price) / current_price) * 100, 2),
                'prediction_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def predict_multi_days(self, days_to_predict=7):
        """
        Predict multiple future days
        """
        if not self.is_initialized:
            return {'error': 'Service not initialized'}
        
        if days_to_predict not in [1, 7, 30]:
            return {'error': 'Days to predict must be 1, 7, or 30'}
        
        try:
            # Load latest data
            data = self.data_collector.load_data()
            if data is None:
                return {'error': 'No data available for prediction'}
            
            # Preprocess data
            data = self.preprocessor.handle_missing_values(data)
            data = self.preprocessor.add_technical_indicators(data)
            data = self.preprocessor.handle_missing_values(data)
            
            # Get last 60 days for prediction
            last_60_days = data.tail(60)
            
            # Create prediction input
            prediction_input = self.preprocessor.create_prediction_input(last_60_days, sequence_length=60)
            
            # Get the actual sequence for multi-day prediction
            features = last_60_days[self.preprocessor.feature_columns].values
            scaled_features = self.preprocessor.scaler.transform(features)
            last_sequence = scaled_features[-60:]
            
            # Make multi-day predictions
            predictions = self.model.predict_next_days(
                last_sequence, 
                days_to_predict, 
                self.preprocessor.scaler
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
            
            return {
                'predictions': prediction_data,
                'days_predicted': days_to_predict,
                'trend': trend,
                'total_change': round(float(total_change), 2),
                'total_change_percent': round(float(total_change_percent), 2),
                'base_price': round(float(data['Close'].iloc[-1]), 2),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_historical_data(self, days=365):
        """
        Get historical stock data
        """
        try:
            # Load data
            data = self.data_collector.load_data()
            if data is None:
                return {'error': 'No historical data available'}
            
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
            
            return {
                'data': history_data,
                'total_records': len(history_data),
                'date_range': {
                    'start': history_data[0]['date'] if history_data else None,
                    'end': history_data[-1]['date'] if history_data else None
                }
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_analytics(self):
        """
        Get analytics and insights
        """
        try:
            # Load data
            data = self.data_collector.load_data()
            if data is None:
                return {'error': 'No data available'}
            
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
            
            return {
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
            }
            
        except Exception as e:
            return {'error': str(e)}

# Test the prediction service
if __name__ == "__main__":
    service = StockPredictionService()
    
    print("Initializing prediction service...")
    if service.initialize():
        print("Service initialized successfully!")
        
        # Test prediction
        print("\nTesting next day prediction...")
        prediction = service.predict_next_day()
        print(f"Prediction result: {prediction}")
        
        # Test multi-day prediction
        print("\nTesting 7-day prediction...")
        multi_prediction = service.predict_multi_days(7)
        print(f"Multi-day prediction result: {multi_prediction}")
        
    else:
        print("Failed to initialize service")
