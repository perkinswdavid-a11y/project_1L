import re

with open(r'c:\Users\WDavi\.vscode\project_1L\scripts\run_ilh_v1_stresstest.py', 'r') as f:
    text = f.read()

# Replace variables init
text = text.replace(
'''        # INITIALIZE AT START OF DAY (09:30 EST)
        active_strategy = 0''',
'''        # INITIALIZE AT START OF DAY (09:30 EST)
        active_strategy = 0
        pending_dir = 0
        pending_time = None
        pending_strat = 0'''
)

# Replace close position
old_close = '''        def close_position(price: float, reason: str, current_time: datetime):
            nonlocal position, active_strategy, entry_price, entry_time
            gross_pnl = (price - entry_price) * position * 2.0
            net_pnl = gross_pnl - 2.20
            
            trades.append({
                "date": date,
                "strategy": active_strategy,
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": current_time,
                "exit_price": price,
                "reason": reason,
                "gross_pnl": gross_pnl,
                "net_pnl": net_pnl
            })
            position = 0'''

new_close = '''        def close_position(price: float, reason: str, current_time: datetime):
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
            position = 0'''
text = text.replace(old_close, new_close)

# Replace Entry loop
old_entry_loop = '''            # 1. THE ENTRY LOGIC (With Safety Lock)
            if position == 0 and not traded_today:
                if regime_state == "BALANCE":
                    if current_price < prev_val:
                        position = 1
                        entry_price = prev_val
                        stop_loss = prev_val - 15.0
                        target = prev_poc
                        active_strategy = 1
                        entry_time = current_time
                        traded_today = True  # THE MACHINE GUN KILL-SWITCH
                        
                    elif current_price > prev_vah:
                        position = -1
                        entry_price = prev_vah
                        stop_loss = prev_vah + 15.0
                        target = prev_poc
                        active_strategy = 1
                        entry_time = current_time
                        traded_today = True  # THE MACHINE GUN KILL-SWITCH

                # >>> PASTE THIS NEW STRATEGY 2 BLOCK RIGHT HERE <<<
                elif regime_state == "PENDING_IMBALANCE":
                    # STRATEGY 2: TREND CONTINUATION (With 5-Point Zone)
                    
                    # Bullish: Open above VAH, pullback gets within 5 points of VAH
                    if regime_machine.rth_open_price > prev_vah and current_price <= (prev_vah + 5.0):
                        position = 1
                        entry_price = current_price  # Entering at market in the zone
                        stop_loss = entry_price - 15.0
                        target = entry_price + 100.0  
                        active_strategy = 2
                        entry_time = current_time
                        traded_today = True  
                        
                    # Bearish: Open below VAL, pullback gets within 5 points of VAL
                    elif regime_machine.rth_open_price < prev_val and current_price >= (prev_val - 5.0):
                        position = -1
                        entry_price = current_price  # Entering at market in the zone
                        stop_loss = entry_price + 15.0
                        target = entry_price - 100.0  
                        active_strategy = 2
                        entry_time = current_time
                        traded_today = True'''

new_entry_loop = '''            # 1. THE ENTRY LOGIC (With Safety Lock)
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
                        pending_strat = 2'''

text = text.replace(old_entry_loop, new_entry_loop)

# Disable the second layer of institutional fee because we computed total_fee dynamically per prompt
text = text.replace(
'''        # --- >>> NEW: INSTITUTIONAL FRICTION TAX <<< ---
        friction_per_trade = 2.24  # $1.24 commissions + $1.00 total slippage
        
        # Tax every individual trade FIRST so Win Rate and Drawdown are mathematically pure
        for t in trades:
            t["net_pnl"] -= friction_per_trade''',
'''        # (Fees and Slippage now integrated per trade)'''
)

with open(r'c:\Users\WDavi\.vscode\project_1L\scripts\run_ilh_v1_stresstest.py', 'w') as f:
    f.write(text)
