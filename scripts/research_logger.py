import json
import logging
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

LOG_PATH = Path("docs/research/strategy_experiment_log.md")

TEMPLATE = """# Project 1L Strategy Experiment Log

Canonical research record for Project 1L strategy experiments.

This document is the human-readable source of truth for:
- what was tested,
- why it was tested,
- what configuration was used,
- what the result was,
- what we think happened,
- and what we should do next.

## Why this file exists

Without a disciplined research log, systematic strategy development turns into noise:
- the same ideas get retested accidentally,
- failed ideas are rediscovered and repeated,
- good ideas lose context,
- and results become hard to compare across time.

This file is meant to function like an institutional research notebook:
- searchable,
- reproducible,
- append-only,
- and readable months later.

## Operating Rules

1. One completed run = one experiment record.
2. Never overwrite old records. Add new records.
3. Every record must include:
   - metadata,
   - configuration,
   - results,
   - interpretation,
   - recommendation.
4. Every follow-up test should change only one meaningful variable whenever possible.
5. A baseline that is clearly weak should be rejected quickly.
6. A baseline that is close enough to viability should be promoted and refined deliberately.
7. The top index table should always let us scan the research state in under one minute.
8. The detailed experiment entries should always let us reconstruct exactly what happened.

## Status Legend

- `COMPLETED` = run finished successfully
- `FAILED` = run failed and result is invalid
- `ABORTED` = run intentionally stopped
- `SUPERSEDED` = historically kept, but no longer an active reference baseline

## Decision Legend

- `PROMOTE` = continue testing this strategy / parameter direction
- `HOLD` = inconclusive, can revisit later
- `REJECT_CURRENT_BASELINE` = do not spend more time on this version right now
- `INVALID_RUN` = config / data / runtime issue prevents interpretation
- `SUPERSEDED` = replaced by a newer preferred baseline

---

## Experiment Index

| Experiment ID | Date | Status | Strategy | Family | Interval | Sample | Closed Trades | Trades/Tested Day | Profit Factor | Net PnL | Max DD % | Decision | Next Action | Run ID |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|

---

# Experiment Records

"""

def _ensure_template() -> None:
    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(TEMPLATE, encoding="utf-8")

def _get_git_metadata() -> Tuple[str, str]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL, timeout=2
        ).decode().strip()
    except Exception:
        commit = "unknown"
        
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL, timeout=2
        ).decode().strip()
    except Exception:
        branch = "unknown"
        
    if branch == "HEAD":
        branch = "detached"
        
    return commit, branch

def _derive_next_id() -> Tuple[str, str]:
    today = datetime.now().strftime("%Y%m%d")
    seq = 1
    
    if LOG_PATH.exists():
        content = LOG_PATH.read_text(encoding="utf-8")
        pattern = rf"EXP-{today}-(\d{{3}})"
        matches = re.findall(pattern, content)
        if matches:
            seq = max(int(m) for m in matches) + 1
            
    experiment_id = f"EXP-{today}-{seq:03d}"
    date_str = datetime.now().strftime("%Y-%m-%d")
    return experiment_id, date_str

def _check_duplicate_run_id(run_id: str) -> bool:
    if not run_id:
        return False
    if not LOG_PATH.exists():
        return False
    content = LOG_PATH.read_text(encoding="utf-8")
    return f"`{run_id}`" in content

def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        if val is None:
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

