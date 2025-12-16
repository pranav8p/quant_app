# analytics/kalman.py

import numpy as np
import pandas as pd


def kalman_hedge_ratio(y, x, Q=1e-5, R=1e-3):
    beta = 0.0
    P = 1.0
    betas = []

    for i in range(len(y)):
        P = P + Q

        if np.isnan(y.iloc[i]) or np.isnan(x.iloc[i]):
            betas.append(np.nan)
            continue

        K = P * x.iloc[i] / (x.iloc[i] ** 2 * P + R)
        beta = beta + K * (y.iloc[i] - beta * x.iloc[i])
        P = (1 - K * x.iloc[i]) * P

        betas.append(beta)

    return pd.Series(betas, index=y.index)
