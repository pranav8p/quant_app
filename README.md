# Real-Time Quant Analytics Dashboard

## Project Description

This project implements a real-time quantitative analytics system for monitoring statistical signals on live cryptocurrency market data. The system ingests tick-level data, stores it locally, resamples it into multiple timeframes, computes statistical indicators, and visualizes the results using an interactive dashboard.

The project is intended for educational and evaluation purposes and demonstrates end-to-end data ingestion, analytics, alerting, and visualization.

---

## Features

- Live cryptocurrency market data ingestion using Binance WebSocket
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

## System Architecture

### Architecture Diagram

![System Architecture](architecture_diagram.png)
![sig](https://github.com/user-attachments/assets/7bf0a1b1-96d9-4e74-8fd3-57119c586566)


### Architecture Description

The system follows a modular pipeline architecture:

1. **Data Ingestion**
   - Live tick data is received from Binance using a WebSocket connection.

2. **Storage Layer**
   - Incoming tick data is stored in a local SQLite database for persistence.

3. **Resampling Engine**
   - Stored tick data is aggregated into OHLC bars across multiple timeframes (1s, 5min, 10min).

4. **Analytics Engine**
   - Computes statistical analytics including spread, Z-score, rolling correlation, and mean-reversion backtesting.
   - Applies liquidity filtering to avoid unreliable signals.

5. **Alert Engine**
   - Generates rule-based alerts based on Z-score thresholds, liquidity conditions, and correlation strength.

6. **Frontend Dashboard**
   - Displays live metrics, charts, alerts, and tables using Streamlit.
   - Allows CSV export of analytics data.

---

## System Flow

1. Market tick data is received via WebSocket
2. Tick data is stored in a local SQLite database
3. Stored data is resampled into OHLC bars
4. Statistical analytics are computed on resampled data
5. Alerts are generated using predefined rules
6. Results are displayed in a live dashboard

---

## Setup Instructions

### Create Virtual Environment

```bash
python -m venv quant-env
````

Activate the environment:

**Windows**

```bash
quant-env\Scripts\activate
```

**Linux / macOS**

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

* WebSocket data ingestion
* Tick storage
* Analytics computation
* Terminal-based alerts

---

### Start Frontend

Open a new terminal and run:

```bash
streamlit run frontend.py
```

The dashboard updates automatically at regular intervals.

---

## Dashboard Overview

The dashboard displays:

* Latest price metrics
* Z-score and rolling correlation values
* Trade count and PnL from backtesting logic
* Time-series charts for price, spread, and Z-score
* Recent OHLC data table
* CSV download option for analytics output

---

## ChatGPT Usage Disclosure

ChatGPT was used as a development assistant to help with debugging, structuring code modules, and drafting documentation. All code was manually reviewed, tested, and integrated by the developer.

---

## Notes

* For demonstration purposes, a lagged version of the same asset is used to illustrate spread-based statistical analysis.
* The project is designed for learning and evaluation and is not intended for live trading.

---

## Conclusion

This project demonstrates a complete pipeline for real-time data ingestion, statistical analysis, alerting, and visualization using Python.
