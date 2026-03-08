import json
import os
import sys
from pathlib import Path

# Ensure we can import from scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_research_logger_can_create_from_template(tmp_path: Path):
    from scripts.research_logger import log_experiment, LOG_PATH
    import scripts.research_logger
    
    # Override log path
    scripts.research_logger.LOG_PATH = tmp_path / "test_log.md"
    
    config = {"strategy": "test_strat", "family": "ES"}
    result = {"run_id": "test-123"}
    
    log_experiment(config=config, result=result)
    
    assert scripts.research_logger.LOG_PATH.exists()
    content = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    assert "# Project 1L Strategy Experiment Log" in content
    assert "test-123" in content
    assert "test_strat" in content

def test_research_logger_appends_failed_runs_and_preserves_configs(tmp_path: Path):
    from scripts.research_logger import log_experiment, LOG_PATH
    import scripts.research_logger
    
    # Override log path
    scripts.research_logger.LOG_PATH = tmp_path / "test_log_fail.md"
    
    config = {"strategy": "bad_strat"}
    
    log_experiment(config=config, error_msg="DuckDB Error 500", config_path="configs/bad.json")
    
    content = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    assert "DuckDB Error 500" in content
    assert "bad_strat" in content
    assert "FAILED" in content
    
    # Ensure it's in the index
    lines = content.split("\n")
    index_header = "| Experiment ID | Date | Status | Strategy | Family | Interval | Sample | Closed Trades | Trades/Tested Day | Profit Factor | Net PnL | Max DD % | Decision | Next Action | Run ID |"
    header_idx = lines.index(index_header)
    
    row_1 = lines[header_idx + 2]
    assert "FAILED" in row_1
    assert "bad_strat" in row_1

def test_duplicate_prevention_on_success(tmp_path: Path):
    from scripts.research_logger import log_experiment, LOG_PATH
    import scripts.research_logger
    
    scripts.research_logger.LOG_PATH = tmp_path / "test_log_dedupe.md"
    
    config = {"strategy": "dup_strat"}
    result = {"run_id": "duplicate-run-999", "final_equity": 10000.0}
    
    log_experiment(config=config, result=result)
    content1 = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    assert content1.count("duplicate-run-999") >= 2 # 1 in table, 1 in details
    
    # Run again, exact same run_id
    log_experiment(config=config, result=result)
    content2 = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    
    # Content should not be larger
    assert len(content1) == len(content2)

def test_research_logger_math_calculations(tmp_path: Path):
    from scripts.research_logger import log_experiment
    import scripts.research_logger
    
    scripts.research_logger.LOG_PATH = tmp_path / "test_log_math.md"
    
    config = {"strategy": "math_strat"}
    result = {
        "run_id": "math_run_01",
        "days_tested": 10,
        "closed_trade_count": 50,
        "win_rate_pct": 20.0,
        "gross_profit": 500.0,
        "gross_loss": 1000.0
    }
    
    log_experiment(config=config, result=result)
    content = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    
    # 50 trades / 10 days = 5.0
    assert "Trades / Tested Day | 5.0" in content
    # 50 * 20% = 10 winners
    assert "Approx Winning Trades | 10" in content
    # 50 - 10 = 40 losers
    assert "Approx Losing Trades | 40" in content
    # 500 / 10 = 50 avg winner
    assert "Approx Average Winner | 50.0" in content
    # 1000 / 40 = 25 avg loser
    assert "Approx Average Loser | 25.0" in content

def test_research_logger_top_of_index_insertion(tmp_path: Path):
    from scripts.research_logger import log_experiment
    import scripts.research_logger
    
    scripts.research_logger.LOG_PATH = tmp_path / "test_log_order.md"
    
    # First run
    log_experiment(config={"strategy": "oldest"}, result={"run_id": "run-001"})
    
    # Second run
    log_experiment(config={"strategy": "newest"}, result={"run_id": "run-002"})
    
    content = scripts.research_logger.LOG_PATH.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    index_header = "| Experiment ID | Date | Status | Strategy | Family | Interval | Sample | Closed Trades | Trades/Tested Day | Profit Factor | Net PnL | Max DD % | Decision | Next Action | Run ID |"
    header_idx = lines.index(index_header)
    
    # Since we insert at the top, the row immediately below the separator should belong to "newest"
    assert "newest" in lines[header_idx + 2]
    assert "oldest" in lines[header_idx + 3]
