import pandas as pd
import sqlite3

class Resampler:
    def __init__(self, db="ticks.db"):
        self.db = db

    def load(self, symbol):
        conn = sqlite3.connect(self.db)
        df = pd.read_sql(
            "SELECT * FROM ticks WHERE symbol=? ORDER BY timestamp",
            conn,
            params=(symbol,)
        )
        conn.close()

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df

    def ohlc(self, df, tf="1s"):
        ohlc = df["price"].resample(tf).ohlc()
        vol = df["qty"].resample(tf).sum()
        ohlc["volume"] = vol
        return ohlc.dropna()
