import pandas as pd 

def calculate_rsi(series: pd.Series, period: int=14) -> pd.Series:
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_average(series: pd.Series, period: int=20) -> pd.Series:
    """
    Calculate the moving average for a given period.

    Args:
        series (pd.Series): The data series for which the moving average is calculated.
        period (int): The number of periods for the moving average.

    Returns:
        pd.Series: A series containing the moving average values.
    """
    if period <= 0:
        raise ValueError("Period must be greater than 0")
    return series.rolling(window=period).mean()

def check_cross_ohlc(df: pd.DataFrame, ma_column: str):
    """
    Checks if the price crosses the moving average (MA) using OHLC data.

    Parameters:
        df (pd.DataFrame): DataFrame containing OHLC columns ('Open', 'High', 'Low', 'Close') and the MA column.
        ma_column (str): The column name of the moving average (e.g., 'MA20').

    Returns:
        pd.DataFrame: A DataFrame with 'Cross Above' and 'Cross Below' indicators.
    """
    crosses = pd.DataFrame({
        'Open': df['Open'],
        'High': df['High'],
        'Low': df['Low'],
        'Close': df['Close'],
        ma_column: df[ma_column],
        # Cross Above: MA is between Low and High, and Close > MA
        'Cross Above': (df['Low'] < df[ma_column]) & (df['High'] > df[ma_column]) & (df['Close'] > df[ma_column]),
        # Cross Below: MA is between Low and High, and Close < MA
        'Cross Below': (df['Low'] < df[ma_column]) & (df['High'] > df[ma_column]) & (df['Close'] < df[ma_column]),
    })
    return crosses

def notify_cross(df: pd.Series, ma_column: str) -> str:
    message = ''
    if df['Low'] < df[ma_column] and df['High'] > df[ma_column] and df['Close'] > df[ma_column]:
        message = "\n- Price crossed above {}\n".format(ma_column)
    elif df['Low'] < df[ma_column] and df['High'] > df[ma_column] and df['Close'] < df[ma_column]:
        message = "\n- Price crossed below {}\n".format(ma_column)
    return message