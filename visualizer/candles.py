import mplfinance as mpf
import pandas as pd

class Drawer:
    def __init__(self) -> None:
        pass
    
    def draw_candle_stick_chart(self, df: pd.DataFrame) -> None:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        add_plots = [
    		mpf.make_addplot(df['MA20'], color='orange', width=1, panel=0, ylabel='Price'),
    		mpf.make_addplot(df['RSI'], color='purple', width=1.2, panel=1, ylabel='RSI'),
		]
        mpf.plot(
    		df,
    		type="candle",  # Specify candlestick chart
    		style="charles",  # Chart style
      		addplot=add_plots,
    		title="Bitcoin OHLC Candlestick Chart",
    		ylabel="Price",
    		volume=True  # Show volume
		)