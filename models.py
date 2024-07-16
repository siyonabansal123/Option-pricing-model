import numpy as np
from scipy.stats import norm

def monte_carlo(S, K, T, r, sigma, num_simulations, option_type='call'):

    dt = T
    simulations = np.random.normal((r - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), num_simulations)
    S_T = S * np.exp(simulations)

    if option_type == 'call':
        payoff = np.maximum(S_T - K, 0)
    elif option_type == 'put':
        payoff = np.maximum(K - S_T, 0)

    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price


def black_scholes(S0, K, T, r, sigma, option_type):

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S0 * np.exp(-r * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * np.exp(-r * T) * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")
    
    
def binomial(S0, K, T, r, sigma, N, option_type):

    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Initialize stock price tree
    S = np.zeros((N + 1, N + 1))
    S[0, 0] = S0

    # Fill the stock price tree
    for i in range(1, N + 1):
        S[i, 0] = S[i - 1, 0] * u
        for j in range(1, i + 1):
            S[i, j] = S[i - 1, j - 1] * d

    # Initialize option value tree
    V = np.zeros((N + 1, N + 1))

    # Calculate option payoff at maturity
    for j in range(N + 1):
        V[N, j] = max(0, S[N, j] - K) if option_type == 'call' else max(0, K - S[N, j])

    # Calculate option price at earlier nodes
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            V[i, j] = np.exp(-r * dt) * (p * V[i + 1, j + 1] + (1 - p) * V[i + 1, j])

    return V[0, 0]