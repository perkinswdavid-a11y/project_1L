from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import duckdb  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "duckdb is required for Stage 5. Install it with: python -m pip install duckdb"
    ) from exc


TS_CANDIDATES = ("ts_event", "ts_recv", "ts", "timestamp", "event_ts")
PRICE_CANDIDATES = ("trade_px", "price", "trade_price", "px", "last_price")
SIZE_CANDIDATES = ("trade_sz", "size", "trade_size", "qty", "volume")
INSTRUMENT_CANDIDATES = ("instrument_key", "symbol", "raw_symbol", "instrument_id", "symbol_id")
DATE_FMT = "%Y%m%d"


@dataclass(frozen=True)
class TradeFile:
    family: str
    yyyymmdd: str
    path: Path


@dataclass(frozen=True)
class IntervalSpec:
    label: str
    duckdb_interval: str


@dataclass(frozen=True)
class SchemaChoice:
    ts_col: str
    price_col: str
    size_col: Optional[str]
    instrument_col: Optional[str]


@dataclass(frozen=True)
class ManifestRow:
    interval: str
    family: str
    yyyymmdd: str
    in_trades_path: str
    out_bars_path: str
    row_count: Optional[int]
    bar_ts_min: Optional[str]
    bar_ts_max: Optional[str]
    ts_col: Optional[str]
    price_col: Optional[str]
    size_col: Optional[str]
    instrument_col: Optional[str]
    status: str
    error: Optional[str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "interval": self.interval,
                "family": self.family,
                "yyyymmdd": self.yyyymmdd,
                "in_trades_path": self.in_trades_path,
                "out_bars_path": self.out_bars_path,
                "row_count": self.row_count,
                "bar_ts_min": self.bar_ts_min,
                "bar_ts_max": self.bar_ts_max,
                "ts_col": self.ts_col,
                "price_col": self.price_col,
                "size_col": self.size_col,
                "instrument_col": self.instrument_col,
                "status": self.status,
                "error": self.error,
            },
            ensure_ascii=False,
        )


_INTERVAL_RE = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)


def normalize_family(name: str) -> str:
    return name.upper().strip()


def is_yyyymmdd(text: str) -> bool:
    if len(text) != 8 or not text.isdigit():
        return False
    try:
        datetime.strptime(text, DATE_FMT)
        return True
    except ValueError:
        return False


def parse_interval(text: str) -> IntervalSpec:
    match = _INTERVAL_RE.fullmatch(text.strip())
    if not match:
        raise ValueError(f"Invalid interval '{text}'. Use values like 30s, 1m, 5m, 15m, 1h.")
    qty = int(match.group(1))
    unit = match.group(2).lower()
    if qty <= 0:
        raise ValueError(f"Invalid interval '{text}'. Quantity must be > 0.")
    duck_unit = {"s": "second", "m": "minute", "h": "hour", "d": "day"}[unit]
    plural = duck_unit if qty == 1 else f"{duck_unit}s"
    return IntervalSpec(label=f"{qty}{unit}", duckdb_interval=f"{qty} {plural}")


def parse_intervals(text: str) -> List[IntervalSpec]:
    specs: List[IntervalSpec] = []
    seen = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        spec = parse_interval(part)
        if spec.label not in seen:
            specs.append(spec)
            seen.add(spec.label)
    if not specs:
        raise ValueError("At least one interval is required.")
    return specs


def infer_trade_file(path: Path) -> Optional[TradeFile]:
    if not path.name.endswith(".trades.parquet"):
        return None
    try:
        family = normalize_family(path.parents[3].name)
        yyyy = path.parents[2].name
        mm = path.parents[1].name
        dd = path.parent.name
    except Exception:
        return None
    yyyymmdd = f"{yyyy}{mm}{dd}"
    if not is_yyyymmdd(yyyymmdd):
        return None
    return TradeFile(family=family, yyyymmdd=yyyymmdd, path=path)


