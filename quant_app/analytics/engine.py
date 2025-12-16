# quant_app/analytics/engine.py

from analytics.stats import spread, zscore, rolling_corr
from analytics.kalman import kalman_hedge_ratio
from analytics.backtest import mean_reversion_backtest


class AnalyticsEngine:
    def __init__(self, z_window=15):
        self.z_window = z_window

    def run(self, bars):
        price_a = bars["close"]
        price_b = bars["close"].shift(1)

        beta = kalman_hedge_ratio(price_a, price_b)

        spr = spread(price_a, price_b, beta)

        zs = zscore(spr, window=self.z_window)

        corr = rolling_corr(
            price_a,
            price_b,
            window=self.z_window
)


        # Backtest (NOW ACTUALLY CALLED)
        backtest_results = mean_reversion_backtest(
            zs.dropna(),
            entry=2.0,

        )

        latest = {
            "zscore": zs.dropna().iloc[-1] if not zs.dropna().empty else None,
            "volume": bars["volume"].iloc[-1],
            "correlation": corr.dropna().iloc[-1] if not corr.dropna().empty else None
        }

        return {
            "beta": beta,
            "spread": spr,
            "zscore": zs,
            "correlation": corr,
            "backtest": backtest_results,
            "latest": latest
        }
