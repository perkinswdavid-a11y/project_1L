import re
import json

log_path = r'c:\Users\WDavi\.vscode\project_1L\docs\research\strategy_experiment_log.md'
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

experiments = []
blocks = text.split('## EXP-')
for block in blocks[1:]:
    lines = block.strip().split('\n')
    header = lines[0]
    
    if not ('opening_range_breakout_v14a' in header or 'opening_range_breakout_v17a' in header):
        continue
    
    strategy_match = re.search(r'- \*\*Strategy:\*\* `(.*?)`', block)
    dates_match = re.search(r'- \*\*Date Range:\*\* `(.*?)`', block)
    
    if not strategy_match or not dates_match:
        continue
        
    strategy = strategy_match.group(1)
    dates = dates_match.group(1)
    
    metrics = {}
    table_started = False
    for line in block.split('\n'):
        if line.startswith('| Metric | Value |'):
            table_started = True
            continue
        if table_started:
            if not line.startswith('|') or '---' in line:
                if len(metrics) > 0 and not line.startswith('|'):
                    break
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                name = parts[1]
                val = parts[2]
                if name:
                    metrics[name] = val
                    
    experiments.append({
        'header': header,
        'strategy': strategy,
        'dates': dates,
        'metrics': metrics
    })

latest = {}
for exp in experiments:
    key = f"{exp['strategy']}_{exp['dates']}"
    latest[key] = exp

with open('temp_metrics.json', 'w') as f:
    json.dump(latest, f, indent=2)

print("Metrics extracted to temp_metrics.json")
