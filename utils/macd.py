import pandas as pd
from scipy.signal import find_peaks
import numpy as np

def calculate_macd_histogram(
    ohlc: pd.DataFrame, 
    short_window: int = 12, 
    long_window: int = 26, 
    signal_window: int = 9
) -> pd.DataFrame:
    """
    Calculates the MACD line, signal line, and histogram from an OHLC DataFrame.
    :param ohlc: pd.DataFrame - The input OHLC data containing a 'Close' column.
    :param short_window: int - The period for the short-term EMA (default: 12).
    :param long_window: int - The period for the long-term EMA (default: 26).
    :param signal_window: int - The period for the signal line EMA (default: 9).
    :return: pd.DataFrame - The input DataFrame with added MACD, Signal, and Histogram columns.
    """
    if 'Close' not in ohlc:
        raise ValueError("The input DataFrame must contain a 'Close' column.")
    # Calculate the short-term EMA (fast EMA)
    ohlc['EMA_Short'] = ohlc['Close'].ewm(span=short_window, adjust=False).mean()
    # Calculate the long-term EMA (slow EMA)
    ohlc['EMA_Long'] = ohlc['Close'].ewm(span=long_window, adjust=False).mean()
    # Calculate the MACD line (difference between short and long EMAs)
    ohlc['MACD'] = ohlc['EMA_Short'] - ohlc['EMA_Long']
    # Calculate the Signal line (EMA of the MACD line)
    ohlc['Signal'] = ohlc['MACD'].ewm(span=signal_window, adjust=False).mean()
    # Calculate the MACD histogram (difference between MACD and Signal line)
    ohlc['MACD_Histogram'] = ohlc['MACD'] - ohlc['Signal']
    # Optionally drop intermediate EMA columns if not needed
    ohlc.drop(columns=['EMA_Short', 'EMA_Long'], inplace=True)
    return ohlc

def find_divergence_convergence(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check divergence and convergence using MACD Histogram and RSI history of 2 tops or bottoms.
    :param df: pd.DataFrame with columns ['Date', 'Close', 'MACD_Histogram', 'RSI'].
    :return: pd.DataFrame with 'Divergence' and 'Convergence' columns added.
    """
    if not {'Close', 'MACD_Histogram', 'RSI'}.issubset(df.columns):
        raise ValueError("The DataFrame must contain 'Close', 'MACD_Histogram', and 'RSI' columns.")
    
    # Identify tops and bottoms for Price, MACD Histogram, and RSI
    price_peaks, _ = find_peaks(df['Close'])
    price_troughs, _ = find_peaks(-df['Close'])
    macd_peaks, _ = find_peaks(df['MACD_Histogram'])
    macd_troughs, _ = find_peaks(-df['MACD_Histogram'])
    rsi_peaks, _ = find_peaks(df['RSI'])
    rsi_troughs, _ = find_peaks(-df['RSI'])

    # Prepare columns
    df['Divergence'] = np.nan
    df['Convergence'] = np.nan

    # Check for divergence and convergence
    for i in range(1, len(df)):
        # Divergence or Convergence between Price and MACD Histogram
        if i in price_troughs and i in macd_troughs:
            # Bullish Divergence
            if df['Close'].iloc[i] < df['Close'].iloc[i - 1] and df['MACD_Histogram'].iloc[i] > df['MACD_Histogram'].iloc[i - 1]:
                df.loc[df.index[i], 'Divergence'] = 'Bullish Divergence'
            # Bearish Convergence
            elif df['Close'].iloc[i] < df['Close'].iloc[i - 1] and df['MACD_Histogram'].iloc[i] < df['MACD_Histogram'].iloc[i - 1]:
                df.loc[df.index[i], 'Convergence'] = 'Bearish Convergence'

        if i in price_peaks and i in macd_peaks:
            # Bearish Divergence
            if df['Close'].iloc[i] > df['Close'].iloc[i - 1] and df['MACD_Histogram'].iloc[i] < df['MACD_Histogram'].iloc[i - 1]:
                df.loc[df.index[i], 'Divergence'] = 'Bearish Divergence'
            # Bullish Convergence
            elif df['Close'].iloc[i] > df['Close'].iloc[i - 1] and df['MACD_Histogram'].iloc[i] > df['MACD_Histogram'].iloc[i - 1]:
                df.loc[df.index[i], 'Convergence'] = 'Bullish Convergence'

        # Divergence or Convergence between Price and RSI
        if i in price_troughs and i in rsi_troughs:
            # Bullish Divergence
            if df['Close'].iloc[i] < df['Close'].iloc[i - 1] and df['RSI'].iloc[i] > df['RSI'].iloc[i - 1]:
                df.loc[df.index[i], 'Divergence'] = 'Bullish Divergence (RSI)'
            # Bearish Convergence
            elif df['Close'].iloc[i] < df['Close'].iloc[i - 1] and df['RSI'].iloc[i] < df['RSI'].iloc[i - 1]:
                df.loc[df.index[i], 'Convergence'] = 'Bearish Convergence (RSI)'

        if i in price_peaks and i in rsi_peaks:
            # Bearish Divergence
            if df['Close'].iloc[i] > df['Close'].iloc[i - 1] and df['RSI'].iloc[i] < df['RSI'].iloc[i - 1]:
                df.loc[df.index[i], 'Divergence'] = 'Bearish Divergence (RSI)'
            # Bullish Convergence
            elif df['Close'].iloc[i] > df['Close'].iloc[i - 1] and df['RSI'].iloc[i] > df['RSI'].iloc[i - 1]:
                df.loc[df.index[i], 'Convergence'] = 'Bullish Convergence (RSI)'

    return df

# Example usage
data = {
    'Date': pd.date_range(start='2024-01-01', periods=20, freq='D'),
    'Close': [102, 105, 107, 106, 109, 110, 113, 114, 116, 119, 118, 115, 117, 120, 122, 124, 123, 125, 127, 130],
    'MACD_Histogram': [0.1, 0.15, 0.12, 0.08, 0.10, 0.11, 0.13, 0.10, 0.08, 0.06, 0.07, 0.04, 0.05, 0.06, 0.09, 0.12, 0.10, 0.13, 0.15, 0.18],
    'RSI': [45, 50, 55, 52, 58, 60, 62, 59, 57, 55, 53, 50, 52, 55, 58, 61, 60, 63, 65, 68],
}

df = pd.DataFrame(data)
df_with_signals = find_divergence_convergence(df)
print(df_with_signals[['Date', 'Close', 'Divergence', 'Convergence']])