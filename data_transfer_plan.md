# Project 1L Market Data Engineering Plan (RAW → CLEAN → CATALOG → VALIDATE)

## Purpose (Read Once)
This plan moves your Databento market data from the 2TB SSD (D:) to a professional, audit-ready dataset on the 8TB SSD (E:), prepared for later backtesting.

**Quality > speed.** If anything looks wrong at any point, **STOP** and do not continue until it is understood and fixed.

---

## Non‑Negotiable Rules
1. **RAW is immutable.** Never rename, reorganize, edit, partially delete, or “clean up” vendor files in place.
2. **CLEAN is derived.** CLEAN outputs (Parquet, DuckDB catalog) are allowed to be rebuilt from RAW.
3. **No guessing.** If a file looks unexpected, STOP.
4. **Keep provenance.** Preserve Databento package folder names, and keep the JSON support files with RAW.

---

## Drive Letters (Confirmed)
- Source / old RAW location: **D:** (2TB SSD)
- Destination / permanent vault: **E:** (8TB SSD)

---

## Data Vault Root (On E:)
All project market data lives under:

E:\project_1l_marketdata\

Standard subfolders:
- E:\project_1l_marketdata\raw\
- E:\project_1l_marketdata\clean\
- E:\project_1l_marketdata\db\
- E:\project_1l_marketdata\manifests\

---

# Stage 1 — RAW Data Vault (Immutable Vendor Archive) ✅ DONE

## Goal
Copy Databento vendor packages from D: to E: without changing anything.

## What RAW Contains
- Daily market data files: `*.dbn`
- Support JSONs at package root (exact filenames may vary):
  - condition.json
  - metadata.json
  - manifest JSON

## RAW Copy Location (On E:)
E:\project_1l_marketdata\raw\databento\

RAW packages (folder names preserved exactly):
- E:\project_1l_marketdata\raw\databento\GLBX-20260226-C54N6VA68U-MES\
- E:\project_1l_marketdata\raw\databento\GLBX-20260226-55CCFTR4TP-MNQ\

## Stage 1 Verification (What You Already Did)
- Copied full D:\databento\ → E:\project_1l_marketdata\raw\databento\
- Confirmed total size and file counts match
- Spot-checked daily `.dbn` files exist on E:
- Confirmed the 3 JSON support files exist at each package root

## Stage 1 Safety Rule Going Forward
Treat:
E:\project_1l_marketdata\raw\
as **read-only mentally** (do not edit).

---

# Stage 2 — CLEAN Parquet Dataset (Organized Research Format) ✅ APPROVED

## Goal
Convert each daily RAW Databento `.dbn` file into a clean, queryable Parquet dataset on E: while preserving maximum fidelity (no float rounding, keep timestamps, keep all MBP‑1 fields).

## Outputs (On E:)
Create:
E:\project_1l_marketdata\clean\parquet\mbp-1\

Output layout (one Parquet file per day per product family):
- E:\project_1l_marketdata\clean\parquet\mbp-1\MES\YYYY\MM\DD\glbx-mdp3-YYYYMMDD.mbp-1.parquet
- E:\project_1l_marketdata\clean\parquet\mbp-1\MNQ\YYYY\MM\DD\glbx-mdp3-YYYYMMDD.mbp-1.parquet

## Stage 2 Step-by-Step (Beginner Safe)
1) Confirm RAW is present on E:
   - Open File Explorer
   - Go to: E:\project_1l_marketdata\raw\databento\
   - Confirm both package folders are there (MES and MNQ)

2) Create the CLEAN folders on E:
   - Create: E:\project_1l_marketdata\clean\
   - Create: E:\project_1l_marketdata\clean\parquet\
   - Create: E:\project_1l_marketdata\clean\parquet\mbp-1\
   - Create: E:\project_1l_marketdata\clean\parquet\mbp-1\MES\
   - Create: E:\project_1l_marketdata\clean\parquet\mbp-1\MNQ\

3) Create the manifests folder (if not already created):
   - Create: E:\project_1l_marketdata\manifests\

4) Plan the transcoder script (no strategy logic):
   - It will read RAW `.dbn` files under:
     E:\project_1l_marketdata\raw\databento\
   - It will determine product family (MES vs MNQ) from the **package folder name**, not the filename.
   - It will parse YYYYMMDD from the filename (e.g., glbx-mdp3-20260206...).
   - It will write the Parquet output into the year/month/day folder structure above.
   - It will write a processing manifest file to:
     E:\project_1l_marketdata\manifests\stage2_parquet_build.jsonl
     (one line per raw file processed: raw_path, output_path, rows, min_ts_event, max_ts_event, status)

5) Run the Stage 2 transcoder script (when implemented):
   - Run it from the project root using `uv run python ...`
   - Let it process all files sequentially (stable, RAM-safe)

6) After Stage 2 completes, do a simple manual spot-check:
   - Navigate to:
     E:\project_1l_marketdata\clean\parquet\mbp-1\MES\
   - Confirm you see year folders, then month folders, then day folders
   - Confirm `.parquet` files exist
   - Repeat for MNQ

7) STOP Conditions (do not proceed to Stage 3 if any happen):
   - The script logs errors reading `.dbn` files
   - Output Parquet files are not being created
   - MES and MNQ outputs appear mixed together
   - Output folder structure is not year/month/day
   - Manifest file isn’t created or is empty

---

# Stage 3 — DuckDB Catalog (Query + Audit Layer over Parquet) ✅ APPROVED

