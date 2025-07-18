from dotenv import load_dotenv
import os
import pandas as pd
from scrape import scrape # use as a function not a module
import requests
from datetime import datetime, timedelta

load_dotenv() 
api_key = os.getenv("API_KEY")

def get_info():
    df = pd.DataFrame() # initializes a new df every time 
    tickers, names, sectors, subsectors, hqs, dates = scrape("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    count = 0
    for ticker, name in zip(tickers, names):
        headers = {
            'Content-Type': 'application/json'
        }

        base_url = 'https://api.tiingo.com/tiingo/daily/'
        f = 'snapshot/locale/us/markets/stocks/tickers/'
        token = api_key
        yesterday = (datetime.today() - timedelta(days=1)).date()
        yesterday_str = str(yesterday)
        url = f'{base_url}{ticker}/prices?startDate={yesterday_str}&token={token}'

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            latest_data = data[-1]  # the dict is the last item in the list

            stock_data = {
                'Company': name, 
                'Stock Symbol': ticker,
                'Open': float(latest_data['open']),
                'High': float(latest_data['high']),
                'Low': float(latest_data['low']),
                'Close': float(latest_data['close']),
                'Volume': int(latest_data['volume'])
            }

            df = df.append(stock_data, ignore_index=True)
            print(f'\nDate: {yesterday}')
            print(f'Company: {name}')
            print(f'Ticker: {ticker}')
            print(f'{ticker} open price is {stock_data["Open"]}')
            print(f'{ticker} high price is {stock_data["High"]}')
            print(f'{ticker} low price is {stock_data["Low"]}')
            print(f'{ticker} close price is {stock_data["Close"]}')
            print(f'{ticker} volume is {stock_data["Volume"]}\n')

            count+=1
            if count == 50:  # hourly limit of 50 requests
                break

        else: 
            print("API request was unsuccessful")

    return df

print(get_info())

