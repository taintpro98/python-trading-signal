import pandas as pd
import numpy as np

def find_pivot_points(data, left_bars, right_bars):
    """Find pivot highs and lows in the data"""
    pivot_highs = []
    pivot_lows = []
    for i in range(left_bars, len(data) - right_bars):
        window = data[i-left_bars:i+right_bars+1]
        if data[i] == max(window):
            pivot_highs.append(i)
        if data[i] == min(window):
            pivot_lows.append(i)
    return pivot_highs, pivot_lows

def check_regular_bullish_divergence(price, rsi, pivot_idx, lookback_range):
    """Check for regular bullish divergence"""
    divergence_points = []
    print("lookback", lookback_range)

    for i in range(len(pivot_idx)-1):
        curr_idx = pivot_idx[i]
        prev_idx = pivot_idx[i-1]
        print("cur_idx", curr_idx)
        if lookback_range[0] <= curr_idx - prev_idx <= lookback_range[1]:
            if price[curr_idx] < price[prev_idx] and rsi[curr_idx] > rsi[prev_idx]:
                divergence_points.append((prev_idx, curr_idx))
    return divergence_points


def check_hidden_bullish_divergence(price, rsi, pivot_idx, lookback_range):
    """Check for hidden bullish divergence"""
    divergence_points = []

    for i in range(len(pivot_idx)-1):
        curr_idx = pivot_idx[i]
        prev_idx = pivot_idx[i-1]

        if lookback_range[0] <= curr_idx - prev_idx <= lookback_range[1]:
            # Price: Higher Low
            if price[curr_idx] > price[prev_idx]:
                # RSI: Lower Low
                if rsi[curr_idx] < rsi[prev_idx]:
                    divergence_points.append((prev_idx, curr_idx))
    return divergence_points


def check_regular_bearish_divergence(price, rsi, pivot_idx, lookback_range):
    """Check for regular bearish divergence"""
    divergence_points = []

    for i in range(len(pivot_idx)-1):
        curr_idx = pivot_idx[i]
        prev_idx = pivot_idx[i-1]

        if lookback_range[0] <= curr_idx - prev_idx <= lookback_range[1]:
            # Price: Higher High
            if price[curr_idx] > price[prev_idx]:
                # RSI: Lower High
                if rsi[curr_idx] < rsi[prev_idx]:
                    divergence_points.append((prev_idx, curr_idx))
    return divergence_points


def check_hidden_bearish_divergence(price, rsi, pivot_idx, lookback_range):
    """Check for hidden bearish divergence"""
    divergence_points = []

    for i in range(len(pivot_idx)-1):
        curr_idx = pivot_idx[i]
        prev_idx = pivot_idx[i-1]

        if lookback_range[0] <= curr_idx - prev_idx <= lookback_range[1]:
            # Price: Lower High
            if price[curr_idx] < price[prev_idx]:
                # RSI: Higher High
                if rsi[curr_idx] > rsi[prev_idx]:
                    divergence_points.append((prev_idx, curr_idx))
    return divergence_points


def find_rsi_divergences(df: pd.DataFrame, left_bars: int=5, right_bars: int=5,
                         range_lower: int=5, range_upper: int=60):
    rsi = df['RSI'].to_numpy()
    pivot_highs, pivot_lows = find_pivot_points(rsi, left_bars, right_bars)
    lookback_range = (range_lower, range_upper)
    print(df['Low'])
    print(rsi)
    divergences = {
        'regular_bullish': check_regular_bullish_divergence(
            df['Low'], rsi, pivot_lows, lookback_range
        ),
        'hidden_bullish': check_hidden_bullish_divergence(
            df['Low'], rsi, pivot_lows, lookback_range
        ),
        'regular_bearish': check_regular_bearish_divergence(
            df['High'], rsi, pivot_highs, lookback_range
        ),
        'hidden_bearish': check_hidden_bearish_divergence(
            df['High'], rsi, pivot_highs, lookback_range
        )
    }
    print(df['Low'][divergences['regular_bullish'][0][1]])
    return divergences

# Sử dụng:
# df = pd.DataFrame với các cột: open, high, low, close
# divergences = find_rsi_divergences(df)
