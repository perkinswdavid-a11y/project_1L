from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple

import duckdb


DEFAULT_DB = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
DEFAULT_OUT_ROOT = Path(r"E:\project_1L\marketdata\clean\derived\bars_1m")
DEFAULT_MANIFEST = Path(r"E:\project_1L\marketdata\manifests\stage3_bars_1m_build.jsonl")
DEFAULT_LOG = Path(r"audit\logs\stage3_bars_1m.log")


@dataclass
class ManifestEntry:
    family: str
    yyyymmdd: str
    in_parquet_path: str
    out_parquet_path: str
    row_count: int
    bar_start_min: Optional[str]
    bar_start_max: Optional[str]
    status: str  # OK / FAIL / SKIP_EXISTS
    error: Optional[str] = None


def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("stage3_bars_1m")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger


def write_manifest_line(path: Path, entry: ManifestEntry) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.__dict__, ensure_ascii=False) + "\n")
        f.flush()


def build_out_path(out_root: Path, family: str, yyyymmdd: str) -> Path:
    yyyy, mm, dd = yyyymmdd[0:4], yyyymmdd[4:6], yyyymmdd[6:8]
    out_dir = out_root / family / yyyy / mm / dd
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"glbx-mdp3-{yyyymmdd}.bars_1m.parquet"


def sql_quote_path(path: Path) -> str:
    # DuckDB accepts forward slashes on Windows; easier than escaping backslashes.
    s = str(path).replace("\\", "/").replace("'", "''")
    return f"'{s}'"


def preflight_or_die(db_path: Path, out_root: Path, logger: logging.Logger) -> None:
    logger.info(f"[PREFLIGHT] DUCKDB={db_path}")
    logger.info(f"[PREFLIGHT] OUT_ROOT={out_root}")
    if not db_path.exists():
        raise SystemExit(f"DuckDB catalog not found: {db_path}")
    out_root.mkdir(parents=True, exist_ok=True)


def fetch_stage2_ok_files(con: duckdb.DuckDBPyConnection, family: str) -> List[Tuple[str, str]]:
    fam = family.upper()
    rows = con.execute(
        """
        SELECT yyyymmdd, parquet_path
        FROM mbp1_files
        WHERE family = ? AND status = 'OK'
        ORDER BY yyyymmdd;
        """,
        [fam],
    ).fetchall()
    return [(r[0], r[1]) for r in rows]


