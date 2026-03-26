import re

with open("scripts/run_ilh_v1.py", "r", encoding="utf-8") as f:
    text = f.read()

import_str = "import argparse\nimport csv\n"
text = text.replace("import argparse\n", import_str)

old_rt = """def record_trade(trades_list: List[Dict[str, Any]], date: str, position: int, entry_price: float, exit_price: float, reason: str, strat: str):
    pnl_points = (exit_price - entry_price) * position
    gross_pnl = pnl_points * 2.0
    net_pnl = gross_pnl - 2.20
    
    trades_list.append({
        "date": date,
        "position": position,
        "entry": entry_price,
        "exit": exit_price,
        "gross": gross_pnl,
        "net": net_pnl,
        "reason": reason,
        "strat": strat
    })"""
new_rt = """def record_trade(date: str, strat: str, entry_t: str, entry_p: float, exit_t: str, exit_p: float, reason: str, position: int):
    pnl_points = (exit_p - entry_p) * position
    gross_pnl = pnl_points * 2.0
    net_pnl = gross_pnl - 2.20
    with open("trades_q1.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, strat, entry_t, entry_p, exit_t, exit_p, reason, gross_pnl, net_pnl])"""
text = text.replace(old_rt, new_rt)

text = text.replace("pending_sell_limit = None\n                        if active_strategy == 1:", "pending_sell_limit = None\n                        entry_time = ts\n                        if active_strategy == 1:")
text = text.replace("pending_buy_limit = None\n                        if active_strategy == 1:", "pending_buy_limit = None\n                        entry_time = ts\n                        if active_strategy == 1:")

text = text.replace("record_trade(all_trades, date, position, entry_price, exit_price, reason, str(active_strategy))", "record_trade(date, str(active_strategy), str(entry_time), entry_price, str(ts), exit_price, reason, position)")

text = re.sub(r'print\(f"\\n--- STRAT 2 LOG TRADE.*?\\n"\)', '', text)
text = re.sub(r'print\(f"Entry: Time=\{ts\}, Price=\{entry_price\}, Type=.*?"\)', '', text)
text = re.sub(r'print\(f"Gate Status: \{status_msg\} \(Time=\{ts\}, Price=\{price\}\)"\)', '', text)
text = re.sub(r'print\(f"Exit: Time=\{ts\}, Price=\{exit_price\}, Reason=\{reason\}"\)', '', text)

# Remove manual print guards
text = re.sub(r'if strat2_trade_count < 3:\n\s+strat2_trade_count \+= 1', '', text)
text = re.sub(r'strat2_trade_count \+= 1', '', text)
text = re.sub(r'if strat2_trade_count < 3:', '', text)
text = re.sub(r'if active_strategy == 2 and strat2_trade_count < 3:', '', text)
text = re.sub(r'strat2_trade_count = 0', '', text)
text = re.sub(r'if active_strategy == 2:\n\s+halt_trading_today = True', 'if active_strategy == 2:\n                                    halt_trading_today = True', text)


summary_regex = r'print\("\\n========================================"\).*?print\(f"Strat 2 Trades: \{len\(strat2\)\}"\)'
text = re.sub(summary_regex, 'print("[PROCESS COMPLETE: trades_q1.csv GENERATED]")', text, flags=re.DOTALL)
ledger_regex = r'print\("\\n--- DETAILED TRADE LEDGER ---"\).*?print\(f"#\{i\+1\}.*?"\)'
text = re.sub(ledger_regex, '', text, flags=re.DOTALL)

text = text.replace("def run_ilh_batch(dates: List[str]):", "def run_ilh_batch(dates: List[str]):\n    with open('trades_q1.csv', 'w', newline='') as f:\n        f.write('Date,Strategy_Num,Entry_Time,Entry_Price,Exit_Time,Exit_Price,Exit_Reason,Gross_PnL,Net_PnL\\n')")

text = re.sub(r'print\(f"Executing Fast Query for \{date\} \(08:30:00 to 16:00:00\)..."\)', '', text)
text = re.sub(r'print\(f"Running chronological tick-by-tick simulation over \{len\(dates\)\} days..."\)', '', text)

# Also remove 'all_trades = []' logic since it's unused, or just leave it.

with open("scripts/run_ilh_v1.py", "w", encoding="utf-8") as f:
    f.write(text)
