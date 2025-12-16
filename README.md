
### ✅ **FINAL `README.md` (USE THIS)**

```markdown
# Real-Time Quant Analytics Dashboard

## Project Description

This project implements a real-time quantitative analytics system for monitoring statistical signals on live cryptocurrency market data. The system ingests tick-level data, aggregates it into multiple timeframes, computes statistical indicators, and visualizes the results through an interactive dashboard.

The focus of this project is to demonstrate data ingestion, time-series resampling, statistical analysis, alerting, and visualization in a unified pipeline.

---

## Features

- Live market data ingestion using Binance WebSocket
- Tick data storage using SQLite
- OHLC bar generation for multiple timeframes
- Spread and Z-score computation
- Rolling correlation analysis
- Mean-reversion backtesting logic
- Rule-based alert generation
- Interactive Streamlit dashboard
- CSV export of analytics data

---

## Folder Structure

```

gamescap/
│
├── quant_app/
│   ├── alerts/
│   │   └── alerts.py
│   │
│   ├── analytics/
│   │   ├── backtest.py
│   │   ├── engine.py
│   │   ├── heatmap.py
│   │   ├── kalman.py
│   │   ├── regression.py
│   │   ├── stationarity.py
│   │   └── stats.py
│   │
│   ├── ingestion/
│   │   └── websocket_client.py
│   │
│   ├── resampling/
│   │   └── resampler.py
│   │
│   ├── storage/
│   │   └── db.py
│   │
│   ├── app.py
│   ├── frontend.py
│   └── ticks.db
│
└── quant-env/

````

---

## System Flow

1. Market ticks are received via WebSocket
2. Tick data is stored in a local SQLite database
3. Stored data is resampled into OHLC bars
4. Statistical analytics are computed on resampled data
5. Alerts are generated based on predefined rules
6. Results are displayed on a live dashboard

---

## Setup Instructions

### Create Virtual Environment

```bash
python -m venv quant-env
````

Activate the environment:

* Windows:

```bash
quant-env\Scripts\activate
```

* Linux / macOS:

```bash
source quant-env/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Start Backend

```bash
python app.py
```

This starts:

* WebSocket ingestion
* Data storage
* Analytics computation
* Terminal-based alerts

---

### Start Frontend

In a separate terminal:

```bash
streamlit run frontend.py
```

The dashboard updates automatically at regular intervals.

---

## Dashboard Overview

The dashboard displays:

* Latest price metrics
* Z-score and correlation values
* Trade count and PnL from backtest logic
* Time-series plots for price, spread, and Z-score
* Recent OHLC data table
* CSV download option

---

## ChatGPT Usage Disclosure

ChatGPT was used as a development assistant to help with debugging, code structuring, and documentation drafting. All code was reviewed, tested, and integrated manually.

---

## Notes

* For demonstration purposes, a lagged version of the same asset is used to illustrate spread-based analytics.
* The project is designed for educational and evaluation purposes.

---

## Conclusion

This project demonstrates a complete pipeline for real-time data ingestion, statistical analysis, alerting, and visualization using Python.

```


