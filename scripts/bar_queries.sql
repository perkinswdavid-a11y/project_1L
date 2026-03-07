-- Run these one at a time in DuckDB.
-- Database:
--   E:\project_1L\marketdata\catalog\marketdata.duckdb

-- 1) Stage 5 bar coverage summary by interval and family
SELECT *
FROM catalog.stage5_bar_coverage_summary
ORDER BY interval, family;

-- 2) Any missing Stage 5 bar days relative to Stage 3 trades
SELECT *
FROM catalog.stage5_bar_missing_days
ORDER BY interval, family, yyyymmdd;

-- 3) Any extra Stage 5 bar days with no matching Stage 3 source day
SELECT *
FROM catalog.stage5_bar_extra_days
ORDER BY interval, family, yyyymmdd;

-- 4) Recent bar files with counts and time ranges
SELECT interval, family, yyyymmdd, manifest_row_count, bar_ts_min, bar_ts_max, parquet_path
FROM catalog.stage5_bar_files
WHERE manifest_status = 'OK'
ORDER BY interval, family, yyyymmdd DESC
LIMIT 50;

-- 5) Days with suspiciously low 1-minute bar counts
SELECT interval, family, yyyymmdd, manifest_row_count, parquet_path
FROM catalog.stage5_bar_files
WHERE interval = '1m'
  AND manifest_status = 'OK'
  AND manifest_row_count < 100
ORDER BY family, yyyymmdd;

-- 6) Coverage comparison: Stage 3 trade file and Stage 5 bar file side by side
SELECT *
FROM catalog.stage5_bar_coverage_comparison
WHERE has_stage5_bars = FALSE
ORDER BY interval, family, yyyymmdd;

-- 7) Count files per interval/family directly from the catalog
SELECT interval, family, COUNT(*) AS file_count
FROM catalog.stage5_bar_files
WHERE file_exists
GROUP BY interval, family
ORDER BY interval, family;