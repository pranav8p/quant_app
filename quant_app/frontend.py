import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

from resampling.resampler import Resampler
from analytics.engine import AnalyticsEngine
from alerts.alerts import zscore_alert


# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Real-Time Quant Analytics",
    layout="wide"
)


# ======================================================
# HEADER
# ======================================================
st.title("📊 Real-Time Quant Analytics Dashboard")
st.caption("Live statistical arbitrage analytics using streaming market data")

heartbeat = random.randint(1000, 9999)
st.success(f"🟢 Live data stream active | Update ID: {heartbeat}")


# ======================================================
# CONTROLS
# ======================================================
st.subheader("⚙️ Controls")

tf_label = st.selectbox(
    "Select Timeframe",
    ["1 Second", "5 Minutes", "10 Minutes"],
    index=0
)

TF_MAP = {
    "1 Second": "1s",
    "5 Minutes": "5min",
    "10 Minutes": "10min"
}

timeframe = TF_MAP[tf_label]
st.caption(f"⏱️ Active Timeframe: {tf_label}")


# ======================================================
# LOAD DATA
# ======================================================
resampler = Resampler()
engine = AnalyticsEngine()
symbol = "BTCUSDT"

df = resampler.load(symbol)

if df.empty:
    st.warning("Waiting for market data...")
    st.stop()

bars = resampler.ohlc(df, timeframe)

min_bars_required = {
    "1s": 20,
    "5min": 10,
    "10min": 5
}

if len(bars) < min_bars_required[timeframe]:
    st.info(f"Waiting for sufficient data for {tf_label} timeframe...")
    st.stop()

out = engine.run(bars)

if out is None:
    st.info("Liquidity filter active — waiting for valid bars...")
    st.stop()

alerts = zscore_alert(out["latest"])


# ======================================================
# METRICS
# ======================================================
latest_price = bars["close"].iloc[-1]
latest_z = out["latest"]["zscore"]
latest_corr = out["latest"]["correlation"]

backtest = out.get("backtest", {"trades": 0, "pnl": 0.0})


m1, m2, m3, m4 = st.columns(4)

m1.metric("Price", f"{latest_price:,.2f}")
m2.metric("Z-score", f"{latest_z:.2f}" if latest_z is not None else "—")
m3.metric("Correlation", f"{latest_corr:.2f}" if latest_corr is not None else "—")
m4.metric("Trades", backtest["trades"])

if alerts:
    st.error(f"🚨 Alerts Triggered: {', '.join(alerts)}")
else:
    st.success("✅ No active alerts")


# ======================================================
# BACKTEST SUMMARY
# ======================================================
st.subheader("📈 Mean-Reversion Backtest Summary")

bt1, bt2 = st.columns(2)
bt1.metric("Total Trades", backtest["trades"])
bt2.metric("Total PnL (Z-units)", f"{backtest['pnl']:.2f}")


# ======================================================
# PRICE CHART (ZOOMED)
# ======================================================
price_data = bars["close"].tail(60)
p_min, p_max = price_data.min(), price_data.max()
pad = (p_max - p_min) * 0.25 if p_max != p_min else 1

fig_price = go.Figure()
fig_price.add_trace(go.Scatter(
    x=price_data.index,
    y=price_data.values,
    mode="lines",
    line=dict(color="#2563eb", width=2)
))

fig_price.update_layout(
    title="Price (Zoomed)",
    template="plotly_white",
    height=280,
    yaxis=dict(range=[p_min - pad, p_max + pad]),
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_price, use_container_width=True)


# ======================================================
# SPREAD + Z-SCORE
# ======================================================
c1, c2 = st.columns(2)

with c1:
    spread_data = out["spread"].dropna().tail(60)
    fig_spread = go.Figure()
    fig_spread.add_trace(go.Scatter(
        x=spread_data.index,
        y=spread_data.values,
        mode="lines",
        line=dict(color="#dc2626", width=2)
    ))
    fig_spread.update_layout(
        title="Spread",
        template="plotly_white",
        height=260
    )
    st.plotly_chart(fig_spread, use_container_width=True)

with c2:
    z_data = out["zscore"].dropna().tail(60)
    fig_z = go.Figure()
    fig_z.add_trace(go.Scatter(
        x=z_data.index,
        y=z_data.values,
        mode="lines",
        line=dict(color="#16a34a", width=2)
    ))
    fig_z.update_layout(
        title="Z-score",
        template="plotly_white",
        height=260,
        yaxis=dict(range=[-3, 3])
    )
    st.plotly_chart(fig_z, use_container_width=True)


# ======================================================
# CORRELATION
# ======================================================
corr_data = out["correlation"].dropna().tail(60)
fig_corr = go.Figure()
fig_corr.add_trace(go.Scatter(
    x=corr_data.index,
    y=corr_data.values,
    mode="lines",
    line=dict(color="#7c3aed", width=2)
))
fig_corr.update_layout(
    title="Rolling Correlation (Lagged)",
    template="plotly_white",
    height=260,
    yaxis=dict(range=[-1, 1])
)
st.plotly_chart(fig_corr, use_container_width=True)


# ======================================================
# LIVE DATA TABLE
# ======================================================
st.subheader("📥 Live Input Bars")

table_df = bars.tail(15).copy()
table_df.reset_index(inplace=True)
table_df.columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]

st.dataframe(table_df, use_container_width=True, height=350)


# ======================================================
# CSV EXPORT
# ======================================================
st.subheader("⬇️ Export Analytics")

export_df = pd.DataFrame({
    "timestamp": bars.index,
    "price": bars["close"],
    "volume": bars["volume"],
    "beta": out["beta"],
    "spread": out["spread"],
    "zscore": out["zscore"],
    "correlation": out["correlation"]
}).dropna()

st.download_button(
    label="Download CSV",
    data=export_df.to_csv(index=False).encode("utf-8"),
    file_name="quant_analytics.csv",
    mime="text/csv"
)


# ======================================================
# AUTO REFRESH (DEMO MODE)
# ======================================================
time.sleep(5)
st.rerun()
