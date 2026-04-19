import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import json

from .data_collector import AppleStockDataCollector
from ..core.preprocessor import StockDataPreprocessor
from ..core.model import LSTMStockPredictor

class ModelTrainer:
    def __init__(self):
        self.data_collector = AppleStockDataCollector()
        self.preprocessor = StockDataPreprocessor()
        self.model = None
        self.history = None
        self.metrics = None
        
    def prepare_training_data(self, data_path=None, sequence_length=60):
        """
        Prepare data for training
        """
        if data_path is None:
            # Collect fresh data
            print("Collecting fresh data...")
            data = self.data_collector.fetch_historical_data()
            data_path = self.data_collector.save_data(data)
        
        # Prepare data for training
        X_train, X_val, X_test, y_train, y_val, y_test, processed_data = self.preprocessor.prepare_data(
            data_path, sequence_length
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test, processed_data
    
    def train_model(self, X_train, X_val, y_train, y_val, epochs=100, batch_size=32):
        """
        Train the LSTM model
        """
        # Get input shape
        input_shape = (X_train.shape[1], X_train.shape[2])
        
        # Create and build model
        self.model = LSTMStockPredictor(input_shape)
        self.model.build_model()
        
        # Train model
        print(f"Training model with {X_train.shape[0]} samples...")
        self.history = self.model.train_model(
            X_train, y_train, X_val, y_val, epochs, batch_size
        )
        
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the trained model
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model first.")
        
        self.metrics, predictions = self.model.evaluate_model(X_test, y_test)
        
        return self.metrics, predictions
    
    def save_model_and_results(self, model_dir="../models"):
        """
        Save the trained model and training results
        """
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, "apple_stock_lstm_model.h5")
        self.model.save_model(model_path)
        
        # Save training history
        if self.history is not None:
            history_dict = {
                'loss': [float(x) for x in self.history.history['loss']],
                'val_loss': [float(x) for x in self.history.history['val_loss']],
                'mae': [float(x) for x in self.history.history['mae']],
                'val_mae': [float(x) for x in self.history.history['val_mae']]
            }
            
            history_path = os.path.join(model_dir, "training_history.json")
            with open(history_path, 'w') as f:
                json.dump(history_dict, f, indent=2)
            
            print(f"Training history saved to {history_path}")
        
        # Save evaluation metrics
        if self.metrics is not None:
            metrics_path = os.path.join(model_dir, "evaluation_metrics.json")
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            
            print(f"Evaluation metrics saved to {metrics_path}")
        
        return model_path
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history
        """
        if self.history is None:
            print("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot loss
        ax1.plot(self.history.history['loss'], label='Training Loss')
        ax1.plot(self.history.history['val_loss'], label='Validation Loss')
        ax1.set_title('Model Loss')
        ax1.set_ylabel('Loss')
        ax1.set_xlabel('Epoch')
        ax1.legend()
        ax1.grid(True)
        
        # Plot MAE
        ax2.plot(self.history.history['mae'], label='Training MAE')
        ax2.plot(self.history.history['val_mae'], label='Validation MAE')
        ax2.set_title('Model MAE')
        ax2.set_ylabel('MAE')
        ax2.set_xlabel('Epoch')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Training history plot saved to {save_path}")
        else:
            plt.show()
    
    def plot_predictions(self, X_test, y_test, predictions, num_samples=100, save_path=None):
        """
        Plot actual vs predicted prices
        """
        # Inverse transform to get actual prices
        actual_prices = self.preprocessor.inverse_transform_predictions(
            y_test, X_test.shape[2]
        )
        predicted_prices = self.preprocessor.inverse_transform_predictions(
            predictions, X_test.shape[2]
        )
        
        # Plot only first num_samples for clarity
        actual_prices = actual_prices[:num_samples]
        predicted_prices = predicted_prices[:num_samples]
        
        plt.figure(figsize=(15, 6))
        plt.plot(actual_prices, label='Actual Prices', color='blue', alpha=0.7)
        plt.plot(predicted_prices, label='Predicted Prices', color='red', alpha=0.7)
        
        plt.title('Apple Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price ($)')
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Predictions plot saved to {save_path}")
        else:
            plt.show()

def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("Apple Stock Price Prediction - Training Pipeline")
    print("=" * 60)
    
    trainer = ModelTrainer()
    
    # Prepare data
    print("\n1. Preparing training data...")
    X_train, X_val, X_test, y_train, y_val, y_test, processed_data = trainer.prepare_training_data()
    
    # Train model
    print("\n2. Training LSTM model...")
    history = trainer.train_model(X_train, X_val, y_train, y_val, epochs=50, batch_size=32)
    
    # Evaluate model
    print("\n3. Evaluating model...")
    metrics, predictions = trainer.evaluate_model(X_test, y_test)
    
    # Save model and results
    print("\n4. Saving model and results...")
    model_path = trainer.save_model_and_results()
    
    # Plot results
    print("\n5. Generating plots...")
    trainer.plot_training_history("../models/training_history.png")
    trainer.plot_predictions(X_test, y_test, predictions, save_path="../models/predictions.png")
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Model saved to: {model_path}")
    print(f"Final Metrics: {metrics}")
    print("=" * 60)

if __name__ == "__main__":
    main()
