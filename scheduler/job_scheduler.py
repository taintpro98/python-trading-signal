from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import timedelta

import asyncio
import pandas as pd
from data.data_fetcher import PriceChecker
from utils.ma import calculate_moving_average, notify_cross, calculate_min_max_scalar
from utils.rsi import calculate_rsi_wilders
from bot.telegram_bot import TelegramBot

async def notify_signal(df: pd.DataFrame):
    bot = TelegramBot()
    last_row = df.iloc[-1]
    is_signal = False
    # Convert the string to a datetime object
    time_obj = last_row['Date'].to_pydatetime()
    new_time = time_obj + timedelta(hours=7)
    message = "At {}: ".format(new_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    if last_row['RSI'] < 35 or last_row['RSI'] > 65:
        is_signal = True
        message += "\n- RSI is over: {}".format(last_row['RSI'])
    if last_row['Volume'] > last_row['Average_Volume_20']:
        rate = last_row['Volume'] / last_row['Average_Volume_20']
        if rate > 1.5:
            is_signal = True
            message += "\n- Sudden trading volume occurred. Rate: {}, Volume: {}, Average_Volume_20: {}".format(rate, last_row['Volume'], last_row['Average_Volume_20'])
    cross = notify_cross(last_row, 'MA20')
    if cross != "":
        is_signal = True
        message += cross
    cross = notify_cross(last_row, 'MA50')
    if cross != "":
        is_signal = True
        message += cross
    cross = notify_cross(last_row, 'MA200')
    if cross != "":
        is_signal = True
        message += cross
    periods = [20, 50, 200]
    min_max_scalar = calculate_min_max_scalar(df, periods)
    for p in periods:
        if last_row['Close'] < min_max_scalar[f'MinLow{p}']:
            is_signal = True
            message += "\n- The price breaks below the {}-candle low".format(p)
        if last_row['Close'] > min_max_scalar[f'MaxHigh{p}']:
            is_signal = True
            message += "\n- The price breaks above the {}-candle high".format(p)
    if is_signal:
        message += "\n- Percentage change: {} to {}".format(last_row['Percent_Change_Display'], last_row['Close'])
        await bot.send_message(message)

async def scheduled_task():
    checker = PriceChecker()
    data = checker.fetch_candles(300)
    price = data.iloc[:-1].copy()
    price['MA20'] = calculate_moving_average(price['Close'], 20)
    price['MA50'] = calculate_moving_average(price['Close'], 50)
    price['MA200'] = calculate_moving_average(price['Close'], 200)
    price['RSI'] = calculate_rsi_wilders(price['Close'])
    price['Average_Volume_20'] = calculate_moving_average(price['Volume'], 20)
    price["Percent_Change"] = ((price["Close"] - price["Open"]) / price["Open"]) * 100
    price["Percent_Change_Display"] = price["Percent_Change"].apply(lambda x: f"{x:+.2f}%")
    await notify_signal(price)
    
def run_scheduled_task():
    asyncio.run(scheduled_task())  # Wrap async task

def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scheduled_task, 'cron', second=20, minute='0,15,30,45')
    print("Scheduler started...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")