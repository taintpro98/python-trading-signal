import numpy as np
import pandas as pd

def calculate_rsi_fireant(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the RSI using Fireant-compatible smoothing (Wilder's method).
    :param data: pd.Series, the closing prices.
    :param period: int, the RSI period (default 14).
    :return: pd.Series, the RSI values.
    """
    if len(data) < period:
        raise ValueError(f"Data length must be at least {period}.")
    # Calculate price changes (delta)
    delta = data.diff()
    # Separate positive and negative changes
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Initial averages using a simple mean
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Use exponential moving average (EMA) for smoothing
    avg_gain = avg_gain.fillna(0).ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = avg_loss.fillna(0).ewm(alpha=1 / period, adjust=False).mean()

    # Calculate RS (relative strength)
    rs = avg_gain / avg_loss
    # Avoid division by zero in RS calculation
    rs = rs.replace([np.inf, -np.inf], np.nan).fillna(0)
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    # RSI values before enough periods should be NaN
    rsi[:period] = np.nan
    return rsi 

def calculate_rsi_wilders(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the RSI using Wilder's smoothing method.
    :param data: pd.Series, the closing prices.
    :param period: int, the RSI period (default 14).
    :return: pd.Series, the RSI values.
    """
    if len(data) < period:
        raise ValueError(f"Data length must be at least {period}.")

    # Calculate daily price changes
    delta = data.diff()

    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Wilder's smoothed averages
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Apply Wilder's smoothing for subsequent values
    for i in range(period, len(data)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    # Calculate RS (relative strength)
    rs = avg_gain / avg_loss
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_rsi(data: pd.Series, period: int=14) -> pd.Series:
    if len(data) < period:
        raise ValueError(f"Data length must be at least {period}")
    
    # Calculate daily price changes
    delta = data.diff()
    
    # Gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate SMA of gains and losses
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Avoid division by zero
    avg_loss = avg_loss.replace(0, np.nan)
    
    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Fill NaN for initial periods with None
    return rsi.fillna(np.nan)

def calculate_rsi_with_smoothing(data: pd.Series, period: int = 14, smooth_period: int = 14) -> pd.Series:
    if len(data) < period + smooth_period:
        raise ValueError(f"Data length must be at least {period + smooth_period}")
    # Calculate daily price changes
    delta = data.diff()

    # Gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate initial Average Gain and Average Loss
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Smooth the averages using SMA
    smooth_gain = avg_gain.rolling(window=smooth_period, min_periods=smooth_period).mean()
    smooth_loss = avg_loss.rolling(window=smooth_period, min_periods=smooth_period).mean()

    # Avoid division by zero
    smooth_loss = smooth_loss.replace(0, np.nan)

    # Calculate RSI
    rs = smooth_gain / smooth_loss
    rsi = 100 - (100 / (1 + rs))

    # Fill NaN for initial periods with None
    return rsi.fillna(np.nan)

def calculate_rsi_with_ema(data: pd.Series, period: int = 14) -> pd.Series:
    if len(data) < period:
        raise ValueError(f"Data length must be at least {period}")

    # Calculate daily price changes
    delta = data.diff()

    # Gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the exponential moving averages of gains and losses
    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()

    # Avoid division by zero
    avg_loss = avg_loss.replace(0, np.nan)

    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(0)  # Fill NaN values with 0 for initial periods
