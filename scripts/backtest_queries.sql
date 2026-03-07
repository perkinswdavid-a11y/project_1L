-- Latest backtest runs
SELECT
    run_id,
    created_at,
    family,
    interval,
    strategy,
    start_date,
    end_date,
    final_equity,
    net_pnl,
    total_return_pct,
    max_drawdown_pct,
    daily_sharpe_approx
FROM backtest.runs
ORDER BY created_at DESC
LIMIT 20;

-- Daily equity for a specific run
-- Replace the run_id literal before running.
SELECT *
FROM backtest.daily_equity
WHERE run_id = 'REPLACE_ME'
ORDER BY trade_date;

-- Closed trades for a specific run
SELECT *
FROM backtest.closed_trades
WHERE run_id = 'REPLACE_ME'
ORDER BY exit_ts;

-- Execution log for a specific run
SELECT *
FROM backtest.executions
WHERE run_id = 'REPLACE_ME'
ORDER BY ts;

-- Compare multiple runs by strategy and family
SELECT
    family,
    interval,
    strategy,
    COUNT(*) AS run_count,
    AVG(net_pnl) AS avg_net_pnl,
    AVG(total_return_pct) AS avg_return_pct,
    AVG(max_drawdown_pct) AS avg_max_drawdown_pct
FROM backtest.runs
GROUP BY 1, 2, 3
ORDER BY family, interval, strategy;