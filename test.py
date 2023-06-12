import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def data_reading(crypto_name):
    with open('crypto_data.json', 'r') as f:
        data_json = f.read()
    data_dict = json.loads(data_json)
    print(data_dict[crypto_name]['data'])
    return data_dict[crypto_name]['data']


def transform(input_data):
    output_data = [1.0]*len(input_data)
    for i in range(len(input_data)):
        if i != 0:
            fraction = input_data[i]/input_data[i-1]
            output_data[i] = output_data[i-1]*fraction
    return output_data


if __name__ == '__main__':
    currencies = ["BTC", "ETH", "BNB", "XRP", "LTC", "DOGE", "USDT", "USDC", 'ADA']
    dates = pd.date_range("20190101", periods=1461)
    data_array = np.empty((len(dates), len(currencies)))

    for i, coin in enumerate(currencies):
        data = data_reading(coin)
        data_trans = transform(data)
        data_array[:, i] = data_trans

    fig, ax = plt.subplots()
    df = pd.DataFrame(data_array, index=dates, columns=currencies)
    df.plot(ax=ax)
    ax.set_xlabel('Day')
    ax.set_ylabel('Cumulative Returns')

    plt.show()