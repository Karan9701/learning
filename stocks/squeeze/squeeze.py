import os, pandas 

symbols = ['AAPL']

def in_squeeze(df):
    return df['lowerband'] > df['lower_keltner'] and df['upperband'] < df['upper_keltner'] 

def in_buy_zone(df):
    return (df['Close'] < (df['20ema'] + df['ATR-10'])) and (df['Close'] > (df['20ema'] - df['ATR-10']))

def stacked_emas(df):
    return (df['8ema'] > df['21ema'] and df['21ema'] > df['34ema']) or (df['8ema'] < df['21ema'] and df['21ema'] < df['34ema'])


directories = ['daily', 'four_hour', 'thirty_min', 'weekly']

for directory in directories:
    print(f'---------------------{directory.upper()} Squeezes--------------------:')
    for filename in os.listdir('datasets/' + directory):
        symbol = filename.split('.')[0]
        
        df = pandas.read_csv(f'datasets/{directory}/{filename}')

        if df.empty:
            continue

        if symbol == 'TSLA':
            print("hello")

        df['20sma'] = df['Close'].rolling(window=20).mean()
        df['20ema'] = df['Close'].ewm(alpha=2/21, min_periods=20).mean()
        df['8ema'] = df['Close'].ewm(alpha=2/9, adjust=False).mean()
        df['21ema'] = df['Close'].ewm(alpha=2/22, adjust=False).mean()
        df['34ema'] = df['Close'].ewm(alpha=2/35, adjust=False).mean()

        df['stddev'] = df['Close'].rolling(window=20).std()
        df['lowerband'] = df['20sma'] - (2 * df['stddev'])
        df['upperband'] = df['20sma'] + (2 * df['stddev'])

        df['TR'] = df['High'] - df['Low']
        df['ATR'] = df['TR'].rolling(window=20).mean()
        df['ATR-10'] = df['TR'].rolling(window=10).mean()
        df['upper_keltner'] = df['20sma'] + (df['ATR'] * 2)
        df['lower_keltner'] = df['20sma'] - (df['ATR'] * 2)

        df['squeeze_on'] = df.apply(in_squeeze, axis=1)

        df['in_buyzone'] = df.apply(in_buy_zone, axis=1)

        df['stacked_emas'] = df.apply(stacked_emas, axis=1)

        if df.iloc[-1]['squeeze_on'] and df.iloc[-1]['in_buyzone'] and df.iloc[-1]['stacked_emas']:
            print(f"{symbol} is in a squeeze right now on the {directory} timeframe and in the 1ATR buyzone and the EMAs are stacked")
    
    print("\n\n\n")




    
    
    