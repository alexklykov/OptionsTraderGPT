import yfinance as yf
import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "mu_prices.csv"
PLOT_FILE = "mu_prices_plot.png"

def get_mu_price():
    ticker = yf.Ticker("MU")
    # Using .get() is safer than direct key access in case the API response changes
    data = ticker.info.get("currentPrice")
    
    # Fallback to history if currentPrice is not available
    if data is None:
        history = ticker.history(period="1d")
        if not history.empty:
            data = history['Close'].iloc[-1]
            
    if data is None:
        raise ValueError("Could not retrieve price for MU")
    
    current_price = data

    return float(current_price)

def save_to_csv(price):
    # Check if file exists to know if we need to write headers (in case it gets deleted)
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # If the file was just created or empty, write headers
        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writerow(["Timestamp", "Price"])
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, price])

def create_plot():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        print("No data to plot.")
        return

    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            print("Dataset is empty, skipping plot.")
            return

        # Convert Timestamp to datetime objects
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        plt.figure(figsize=(10, 6))
        plt.plot(df['Timestamp'], df['Price'], marker='o', linestyle='-', color='blue')
        plt.title('MU Stock Price Over Time')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(PLOT_FILE)
        plt.close()
        print(f"Plot saved to {PLOT_FILE}")
    except Exception as e:
        print(f"Failed to create plot: {e}")

if __name__ == "__main__":
    try:
        price = get_mu_price()
        save_to_csv(price)
        print(f"Successfully saved MU price: {price}")
        create_plot()
    except Exception as e:
        print(f"An error occurred: {e}")
