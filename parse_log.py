with open("out_matrix.log", mode="rb") as f:
    try:
        content = f.read().decode("utf-16le", errors="ignore")
    except:
        content = f.read().decode("utf-8", errors="ignore")

lines = content.replace("\r", "\n").split("\n")

clean_lines = []
for line in lines:
    line = line.strip()
    if not line: continue
    if "BACKTEST" in line or "Total Trades:" in line or "Win Rate:" in line or "Net PnL:" in line or "Max Drawdown:" in line or "Strat 1 Trades:" in line or "Strat 2 Trades:" in line or "DETAILED TRADE LEDGER" in line or "#" in line:
        clean_lines.append(line)

print("\n".join(clean_lines))