def log_experiment(
    config: Optional[Dict[str, Any]] = None,
    result: Optional[Dict[str, Any]] = None,
    error_msg: Optional[str] = None,
    config_path: Optional[str] = None
) -> None:
    _ensure_template()
    
    # Defaults and parsing
    config = config or {}
    result = result or {}
    
    run_id = result.get("run_id") or config.get("run_id") or "unknown"
    
    # Check duplicate on complete runs
    if not error_msg and run_id != "unknown" and _check_duplicate_run_id(run_id):
        logging.info(f"[LOGGER] Skipping duplicate research entry for run_id: {run_id}")
        return

    experiment_id, run_date = _derive_next_id()
    commit_hash, branch_name = _get_git_metadata()
    code_version = f"{branch_name} @ {commit_hash}"
    status = "FAILED" if error_msg else "COMPLETED"
    
    strategy = config.get("strategy", "unknown")
    family = config.get("family", "unknown")
    interval = config.get("interval", "unknown")
    sample_type = "SMOKE" if config.get("max_days") else "FULL"
    decision = config.get("research_decision") or ("INVALID_RUN" if error_msg else "TBD")
    decision_clean = decision.replace(" ", "_").upper()
    
    # Strategy Archetype (infer if possible)
    strategy_archetype = "unknown"
    if "reversion" in strategy.lower():
        strategy_archetype = "mean_reversion"
    elif "breakout" in strategy.lower() or "orb" in strategy.lower():
        strategy_archetype = "breakout"
    elif "trend" in strategy.lower() or "pullback" in strategy.lower() or "sma" in strategy.lower():
        strategy_archetype = "trend"

    next_action_cell = config.get("research_recommendation", "TBD")
    if error_msg:
        next_action_cell = "Fix error in config or execution"

    # Extraction for index row
    closed_trades = result.get("closed_trade_count", 0)
    profit_factor = result.get("profit_factor", 0.0)
    net_pnl = result.get("net_pnl", 0.0)
    max_dd_pct = result.get("max_drawdown_pct", 0.0)
    
    # Derivations
    days_tested = result.get("days_tested", 1)
    if days_tested <= 0:
        days_tested = 1

    trades_per_tested_day = closed_trades / days_tested
    win_rate_pct = result.get("win_rate_pct", 0.0)
    gross_profit = result.get("gross_profit", 0.0)
    gross_loss = result.get("gross_loss", 0.0)
    
    approx_winning_trades = int(round(closed_trades * win_rate_pct / 100))
    approx_losing_trades = closed_trades - approx_winning_trades
    approx_average_winner = gross_profit / approx_winning_trades if approx_winning_trades > 0 else 0.0
    approx_average_loser = gross_loss / approx_losing_trades if approx_losing_trades > 0 else 0.0
    approx_winner_loser_ratio = approx_average_winner / approx_average_loser if approx_average_loser > 0 else 0.0
    
    report_dir = result.get("report_dir") or "unknown"
    if config_path and status == "FAILED":
        report_dir = f"Config: {config_path}"

    # Generate Tags
    tag_strategy = f"#strategy/{strategy.replace('_', '')}" if strategy != "unknown" else ""
    tag_family = f"#family/{family}" if family != "unknown" else ""
    tag_interval = f"#interval/{interval}" if interval != "unknown" else ""
    tag_sample = f"#sample/{sample_type.lower()}"
    tag_status = f"#status/{status.lower()}"
    tag_decision = f"#decision/{decision_clean.lower()}"
    
    tags_line = f"**Tags:** {' '.join(filter(None, [tag_strategy, tag_family, tag_interval, tag_sample, tag_status, tag_decision]))}"

    # Build Index Row
    index_row_parts = [
        experiment_id,
        run_date,
        status,
        strategy,
        family,
        interval,
        sample_type,
        f"{closed_trades}",
        f"{trades_per_tested_day:.2f}",
        f"{profit_factor:.4f}",
        f"{net_pnl:.2f}",
        f"{max_dd_pct:.2f}",
        decision_clean,
        next_action_cell,
        run_id,
    ]
    index_row = "| " + " | ".join(index_row_parts) + " |\n"

    # Build Markdown Entry
    entry = f"""
## {experiment_id} | {strategy} | {family} | {interval} | {sample_type}

{tags_line}

**Status:** `{status}`  
**Decision:** `{decision_clean}`

### Metadata
- **Run ID:** `{run_id}`
- **Run Date:** `{run_date}`
- **Researcher:** `auto`
- **Code Version / Commit:** `{code_version}`
- **Report Directory:** `{report_dir}`
- **Strategy:** `{strategy}`
- **Strategy Archetype:** `{strategy_archetype}`
- **Family:** `{family}`
- **Interval:** `{interval}`
- **Sample Type:** `{sample_type}`
- **Date Range:** `{result.get('start_date', config.get('start_date', 'unknown'))} -> {result.get('end_date', config.get('end_date', 'unknown'))}`
- **Days Tested:** `{days_tested}`
- **Instrument Mode:** `{config.get('instrument_mode', 'unknown')}`
- **Instrument Key:** `{config.get('instrument_key', 'null')}`

### Research Question / Hypothesis
{config.get('research_hypothesis', 'TBD')}

### Change Description
- **Parent Experiment:** `{config.get('research_parent_experiment_id', 'TBD')}`
- **What changed:** `{config.get('research_change_description', 'TBD')}`
- **Why this run exists:** `{config.get('research_why_it_exists', 'TBD')}`

### Execution Assumptions
- **Session Timezone:** `{config.get('session_timezone', 'unknown')}`
- **Session:** `{config.get('session_start', 'unknown')} -> {config.get('session_end', 'unknown')}`
- **Flatten Daily:** `{str(config.get('flatten_daily', 'unknown')).lower()}`
- **Flatten On Last Bar:** `{str(config.get('flatten_on_last_bar', 'unknown')).lower()}`
- **Initial Cash:** `{config.get('initial_cash', 'unknown')}`
- **Contract Multiplier:** `{config.get('contract_multiplier', 'unknown')}`
- **Tick Size:** `{config.get('tick_size', 'unknown')}`
- **Slippage Ticks:** `{config.get('slippage_ticks', 'unknown')}`
- **Commission Per Side:** `{config.get('commission_per_side', 'unknown')}`

### Strategy Parameters
```json
{json.dumps(config.get('strategy_params', {}), indent=2)}
```

### Results
"""
    
    if error_msg:
        entry += f"Run failed with error:\n```\n{error_msg}\n```\n\n"
    else:
        entry += f"""| Metric | Value |
|---|---:|
| Final Equity | {result.get('final_equity', 0.0):.2f} |
| Net PnL | {net_pnl:.2f} |
| Total Return % | {result.get('total_return_pct', 0.0):.4f} |
| Max Drawdown Abs | {result.get('max_drawdown_abs', 0.0):.2f} |
| Max Drawdown % | {max_dd_pct:.4f} |
| Daily Sharpe Approx | {result.get('daily_sharpe_approx', 0.0):.4f} |
| Execution Count | {result.get('execution_count', 0)} |
| Closed Trade Count | {closed_trades} |
| Win Rate % | {win_rate_pct:.4f} |
| Gross Profit | {gross_profit:.2f} |
| Gross Loss | {gross_loss:.2f} |
| Profit Factor | {profit_factor:.4f} |
| Trades / Tested Day | {trades_per_tested_day:.2f} |
| Approx Winning Trades | {approx_winning_trades} |
| Approx Losing Trades | {approx_losing_trades} |
| Approx Average Winner | {approx_average_winner:.2f} |
| Approx Average Loser | {approx_average_loser:.2f} |
| Approx Winner / Loser Ratio | {approx_winner_loser_ratio:.2f} |

"""

    entry += f"""### Behavioral Read
{config.get('research_behavioral_read', 'TBD')}

### Interpretation
{config.get('research_interpretation', 'TBD')}

### Risk Notes
{config.get('research_risk_notes', 'TBD')}

### Recommendation / Next Action
{config.get('research_recommendation', 'TBD')}

### Artifacts
- **Report Directory:** `{report_dir}`
- **Closed Trades CSV:** `{os.path.join(report_dir, 'closed_trades.csv') if report_dir != 'unknown' and not error_msg else 'unknown'}`
- **Daily Equity CSV:** `{os.path.join(report_dir, 'daily_equity.csv') if report_dir != 'unknown' and not error_msg else 'unknown'}`

---
"""

    content = LOG_PATH.read_text(encoding="utf-8")
    
    # 1. Inject the index row at the top of the table.
    table_header = "| Experiment ID | Date | Status | Strategy | Family | Interval | Sample | Closed Trades | Trades/Tested Day | Profit Factor | Net PnL | Max DD % | Decision | Next Action | Run ID |\n|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|\n"
    if table_header in content:
        split_content = content.split(table_header, 1)
        content = split_content[0] + table_header + index_row + split_content[1]
    else:
        # Fallback if the header changed somehow
        logging.warning("Experiment index table header not found; skipping index update.")
    
    # 2. Append the entry to the end of the file.
    content += entry
    
    # 3. Write atomically back.
    temp_path = LOG_PATH.with_suffix(".md.tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(LOG_PATH)
    
    logging.info(f"[LOGGER] Automatically documented experiment {experiment_id} ({status})")
