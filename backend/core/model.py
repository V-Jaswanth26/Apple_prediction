import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import numpy as np

class LSTMStockPredictor:
    def __init__(self, input_shape, dropout_rate=0.2):
        self.input_shape = input_shape
        self.dropout_rate = dropout_rate
        self.model = None
        
    def build_model(self):
        """
        Build LSTM model for stock price prediction
        """
        model = Sequential()
        
        # First LSTM layer with Batch Normalization
        model.add(LSTM(units=100, return_sequences=True, input_shape=self.input_shape))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Second LSTM layer
        model.add(LSTM(units=100, return_sequences=True))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Third LSTM layer
        model.add(LSTM(units=100, return_sequences=False))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Dense layers
        model.add(Dense(units=50, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Output layer
        model.add(Dense(units=1, activation='linear'))
        
        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        self.model = model
        
        print("Model architecture:")
        model.summary()
        
        return model
    
    def train_model(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
        """
        Train the LSTM model
        """
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=0.00001,
            verbose=1
        )
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        """
        Make predictions using the trained model
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model first.")
        
        predictions = self.model.predict(X)
        return predictions
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the model on test data
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model first.")
        
        # Make predictions
        predictions = self.predict(X_test)
        
        # Calculate metrics
        mse = tf.keras.losses.MeanSquaredError()(y_test, predictions.flatten())
        mae = tf.keras.losses.MeanAbsoluteError()(y_test, predictions.flatten())
        rmse = tf.sqrt(mse)
        
        metrics = {
            'mse': float(tf.reduce_mean(mse)),
            'mae': float(tf.reduce_mean(mae)),
            'rmse': float(tf.reduce_mean(rmse))
        }
        
        print("Model Evaluation Metrics:")
        print(f"MSE: {metrics['mse']:.4f}")
        print(f"MAE: {metrics['mae']:.4f}")
        print(f"RMSE: {metrics['rmse']:.4f}")
        
        return metrics, predictions
    
    def save_model(self, filepath):
        """
        Save the trained model
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model first.")
        
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model
        """
        self.model = tf.keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")
        return self.model
    
    def predict_next_days(self, last_sequence, days_to_predict=7, scaler=None):
        """
        Predict multiple future days
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model first.")
        
        predictions = []
        current_sequence = last_sequence.copy()
        
        for day in range(days_to_predict):
            # Make prediction for next day
            pred = self.model.predict(current_sequence.reshape(1, *current_sequence.shape), verbose=0)
            predictions.append(pred[0, 0])
            
            # Update sequence for next prediction
            # Shift the sequence and add the new prediction
            new_row = current_sequence[-1].copy()
            new_row[3] = pred[0, 0]  # Update Close price (index 3)
            
            # Remove first row and add new prediction
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        predictions = np.array(predictions)
        
        # Inverse transform if scaler is provided
        if scaler is not None:
            # Create dummy array for inverse transformation
            dummy_array = np.zeros((len(predictions), current_sequence.shape[1]))
            dummy_array[:, 3] = predictions  # Put predictions in Close column
            predictions = scaler.inverse_transform(dummy_array)[:, 3]
        
        return predictions

class GRUStockPredictor:
    """
    Alternative model using GRU layers
    """
    def __init__(self, input_shape, dropout_rate=0.2):
        self.input_shape = input_shape
        self.dropout_rate = dropout_rate
        self.model = None
        
    def build_model(self):
        """
        Build GRU model for stock price prediction
        """
        model = Sequential()
        
        # First GRU layer
        model.add(tf.keras.layers.GRU(units=100, return_sequences=True, input_shape=self.input_shape))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Second GRU layer
        model.add(tf.keras.layers.GRU(units=100, return_sequences=True))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Third GRU layer
        model.add(tf.keras.layers.GRU(units=100, return_sequences=False))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Dense layers
        model.add(Dense(units=50, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(self.dropout_rate))
        
        # Output layer
        model.add(Dense(units=1, activation='linear'))
        
        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        self.model = model
        
        print("GRU Model architecture:")
        model.summary()
        
        return model

if __name__ == "__main__":
    # Test the model architecture
    input_shape = (60, 17)  # sequence_length, num_features
    model = LSTMStockPredictor(input_shape)
    model.build_model()
