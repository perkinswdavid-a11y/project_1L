from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import duckdb  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "duckdb is required for Stage 4. Install it with: python -m pip install duckdb"
    ) from exc


DATE_FMT = "%Y%m%d"


@dataclass(frozen=True)
class FileRecord:
    stage: str
    family: str
    yyyymmdd: str
    parquet_path: str
    file_size_bytes: int


@dataclass(frozen=True)
class ManifestRecord:
    stage: str
    family: str
    yyyymmdd: str
    parquet_path: str
    row_count: Optional[int]
    ts_event_min: Optional[str]
    ts_event_max: Optional[str]
    status: str
    error: Optional[str]
    manifest_line_num: int


def normalize_family(name: str) -> str:
    return name.upper()


def is_yyyymmdd(text: str) -> bool:
    if len(text) != 8 or not text.isdigit():
        return False
    try:
        datetime.strptime(text, DATE_FMT)
        return True
    except ValueError:
        return False


def infer_stage2_date(path: Path) -> Optional[Tuple[str, str]]:
    # .../<family>/YYYY/MM/DD/glbx-mdp3-YYYYMMDD.mbp-1.parquet
    if not path.name.endswith(".mbp-1.parquet"):
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
    return family, yyyymmdd


def infer_stage3_date(path: Path) -> Optional[Tuple[str, str]]:
    # .../<family>/YYYY/MM/DD/glbx-mdp3-YYYYMMDD.trades.parquet
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
    return family, yyyymmdd


def scan_stage(stage: str, root: Path) -> List[FileRecord]:
    if not root.exists():
        return []

    records: List[FileRecord] = []
    for path in root.rglob("*.parquet"):
        try:
            if stage == "stage2":
                inferred = infer_stage2_date(path)
            elif stage == "stage3":
                inferred = infer_stage3_date(path)
            else:
                raise ValueError(f"Unknown stage: {stage}")

            if not inferred:
                continue

            family, yyyymmdd = inferred
            records.append(
                FileRecord(
                    stage=stage,
                    family=family,
                    yyyymmdd=yyyymmdd,
                    parquet_path=str(path),
                    file_size_bytes=path.stat().st_size,
                )
            )
        except FileNotFoundError:
            continue

    records.sort(key=lambda r: (r.stage, r.family, r.yyyymmdd, r.parquet_path))
    return records


def read_jsonl_manifest(stage: str, manifest_path: Path, path_field: str) -> List[ManifestRecord]:
    if not manifest_path.exists():
        return []

    rows: List[ManifestRecord] = []
    with manifest_path.open("r", encoding="utf-8") as fh:
        for line_num, raw in enumerate(fh, start=1):
            text = raw.strip()
            if not text:
                continue
            try:
                data = json.loads(text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Invalid JSON on line {line_num} of {manifest_path}: {exc}"
                ) from exc

            family = normalize_family(
                str(
                    data.get("family")
                    or data.get("product_family")
                    or ""
                )
            )
            yyyymmdd = str(
                data.get("yyyymmdd")
                or data.get("date_yyyymmdd")
                or ""
            )
            parquet_path = str(
                data.get(path_field)
                or data.get("parquet_path")
                or ""
            )
            status = str(data.get("status", "UNKNOWN"))

            row_count_raw = data.get("row_count")
            try:
                row_count = int(row_count_raw) if row_count_raw is not None else None
            except (TypeError, ValueError):
                row_count = None

            ts_event_min = data.get("ts_event_min")
            ts_event_max = data.get("ts_event_max")
            error = data.get("error")

            if not family or not is_yyyymmdd(yyyymmdd):
                continue

            rows.append(
                ManifestRecord(
                    stage=stage,
                    family=family,
                    yyyymmdd=yyyymmdd,
                    parquet_path=parquet_path,
                    row_count=row_count,
                    ts_event_min=str(ts_event_min) if ts_event_min is not None else None,
                    ts_event_max=str(ts_event_max) if ts_event_max is not None else None,
                    status=status,
                    error=str(error) if error is not None else None,
                    manifest_line_num=line_num,
                )
            )
    return rows


