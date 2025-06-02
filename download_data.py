import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")
else:
    # Clean out any existing files
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed existing file: {file_path}")

# Define symbols to download
symbols = ['AAPL', 'MSFT', 'SPY']

# Calculate start date (5 years ago from today)
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)  # Approximate 5 years

print(f"Downloading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

# Download and save data for each symbol
for symbol in symbols:
    print(f"Downloading data for {symbol}...")
    
    try:
        # Create a Ticker object
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        data = ticker.history(
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval="1d"
        )
        
        # Keep only the standard OHLCV columns
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Make sure the index is properly named
        data.index.name = 'Date'
        
        # Create a clean pandas DataFrame with explicit column order
        clean_df = pd.DataFrame({
            'Open': data['Open'],
            'High': data['High'],
            'Low': data['Low'],
            'Close': data['Close'],
            'Volume': data['Volume']
        }, index=data.index)
        
        # Ensure Date index is properly formatted
        clean_df.index.name = 'Date'
        
        # Save to CSV with proper formatting
        csv_path = os.path.join(data_dir, f"{symbol}.csv")
        clean_df.to_csv(csv_path)
        
        print(f"Saved {len(clean_df)} rows of {symbol} data to {csv_path}")
        
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")

print("Data download completed")

# Simple test to see if files can be read properly
try:
    print("\nTesting if files can be read with pandas:")
    for symbol in symbols:
        file_path = os.path.join(data_dir, f"{symbol}.csv")
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
        print(f"Successfully read {symbol} data with {len(df)} rows")
except Exception as e:
    print(f"Error reading CSV files: {e}")

