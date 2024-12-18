from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

import asyncio
import pandas as pd
from data.data_fetcher import PriceChecker
from utils.ma import calculate_moving_average, calculate_rsi
from bot.telegram_bot import TelegramBot

async def notify_signal(df: pd.DataFrame):
    bot = TelegramBot()
    last_row = df.iloc[-2]
    if last_row['Volume'] > last_row['Average_Volume_20']:
        rate = last_row['Volume'] / last_row['Average_Volume_20']
        if rate > 1.5:
            # Convert the string to a datetime object
            time_obj = datetime.strptime(last_row['Date'], '%Y-%m-%d %H:%M:%S')
            new_time = time_obj + timedelta(hours=7)
            message = "Huge trading volume occurred. Time: {}, Rate: {}, Volume: {}, Average_Volume_20: {}".format(new_time.strftime('%Y-%m-%d %H:%M:%S'), rate, last_row['Volume'], last_row['Average_Volume_20'])
            await bot.send_message(message)

async def scheduled_task():
    checker = PriceChecker()
    price = checker.fetch_candles(300)
    # price['MA20'] = calculate_moving_average(price['Close'], 20)
    # price['MA50'] = calculate_moving_average(price['Close'], 50)
    # price['MA200'] = calculate_moving_average(price['Close'], 200)
    # price['RSI'] = calculate_rsi(price['Close'])
    price['Average_Volume_20'] = calculate_moving_average(price['Volume'], 20)
    await notify_signal(price)
    
def run_scheduled_task():
    asyncio.run(scheduled_task())  # Wrap async task

def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scheduled_task, 'cron', minute='1,16,31,46')
    print("Scheduler started...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")