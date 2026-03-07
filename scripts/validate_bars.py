from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import duckdb  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "duckdb is required for Stage 5 validation. Install it with: python -m pip install duckdb"
    ) from exc


DATE_FMT = "%Y%m%d"


@dataclass(frozen=True)
class Stage3File:
    family: str
    yyyymmdd: str
    parquet_path: str
    file_size_bytes: int


@dataclass(frozen=True)
class BarFile:
    interval: str
    family: str
    yyyymmdd: str
    parquet_path: str
    file_size_bytes: int


@dataclass(frozen=True)
class ManifestRecord:
    interval: str
    family: str
    yyyymmdd: str
    parquet_path: str
    row_count: Optional[int]
    bar_ts_min: Optional[str]
    bar_ts_max: Optional[str]
    status: str
    error: Optional[str]
    manifest_line_num: int


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


def infer_stage3(path: Path) -> Optional[Stage3File]:
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
    return Stage3File(
        family=family,
        yyyymmdd=yyyymmdd,
        parquet_path=str(path),
        file_size_bytes=path.stat().st_size,
    )


def infer_bar(path: Path) -> Optional[BarFile]:
    if not path.name.endswith(".bars.parquet"):
        return None
    try:
        interval = path.parents[4].name
        family = normalize_family(path.parents[3].name)
        yyyy = path.parents[2].name
        mm = path.parents[1].name
        dd = path.parent.name
    except Exception:
        return None
    yyyymmdd = f"{yyyy}{mm}{dd}"
    if not is_yyyymmdd(yyyymmdd):
        return None
    return BarFile(
        interval=interval,
        family=family,
        yyyymmdd=yyyymmdd,
        parquet_path=str(path),
        file_size_bytes=path.stat().st_size,
    )


def scan_stage3(root: Path, families: Sequence[str]) -> List[Stage3File]:
    allowed = {normalize_family(x) for x in families} if families else set()
    rows: List[Stage3File] = []
    if not root.exists():
        return rows
    for path in root.rglob("*.trades.parquet"):
        rec = infer_stage3(path)
        if rec is None:
            continue
        if allowed and rec.family not in allowed:
            continue
        rows.append(rec)
    rows.sort(key=lambda r: (r.family, r.yyyymmdd, r.parquet_path))
    return rows


def scan_bars(root: Path, families: Sequence[str], intervals: Optional[Sequence[str]]) -> List[BarFile]:
    allowed_families = {normalize_family(x) for x in families} if families else set()
    allowed_intervals = {x.strip() for x in intervals} if intervals else set()
    rows: List[BarFile] = []
    if not root.exists():
        return rows
    for path in root.rglob("*.bars.parquet"):
        rec = infer_bar(path)
        if rec is None:
            continue
        if allowed_families and rec.family not in allowed_families:
            continue
        if allowed_intervals and rec.interval not in allowed_intervals:
            continue
        rows.append(rec)
    rows.sort(key=lambda r: (r.interval, r.family, r.yyyymmdd, r.parquet_path))
    return rows


