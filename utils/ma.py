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