def build_bars_one_day(
    con: duckdb.DuckDBPyConnection,
    family: str,
    yyyymmdd: str,
    in_path: str,
    out_path: Path,
) -> Tuple[int, Optional[str], Optional[str]]:
    in_sql = sql_quote_path(Path(in_path))
    out_sql = sql_quote_path(out_path)

    # IMPORTANT: no floats.
    # mid_px is computed with integer arithmetic using bitshift >> 1 (divide by 2).
    # open/close use sequence (monotonic within day) to avoid timestamp tie ambiguity.
    query = f"""
    COPY (
        WITH e AS (
            SELECT
                date_trunc('minute', ts_event) AS bar_start_utc,
                symbol,
                instrument_id,
                action,
                CAST(size AS BIGINT) AS sz,
                CAST(price AS BIGINT) AS trade_px,  -- only meaningful for action='T'
                CAST(bid_px_00 AS BIGINT) AS bid_px,
                CAST(ask_px_00 AS BIGINT) AS ask_px,
                CAST(sequence AS BIGINT) AS seq,
                -- valid BBO guard
                CASE
                    WHEN bid_px_00 IS NOT NULL
                     AND ask_px_00 IS NOT NULL
                     AND bid_px_00 > 0
                     AND ask_px_00 > 0
                     AND ask_px_00 >= bid_px_00
                    THEN CAST(ask_px_00 - bid_px_00 AS BIGINT)
                    ELSE NULL
                END AS spread,
                CASE
                    WHEN bid_px_00 IS NOT NULL
                     AND ask_px_00 IS NOT NULL
                     AND bid_px_00 > 0
                     AND ask_px_00 > 0
                     AND ask_px_00 >= bid_px_00
                    THEN (CAST(bid_px_00 + ask_px_00 AS BIGINT) >> 1)
                    ELSE NULL
                END AS mid_px
            FROM read_parquet({in_sql})
        )
        SELECT
            bar_start_utc,
            '{family}' AS family,
            symbol,
            instrument_id,

            -- Mid OHLC (integer fixed units)
            arg_min(mid_px, seq) FILTER (WHERE mid_px IS NOT NULL) AS open_mid,
            max(mid_px)          FILTER (WHERE mid_px IS NOT NULL) AS high_mid,
            min(mid_px)          FILTER (WHERE mid_px IS NOT NULL) AS low_mid,
            arg_max(mid_px, seq) FILTER (WHERE mid_px IS NOT NULL) AS close_mid,

            -- Spread open/close (integer fixed units)
            arg_min(spread, seq) FILTER (WHERE spread IS NOT NULL) AS open_spread,
            arg_max(spread, seq) FILTER (WHERE spread IS NOT NULL) AS close_spread,

            -- Trade stats (from action='T')
            sum(CASE WHEN action = 'T' THEN sz ELSE 0 END) AS trade_volume,
            sum(CASE WHEN action = 'T' THEN 1  ELSE 0 END) AS trade_count,

            -- Total events contributing to this minute (all actions)
            count(*) AS event_count

        FROM e
        GROUP BY 1, 2, 3, 4
        ORDER BY bar_start_utc, symbol, instrument_id
    )
    TO {out_sql}
    (FORMAT PARQUET);
    """

    con.execute(query)

    stats = con.execute(
        f"""
        SELECT
            COUNT(*)::BIGINT AS n,
            MIN(bar_start_utc) AS tmin,
            MAX(bar_start_utc) AS tmax
        FROM read_parquet({out_sql});
        """
    ).fetchone()

    n = int(stats[0])
    # DuckDB returns datetime objects; isoformat is fine.
    tmin = stats[1].isoformat().replace("+00:00", "Z") if stats[1] else None
    tmax = stats[2].isoformat().replace("+00:00", "Z") if stats[2] else None
    return n, tmin, tmax


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 3B: build 1-minute bars (mid-price OHLC + trade stats) from Stage 2 MBP-1.")
    ap.add_argument("--duckdb", type=str, default=str(DEFAULT_DB))
    ap.add_argument("--out-root", type=str, default=str(DEFAULT_OUT_ROOT))
    ap.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST))
    ap.add_argument("--log", type=str, default=str(DEFAULT_LOG))
    ap.add_argument("--family", type=str, choices=["MES", "MNQ", "BOTH"], default="BOTH")
    ap.add_argument("--smoke", action="store_true", help="Process 1 day per family only (earliest OK in catalog).")
    args = ap.parse_args()

    db_path = Path(args.duckdb)
    out_root = Path(args.out_root)
    manifest_path = Path(args.manifest)
    log_path = Path(args.log)

    logger = setup_logging(log_path)
    preflight_or_die(db_path, out_root, logger)

    con = duckdb.connect(str(db_path), read_only=True)

    families = ["MES", "MNQ"] if args.family == "BOTH" else [args.family]

    ok = fail = skip = 0
    try:
        for fam in families:
            files = fetch_stage2_ok_files(con, fam)
            if not files:
                logger.info(f"[INFO] No OK files in catalog for {fam}.")
                continue

            if args.smoke:
                files = files[:1]

            for yyyymmdd, in_path in files:
                out_path = build_out_path(out_root, fam, yyyymmdd)

                if out_path.exists():
                    entry = ManifestEntry(
                        family=fam,
                        yyyymmdd=yyyymmdd,
                        in_parquet_path=in_path,
                        out_parquet_path=str(out_path),
                        row_count=0,
                        bar_start_min=None,
                        bar_start_max=None,
                        status="SKIP_EXISTS",
                        error=None,
                    )
                    write_manifest_line(manifest_path, entry)
                    logger.info(f"[SKIP] {fam} {yyyymmdd} out exists: {out_path}")
                    skip += 1
                    continue

                logger.info(f"[START] {fam} {yyyymmdd} in={in_path}")
                try:
                    n, tmin, tmax = build_bars_one_day(con, fam, yyyymmdd, in_path, out_path)
                    entry = ManifestEntry(
                        family=fam,
                        yyyymmdd=yyyymmdd,
                        in_parquet_path=in_path,
                        out_parquet_path=str(out_path),
                        row_count=n,
                        bar_start_min=tmin,
                        bar_start_max=tmax,
                        status="OK",
                        error=None,
                    )
                    write_manifest_line(manifest_path, entry)
                    logger.info(f"[DONE] {fam} {yyyymmdd} OK rows={n} out={out_path}")
                    ok += 1
                except Exception as e:
                    entry = ManifestEntry(
                        family=fam,
                        yyyymmdd=yyyymmdd,
                        in_parquet_path=in_path,
                        out_parquet_path=str(out_path),
                        row_count=0,
                        bar_start_min=None,
                        bar_start_max=None,
                        status="FAIL",
                        error=str(e),
                    )
                    write_manifest_line(manifest_path, entry)
                    logger.error(f"[FAIL] {fam} {yyyymmdd} error={e}")
                    fail += 1
    finally:
        con.close()

    logger.info(f"[SUMMARY] OK={ok} FAIL={fail} SKIP={skip}")
    print(f"STAGE3_BARS_1M DONE: OK={ok} FAIL={fail} SKIP={skip}")


if __name__ == "__main__":
    main()