def latest_manifest_by_key(records: Iterable[ManifestRecord]) -> Dict[Tuple[str, str, str], ManifestRecord]:
    latest: Dict[Tuple[str, str, str], ManifestRecord] = {}
    for rec in records:
        key = (rec.stage, rec.family, rec.yyyymmdd)
        prev = latest.get(key)
        if prev is None or rec.manifest_line_num >= prev.manifest_line_num:
            latest[key] = rec
    return latest


def latest_metrics_by_key(records: Iterable[ManifestRecord]) -> Dict[Tuple[str, str, str], ManifestRecord]:
    """
    Best metrics source for the catalog. Prefer the latest OK record. If there is no OK
    record, fall back to the latest record with a non-null row count or timestamp.
    """
    best: Dict[Tuple[str, str, str], ManifestRecord] = {}
    for rec in records:
        key = (rec.stage, rec.family, rec.yyyymmdd)
        prev = best.get(key)

        def usable(r: ManifestRecord) -> bool:
            return (
                r.status == "OK"
                or r.row_count is not None
                or r.ts_event_min is not None
                or r.ts_event_max is not None
            )

        if prev is None:
            best[key] = rec
            continue

        prev_ok = prev.status == "OK"
        rec_ok = rec.status == "OK"
        if rec_ok and not prev_ok:
            best[key] = rec
        elif rec_ok and prev_ok and rec.manifest_line_num >= prev.manifest_line_num:
            best[key] = rec
        elif not prev_ok and not rec_ok:
            if usable(rec) and (not usable(prev) or rec.manifest_line_num >= prev.manifest_line_num):
                best[key] = rec
            elif not usable(prev) and rec.manifest_line_num >= prev.manifest_line_num:
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


