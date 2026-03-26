import duckdb
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.project_1l.data_layer.regime_filter import RegimeMachine

DB_PATH = r"E:\project_1L\marketdata\catalog\marketdata.duckdb"

def generate_weekdays(start_date: str, end_date: str) -> List[str]:
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    days = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            days.append(current.strftime("%Y%m%d"))
        current += timedelta(days=1)
    return days

def record_trade(trades_list: List[Dict[str, Any]], date: str, position: int, entry_price: float, exit_price: float, reason: str):
    pnl_points = (exit_price - entry_price) * position
    gross_pnl = pnl_points * 2.0
    net_pnl = gross_pnl - 2.20
    trades_list.append({
        "date": date, "position": position, "entry": entry_price, 
        "exit": exit_price, "gross": gross_pnl, "net": net_pnl, "reason": reason
    })

def fast_run():
    rm = RegimeMachine(DB_PATH)
    dates = generate_weekdays("20260101", "20260131")
    regime_symbol = "MNQ.v.0"
    all_trades = []
    
    for date in dates:
        vp = rm.compute_previous_vp(date, regime_symbol)
        if not vp: continue
            
        poc, vah, val = vp
        target_date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
        
        row_path = rm.con.execute(f"SELECT parquet_path FROM mbp1_ok_files WHERE family='MNQ' AND yyyymmdd='{date}'").fetchone()
        if not row_path: continue
        parquet_path = row_path[0]
        
        # Load only what we need in an optimized way
        query = f"""
            SELECT ts_event, price/1e9 as price
            FROM read_parquet('{parquet_path}')
            WHERE symbol='MNQ.v.0' AND ts_event >= '{target_date} 08:30:00' AND ts_event <= '{target_date} 16:00:00'
            ORDER BY ts_event
        """
        df = rm.con.execute(query).df()
        
        rm.logged_today = False
        last_logged = None
        
        cash_protocol_logged = False
        strategy_initialized = False
        position = 0
        entry_price = 0.0
        pending_buy_limit = None
        pending_sell_limit = None
        target_price = None
        stop_loss = None
        
        for ts, price in zip(df['ts_event'], df['price']):
            regime = rm.evaluate_regime(ts, price, vp)
            if regime and regime != last_logged:
                last_logged = regime
            
            if rm.logged_today:
                if regime in ["PENDING_IMBALANCE", "REJECTION_UP", "REJECTION_DOWN"]:
                    if not cash_protocol_logged:
                        # [REGIME IMBALANCED: SITTING IN CASH]
                        cash_protocol_logged = True
                    continue
                elif regime == "BALANCE":
                    if not strategy_initialized:
                        pending_buy_limit = val
                        pending_sell_limit = vah
                        strategy_initialized = True
                    
                    if ts.hour == 15 and ts.minute >= 0 and position == 0 and strategy_initialized:
                        if pending_buy_limit or pending_sell_limit:
                            pending_buy_limit = None
                            pending_sell_limit = None
                    
                    if position == 0:
                        if pending_buy_limit is not None and price < pending_buy_limit:
                            position = 1
                            entry_price = pending_buy_limit
                            pending_buy_limit = None
                            pending_sell_limit = None
                            target_price = poc
                            stop_loss = val - 15.0
                        elif pending_sell_limit is not None and price > pending_sell_limit:
                            position = -1
                            entry_price = pending_sell_limit
                            pending_sell_limit = None
                            pending_buy_limit = None
                            target_price = poc
                            stop_loss = vah + 15.0
                    elif position != 0:
                        if ts.hour == 15 and ts.minute >= 55:
                            record_trade(all_trades, date, position, entry_price, price, "15:55 FORCE CLOSE")
                            position = 0
                        else:
                            if position == 1:
                                if price > target_price:
                                    record_trade(all_trades, date, position, entry_price, target_price, "TARGET")
                                    position = 0
                                elif price <= stop_loss:
                                    record_trade(all_trades, date, position, entry_price, stop_loss, "STOP LOSS")
                                    position = 0
                            elif position == -1:
                                if price < target_price:
                                    record_trade(all_trades, date, position, entry_price, target_price, "TARGET")
                                    position = 0
                                elif price >= stop_loss:
                                    record_trade(all_trades, date, position, entry_price, stop_loss, "STOP LOSS")
                                    position = 0

    print("\n========================================")
    print("BACKTEST SUMMARY - JANUARY 2026")
    total_trades = len(all_trades)
    net_pnl = sum(t["net"] for t in all_trades)
    wins = sum(1 for t in all_trades if t["net"] > 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0
    
    peak = 0.0
    max_dd = 0.0
    cumulative = 0.0
    for t in all_trades:
        cumulative += t["net"]
        if cumulative > peak: peak = cumulative
        dd = peak - cumulative
        if dd > max_dd: max_dd = dd
            
    print(f"Total Trades:  {total_trades}")
    print(f"Win Rate:      {win_rate:.2f}%")
    print(f"Net PnL:       ${net_pnl:.2f}")
    print(f"Max Drawdown:  ${max_dd:.2f}")
    print("========================================\n")

if __name__ == "__main__":
    fast_run()
