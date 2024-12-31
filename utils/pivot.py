import pandas as pd

def calculate_pivot(df: pd.DataFrame) -> pd.Series:
    """
    Calculate pivot point (P) for the given DataFrame.
    
    :param df: DataFrame with columns ['High', 'Low', 'Close'].
    :return: Series containing the pivot points.
    """
    if not {'High', 'Low', 'Close'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'High', 'Low', and 'Close' columns.")
    return (df['High'] + df['Low'] + df['Close']) / 3