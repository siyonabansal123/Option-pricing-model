import yfinance as yf
import numpy as np
import datetime

def get_option_pricing_data(ticker, option_type):

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")  # Get 1 year of historical data
    
    S0 = hist['Close'][-1]
    
    expiry_dates = stock.options
    expiry_date = expiry_dates[0]
    today = datetime.datetime.now()
    expiry = datetime.datetime.strptime(expiry_date, '%Y-%m-%d')
    T = (expiry - today).days / 365.0
    
    hist['Daily Return'] = hist['Close'].pct_change()
    sigma = hist['Daily Return'].std() * np.sqrt(252)  # Annualized volatility
    
    option_data = {
        'S0': S0,
        'K': S0,
        'T': T,
        'r': 0.03,
        'sigma': sigma,
        'option_type': option_type,
        'expiry_date': expiry_date, 
        'ticker':ticker
    }
    
    return option_data