def read_manifest(path: Path, intervals: Optional[Sequence[str]], families: Sequence[str]) -> List[ManifestRecord]:
    if not path.exists():
        return []
    allowed_intervals = {x.strip() for x in intervals} if intervals else set()
    allowed_families = {normalize_family(x) for x in families} if families else set()
    rows: List[ManifestRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_num, raw in enumerate(fh, start=1):
            text = raw.strip()
            if not text:
                continue
            data = json.loads(text)
            interval = str(data.get("interval", "")).strip()
            family = normalize_family(str(data.get("family", "")))
            yyyymmdd = str(data.get("yyyymmdd", "")).strip()
            parquet_path = str(data.get("out_bars_path") or data.get("parquet_path") or "")
            if allowed_intervals and interval not in allowed_intervals:
                continue
            if allowed_families and family not in allowed_families:
                continue
            if not interval or not family or not is_yyyymmdd(yyyymmdd):
                continue
            row_count_raw = data.get("row_count")
            try:
                row_count = int(row_count_raw) if row_count_raw is not None else None
            except (TypeError, ValueError):
                row_count = None
            rows.append(
                ManifestRecord(
                    interval=interval,
                    family=family,
                    yyyymmdd=yyyymmdd,
                    parquet_path=parquet_path,
                    row_count=row_count,
                    bar_ts_min=str(data.get("bar_ts_min")) if data.get("bar_ts_min") is not None else None,
                    bar_ts_max=str(data.get("bar_ts_max")) if data.get("bar_ts_max") is not None else None,
                    status=str(data.get("status", "UNKNOWN")),
                    error=str(data.get("error")) if data.get("error") is not None else None,
                    manifest_line_num=line_num,
                )
            )
    return rows


def latest_manifest_by_key(records: Iterable[ManifestRecord]) -> Dict[Tuple[str, str, str], ManifestRecord]:
    latest: Dict[Tuple[str, str, str], ManifestRecord] = {}
    for rec in records:
        key = (rec.interval, rec.family, rec.yyyymmdd)
        prev = latest.get(key)
        if prev is None or rec.manifest_line_num >= prev.manifest_line_num:
            latest[key] = rec
    return latest


def latest_metrics_by_key(records: Iterable[ManifestRecord]) -> Dict[Tuple[str, str, str], ManifestRecord]:
    best: Dict[Tuple[str, str, str], ManifestRecord] = {}
    for rec in records:
        key = (rec.interval, rec.family, rec.yyyymmdd)
        prev = best.get(key)
        if prev is None:
            best[key] = rec
            continue
        prev_ok = prev.status == "OK"
        rec_ok = rec.status == "OK"
        if rec_ok and not prev_ok:
            best[key] = rec
        elif rec_ok == prev_ok and rec.manifest_line_num >= prev.manifest_line_num:
            best[key] = rec
    return best


def write_csv(path: Path, fieldnames: List[str], rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def build_catalog_rows(
    bars_disk: List[BarFile],
    manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
    manifest_metrics: Dict[Tuple[str, str, str], ManifestRecord],
) -> List[dict]:
    disk_by_key = {(r.interval, r.family, r.yyyymmdd): r for r in bars_disk}
    all_keys = sorted(set(disk_by_key) | set(manifest_latest))
    rows: List[dict] = []
    for key in all_keys:
        interval, family, yyyymmdd = key
        disk_rec = disk_by_key.get(key)
        manifest_rec = manifest_latest.get(key)
        metrics_rec = manifest_metrics.get(key, manifest_rec)
        parquet_path = disk_rec.parquet_path if disk_rec else (manifest_rec.parquet_path if manifest_rec else "")
        rows.append(
            {
                "interval": interval,
                "family": family,
                "yyyymmdd": yyyymmdd,
                "trade_date": f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}",
                "parquet_path": parquet_path,
                "file_exists": bool(disk_rec),
                "file_size_bytes": disk_rec.file_size_bytes if disk_rec else None,
                "manifest_status": manifest_rec.status if manifest_rec else None,
                "manifest_row_count": metrics_rec.row_count if metrics_rec else None,
                "bar_ts_min": metrics_rec.bar_ts_min if metrics_rec else None,
                "bar_ts_max": metrics_rec.bar_ts_max if metrics_rec else None,
                "manifest_line_num": manifest_rec.manifest_line_num if manifest_rec else None,
                "manifest_error": manifest_rec.error if manifest_rec else None,
            }
        )
    return rows


def build_summary_rows(catalog_rows: List[dict]) -> List[dict]:
    groups: Dict[Tuple[str, str], List[dict]] = defaultdict(list)
    for row in catalog_rows:
        groups[(row["interval"], row["family"])].append(row)
    out: List[dict] = []
    for (interval, family), rows in sorted(groups.items()):
        dates = sorted(row["trade_date"] for row in rows)
        statuses = [row.get("manifest_status") or "UNKNOWN" for row in rows]
        out.append(
            {
                "interval": interval,
                "family": family,
                "file_count": sum(1 for row in rows if row["file_exists"]),
                "ok_count": sum(1 for x in statuses if x == "OK"),
                "fail_count": sum(1 for x in statuses if x == "FAIL"),
                "skip_count": sum(1 for x in statuses if x == "SKIP_EXISTS"),
                "date_min": dates[0] if dates else None,
                "date_max": dates[-1] if dates else None,
            }
        )
    return out


def resolve_expected_intervals(
    requested_intervals: Optional[Sequence[str]],
    bars_disk: List[BarFile],
    manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
) -> List[str]:
    if requested_intervals:
        return sorted({x.strip() for x in requested_intervals if x.strip()})
    found: Set[str] = {rec.interval for rec in bars_disk}
    found.update(key[0] for key in manifest_latest)
    return sorted(found)


def compare_stage3_vs_bars(
    stage3_disk: List[Stage3File],
    bars_disk: List[BarFile],
    expected_intervals: Sequence[str],
) -> Tuple[List[dict], List[dict]]:
    stage3_keys = {(r.family, r.yyyymmdd): r for r in stage3_disk}
    by_interval: Dict[str, Dict[Tuple[str, str], BarFile]] = defaultdict(dict)
    for rec in bars_disk:
        by_interval[rec.interval][(rec.family, rec.yyyymmdd)] = rec

    missing: List[dict] = []
    extra: List[dict] = []
    for interval in expected_intervals:
        bar_map = by_interval.get(interval, {})
        missing_keys = sorted(set(stage3_keys) - set(bar_map))
        extra_keys = sorted(set(bar_map) - set(stage3_keys))
        for key in missing_keys:
            s3 = stage3_keys[key]
            expected_path = (
                Path(s3.parquet_path.replace(str(Path("clean") / "derived" / "trades"), str(Path("clean") / "derived" / "bars" / interval)))
                .with_name(Path(s3.parquet_path).name.replace(".trades.parquet", f".{interval}.bars.parquet"))
            )
            missing.append(
                {
                    "interval": interval,
                    "family": s3.family,
                    "yyyymmdd": s3.yyyymmdd,
                    "stage3_path": s3.parquet_path,
                    "stage5_bars_path_expected": str(expected_path),
                }
            )
        for key in extra_keys:
            bar = bar_map[key]
            extra.append(
                {
                    "interval": interval,
                    "family": bar.family,
                    "yyyymmdd": bar.yyyymmdd,
                    "stage5_bars_path": bar.parquet_path,
                }
            )
    return missing, extra


def compare_manifest_vs_disk(catalog_rows: List[dict]) -> Tuple[List[dict], List[dict]]:
    manifest_missing_on_disk: List[dict] = []
    disk_missing_in_manifest: List[dict] = []
    for row in catalog_rows:
        has_manifest = row.get("manifest_status") is not None
        has_disk = bool(row.get("file_exists"))
        if has_manifest and not has_disk:
            manifest_missing_on_disk.append(
                {
                    "interval": row["interval"],
                    "family": row["family"],
                    "yyyymmdd": row["yyyymmdd"],
                    "parquet_path": row["parquet_path"],
                    "manifest_status": row["manifest_status"],
                    "manifest_row_count": row["manifest_row_count"],
                }
            )
        elif has_disk and not has_manifest:
            disk_missing_in_manifest.append(
                {
                    "interval": row["interval"],
                    "family": row["family"],
                    "yyyymmdd": row["yyyymmdd"],
                    "parquet_path": row["parquet_path"],
                    "file_size_bytes": row["file_size_bytes"],
                }
            )
    return manifest_missing_on_disk, disk_missing_in_manifest


def load_duckdb(
    duckdb_path: Path,
    catalog_rows: List[dict],
    summary_rows: List[dict],
    missing_rows: List[dict],
    extra_rows: List[dict],
    manifest_missing_rows: List[dict],
    disk_missing_rows: List[dict],
) -> None:
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(duckdb_path))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS catalog")
        con.execute("DROP TABLE IF EXISTS catalog.stage5_bar_files")
        con.execute(
            """
            CREATE TABLE catalog.stage5_bar_files (
                interval VARCHAR,
                family VARCHAR,
                yyyymmdd VARCHAR,
                trade_date DATE,
                parquet_path VARCHAR,
                file_exists BOOLEAN,
                file_size_bytes BIGINT,
                manifest_status VARCHAR,
                manifest_row_count BIGINT,
                bar_ts_min TIMESTAMPTZ,
                bar_ts_max TIMESTAMPTZ,
                manifest_line_num BIGINT,
                manifest_error VARCHAR
            )
            """
        )
        if catalog_rows:
            con.executemany(
                "INSERT INTO catalog.stage5_bar_files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        row["interval"],
                        row["family"],
                        row["yyyymmdd"],
                        row["trade_date"],
                        row["parquet_path"],
                        row["file_exists"],
                        row["file_size_bytes"],
                        row["manifest_status"],
                        row["manifest_row_count"],
                        row["bar_ts_min"],
                        row["bar_ts_max"],
                        row["manifest_line_num"],
                        row["manifest_error"],
                    )
                    for row in catalog_rows
                ],
            )

        con.execute("DROP TABLE IF EXISTS catalog.stage5_bar_coverage_summary")
        con.execute(
            """
            CREATE TABLE catalog.stage5_bar_coverage_summary (
                interval VARCHAR,
                family VARCHAR,
                file_count BIGINT,
                ok_count BIGINT,
                fail_count BIGINT,
                skip_count BIGINT,
                date_min DATE,
                date_max DATE
            )
            """
        )
        if summary_rows:
            con.executemany(
                "INSERT INTO catalog.stage5_bar_coverage_summary VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        row["interval"],
                        row["family"],
                        row["file_count"],
                        row["ok_count"],
                        row["fail_count"],
                        row["skip_count"],
                        row["date_min"],
                        row["date_max"],
                    )
                    for row in summary_rows
                ],
            )

        def load_simple_table(table_name: str, rows: List[dict], cols: List[str]) -> None:
            con.execute(f"DROP TABLE IF EXISTS catalog.{table_name}")
            ddl_cols = ", ".join(
                f"{col} VARCHAR" if col not in {"file_size_bytes", "manifest_row_count"} else f"{col} BIGINT"
                for col in cols
            )
            con.execute(f"CREATE TABLE catalog.{table_name} ({ddl_cols})")
            if rows:
                placeholders = ", ".join(["?"] * len(cols))
                con.executemany(
                    f"INSERT INTO catalog.{table_name} VALUES ({placeholders})",
                    [tuple(row.get(col) for col in cols) for row in rows],
                )

        load_simple_table(
            "stage5_bar_missing_days",
            missing_rows,
            ["interval", "family", "yyyymmdd", "stage3_path", "stage5_bars_path_expected"],
        )
        load_simple_table(
            "stage5_bar_extra_days",
            extra_rows,
            ["interval", "family", "yyyymmdd", "stage5_bars_path"],
        )
        load_simple_table(
            "stage5_bar_manifest_missing_on_disk",
            manifest_missing_rows,
            ["interval", "family", "yyyymmdd", "parquet_path", "manifest_status", "manifest_row_count"],
        )
        load_simple_table(
            "stage5_bar_disk_missing_in_manifest",
            disk_missing_rows,
            ["interval", "family", "yyyymmdd", "parquet_path", "file_size_bytes"],
        )

        con.execute("DROP VIEW IF EXISTS catalog.stage5_bar_coverage_comparison")
        con.execute(
            """
            CREATE VIEW catalog.stage5_bar_coverage_comparison AS
            SELECT
                b.interval,
                s3.family,
                s3.yyyymmdd,
                s3.parquet_path AS stage3_path,
                b.parquet_path AS stage5_bars_path,
                CASE WHEN b.parquet_path IS NULL THEN FALSE ELSE TRUE END AS has_stage5_bars
            FROM catalog.stage3_files s3
            LEFT JOIN catalog.stage5_bar_files b
              ON s3.family = b.family
             AND s3.yyyymmdd = b.yyyymmdd
            """
        )
    finally:
        con.close()


