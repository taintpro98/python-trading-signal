import mplfinance as mpf
import pandas as pd

class Drawer:
    def __init__(self) -> None:
        pass
    
    def draw_candle_stick_chart(self, df: pd.DataFrame) -> None:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        latest_pivot = df["P"].iloc[-1]
        pivot_line = [latest_pivot] * len(df)
        add_plots = [
    		# mpf.make_addplot(df['MA20'], color='orange', width=1, panel=0, ylabel='Price'),
    		# mpf.make_addplot(df['RSI'], color='purple', width=1.2, panel=1, ylabel='RSI'),
			mpf.make_addplot(pivot_line, color='blue', width=1.5, linestyle='--', label='Pivot Point'),
   			mpf.make_addplot(df["P"], color="blue", width=1, label="Pivot")
		]
        mpf.plot(
    		df,
    		type="candle",  # Specify candlestick chart
    		style="charles",  # Chart style
      		addplot=add_plots,
    		title="Bitcoin OHLC Candlestick Chart",
    		ylabel="Price",
    		volume=True,  # Show volume
      		savefig='chart.png'
		)