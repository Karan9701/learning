import os 
import pandas as pd
import yfinance as yf

def daily_data():
    with open('sp500_tickers.csv') as tickers:
        symbols = tickers.read().strip().split('\n')

        for symbol in symbols:
            print(symbol)
            data = yf.download(symbol, start="2023-10-14", end="2023-12-27")
            data.to_csv(f'datasets/daily/{symbol}.csv')

def weekly_data():
    with open('sp500_tickers.csv') as tickers:
        symbols = tickers.read().strip().split('\n')

        for symbol in symbols:
            print(symbol)
            data = yf.download(symbol, start="2023-03-14", end="2023-12-27", interval="1wk")
            data.to_csv(f'datasets/weekly/{symbol}.csv')

def thirty_min_data():
    with open('sp500_tickers.csv') as tickers:
        symbols = tickers.read().strip().split('\n')

        for symbol in symbols:
            print(symbol)
            data = yf.download(symbol, start="2023-12-11", end="2023-12-27", interval="30m")
            data.to_csv(f'datasets/thirty_min/{symbol}.csv')


def four_hour_data():
    with open('sp500_tickers.csv') as tickers:
        symbols = tickers.read().strip().split('\n')

        for symbol in symbols:
            start_idx = 0
            print(symbol)
            data = yf.download(symbol, start="2023-11-27", end="2023-12-27", interval="1h")
            df_4h = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close'])
            pattern = [4, 3] * (len(data) // 7)

            for num_rows in pattern:
                end_index = start_idx + num_rows
                high = data.iloc[start_idx:end_index].drop(columns='Volume').max().max()
                low = data.iloc[start_idx:end_index].drop(columns='Volume').min().min()
                open_price = data.iloc[start_idx]['Open']
                close_price = data.iloc[end_index-1]['Close']

                datetime_value = data.index[start_idx]

                # Create a dictionary with the values
                row_data = {'Datetime': datetime_value, 'Open': open_price, 'High': high, 'Low': low, 'Close': close_price}

                # Append the dictionary as a new row to the df_4h DataFrame
                df_4h.loc[len(df_4h)] = [datetime_value, open_price, high, low, close_price]

                start_idx += num_rows
                    

                df_4h.to_csv(f'datasets/four_hour/{symbol}.csv')

import time

t0 = time.time()
daily_data()
weekly_data()
thirty_min_data()
four_hour_data()
t1 = time.time()

total = t1-t0
print(total)

