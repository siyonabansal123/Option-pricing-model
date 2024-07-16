import yfinance as yf
import numpy as np
import pandas as pd

from extarct_data import get_option_pricing_data
from models import monte_carlo, black_scholes, binomial

def predict_accuracy(ticker, option_type, num_simulations=10000, N=100, days_back=30):

    option_data = get_option_pricing_data(ticker, option_type)
    
    # Get historical option prices
    stock = yf.Ticker(ticker)
    option_chain = stock.option_chain(option_data['expiry_date'])
    
    # Choose the correct DataFrame based on option_type
    if option_data['option_type'] == 'call':
        historical_prices = option_chain.calls
    elif option_data['option_type'] == 'put':
        historical_prices = option_chain.puts
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")
    
    actual_prices = historical_prices['lastPrice'][-days_back:]
    
    # Initialize arrays to store model prices and accuracies
    mc_prices = np.zeros(days_back)
    bs_prices = np.zeros(days_back)
    binomial_prices = np.zeros(days_back)
    accuracies = np.zeros(days_back)
    
    # Calculate prices and accuracies for each day
    for i in range(days_back):
        mc_prices[i] = monte_carlo(option_data['S0'], option_data['K'], option_data['T'], option_data['r'], option_data['sigma'], num_simulations, option_type)
        bs_prices[i] = black_scholes(option_data['S0'], option_data['K'], option_data['T'], option_data['r'], option_data['sigma'], option_type)
        binomial_prices[i] = binomial(option_data['S0'], option_data['K'], option_data['T'], option_data['r'], option_data['sigma'], N, option_type)
    
    # Mean Abosulute Error 
    mc_mae = np.sum(np.abs(mc_prices - actual_prices))/days_back
    bs_mae = np.sum(np.abs(bs_prices - actual_prices))/days_back
    binomial_mae = np.sum(np.abs(binomial_prices - actual_prices))/days_back
    
    # Mean Squared Error (MSE)
    mc_mse = np.sum((mc_prices - actual_prices)**2)/days_back
    bs_mse = np.sum((bs_prices - actual_prices)**2)/days_back
    binomial_mse = np.sum((binomial_prices - actual_prices)**2)/days_back 
    
    # Create a DataFrame to display the results
    data = {
        'MAE': [mc_mae, bs_mae, binomial_mae],
        'MSE': [mc_mse, bs_mse, binomial_mse]
    }
    
    results_df = pd.DataFrame(data, index=['Monte Carlo', 'Black-Scholes', 'Binomial'])
    
    
    return results_df
    
    
    