def scan_trade_files(root: Path, families: Sequence[str]) -> List[TradeFile]:
    allowed = {normalize_family(x) for x in families} if families else set()
    rows: List[TradeFile] = []
    if not root.exists():
        return rows
    for path in root.rglob("*.trades.parquet"):
        rec = infer_trade_file(path)
        if rec is None:
            continue
        if allowed and rec.family not in allowed:
            continue
        rows.append(rec)
    rows.sort(key=lambda r: (r.family, r.yyyymmdd, str(r.path)))
    return rows


def choose_smoke_jobs(files: List[TradeFile]) -> List[TradeFile]:
    first_by_family: Dict[str, TradeFile] = {}
    for rec in files:
        first_by_family.setdefault(rec.family, rec)
    return [first_by_family[key] for key in sorted(first_by_family)]


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def sql_literal(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def detect_schema(con: duckdb.DuckDBPyConnection, parquet_path: Path) -> SchemaChoice:
    rows = con.execute("DESCRIBE SELECT * FROM read_parquet(?)", [str(parquet_path)]).fetchall()
    names = [row[0] for row in rows]
    lowered = {name.lower(): name for name in names}

    def pick(candidates: Iterable[str]) -> Optional[str]:
        for cand in candidates:
            actual = lowered.get(cand.lower())
            if actual is not None:
                return actual
        return None

    ts_col = pick(TS_CANDIDATES)
    price_col = pick(PRICE_CANDIDATES)
    size_col = pick(SIZE_CANDIDATES)
    instrument_col = pick(INSTRUMENT_CANDIDATES)

    if ts_col is None:
        raise RuntimeError(f"Could not find a timestamp column in {parquet_path.name}. Columns: {names}")
    if price_col is None:
        raise RuntimeError(f"Could not find a price column in {parquet_path.name}. Columns: {names}")

    return SchemaChoice(
        ts_col=ts_col,
        price_col=price_col,
        size_col=size_col,
        instrument_col=instrument_col,
    )


def build_output_path(out_root: Path, interval: IntervalSpec, src: TradeFile) -> Path:
    file_name = src.path.name.replace(".trades.parquet", f".{interval.label}.bars.parquet")
    return out_root / interval.label / src.family / src.yyyymmdd[0:4] / src.yyyymmdd[4:6] / src.yyyymmdd[6:8] / file_name


def build_bar_sql(interval: IntervalSpec, schema: SchemaChoice, src: TradeFile, out_path: Path) -> str:
    ts_col = quote_ident(schema.ts_col)
    price_col = quote_ident(schema.price_col)

    price_expr = f"CAST({price_col} AS DOUBLE) / 1000000000.0"
    size_expr = "1"
    if schema.size_col:
        size_expr = f"COALESCE(CAST({quote_ident(schema.size_col)} AS BIGINT), 0)"

    instrument_expr = sql_literal(src.family)
    if schema.instrument_col:
        inst_col = quote_ident(schema.instrument_col)
        instrument_expr = (
            f"COALESCE(NULLIF(TRIM(CAST({inst_col} AS VARCHAR)), ''), {sql_literal(src.family)})"
        )

    return f"""
    COPY (
        WITH base AS (
            SELECT
                {sql_literal(src.family)} AS family,
                {sql_literal(src.yyyymmdd)} AS yyyymmdd,
                {instrument_expr} AS instrument_key,
                time_bucket(INTERVAL '{interval.duckdb_interval}', {ts_col}) AS bar_ts,
                {ts_col} AS ts_event,
                {price_expr} AS price,
                {size_expr} AS size
            FROM read_parquet(?)
            WHERE {ts_col} IS NOT NULL
              AND {price_col} IS NOT NULL
        )
        SELECT
            family,
            yyyymmdd,
            instrument_key,
            bar_ts,
            arg_min(price, ts_event) AS open,
            max(price) AS high,
            min(price) AS low,
            arg_max(price, ts_event) AS close,
            sum(size) AS volume,
            count(*) AS trade_count,
            min(ts_event) AS ts_first,
            max(ts_event) AS ts_last
        FROM base
        GROUP BY 1, 2, 3, 4
        ORDER BY instrument_key, bar_ts
    ) TO {sql_literal(str(out_path))} (FORMAT PARQUET, COMPRESSION ZSTD)
    """


def read_bar_metrics(con: duckdb.DuckDBPyConnection, parquet_path: Path) -> Tuple[int, Optional[str], Optional[str]]:
    row = con.execute(
        """
        SELECT
            COUNT(*)::BIGINT AS row_count,
            MIN(bar_ts)::VARCHAR AS bar_ts_min,
            MAX(bar_ts)::VARCHAR AS bar_ts_max
        FROM read_parquet(?)
        """,
        [str(parquet_path)],
    ).fetchone()
    if row is None:
        return 0, None, None
    return int(row[0] or 0), row[1], row[2]


def append_manifest(manifest_path: Path, row: ManifestRow) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as fh:
        fh.write(row.to_json() + "\n")


def run_build(
    project_root: Path,
    intervals: Sequence[IntervalSpec],
    families: Sequence[str],
    overwrite: bool,
    smoke: bool,
    max_files: Optional[int],
    manifest_name: str,
    threads: int,
) -> int:
    trades_root = project_root / "marketdata" / "clean" / "derived" / "trades"
    bars_root = project_root / "marketdata" / "clean" / "derived" / "bars"
    manifest_path = project_root / "marketdata" / "manifests" / manifest_name

    jobs = scan_trade_files(trades_root, families)
    if smoke:
        jobs = choose_smoke_jobs(jobs)
    if max_files is not None:
        jobs = jobs[:max_files]

    logging.info("[PREFLIGHT] TRADES_ROOT=%s", trades_root)
    logging.info("[PREFLIGHT] BARS_ROOT=%s", bars_root)
    logging.info("[PREFLIGHT] MANIFEST=%s", manifest_path)
    logging.info("[PREFLIGHT] JOBS=%s files x %s intervals", len(jobs), len(intervals))

    if not trades_root.exists():
        raise SystemExit(f"Stage 3 trades root not found: {trades_root}")
    if not jobs:
        raise SystemExit("No Stage 3 trade files found to process.")

    counts = {"OK": 0, "FAIL": 0, "SKIP_EXISTS": 0}
    con = duckdb.connect()
    try:
        con.execute(f"PRAGMA threads={max(1, int(threads))}")
        con.execute("SET TimeZone='America/Chicago'")

        schema_cache: Dict[Path, SchemaChoice] = {}
        for src in jobs:
            for interval in intervals:
                out_path = build_output_path(bars_root, interval, src)
                schema: Optional[SchemaChoice] = None
                try:
                    logging.info("[START] %s %s %s in=%s", interval.label, src.family, src.yyyymmdd, src.path)
                    out_path.parent.mkdir(parents=True, exist_ok=True)

                    if out_path.exists() and out_path.stat().st_size > 0 and not overwrite:
                        row_count, bar_ts_min, bar_ts_max = read_bar_metrics(con, out_path)
                        append_manifest(
                            manifest_path,
                            ManifestRow(
                                interval=interval.label,
                                family=src.family,
                                yyyymmdd=src.yyyymmdd,
                                in_trades_path=str(src.path),
                                out_bars_path=str(out_path),
                                row_count=row_count,
                                bar_ts_min=bar_ts_min,
                                bar_ts_max=bar_ts_max,
                                ts_col=None,
                                price_col=None,
                                size_col=None,
                                instrument_col=None,
                                status="SKIP_EXISTS",
                                error=None,
                            ),
                        )
                        counts["SKIP_EXISTS"] += 1
                        logging.info("[SKIP] %s %s %s out=%s", interval.label, src.family, src.yyyymmdd, out_path)
                        continue

                    if out_path.exists() and overwrite:
                        out_path.unlink()

                    schema = schema_cache.get(src.path)
                    if schema is None:
                        schema = detect_schema(con, src.path)
                        schema_cache[src.path] = schema

                    sql = build_bar_sql(interval, schema, src, out_path)
                    con.execute(sql, [str(src.path)])

                    if not out_path.exists() or out_path.stat().st_size == 0:
                        raise RuntimeError(f"Output not written: {out_path}")

                    row_count, bar_ts_min, bar_ts_max = read_bar_metrics(con, out_path)
                    append_manifest(
                        manifest_path,
                        ManifestRow(
                            interval=interval.label,
                            family=src.family,
                            yyyymmdd=src.yyyymmdd,
                            in_trades_path=str(src.path),
                            out_bars_path=str(out_path),
                            row_count=row_count,
                            bar_ts_min=bar_ts_min,
                            bar_ts_max=bar_ts_max,
                            ts_col=schema.ts_col,
                            price_col=schema.price_col,
                            size_col=schema.size_col,
                            instrument_col=schema.instrument_col,
                            status="OK",
                            error=None,
                        ),
                    )
                    counts["OK"] += 1
                    logging.info(
                        "[DONE] %s %s %s OK rows=%s out=%s",
                        interval.label,
                        src.family,
                        src.yyyymmdd,
                        row_count,
                        out_path,
                    )
                except Exception as exc:  # pragma: no cover
                    counts["FAIL"] += 1
                    append_manifest(
                        manifest_path,
                        ManifestRow(
                            interval=interval.label,
                            family=src.family,
                            yyyymmdd=src.yyyymmdd,
                            in_trades_path=str(src.path),
                            out_bars_path=str(out_path),
                            row_count=None,
                            bar_ts_min=None,
                            bar_ts_max=None,
                            ts_col=schema.ts_col if schema else None,
                            price_col=schema.price_col if schema else None,
                            size_col=schema.size_col if schema else None,
                            instrument_col=schema.instrument_col if schema else None,
                            status="FAIL",
                            error=str(exc),
                        ),
                    )
                    try:
                        if out_path.exists():
                            out_path.unlink()
                    except Exception:
                        pass
                    logging.exception("[FAIL] %s %s %s out=%s", interval.label, src.family, src.yyyymmdd, out_path)

    finally:
        con.close()

    logging.info("[SUMMARY] OK=%s FAIL=%s SKIP=%s", counts["OK"], counts["FAIL"], counts["SKIP_EXISTS"])
    print(f"STAGE5_BARS DONE: OK={counts['OK']} FAIL={counts['FAIL']} SKIP={counts['SKIP_EXISTS']}")
    return 0 if counts["FAIL"] == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 5A: build OHLCV bars from Stage 3 trades parquet")
    parser.add_argument(
        "--project-root",
        default=r"E:\project_1L",
        help=r"Project root path. Default: E:\project_1L",
    )
    parser.add_argument(
        "--intervals",
        default="1m,5m,15m",
        help="Comma-separated bar intervals. Example: 1m,5m,15m,1h",
    )
    parser.add_argument(
        "--families",
        default="MES,MNQ",
        help="Comma-separated product families to process. Example: MES,MNQ",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output bar files")
    parser.add_argument("--smoke", action="store_true", help="Process only the first date per family")
    parser.add_argument("--max-files", type=int, default=None, help="Limit number of input trade files")
    parser.add_argument(
        "--manifest-name",
        default="stage5_bars_build.jsonl",
        help="Manifest file name under marketdata/manifests",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="DuckDB worker threads to use. Default: 4",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    intervals = parse_intervals(args.intervals)
    families = [normalize_family(x) for x in args.families.split(",") if x.strip()]

    raise SystemExit(
        run_build(
            project_root=Path(args.project_root),
            intervals=intervals,
            families=families,
            overwrite=args.overwrite,
            smoke=args.smoke,
            max_files=args.max_files,
            manifest_name=args.manifest_name,
            threads=args.threads,
        )
    )


if __name__ == "__main__":
    main()