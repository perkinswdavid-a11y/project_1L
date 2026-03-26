import pandas as pd

try:
    df = pd.read_csv('trades_q1.csv')
    total_trades = len(df)
    net_pnl = df['Net_PnL'].sum() if total_trades > 0 else 0.0
    wins = len(df[df['Net_PnL'] > 0])
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0
    
    peak = 0.0
    max_dd = 0.0
    cumulative = 0.0
    for _, row in df.iterrows():
        cumulative += row['Net_PnL']
        if cumulative > peak:
            peak = cumulative
        dd = peak - cumulative
        if dd > max_dd:
            max_dd = dd
            
    strat1 = len(df[df['Strategy_Num'] == 1])
    strat2 = len(df[df['Strategy_Num'] == 2])
    
    print("========================================")
    print("BACKTEST SUMMARY - ENSEMBLE Q1 2026")
    print(f"Total Trades:  {total_trades}")
    print(f"Win Rate:      {win_rate:.2f}%")
    print(f"Net PnL:       ${net_pnl:.2f}")
    print(f"Max Drawdown:  ${max_dd:.2f}")
    print("========================================")
    print(f"Strat 1 Trades: {strat1}")
    print(f"Strat 2 Trades: {strat2}")
    
    print("\n--- JAN 7TH CHECK ---")
    jan7 = df[df['Date'] == 20260107]
    print(jan7)
except Exception as e:
    print(e)
