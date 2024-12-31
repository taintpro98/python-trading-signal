import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pivot import calculate_pivot
from data.data_fetcher import PriceChecker
from visualizer.candles import Drawer

if __name__ == "__main__":
    checker = PriceChecker()
    data = checker.fetch_candles(300)
    price = data.iloc[:-1].copy()
    price["P"] = (price["High"] + price["Low"] + price["Close"]) / 3
    print(price)
    drawer = Drawer()
    drawer.draw_candle_stick_chart(price)