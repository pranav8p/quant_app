from statsmodels.tsa.stattools import adfuller

def adf_test(series):
    series = series.dropna()

    result = adfuller(series)
    return {
        "adf_statistic": result[0],
        "p_value": result[1],
        "critical_values": result[4]
    }
