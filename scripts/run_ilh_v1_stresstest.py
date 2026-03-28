from __future__ import annotations
import argparse
from pathlib import Path
from typing import List
from datetime import datetime, timedelta

from src.project_1l.data_layer.regime_filter import RegimeMachine

DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")

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

def run_ilh_batch(dates: List[str]):
    regime_machine = RegimeMachine(DB_PATH)
    regime_symbol = "MNQ.v.0"
    
    trades = []
    
    for date in dates:
        vp_levels = regime_machine.compute_previous_vp(date, regime_symbol)
        if not vp_levels:
            continue
            
        prev_poc, prev_vah, prev_val = vp_levels
        
        target_date = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
        row_path = regime_machine.con.execute(f"SELECT parquet_path FROM mbp1_ok_files WHERE family='MNQ' AND yyyymmdd='{date}'").fetchone()
        if not row_path: continue
        parquet_path = row_path[0]
        
        query = f"""
            SELECT ts_event, price/1e9 as price
            FROM read_parquet('{parquet_path}')
            WHERE symbol='MNQ.v.0' AND ts_event >= '{target_date} 08:30:00' AND ts_event <= '{target_date} 16:00:00'
            ORDER BY ts_event
        """
        df = regime_machine.con.execute(query).df()
        if df.empty:
            continue

        # INITIALIZE AT START OF DAY (09:30 EST)
        active_strategy = 0
        pending_dir = 0
        pending_time = None
        pending_strat = 0
        position = 0
        entry_time = None
        entry_price = 0.0
        stop_loss = 0.0
        target = 0.0
        traded_today = False  # THE MACHINE GUN SAFETY LOCK
        gate_checked = False  # <--- RESETS THE 15-MINUTE GATE
        mfe_price = 0.0       # <--- RESETS THE TRAILING STOP HIGH-WATER MARK
        regime_machine.logged_today = False
        
        def close_position(price: float, reason: str, current_time: datetime):
            nonlocal position, active_strategy, entry_price, entry_time
            # Slippage on exit
            exit_price = price * (1 - 0.0005) if position == 1 else price * (1 + 0.0005)
            gross_pnl = (exit_price - entry_price) * position * 2.0
            # Fee: 0.05% of notional on both entry and exit
            total_fee = (entry_price + exit_price) * 0.0005 * 2.0
            net_pnl = gross_pnl - total_fee
            
            trades.append({
                "date": date,
                "strategy": active_strategy,
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": current_time,
                "exit_price": exit_price,
                "reason": reason,
                "gross_pnl": gross_pnl,
                "net_pnl": net_pnl
            })
            position = 0

        # ... [Loop through daily ticks/minutes] ...
        for current_time, current_price in zip(df['ts_event'], df['price']):
            # Regime filter state initialization
            regime_state = regime_machine.evaluate_regime(current_time, current_price, vp_levels)
            if not regime_machine.logged_today:
                continue
                
            # 1. THE ENTRY LOGIC (With Safety Lock)
            # Latency execution
            if pending_dir != 0 and current_time >= pending_time:
                position = pending_dir
                # Execute with slippage on ENTRY
                entry_price = current_price * (1 + 0.0005) if position == 1 else current_price * (1 - 0.0005)
                active_strategy = pending_strat
                entry_time = current_time
                if position == 1:
                    stop_loss = entry_price - 15.0
                    target = entry_price + 100.0 if active_strategy == 2 else prev_poc
                else:
                    stop_loss = entry_price + 15.0
                    target = entry_price - 100.0 if active_strategy == 2 else prev_poc
                traded_today = True
                pending_dir = 0
            
            if position == 0 and pending_dir == 0 and not traded_today:
                if regime_state == "BALANCE":
                    if current_price < prev_val:
                        pending_dir = 1
                        pending_time = current_time + timedelta(milliseconds=200)
                        pending_strat = 1
                        
                    elif current_price > prev_vah:
                        pending_dir = -1
                        pending_time = current_time + timedelta(milliseconds=200)
                        pending_strat = 1

                elif regime_state == "PENDING_IMBALANCE":
                    if regime_machine.rth_open_price > prev_vah and current_price <= (prev_vah + 5.0):
                        pending_dir = 1
                        pending_time = current_time + timedelta(milliseconds=200)
                        pending_strat = 2
                        
                    elif regime_machine.rth_open_price < prev_val and current_price >= (prev_val - 5.0):
                        pending_dir = -1
                        pending_time = current_time + timedelta(milliseconds=200)
                        pending_strat = 2

            # 2. THE EXIT LOGIC
            elif position != 0:
                
                # --- >>> 1. UPDATE THE HIGH-WATER MARK (MFE) <<< ---
                if mfe_price == 0.0:
                    mfe_price = current_price
                elif position == 1:
                    mfe_price = max(mfe_price, current_price)
                elif position == -1:
                    mfe_price = min(mfe_price, current_price)

                # --- >>> 2. STRATEGY 2 RATCHET TRAILING STOP <<< ---
                if active_strategy == 2:
                    activation_points = 20.0  # Start trailing after 20 points
                    trail_distance = 15.0     # Trail 15 points behind peak
                    
                    if position == 1:
                        if (mfe_price - entry_price) >= activation_points:
                            new_stop = mfe_price - trail_distance
                            if new_stop > stop_loss:  # Only move UP
                                stop_loss = new_stop
                                
                    elif position == -1:
                        if (entry_price - mfe_price) >= activation_points:
                            new_stop = mfe_price + trail_distance
                            if new_stop < stop_loss:  # Only move DOWN
                                stop_loss = new_stop

                # --- >>> 3. STRATEGY 2 TIME GATE (15-Minute False Breakout) <<< ---
                if active_strategy == 2 and not gate_checked:
                    if current_time >= entry_time + timedelta(minutes=15):
                        gate_checked = True 
                        
                        # Bullish Failure
                        if position == 1 and current_price < prev_vah:
                            close_position(price=current_price, reason="15-MIN GATE FAIL", current_time=current_time)
                            continue 
                            
                        # Bearish Failure
                        elif position == -1 and current_price > prev_val:
                            close_position(price=current_price, reason="15-MIN GATE FAIL", current_time=current_time)
                            continue 

                # --- >>> 4. STANDARD EXITS (Target & Hard Stop) <<< ---
                # Long Exits
                if position == 1:
                    if current_price >= target:
                        close_position(price=target, reason="TARGET", current_time=current_time)
                    elif current_price <= stop_loss:
                        close_position(price=stop_loss, reason="STOP LOSS", current_time=current_time)
                        
                # Short Exits
                elif position == -1:
                    if current_price <= target:
                        close_position(price=target, reason="TARGET", current_time=current_time)
                    elif current_price >= stop_loss:
                        close_position(price=stop_loss, reason="STOP LOSS", current_time=current_time)

            # 3. TIME EXITS (15:55 EST)
            if current_time.hour == 15 and current_time.minute >= 55 and position != 0:
                close_position(price=current_price, reason="TIME EXPIRY", current_time=current_time)

    # Calculate and print summary matrix
    print("\n" + "="*40)
    print("BACKTEST SUMMARY MATRIX")
    print("="*40)
    total_trades = len(trades)
    print(f"Total Trades: {total_trades}")
    
    if total_trades > 0:
        # (Fees and Slippage now integrated per trade)

        net_pnl = sum(t["net_pnl"] for t in trades)
        winners = sum(1 for t in trades if t["net_pnl"] > 0)
        win_rate = (winners / total_trades) * 100
        
        gross_profit = sum(t["net_pnl"] for t in trades if t["net_pnl"] > 0)
        gross_loss = abs(sum(t["net_pnl"] for t in trades if t["net_pnl"] < 0))
        pf = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        print(f"Profit Factor: {pf:.2f}")
        print(f"Net PnL: ${net_pnl:.2f}")
        print(f"Win Rate: {win_rate:.2f}%")
        
        max_drawdown = 0.0
        peak = 0.0
        cumulative = 0.0
        for t in trades:
            cumulative += t["net_pnl"]
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_drawdown:
                max_drawdown = dd
        print(f"Max Drawdown: ${max_drawdown:.2f}")
    else:
        print("Net PnL: $0.00")
        print("Win Rate: 0.00%")
        print("Max Drawdown: $0.00")
    print("="*40 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", required=True, type=str, help="Start date YYYYMMDD")
    parser.add_argument("--end-date", required=True, type=str, help="End date YYYYMMDD")
    args = parser.parse_args()
    
    run_ilh_batch(generate_weekdays(args.start_date, args.end_date))
