import yfinance as yf

def get_mu_price():
    ticker = yf.Ticker("MU")
    data = ticker.info["currentPrice"]
    
    current_price = data

    return float(current_price)

if __name__ == "__main__":
    price = get_mu_price()
    print(price)
