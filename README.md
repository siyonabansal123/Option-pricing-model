# Option Pricing Models

This project provides a framework for predicting the accuracy of different option pricing models using historical data. The models included are Monte Carlo simulation, Black-Scholes model, and Binomial option pricing model. The framework fetches option pricing data, computes the prices using the models, and calculates the accuracy metrics Mean Absolute Error (MAE) and Mean Squared Error (MSE) over a specified number of days.

## Project Structure

`├── analysis.py # Main script for running the accuracy prediction`
`├── extract_data.py # Module for fetching option pricing data`
`├── models.py # Module containing the implementation of pricing models`
`├── requirements.txt # List of dependencies`
`├── .gitignore # Git ignore file`
`└── README.md # This file`

## Dependencies

- `numpy`
- `pandas`
- `yfinance`

## Usage
 - Extracting Option Pricing Data:
Implement the get_option_pricing_data function in the extract_data.py module to fetch and return the necessary option pricing data.

 - Implementing Pricing Models:
The models.py module should contain the implementation of the following functions: monte_carlo(S0, K, T, r, sigma, num_simulations, option_type); black_scholes(S0, K, T, r, sigma, option_type); binomial(S0, K, T, r, sigma, N, option_type)

 - Running the Accuracy Prediction:
The analysis.py script calculates the prices and accuracies for each model over the specified number of days (days_back). The function predict_accuracy returns a DataFrame with the MAE and MSE for each model.