def load_duckdb(
    duckdb_path: Path,
    catalog_rows: List[dict],
    stage_summary_rows: List[dict],
    missing_stage3_rows: List[dict],
    extra_stage3_rows: List[dict],
    manifest_missing_rows: List[dict],
    disk_missing_rows: List[dict],
) -> None:
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(duckdb_path))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS catalog")
        con.execute("DROP TABLE IF EXISTS catalog.files")
        con.execute(
            """
            CREATE TABLE catalog.files (
                stage VARCHAR,
                family VARCHAR,
                yyyymmdd VARCHAR,
                trade_date DATE,
                parquet_path VARCHAR,
                file_exists BOOLEAN,
                file_size_bytes BIGINT,
                manifest_status VARCHAR,
                manifest_row_count BIGINT,
                ts_event_min TIMESTAMPTZ,
                ts_event_max TIMESTAMPTZ,
                manifest_line_num BIGINT,
                manifest_error VARCHAR
            )
            """
        )
        if catalog_rows:
            con.executemany(
                """
                INSERT INTO catalog.files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        row["stage"],
                        row["family"],
                        row["yyyymmdd"],
                        row["trade_date"],
                        row["parquet_path"],
                        row["file_exists"],
                        row["file_size_bytes"],
                        row["manifest_status"],
                        row["manifest_row_count"],
                        row["ts_event_min"],
                        row["ts_event_max"],
                        row["manifest_line_num"],
                        row["manifest_error"],
                    )
                    for row in catalog_rows
                ],
            )

        con.execute("DROP TABLE IF EXISTS catalog.stage_summary")
        con.execute(
            """
            CREATE TABLE catalog.stage_summary (
                stage VARCHAR,
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
        if stage_summary_rows:
            con.executemany(
                "INSERT INTO catalog.stage_summary VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        row["stage"],
                        row["family"],
                        row["file_count"],
                        row["ok_count"],
                        row["fail_count"],
                        row["skip_count"],
                        row["date_min"],
                        row["date_max"],
                    )
                    for row in stage_summary_rows
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
            "missing_stage3_days",
            missing_stage3_rows,
            ["family", "yyyymmdd", "stage2_path", "stage3_path_expected"],
        )
        load_simple_table(
            "extra_stage3_days",
            extra_stage3_rows,
            ["family", "yyyymmdd", "stage3_path"],
        )
        load_simple_table(
            "manifest_missing_on_disk",
            manifest_missing_rows,
            ["stage", "family", "yyyymmdd", "parquet_path", "manifest_status", "manifest_row_count"],
        )
        load_simple_table(
            "disk_missing_in_manifest",
            disk_missing_rows,
            ["stage", "family", "yyyymmdd", "parquet_path", "file_size_bytes"],
        )

        con.execute("DROP VIEW IF EXISTS catalog.stage2_files")
        con.execute(
            "CREATE VIEW catalog.stage2_files AS SELECT * FROM catalog.files WHERE stage = 'stage2'"
        )
        con.execute("DROP VIEW IF EXISTS catalog.stage3_files")
        con.execute(
            "CREATE VIEW catalog.stage3_files AS SELECT * FROM catalog.files WHERE stage = 'stage3'"
        )
        con.execute("DROP VIEW IF EXISTS catalog.coverage_comparison")
        con.execute(
            """
            CREATE VIEW catalog.coverage_comparison AS
            SELECT
                s2.family,
                s2.yyyymmdd,
                s2.parquet_path AS stage2_path,
                s2.manifest_row_count AS stage2_row_count,
                s3.parquet_path AS stage3_path,
                s3.manifest_row_count AS stage3_row_count,
                CASE WHEN s3.parquet_path IS NULL THEN FALSE ELSE TRUE END AS has_stage3
            FROM catalog.stage2_files s2
            LEFT JOIN catalog.stage3_files s3
              ON s2.family = s3.family
             AND s2.yyyymmdd = s3.yyyymmdd
            """
        )
    finally:
        con.close()


def build_catalog_rows(
    disk_records: List[FileRecord],
    manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
    manifest_metrics: Dict[Tuple[str, str, str], ManifestRecord],
) -> List[dict]:
    disk_by_key = {(r.stage, r.family, r.yyyymmdd): r for r in disk_records}
    all_keys = sorted(set(disk_by_key) | set(manifest_latest))
    rows: List[dict] = []
    for key in all_keys:
        stage, family, yyyymmdd = key
        disk_rec = disk_by_key.get(key)
        manifest_rec = manifest_latest.get(key)
        metrics_rec = manifest_metrics.get(key, manifest_rec)
        parquet_path = ""
        file_exists = False
        file_size_bytes: Optional[int] = None
        if disk_rec:
            parquet_path = disk_rec.parquet_path
            file_exists = True
            file_size_bytes = disk_rec.file_size_bytes
        elif manifest_rec:
            parquet_path = manifest_rec.parquet_path

        rows.append(
            {
                "stage": stage,
                "family": family,
                "yyyymmdd": yyyymmdd,
                "trade_date": f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}",
                "parquet_path": parquet_path,
                "file_exists": file_exists,
                "file_size_bytes": file_size_bytes,
                "manifest_status": manifest_rec.status if manifest_rec else None,
                "manifest_row_count": metrics_rec.row_count if metrics_rec else None,
                "ts_event_min": metrics_rec.ts_event_min if metrics_rec else None,
                "ts_event_max": metrics_rec.ts_event_max if metrics_rec else None,
                "manifest_line_num": manifest_rec.manifest_line_num if manifest_rec else None,
                "manifest_error": manifest_rec.error if manifest_rec else None,
            }
        )
    return rows


def build_stage_summary(catalog_rows: List[dict]) -> List[dict]:
    groups: Dict[Tuple[str, str], List[dict]] = defaultdict(list)
    for row in catalog_rows:
        groups[(row["stage"], row["family"])].append(row)

    out: List[dict] = []
    for (stage, family), rows in sorted(groups.items()):
        dates = sorted(row["trade_date"] for row in rows)
        statuses = [row.get("manifest_status") or "UNKNOWN" for row in rows]
        out.append(
            {
                "stage": stage,
                "family": family,
                "file_count": sum(1 for row in rows if row["file_exists"]),
                "ok_count": sum(1 for s in statuses if s == "OK"),
                "fail_count": sum(1 for s in statuses if s == "FAIL"),
                "skip_count": sum(1 for s in statuses if s == "SKIP_EXISTS"),
                "date_min": dates[0] if dates else None,
                "date_max": dates[-1] if dates else None,
            }
        )
    return out


