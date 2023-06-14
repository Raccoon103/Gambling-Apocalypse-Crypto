import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dual_momentum(df, df_returns, momentum_periods, escape_periods):
    strategy = df.pct_change(periods=momentum_periods)
    strategy['Momentum Signal'] = strategy[df.columns].max(axis=1).clip(lower=0).fillna(0)

    df_escape = df.pct_change(periods=escape_periods)
    column_labels = strategy[df.columns].idxmax(axis=1)
    strategy['Momentum Signal'] = strategy['Momentum Signal'] * (df_escape.apply(
        lambda row: np.nan if pd.isna(column_labels[row.name]) else row[column_labels[row.name]], axis=1).clip(
        lower=0).fillna(0) > 0)

    strategy['Position'] = strategy['Momentum Signal'] != 0
    strategy['Position'] = strategy['Position'].astype(int).shift(1).fillna(0)
    strategy = strategy.ffill()

    column_labels = strategy[df.columns].idxmax(axis=1)
    # print(column_labels[column_labels.notna()])
    # Create a new column in strategy DataFrame named 'Market Returns'.
    # For each row in the df_returns DataFrame, do the following:
    # If the column label in 'column_labels' for the current row is NaN, then place NaN in 'Market Returns' for that row.
    # Otherwise, place the value from df_returns for that row and the column specified by 'column_labels' in 'Market Returns' for that row.
    strategy['portfolio no leave'] = df_returns.apply(
        lambda row: np.nan if pd.isna(column_labels.shift(2)[row.name]) else row[column_labels.shift(2)[row.name]],
        axis=1)
    strategy['portfolio'] = strategy['portfolio no leave'] * strategy['Position'].shift(1).fillna(0)
    return strategy


def allocation_dual_momentum(strategy, df_returns):
    # Create a DataFrame similar to df, but initially fill it with zeros
    df_weights = pd.DataFrame(0, index=df_returns.index, columns=df_returns.columns)
    column_labels = strategy[df_returns.columns].idxmax(axis=1)

    # For each date, set the column specified by column_labels to 1 and others to 0
    for date in df_weights.index:
        if pd.notna(column_labels.loc[date]):
            # Reset all columns to zero for the current date
            df_weights.loc[date, :] = 0
            # Set the column specified by column_labels to 1 for the current date
            df_weights.loc[date, column_labels.loc[date]] = 1
    # Assuming monthly rebalancing, forward fill the weights
    df_weights = df_weights.resample('5D').first().ffill()

    # Plotting
    fig, ax = plt.subplots()
    df_weights.plot.area(ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Allocation')
    ax.set_title('Asset Allocation Over Time')
    plt.show()
    return df_weights


test2 = [dual_momentum(df.copy(), df_returns.copy(), 10, 20)]

test2.append(dual_momentum(df.copy(), df_returns.copy(), 10, 25))
test2.append(dual_momentum(df.copy(), df_returns.copy(), 10, 30))