## Goal
Create a single DuckDB database file that:
- Stores small metadata tables (raw inventory, parquet inventory, processing lineage)
- Defines views that read Parquet directly
- Does NOT store TBs of tick data as physical DB tables

## Outputs (On E:)
- E:\project_1l_marketdata\db\project_1l.duckdb
- E:\project_1l_marketdata\manifests\stage3_duckdb_catalog_build.json

## Stage 3 Step-by-Step (Beginner Safe)
1) Create folder:
   - E:\project_1l_marketdata\db\

2) Confirm Stage 2 Parquet exists:
   - E:\project_1l_marketdata\clean\parquet\mbp-1\MES\
   - E:\project_1l_marketdata\clean\parquet\mbp-1\MNQ\
   If Parquet does not exist yet: STOP (Stage 2 must complete first)

3) Plan the DuckDB catalog builder script (no strategy logic):
   It will:
   - Create/open: E:\project_1l_marketdata\db\project_1l.duckdb
   - Create metadata tables such as:
     - raw_packages
     - raw_manifest_files (from vendor manifest JSON)
     - raw_condition (from condition.json if present/usable)
     - clean_parquet_files (from Stage 2 build manifest and/or filesystem scan)
   - Create views over Parquet (no data duplication):
     - v_mbp1_mes (reads all MES Parquet)
     - v_mbp1_mnq (reads all MNQ Parquet)
     - v_mbp1_all (union view; adds product_family column)
   - Write a build manifest:
     E:\project_1l_marketdata\manifests\stage3_duckdb_catalog_build.json

4) Run the Stage 3 catalog builder script (when implemented)

5) Teenager verification checks:
   - Confirm file exists:
     E:\project_1l_marketdata\db\project_1l.duckdb
   - Confirm manifest exists:
     E:\project_1l_marketdata\manifests\stage3_duckdb_catalog_build.json
   - Confirm at least one simple query returns rows for MES and MNQ (sanity)

6) STOP Conditions:
   - DuckDB file is not created
   - Views are missing
   - Queries return zero rows for obviously active trading dates
   - Any errors about missing Parquet paths

---

# Stage 4 — End-to-End Validation Pass (RAW → CLEAN → CATALOG)

## Goal
Prove that:
- every RAW daily file you expect is accounted for
- CLEAN Parquet exists for the covered date range
- DuckDB catalog correctly points at the Parquet dataset
- gaps and anomalies are identified and recorded

## Outputs (On E:)
- E:\project_1l_marketdata\manifests\stage4_validation_report.json
- E:\project_1l_marketdata\manifests\stage4_missing_dates.csv (optional)
- E:\project_1l_marketdata\manifests\stage4_anomalies.csv (optional)

## Stage 4 Step-by-Step (Beginner Safe)
1) Confirm Stage 1 RAW exists on E:
   - E:\project_1l_marketdata\raw\databento\...

2) Confirm Stage 2 CLEAN Parquet exists on E:
   - E:\project_1l_marketdata\clean\parquet\mbp-1\...

3) Confirm Stage 3 DuckDB exists on E:
   - E:\project_1l_marketdata\db\project_1l.duckdb

4) Validation tasks the script must perform:
   - Count RAW daily `.dbn` files for MES and MNQ
   - Count CLEAN `.parquet` files for MES and MNQ
   - Ensure each Parquet file can be opened/read (basic schema read)
   - Use DuckDB views to count rows for a few representative days
   - Produce a date coverage report:
     - list available dates per product family
     - list missing dates (if any)
   - Record anomalies:
     - days with unexpectedly tiny row counts (possible holiday/weekend or bad file)
     - days where timestamps do not fall within expected day boundaries

5) Run the Stage 4 validation script (when implemented)

6) STOP Conditions:
   - Large number of missing Parquet days compared to RAW days
   - DuckDB views failing to read Parquet
   - Multiple days with clearly broken timestamp ranges
   - Any consistent parsing errors

---

# Stage 5 — Final “Ready for Research” Snapshot (No Backtesting Yet)

## Goal
After validation passes, create a stable snapshot so you can safely move into strategy research and backtesting later.

## Stage 5 Step-by-Step (Beginner Safe)
1) Confirm Stage 4 validation passed (no major missing coverage)
2) Ensure these folders exist and are populated:
   - E:\project_1l_marketdata\raw\databento\... (immutable archive)
   - E:\project_1l_marketdata\clean\parquet\mbp-1\... (clean dataset)
   - E:\project_1l_marketdata\db\project_1l.duckdb (catalog)
   - E:\project_1l_marketdata\manifests\ (build + validation reports)

3) Make a “snapshot label” file:
   - E:\project_1l_marketdata\manifests\SNAPSHOT_READY_FOR_RESEARCH.txt
   Include:
   - date created
   - machine name
   - drive letters
   - short note: “RAW copied + verified, Parquet built, DuckDB catalog built, validation passed”

4) Keep the original D: copy until you have verified Stage 2+3+4 outputs.
   After that, D: can be repurposed, but only when you are confident E: is complete.

---

# Next Step After This Plan Is Locked
Yes: **then we write the scripts**.

Scripts to implement (no strategy logic inside them):
- Stage 2: DBN → Parquet transcoder (sequential, audit manifest)
- Stage 3: DuckDB catalog builder (tables + views, manifest)
- Stage 4: Validation runner (coverage + anomalies, report)

All scripts live in:
- src/project_1l/data_layer/ (or a top-level scripts/ directory that imports from project_1l)
and must write logs to:
- E:\project_1l_marketdata\manifests\ and/or your project audit/logs

STOP authority remains active: if any output does not match expectations, we pause and reassess before proceeding.