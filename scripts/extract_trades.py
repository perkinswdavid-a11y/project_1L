from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple

import duckdb


DEFAULT_DB = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
DEFAULT_OUT_ROOT = Path(r"E:\project_1L\marketdata\clean\derived\trades")
DEFAULT_MANIFEST = Path(r"E:\project_1L\marketdata\manifests\stage3_trades_build.jsonl")
DEFAULT_LOG = Path(r"audit\logs\stage3_trades.log")


@dataclass
class ManifestEntry:
    family: str
    yyyymmdd: str
    in_parquet_path: str
    out_parquet_path: str
    row_count: int
    ts_event_min: Optional[str]
    ts_event_max: Optional[str]
    status: str  # OK / FAIL / SKIP_EXISTS
    error: Optional[str] = None


def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("stage3_trades")
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


def sql_quote_path(p: str | Path) -> str:
    # DuckDB is happy with forward slashes on Windows; avoids backslash escaping issues.
    s = str(p).replace("\\", "/").replace("'", "''")
    return f"'{s}'"


def build_out_path(out_root: Path, family: str, yyyymmdd: str) -> Path:
    yyyy, mm, dd = yyyymmdd[0:4], yyyymmdd[4:6], yyyymmdd[6:8]
    out_dir = out_root / family / yyyy / mm / dd
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"glbx-mdp3-{yyyymmdd}.trades.parquet"


def preflight_or_die(db_path: Path, out_root: Path, logger: logging.Logger) -> None:
    logger.info(f"[PREFLIGHT] DUCKDB={db_path}")
    logger.info(f"[PREFLIGHT] OUT_ROOT={out_root}")

    if not db_path.exists():
        raise SystemExit(f"DuckDB catalog not found: {db_path}")
    out_root.mkdir(parents=True, exist_ok=True)


def fetch_stage2_ok_files(con: duckdb.DuckDBPyConnection, family: str) -> List[Tuple[str, str]]:
    rows = con.execute(
        """
        SELECT yyyymmdd, parquet_path
        FROM mbp1_files
        WHERE family = ? AND status = 'OK'
        ORDER BY yyyymmdd;
        """,
        [family.upper()],
    ).fetchall()
    return [(r[0], r[1]) for r in rows]


def extract_trades_one(con: duckdb.DuckDBPyConnection, in_path: str, out_path: Path) -> Tuple[int, Optional[str], Optional[str]]:
    in_sql = sql_quote_path(in_path)
    out_sql = sql_quote_path(out_path)

    # Write trades parquet (action='T')
    con.execute(
        f"""
        COPY (
            SELECT
                ts_event,
                ts_recv,
                publisher_id,
                instrument_id,
                symbol,
                action,
                side,
                CAST(price AS BIGINT) AS trade_px,
                CAST(size  AS BIGINT) AS trade_sz,
                CAST(bid_px_00 AS BIGINT) AS bid_px,
                CAST(ask_px_00 AS BIGINT) AS ask_px,
                CAST(bid_sz_00 AS BIGINT) AS bid_sz,
                CAST(ask_sz_00 AS BIGINT) AS ask_sz,
                CAST(bid_ct_00 AS BIGINT) AS bid_ct,
                CAST(ask_ct_00 AS BIGINT) AS ask_ct,
                flags,
                sequence
            FROM read_parquet({in_sql})
            WHERE action = 'T'
            ORDER BY ts_event
        )
        TO {out_sql}
        (FORMAT PARQUET);
        """
    )

    # Stats from the output file we just wrote
    n, ts_min, ts_max = con.execute(
        f"""
        SELECT
            COUNT(*)::BIGINT,
            MIN(ts_event),
            MAX(ts_event)
        FROM read_parquet({out_sql});
        """
    ).fetchone()

    ts_min_s = ts_min.isoformat().replace("+00:00", "Z") if ts_min else None
    ts_max_s = ts_max.isoformat().replace("+00:00", "Z") if ts_max else None
    return int(n), ts_min_s, ts_max_s


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 3A: extract trades (action='T') from Stage 2 MBP-1 Parquet.")
    ap.add_argument("--duckdb", type=str, default=str(DEFAULT_DB))
    ap.add_argument("--out-root", type=str, default=str(DEFAULT_OUT_ROOT))
    ap.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST))
    ap.add_argument("--log", type=str, default=str(DEFAULT_LOG))
    ap.add_argument("--family", type=str, choices=["MES", "MNQ", "BOTH"], default="BOTH")
    ap.add_argument("--smoke", action="store_true", help="Process 1 day per family only.")
    args = ap.parse_args()

    db_path = Path(args.duckdb)
    out_root = Path(args.out_root)
    manifest_path = Path(args.manifest)
    log_path = Path(args.log)

    logger = setup_logging(log_path)
    preflight_or_die(db_path, out_root, logger)

    con = duckdb.connect(str(db_path))  # NOT read_only; we are writing external parquet files
    con.execute("PRAGMA threads=1;")    # keep it simple & deterministic

    families = ["MES", "MNQ"] if args.family == "BOTH" else [args.family]

    ok = fail = skip = 0
    try:
        for fam in families:
            files = fetch_stage2_ok_files(con, fam)
            if not files:
                logger.info(f"[INFO] No OK files in catalog for {fam}.")
                continue

            if args.smoke:
                files = files[:1]  # earliest day only

            for yyyymmdd, in_path in files:
                out_path = build_out_path(out_root, fam, yyyymmdd)

                if out_path.exists():
                    entry = ManifestEntry(
                        family=fam,
                        yyyymmdd=yyyymmdd,
                        in_parquet_path=in_path,
                        out_parquet_path=str(out_path),
                        row_count=0,
                        ts_event_min=None,
                        ts_event_max=None,
                        status="SKIP_EXISTS",
                        error=None,
                    )
                    write_manifest_line(manifest_path, entry)
                    logger.info(f"[SKIP] {fam} {yyyymmdd} out exists: {out_path}")
                    skip += 1
                    continue

                logger.info(f"[START] {fam} {yyyymmdd} in={in_path}")
                try:
                    n, ts_min, ts_max = extract_trades_one(con, in_path, out_path)
                    entry = ManifestEntry(
                        family=fam,
                        yyyymmdd=yyyymmdd,
                        in_parquet_path=in_path,
                        out_parquet_path=str(out_path),
                        row_count=n,
                        ts_event_min=ts_min,
                        ts_event_max=ts_max,
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
                        ts_event_min=None,
                        ts_event_max=None,
                        status="FAIL",
                        error=str(e),
                    )
                    write_manifest_line(manifest_path, entry)
                    logger.error(f"[FAIL] {fam} {yyyymmdd} error={e}")
                    fail += 1
    finally:
        con.close()

    logger.info(f"[SUMMARY] OK={ok} FAIL={fail} SKIP={skip}")
    print(f"STAGE3_TRADES DONE: OK={ok} FAIL={fail} SKIP={skip}")


if __name__ == "__main__":
    main()