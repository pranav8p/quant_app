import pandas as pd
import numpy as np

def spread(series_a, series_b, beta_series):
    df = pd.concat(
        [
            series_a.rename("A"),
            series_b.rename("B"),
            beta_series.rename("beta")
        ],
        axis=1
    ).dropna()

    return df["A"] - df["beta"] * df["B"]


def zscore(spread_series, window=15):
    mean = spread_series.rolling(window).mean()
    std = spread_series.rolling(window).std()
    std = std.replace(0, np.nan)

    return (spread_series - mean) / std


def rolling_corr(series_a, series_b, window=15):
    df = pd.concat(
        [series_a.rename("A"), series_b.rename("B")],
        axis=1
    ).dropna()

    return df["A"].rolling(window).corr(df["B"])
