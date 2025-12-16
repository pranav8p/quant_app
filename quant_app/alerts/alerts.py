def zscore_alert(latest, recent_zscores=None):
    alerts = []

    z = latest.get("zscore")
    vol = latest.get("volume")
    corr = latest.get("correlation")

    # Z-score extreme (latest)
    if z is not None and abs(z) >= 2.0:
        alerts.append("Z_SCORE_EXTREME")

    # Z-score extreme (recent window)
    if recent_zscores is not None:
        if recent_zscores.abs().max() >= 2.0:
            alerts.append("Z_SCORE_EXTREME_RECENT")

    if vol is not None and vol < 20:
        alerts.append("LOW_LIQUIDITY")

    if corr is not None and corr < 0.3:
        alerts.append("WEAK_RELATIONSHIP")

    return list(set(alerts))
