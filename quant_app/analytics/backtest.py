def mean_reversion_backtest(zscore, entry=2.0):
    position = 0          # 1 = long, -1 = short, 0 = flat
    entry_z = None
    pnl = 0.0
    trades = 0

    for z in zscore:
        if z is None:
            continue

        # -------------------------
        # ENTRY
        # -------------------------
        if position == 0:
            if z >= entry:
                position = -1
                entry_z = z
            elif z <= -entry:
                position = 1
                entry_z = z

        # -------------------------
        # EXIT (mean reversion)
        # -------------------------
        elif position == 1 and z >= 0:
            pnl += z - entry_z
            trades += 1
            position = 0

        elif position == -1 and z <= 0:
            pnl += entry_z - z
            trades += 1
            position = 0

    return {
        "trades": trades,
        "pnl": pnl
    }
