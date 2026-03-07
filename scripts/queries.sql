-- Open with:
--   python -c "import duckdb; con=duckdb.connect(r'E:\\project_1L\\marketdata\\catalog\\marketdata.duckdb'); print(con.sql(open(r'scripts\\queries.sql').read()).fetchall())"
-- or run each query interactively in DuckDB.

SELECT *
FROM catalog.stage_summary
ORDER BY stage, family;

SELECT *
FROM catalog.missing_stage3_days
ORDER BY family, yyyymmdd;

SELECT *
FROM catalog.extra_stage3_days
ORDER BY family, yyyymmdd;

SELECT family, MIN(trade_date) AS min_date, MAX(trade_date) AS max_date, COUNT(*) AS file_count
FROM catalog.stage2_files
GROUP BY family
ORDER BY family;

SELECT family, MIN(trade_date) AS min_date, MAX(trade_date) AS max_date, COUNT(*) AS file_count
FROM catalog.stage3_files
GROUP BY family
ORDER BY family;

SELECT
FROM catalog.coverage_comparison
WHERE has_stage3 = FALSE
ORDER BY family, yyyymmdd;