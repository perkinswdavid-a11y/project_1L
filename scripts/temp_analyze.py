import csv
from collections import defaultdict

paths = [
    ('Dev-A', 'E:/project_1L/marketdata/backtests/20260309T190952_opening_range_breakout_v6a_dev_a/closed_trades.csv'),
    ('Dev-B', 'E:/project_1L/marketdata/backtests/20260309T191007_opening_range_breakout_v6a_dev_b/closed_trades.csv')
]

with open('E:/project_1L/marketdata/backtests/v6a_analysis.txt', 'w', encoding='utf-8') as out_f:
    for split, path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            counts = defaultdict(int)
            metrics = defaultdict(lambda: {'net_pnl': 0.0, 'mae_r': 0.0, 'mfe_r': 0.0, 'bars_held': 0.0, 'count': 0})
            
            for row in data:
                reason = row['exit_reason']
                counts[reason] += 1
                metrics[reason]['count'] += 1
                metrics[reason]['net_pnl'] += float(row['net_pnl'])
                
                mae_r = float(row['mae_r']) if row['mae_r'] else 0.0
                mfe_r = float(row['mfe_r']) if row['mfe_r'] else 0.0
                metrics[reason]['mae_r'] += mae_r
                metrics[reason]['mfe_r'] += mfe_r
                metrics[reason]['bars_held'] += float(row['bars_held'])
                
            out_f.write(f'\n--- {split} ---\n')
            out_f.write('Exit Reasons:\n')
            for k, v in counts.items():
                out_f.write(f'  {k}: {v}\n')
                
            out_f.write('\nMetrics per Exit Reason:\n')
            for k, v in metrics.items():
                c = v['count']
                out_f.write(f'  {k} -> Net PnL: {v["net_pnl"]/c:.2f}, MAE_R: {v["mae_r"]/c:.2f}, MFE_R: {v["mfe_r"]/c:.2f}, Bars: {v["bars_held"]/c:.1f}\n')
        except Exception as e:
            out_f.write(f'Error reading {path}: {e}\n')
