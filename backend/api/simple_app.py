from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.predict import StockPredictionService

app = Flask(__name__)
CORS(app)

# Initialize prediction service
prediction_service = StockPredictionService()

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
            '/analytics',
            '/health'
        ]
    })

@app.route('/health')
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy' if prediction_service.is_initialized else 'unhealthy',
        'model_loaded': prediction_service.is_initialized,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict next day's stock price
    """
    try:
        result = prediction_service.predict_next_day()
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_multi', methods=['POST'])
def predict_multi():
    """
    Predict multiple future days (1, 7, 30 days)
    """
    try:
        # Get number of days from request
        request_data = request.get_json()
        days_to_predict = request_data.get('days', 7) if request_data else 7
        
        # Validate days_to_predict
        if days_to_predict not in [1, 7, 30]:
            return jsonify({'error': 'Days to predict must be 1, 7, or 30'}), 400
        
        result = prediction_service.predict_multi_days(days_to_predict)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    """
    Get historical stock data
    """
    try:
        # Get query parameters
        days = request.args.get('days', 365, type=int)
        
        result = prediction_service.get_historical_data(days)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def get_analytics():
    """
    Get analytics and insights
    """
    try:
        result = prediction_service.get_analytics()
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize prediction service before starting the server
    print("Initializing prediction service...")
    if prediction_service.initialize():
        print("Prediction service initialized successfully!")
        print("Starting Flask server on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to initialize prediction service. Exiting...")