def compare_stage2_stage3(
    stage2_disk: List[FileRecord],
    stage3_disk: List[FileRecord],
) -> Tuple[List[dict], List[dict]]:
    s2 = {(r.family, r.yyyymmdd): r for r in stage2_disk}
    s3 = {(r.family, r.yyyymmdd): r for r in stage3_disk}

    missing_stage3: List[dict] = []
    for key in sorted(set(s2) - set(s3)):
        rec = s2[key]
        missing_stage3.append(
            {
                "family": rec.family,
                "yyyymmdd": rec.yyyymmdd,
                "stage2_path": rec.parquet_path,
                "stage3_path_expected": rec.parquet_path.replace(
                    os.path.join("clean", "parquet", "mbp-1"),
                    os.path.join("clean", "derived", "trades"),
                ).replace(".mbp-1.parquet", ".trades.parquet"),
            }
        )

    extra_stage3: List[dict] = []
    for key in sorted(set(s3) - set(s2)):
        rec = s3[key]
        extra_stage3.append(
            {
                "family": rec.family,
                "yyyymmdd": rec.yyyymmdd,
                "stage3_path": rec.parquet_path,
            }
        )
    return missing_stage3, extra_stage3


def compare_manifest_vs_disk(
    catalog_rows: List[dict],
) -> Tuple[List[dict], List[dict]]:
    manifest_missing_on_disk: List[dict] = []
    disk_missing_in_manifest: List[dict] = []
    for row in catalog_rows:
        has_manifest = row.get("manifest_status") is not None
        has_disk = bool(row.get("file_exists"))
        if has_manifest and not has_disk:
            manifest_missing_on_disk.append(
                {
                    "stage": row["stage"],
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
                    "stage": row["stage"],
                    "family": row["family"],
                    "yyyymmdd": row["yyyymmdd"],
                    "parquet_path": row["parquet_path"],
                    "file_size_bytes": row["file_size_bytes"],
                }
            )
    return manifest_missing_on_disk, disk_missing_in_manifest


