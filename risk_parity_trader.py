import numpy as np
import pandas as pd
import json


# Load the collected data from the JSON file
with open("crypto_data.json", "r") as json_file:
    data_collection = json.load(json_file)


# Extract data from data_collection dictionary
currencies = data_collection.keys()

# Create df DataFrame with price history
df = pd.DataFrame(index=pd.date_range(start="01-01-2019", end="31-12-2022"))
for currency in currencies:
    df[currency] = data_collection[currency]["data"]

df_return = df.pct_change().dropna()


# Set the desired lookback period
lookback = 10


def risk_parity(df, df_returns, lookback, exclude=['USDT', 'USDC']):
    # Exclude the stable coins
    df = df.drop(exclude, axis=1)
    df_returns = df_returns.drop(exclude, axis=1)

    # Initialize an empty DataFrame to store the weights
    weights = pd.DataFrame(index=df.index, columns=df.columns)
    strategy = df_returns.copy()
    strategy['portfolio'] = np.nan

    # Calculate the standard deviation of the returns for the lookback period
    std_devs = df_returns.iloc[len(df)-1-lookback: len(df)-1].std()
    # Calculate the inverse of the standard deviation
    inv_std_devs = 1 / std_devs
    # Normalize the inverse standard deviations to get the portfolio weights
    weights.iloc[len(df)-1] = inv_std_devs / np.sum(inv_std_devs)

    # Calculate the portfolio return for the current day
    strategy.iloc[len(df)-1, strategy.columns.get_loc('portfolio')] = np.sum(
        weights.iloc[len(df)-1] * df_returns.iloc[len(df)-1])

    return strategy, weights


if __name__ == '__main__':
    initial_fund = 10000  # Initial fund in USD