def counts_by_family_stage3(records: List[Stage3File]) -> Dict[str, int]:
    out: Dict[str, int] = defaultdict(int)
    for rec in records:
        out[rec.family] += 1
    return dict(sorted(out.items()))


def counts_by_interval_family_bars(records: List[BarFile]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for rec in records:
        out[rec.interval][rec.family] += 1
    return {interval: dict(sorted(fam.items())) for interval, fam in sorted(out.items())}


def manifest_status_counts(records: Dict[Tuple[str, str, str], ManifestRecord]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for rec in records.values():
        out[rec.interval][rec.status] += 1
    return {interval: dict(sorted(statuses.items())) for interval, statuses in sorted(out.items())}


def build_summary_json(
    stage3_disk: List[Stage3File],
    bars_disk: List[BarFile],
    manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
    missing_rows: List[dict],
    extra_rows: List[dict],
    manifest_missing_rows: List[dict],
    disk_missing_rows: List[dict],
    expected_intervals: Sequence[str],
) -> dict:
    return {
        "stage5_validation_completed_at": datetime.now().astimezone().isoformat(),
        "validation_ok": not missing_rows and not extra_rows and not manifest_missing_rows and not disk_missing_rows,
        "expected_intervals": list(expected_intervals),
        "stage3_disk_counts": counts_by_family_stage3(stage3_disk),
        "stage5_bar_disk_counts": counts_by_interval_family_bars(bars_disk),
        "stage5_manifest_status_counts": manifest_status_counts(manifest_latest),
        "missing_bar_days": len(missing_rows),
        "extra_bar_days": len(extra_rows),
        "manifest_missing_on_disk": len(manifest_missing_rows),
        "disk_missing_in_manifest": len(disk_missing_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Stage 5 bar files against Stage 3 trades")
    parser.add_argument(
        "--project-root",
        default=r"E:\project_1L",
        help=r"Project root path. Default: E:\project_1L",
    )
    parser.add_argument(
        "--families",
        default="MES,MNQ",
        help="Comma-separated product families to validate. Example: MES,MNQ",
    )
    parser.add_argument(
        "--intervals",
        default="",
        help="Optional comma-separated intervals to validate. Empty means infer from manifest and disk.",
    )
    parser.add_argument(
        "--manifest-name",
        default="stage5_bars_build.jsonl",
        help="Manifest file name under marketdata/manifests",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root)
    marketdata_root = project_root / "marketdata"
    stage3_root = marketdata_root / "clean" / "derived" / "trades"
    bars_root = marketdata_root / "clean" / "derived" / "bars"
    manifest_path = marketdata_root / "manifests" / args.manifest_name
    reports_root = marketdata_root / "catalog" / "reports"
    duckdb_path = marketdata_root / "catalog" / "marketdata.duckdb"

    families = [normalize_family(x) for x in args.families.split(",") if x.strip()]
    requested_intervals = [x.strip() for x in args.intervals.split(",") if x.strip()] or None

    print(f"[SCAN] stage3 disk: {stage3_root}")
    stage3_disk = scan_stage3(stage3_root, families)
    print(f"[SCAN] stage5 bars disk: {bars_root}")
    bars_disk = scan_bars(bars_root, families, requested_intervals)
    print(f"[READ] stage5 manifest: {manifest_path}")
    manifest_all = read_manifest(manifest_path, requested_intervals, families)
    manifest_latest = latest_manifest_by_key(manifest_all)
    manifest_metrics = latest_metrics_by_key(manifest_all)

    expected_intervals = resolve_expected_intervals(requested_intervals, bars_disk, manifest_latest)
    if not expected_intervals:
        raise SystemExit("No Stage 5 intervals found on disk or in the manifest. Build bars first.")

    catalog_rows = build_catalog_rows(bars_disk, manifest_latest, manifest_metrics)
    summary_rows = build_summary_rows(catalog_rows)
    missing_rows, extra_rows = compare_stage3_vs_bars(stage3_disk, bars_disk, expected_intervals)
    manifest_missing_rows, disk_missing_rows = compare_manifest_vs_disk(catalog_rows)
    summary_json = build_summary_json(
        stage3_disk=stage3_disk,
        bars_disk=bars_disk,
        manifest_latest=manifest_latest,
        missing_rows=missing_rows,
        extra_rows=extra_rows,
        manifest_missing_rows=manifest_missing_rows,
        disk_missing_rows=disk_missing_rows,
        expected_intervals=expected_intervals,
    )

    write_csv(
        reports_root / "stage5_bar_files.csv",
        [
            "interval",
            "family",
            "yyyymmdd",
            "trade_date",
            "parquet_path",
            "file_exists",
            "file_size_bytes",
            "manifest_status",
            "manifest_row_count",
            "bar_ts_min",
            "bar_ts_max",
            "manifest_line_num",
            "manifest_error",
        ],
        catalog_rows,
    )
    write_csv(
        reports_root / "stage5_bar_coverage_summary.csv",
        ["interval", "family", "file_count", "ok_count", "fail_count", "skip_count", "date_min", "date_max"],
        summary_rows,
    )
    write_csv(
        reports_root / "stage5_bar_missing_days.csv",
        ["interval", "family", "yyyymmdd", "stage3_path", "stage5_bars_path_expected"],
        missing_rows,
    )
    write_csv(
        reports_root / "stage5_bar_extra_days.csv",
        ["interval", "family", "yyyymmdd", "stage5_bars_path"],
        extra_rows,
    )
    write_csv(
        reports_root / "stage5_bar_manifest_missing_on_disk.csv",
        ["interval", "family", "yyyymmdd", "parquet_path", "manifest_status", "manifest_row_count"],
        manifest_missing_rows,
    )
    write_csv(
        reports_root / "stage5_bar_disk_missing_in_manifest.csv",
        ["interval", "family", "yyyymmdd", "parquet_path", "file_size_bytes"],
        disk_missing_rows,
    )
    write_json(reports_root / "stage5_bar_validation_summary.json", summary_json)

    print(f"[DUCKDB] writing Stage 5 bar tables/views: {duckdb_path}")
    load_duckdb(
        duckdb_path=duckdb_path,
        catalog_rows=catalog_rows,
        summary_rows=summary_rows,
        missing_rows=missing_rows,
        extra_rows=extra_rows,
        manifest_missing_rows=manifest_missing_rows,
        disk_missing_rows=disk_missing_rows,
    )

    print("[DONE] Stage 5 bar validation complete")
    print(json.dumps(summary_json, indent=2))


if __name__ == "__main__":
    main()