def stage4_summary(
    stage2_disk: List[FileRecord],
    stage3_disk: List[FileRecord],
    stage2_manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
    stage3_manifest_latest: Dict[Tuple[str, str, str], ManifestRecord],
    missing_stage3_rows: List[dict],
    extra_stage3_rows: List[dict],
    manifest_missing_rows: List[dict],
    disk_missing_rows: List[dict],
) -> dict:
    def counts_by_family(records: List[FileRecord]) -> Dict[str, int]:
        out: Dict[str, int] = defaultdict(int)
        for rec in records:
            out[rec.family] += 1
        return dict(sorted(out.items()))

    def manifest_status_counts(records: Dict[Tuple[str, str, str], ManifestRecord]) -> Dict[str, int]:
        out: Dict[str, int] = defaultdict(int)
        for rec in records.values():
            out[rec.status] += 1
        return dict(sorted(out.items()))

    ok = (
        not missing_stage3_rows
        and not extra_stage3_rows
        and not manifest_missing_rows
        and not disk_missing_rows
    )

    return {
        "stage4_completed_at": datetime.now().astimezone().isoformat(),
        "validation_ok": ok,
        "stage2_disk_counts": counts_by_family(stage2_disk),
        "stage3_disk_counts": counts_by_family(stage3_disk),
        "stage2_manifest_status_counts": manifest_status_counts(stage2_manifest_latest),
        "stage3_manifest_status_counts": manifest_status_counts(stage3_manifest_latest),
        "missing_stage3_days": len(missing_stage3_rows),
        "extra_stage3_days": len(extra_stage3_rows),
        "manifest_missing_on_disk": len(manifest_missing_rows),
        "disk_missing_in_manifest": len(disk_missing_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 4 validation and DuckDB catalog build")
    parser.add_argument(
        "--project-root",
        default=r"E:\project_1L",
        help="Project root path, default: E:\\project_1L",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root)
    marketdata_root = project_root / "marketdata"
    stage2_root = marketdata_root / "clean" / "parquet" / "mbp-1"
    stage3_root = marketdata_root / "clean" / "derived" / "trades"
    manifests_root = marketdata_root / "manifests"
    catalog_root = marketdata_root / "catalog"
    reports_root = catalog_root / "reports"
    duckdb_path = catalog_root / "marketdata.duckdb"

    stage2_manifest_path = manifests_root / "stage2_parquet_build.jsonl"
    stage3_manifest_path = manifests_root / "stage3_trades_build.jsonl"

    print(f"[SCAN] stage2 disk: {stage2_root}")
    stage2_disk = scan_stage("stage2", stage2_root)
    print(f"[SCAN] stage3 disk: {stage3_root}")
    stage3_disk = scan_stage("stage3", stage3_root)

    print(f"[READ] stage2 manifest: {stage2_manifest_path}")
    stage2_manifest_all = read_jsonl_manifest("stage2", stage2_manifest_path, "out_parquet_path")
    print(f"[READ] stage3 manifest: {stage3_manifest_path}")
    stage3_manifest_all = read_jsonl_manifest("stage3", stage3_manifest_path, "out_parquet_path")

    stage2_manifest_latest = latest_manifest_by_key(stage2_manifest_all)
    stage3_manifest_latest = latest_manifest_by_key(stage3_manifest_all)
    stage2_manifest_metrics = latest_metrics_by_key(stage2_manifest_all)
    stage3_manifest_metrics = latest_metrics_by_key(stage3_manifest_all)

    catalog_rows = build_catalog_rows(
        disk_records=stage2_disk + stage3_disk,
        manifest_latest={**stage2_manifest_latest, **stage3_manifest_latest},
        manifest_metrics={**stage2_manifest_metrics, **stage3_manifest_metrics},
    )

    stage_summary_rows = build_stage_summary(catalog_rows)
    missing_stage3_rows, extra_stage3_rows = compare_stage2_stage3(stage2_disk, stage3_disk)
    manifest_missing_rows, disk_missing_rows = compare_manifest_vs_disk(catalog_rows)

    summary = stage4_summary(
        stage2_disk=stage2_disk,
        stage3_disk=stage3_disk,
        stage2_manifest_latest=stage2_manifest_latest,
        stage3_manifest_latest=stage3_manifest_latest,
        missing_stage3_rows=missing_stage3_rows,
        extra_stage3_rows=extra_stage3_rows,
        manifest_missing_rows=manifest_missing_rows,
        disk_missing_rows=disk_missing_rows,
    )

    write_csv(
        reports_root / "catalog_files.csv",
        [
            "stage",
            "family",
            "yyyymmdd",
            "trade_date",
            "parquet_path",
            "file_exists",
            "file_size_bytes",
            "manifest_status",
            "manifest_row_count",
            "ts_event_min",
            "ts_event_max",
            "manifest_line_num",
            "manifest_error",
        ],
        catalog_rows,
    )
    write_csv(
        reports_root / "stage_summary.csv",
        ["stage", "family", "file_count", "ok_count", "fail_count", "skip_count", "date_min", "date_max"],
        stage_summary_rows,
    )
    write_csv(
        reports_root / "missing_stage3_days.csv",
        ["family", "yyyymmdd", "stage2_path", "stage3_path_expected"],
        missing_stage3_rows,
    )
    write_csv(
        reports_root / "extra_stage3_days.csv",
        ["family", "yyyymmdd", "stage3_path"],
        extra_stage3_rows,
    )
    write_csv(
        reports_root / "manifest_missing_on_disk.csv",
        ["stage", "family", "yyyymmdd", "parquet_path", "manifest_status", "manifest_row_count"],
        manifest_missing_rows,
    )
    write_csv(
        reports_root / "disk_missing_in_manifest.csv",
        ["stage", "family", "yyyymmdd", "parquet_path", "file_size_bytes"],
        disk_missing_rows,
    )
    write_json(reports_root / "stage4_validation_summary.json", summary)

    print(f"[DUCKDB] writing catalog tables/views: {duckdb_path}")
    load_duckdb(
        duckdb_path=duckdb_path,
        catalog_rows=catalog_rows,
        stage_summary_rows=stage_summary_rows,
        missing_stage3_rows=missing_stage3_rows,
        extra_stage3_rows=extra_stage3_rows,
        manifest_missing_rows=manifest_missing_rows,
        disk_missing_rows=disk_missing_rows,
    )

    print("[DONE] Stage 4 catalog + validation build complete")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()