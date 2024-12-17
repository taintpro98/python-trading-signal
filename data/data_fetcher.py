import pandas as pd
import yfinance as yf
from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET, SYMBOL, INTERVAL


class PriceChecker:
    def __init__(self):
        self.client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
        
    def fetch_candles(self, limit: int, interval=Client.KLINE_INTERVAL_15MINUTE) -> pd.DataFrame:
        candles = self.client.get_klines(symbol=SYMBOL, interval=interval, limit=limit)
        df = pd.DataFrame(candles, columns=[
            'Date', 'Open', 'High', 'Low', 'Close', 'Volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        result = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        result['Date'] = pd.to_datetime(df['Date'], unit='ms')
        float_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        result[float_columns] = df[float_columns].apply(pd.to_numeric)
        return result
    
    def fetch_yahoo_data(self, limit: int) -> pd.DataFrame:
        btc_data = yf.download(ticker_symbol, interval="15m", period="1d")
        # Display the data
        print(btc_data)
