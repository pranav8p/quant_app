# quant_app/app.py

import time
import threading

from ingestion.websocket_client import BinanceWebSocket
from storage.db import TickDB
from resampling.resampler import Resampler
from analytics.engine import AnalyticsEngine
from alerts.alerts import zscore_alert


BUFFER_SIZE = 100
tick_buffer = []

db = TickDB()
resampler = Resampler()
engine = AnalyticsEngine()


def on_tick(tick):
    global tick_buffer
    tick_buffer.append(tick)

    if len(tick_buffer) >= BUFFER_SIZE:
        db.insert_ticks(tick_buffer)
        tick_buffer.clear()


if __name__ == "__main__":
    ws = BinanceWebSocket("btcusdt", on_tick)
    threading.Thread(target=ws.start, daemon=True).start()

    print("Backend running...")

    while True:
        time.sleep(5)

        # --------------------------------------------
        # Load ticks
        # --------------------------------------------
        df = resampler.load("BTCUSDT")

        if df.empty:
            print("Waiting for ticks...")
            continue

        # --------------------------------------------
        # Resample
        # --------------------------------------------
        bars = resampler.ohlc(df, "1s")

        if len(bars) < 20:
            print("Waiting for sufficient bars...")
            continue

        # --------------------------------------------
        # Run analytics
        # --------------------------------------------
        out = engine.run(bars)

        if out is None:
            print("Liquidity filter active — skipping analytics cycle")
            continue

        # --------------------------------------------
        # Alerts
        # --------------------------------------------
        recent_z = out["zscore"].dropna().tail(20)
        alerts = zscore_alert(out["latest"], recent_z)

        if alerts:
            print("ALERTS:", alerts)
        else:
            z = out["latest"]["zscore"]
            if z is not None:
                print("Latest z-score:", round(z, 3))
