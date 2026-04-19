import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class StockDataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_10', 'MA_50', 'MA_200', 'RSI', 'Volatility',
                               'MACD', 'Signal_Line', 'BB_Middle', 'BB_Upper', 'BB_Lower', 'Stoch_K', 'Stoch_D']
        self.target_column = 'Close'
        
    def load_data(self, filepath):
        """
        Load stock data from CSV file
        """
        data = pd.read_csv(filepath)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values('Date')
        return data
    
    def handle_missing_values(self, data):
        """
        Handle missing values in the dataset
        """
        # Check for missing values
        missing_values = data.isnull().sum()
        print("Missing values before handling:")
        print(missing_values[missing_values > 0])
        
        # Forward fill for most columns
        data = data.fillna(method='ffill')
        
        # For any remaining NaN values, use backward fill
        data = data.fillna(method='bfill')
        
        # Drop any remaining rows with NaN values
        data = data.dropna()
        
        print(f"Data shape after handling missing values: {data.shape}")
        return data
    
    def create_sequences(self, data, sequence_length=60):
        """
        Create sequences for time series prediction
        Input: sequence_length days of data
        Output: next day's closing price
        """
        # Select features
        features = data[self.feature_columns].values
        target = data[self.target_column].values
        
        # Normalize features
        scaled_features = self.scaler.fit_transform(features)
        
        X, y = [], []
        
        for i in range(sequence_length, len(scaled_features)):
            X.append(scaled_features[i-sequence_length:i])
            y.append(scaled_features[i, 3])  # Close price is at index 3
        
        X, y = np.array(X), np.array(y)
        
        print(f"Created sequences: X shape = {X.shape}, y shape = {y.shape}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, validation_size=0.1):
        """
        Split data into training, validation, and test sets
        """
        # Calculate split indices
        total_samples = len(X)
        test_split_idx = int(total_samples * (1 - test_size))
        val_split_idx = int(test_split_idx * (1 - validation_size))
        
        # Split the data
        X_train = X[:val_split_idx]
        y_train = y[:val_split_idx]
        
        X_val = X[val_split_idx:test_split_idx]
        y_val = y[val_split_idx:test_split_idx]
        
        X_test = X[test_split_idx:]
        y_test = y[test_split_idx:]
        
        print(f"Training set: {X_train.shape}")
        print(f"Validation set: {X_val.shape}")
        print(f"Test set: {X_test.shape}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def inverse_transform_predictions(self, predictions, original_data_shape):
        """
        Inverse transform predictions back to original scale
        """
        # Create a dummy array with the same shape as the original features
        dummy_array = np.zeros((len(predictions), original_data_shape))
        
        # Place the predictions in the Close price column (index 3)
        dummy_array[:, 3] = predictions.flatten()
        
        # Inverse transform
        inverse_transformed = self.scaler.inverse_transform(dummy_array)
        
        # Extract only the Close price
        return inverse_transformed[:, 3]
    
    def create_prediction_input(self, last_n_days_data, sequence_length=60):
        """
        Create input for prediction from the last N days of data
        """
        # Select features
        features = last_n_days_data[self.feature_columns].values
        
        # Normalize using the same scaler
        scaled_features = self.scaler.transform(features)
        
        # Create sequence
        sequence = scaled_features[-sequence_length:]
        
        # Reshape for model input (1, sequence_length, num_features)
        sequence = sequence.reshape(1, sequence_length, len(self.feature_columns))
        
        return sequence
    
    def add_technical_indicators(self, data):
        """
        Add additional technical indicators
        """
        # MACD (Moving Average Convergence Divergence)
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        data['BB_Middle'] = data['Close'].rolling(window=20).mean()
        bb_std = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
        data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
        
        # Stochastic Oscillator
        low_14 = data['Low'].rolling(window=14).min()
        high_14 = data['High'].rolling(window=14).max()
        data['Stoch_K'] = 100 * ((data['Close'] - low_14) / (high_14 - low_14))
        data['Stoch_D'] = data['Stoch_K'].rolling(window=3).mean()
        
        return data
    
    def prepare_data(self, filepath, sequence_length=60):
        """
        Complete data preparation pipeline
        """
        print("Starting data preparation...")
        
        # Load data
        data = self.load_data(filepath)
        print(f"Loaded data with shape: {data.shape}")
        
        # Handle missing values
        data = self.handle_missing_values(data)
        
        # Add technical indicators
        data = self.add_technical_indicators(data)
        
        # Handle missing values again after adding indicators
        data = self.handle_missing_values(data)
        
        # Create sequences
        X, y = self.create_sequences(data, sequence_length)
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(X, y)
        
        return X_train, X_val, X_test, y_train, y_val, y_test, data

if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = StockDataPreprocessor()
    
    # Prepare data
    X_train, X_val, X_test, y_train, y_val, y_test, processed_data = preprocessor.prepare_data("../data/apple_stock_data.csv")
    
    print("\nData preparation completed successfully!")
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
