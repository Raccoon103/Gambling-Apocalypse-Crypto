import json
from cryptocmd import CmcScraper

currencies = ["BTC", "ETH", "BNB", "XRP", "LTC", "DOGE", "USDT", "USDC", "ADA"]  # Example list of currencies

data_collection = {}  # Dictionary to store the collected data

for currency in currencies:
    print(currency)
    scraper = CmcScraper(currency, "01-01-2019", "31-12-2022")
    data_tuple = scraper.get_data()
    print(data_tuple)

    data_list = [0] * (365 * 3 + 366)
    for i in range(365 * 3 + 366):
        data_list[i] = data_tuple[1][-i - 1][4]
    print(data_list)

    # Store the data in the collection dictionary
    data_collection[currency] = {
        "currency": currency,
        "start_date": "01-01-2019",
        "end_date": "31-12-2022",
        "data": data_list
    }

# Save the collection dictionary to a JSON file
with open("crypto_data.json", "w") as json_file:
    json.dump(data_collection, json_file)
