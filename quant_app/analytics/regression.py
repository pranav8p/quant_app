# analytics/regression.py

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import HuberRegressor


def rolling_hedge_ratio(series_a, series_b, window=30, method="ols"):
    df = pd.concat(
        [series_a.rename("A"), series_b.rename("B")],
        axis=1
    ).dropna()

    betas = []

    for i in range(len(df)):
        if i < window:
            betas.append(np.nan)
            continue

        y = df["A"].iloc[i-window:i]
        X = df["B"].iloc[i-window:i].values.reshape(-1, 1)

        try:
            if method == "huber":
                model = HuberRegressor().fit(X, y.values)
                betas.append(model.coef_[0])
            else:
                X_ols = sm.add_constant(df["B"].iloc[i-window:i])
                model = sm.OLS(y, X_ols).fit()
                betas.append(model.params["B"])
        except Exception:
            betas.append(np.nan)

    return pd.Series(betas, index=df.index)
