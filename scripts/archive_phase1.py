import shutil
import os
from pathlib import Path

root = Path(r"c:\Users\WDavi\.vscode\project_1L")
archive_root = root / "archive" / "Phase_1_ORB"

# 1. Archive Configs
active_configs_dir = root / "configs" / "active"
archive_configs_dir = archive_root / "configs"
if active_configs_dir.exists():
    for f in active_configs_dir.iterdir():
        if f.is_file():
            shutil.move(str(f), str(archive_configs_dir / f.name))

# 2. Archive Root Asset Documentation
root_docs = ["STRATEGY.md", "TRADE_RULES.md", "PARAMS.md", "OVERVIEW.md", "EXECUTION_SPEC.md", "v22a_code_inventory.md", "v23a_final_inventory.md", "data_transfer_plan.md"]
archive_docs_dir = archive_root / "docs"
for doc in root_docs:
    p = root / doc
    if p.exists():
        shutil.move(str(p), str(archive_docs_dir / doc))

# 3. Archive Root logs and txt files
archive_logs_dir = archive_root / "logs"
for f in root.iterdir():
    if f.is_file() and (f.suffix in [".log", ".txt"] or f.name.endswith(".log")):
        shutil.move(str(f), str(archive_logs_dir / f.name))

# 4. Archive Strategy Scripts
strategy_scripts = [
    "replay_backtest_v4b.py",
    "audit_v20a.py",
    "audit_v21a.py",
    "audit_v21a_pf.py",
    "backtest_sma_cross_1m.py",
    "backtest_sma_cross_1m_smoke.py",
    "extract_trades.py",
    "check_data_range_v2.py",
    "check_data_range_v3.py",
    "list_tables.py",
    "format_table.py",
    "temp_analyze.py",
    "backtest_queries.sql",
    "bar_queries.sql",
    "queries.sql"
]
scripts_dir = root / "scripts"
archive_scripts_dir = archive_root / "scripts"
for script in strategy_scripts:
    p = scripts_dir / script
    if p.exists():
        shutil.move(str(p), str(archive_scripts_dir / script))

# 5. Archive the old Research Log
old_log = root / "docs" / "research" / "strategy_experiment_log.md"
if old_log.exists():
    shutil.move(str(old_log), str(archive_root / "strategy_experiment_log_PHASE1.md"))

print("Archive Complete.")
