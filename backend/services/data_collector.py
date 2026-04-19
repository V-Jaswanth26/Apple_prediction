import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class AppleStockDataCollector:
    def __init__(self):
        self.ticker = "AAPL"
        self.data_dir = "../data"
        
    def fetch_historical_data(self, start_date=None, end_date=None):
        """
        Fetch Apple stock data for approximately 40 years
        """
        if start_date is None:
            # Go back 40 years from today
            start_date = datetime.now() - timedelta(days=40*365)
        
        if end_date is None:
            end_date = datetime.now()
            
        print(f"Fetching Apple stock data from {start_date.date()} to {end_date.date()}")
        
        # Download data using yfinance
        stock = yf.Ticker(self.ticker)
        data = stock.history(start=start_date, end=end_date)
        
        # Reset index to make Date a column
        data.reset_index(inplace=True)
        
        # Convert Date to datetime if it's not already
        data['Date'] = pd.to_datetime(data['Date'])
        
        # Add some useful features
        data['Year'] = data['Date'].dt.year
        data['Month'] = data['Date'].dt.month
        data['Day'] = data['Date'].dt.day
        data['DayOfWeek'] = data['Date'].dt.dayofweek
        
        # Calculate moving averages
        data['MA_10'] = data['Close'].rolling(window=10).mean()
        data['MA_50'] = data['Close'].rolling(window=50).mean()
        data['MA_200'] = data['Close'].rolling(window=200).mean()
        
        # Calculate daily returns
        data['Daily_Return'] = data['Close'].pct_change()
        
        # Calculate volatility (rolling standard deviation)
        data['Volatility'] = data['Daily_Return'].rolling(window=20).std()
        
        # Calculate RSI (Relative Strength Index)
        data['RSI'] = self.calculate_rsi(data['Close'])
        
        print(f"Fetched {len(data)} days of data")
        print(f"Date range: {data['Date'].min().date()} to {data['Date'].max().date()}")
        
        return data
    
    def calculate_rsi(self, prices, window=14):
        """
        Calculate Relative Strength Index
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def save_data(self, data, filename="apple_stock_data.csv"):
        """
        Save the collected data to CSV file
        """
        os.makedirs(self.data_dir, exist_ok=True)
        filepath = os.path.join(self.data_dir, filename)
        
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        
        return filepath
    
    def load_data(self, filename="apple_stock_data.csv"):
        """
        Load data from CSV file
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if os.path.exists(filepath):
            data = pd.read_csv(filepath)
            data['Date'] = pd.to_datetime(data['Date'])
            print(f"Data loaded from {filepath}")
            return data
        else:
            print(f"File {filepath} not found")
            return None
    
    def get_data_summary(self, data):
        """
        Get summary statistics of the data
        """
        summary = {
            'total_records': len(data),
            'date_range': {
                'start': data['Date'].min().date(),
                'end': data['Date'].max().date()
            },
            'price_stats': {
                'min_close': data['Close'].min(),
                'max_close': data['Close'].max(),
                'avg_close': data['Close'].mean(),
                'current_close': data['Close'].iloc[-1]
            },
            'volume_stats': {
                'avg_volume': data['Volume'].mean(),
                'max_volume': data['Volume'].max()
            }
        }
        
        return summary

if __name__ == "__main__":
    collector = AppleStockDataCollector()
    
    # Fetch data
    data = collector.fetch_historical_data()
    
    # Save data
    collector.save_data(data)
    
    # Print summary
    summary = collector.get_data_summary(data)
    print("\nData Summary:")
    print(f"Total Records: {summary['total_records']}")
    print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Price Range: ${summary['price_stats']['min_close']:.2f} - ${summary['price_stats']['max_close']:.2f}")
    print(f"Current Price: ${summary['price_stats']['current_close']:.2f}")
