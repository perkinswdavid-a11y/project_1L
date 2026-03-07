from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import databento as db
import pyarrow as pa
import pyarrow.parquet as pq


# ----------------------------
# Defaults (edit only if needed)
# ----------------------------
DEFAULT_RAW_ROOT = Path(r"E:\project_1L\marketdata\raw\databento")
DEFAULT_CLEAN_ROOT = Path(r"E:\project_1L\marketdata\clean\parquet\mbp-1")
DEFAULT_MANIFEST_PATH = Path(r"E:\project_1L\marketdata\manifests\stage2_parquet_build.jsonl")
# log path is relative to repo (caller should run from repo root)
DEFAULT_LOG_PATH = Path(r"audit\logs\stage2_data_ingestion.log")


# ----------------------------
# Helpers / core rules
# ----------------------------
def get_product_family(vendor_folder_name: str) -> str:
    """
    Product family MUST be derived ONLY from the vendor package folder name:
      contains "-MES" => "MES"
      contains "-MNQ" => "MNQ"
    """
    name = vendor_folder_name.upper()
    is_mes = "-MES" in name
    is_mnq = "-MNQ" in name

    if is_mes and not is_mnq:
        return "MES"
    if is_mnq and not is_mes:
        return "MNQ"

    raise ValueError(f"Ambiguous vendor folder name for family detection: {vendor_folder_name!r}")


def parse_yyyymmdd_from_filename(filename: str) -> str:
    """
    Extract YYYYMMDD strictly from the filename segment after 'glbx-mdp3-'.
    Example: glbx-mdp3-20260206.mbp-1.dbn.zst -> 20260206
    """
    token = "glbx-mdp3-"
    idx = filename.find(token)
    if idx < 0:
        raise ValueError(f"Filename does not contain required token {token!r}: {filename!r}")

    start = idx + len(token)
    yyyymmdd = filename[start : start + 8]
    if len(yyyymmdd) != 8 or not yyyymmdd.isdigit():
        raise ValueError(f"Could not parse YYYYMMDD after {token!r} in filename: {filename!r}")

    return yyyymmdd


def build_output_path(clean_root: Path, family: str, yyyymmdd: str) -> Path:
    yyyy = yyyymmdd[0:4]
    mm = yyyymmdd[4:6]
    dd = yyyymmdd[6:8]
    out_dir = clean_root / family / yyyy / mm / dd
    out_name = f"glbx-mdp3-{yyyymmdd}.mbp-1.parquet"
    return out_dir / out_name


def discover_dbn_files(raw_root: Path) -> List[Path]:
    """
    Recursively discover all .dbn and .dbn.zst files under raw_root.
    Ignore JSON and other extensions.
    """
    # allow both variants
    files = list(raw_root.rglob("*.dbn")) + list(raw_root.rglob("*.dbn.zst"))
    # de-dup (in case *.dbn catches *.dbn.zst on some systems; usually it won't)
    uniq = sorted({p.resolve() for p in files}, key=lambda p: str(p).lower())
    return uniq


def deterministic_sort(files: Iterable[Path]) -> List[Path]:
    """
    Sort by (date_yyyymmdd, raw_path.lower()).
    """
    def key(p: Path) -> Tuple[str, str]:
        yyyymmdd = parse_yyyymmdd_from_filename(p.name)
        return (yyyymmdd, str(p).lower())

    return sorted(list(files), key=key)


def iso_z(dt: datetime) -> str:
    # ensure UTC and Z suffix
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    # keep ns precision if present in dt? python datetime is microseconds, ok for manifest
    return dt.isoformat().replace("+00:00", "Z")


def parquet_rowcount_and_ts_event_range(parquet_path: Path) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Get row_count and ts_event min/max WITHOUT pandas.
    Prefer Parquet row group stats for ts_event (fast). If stats are absent, return nulls for ts range.
    """
    pf = pq.ParquetFile(parquet_path)
    meta = pf.metadata
    row_count = int(meta.num_rows) if meta is not None else 0

    # Find ts_event column index
    schema = pf.schema_arrow
    try:
        ts_idx = schema.get_field_index("ts_event")
    except Exception:
        ts_idx = -1

    if ts_idx < 0 or meta is None:
        return row_count, None, None

    ts_min_ns: Optional[int] = None
    ts_max_ns: Optional[int] = None

    # Parquet stats may store timestamp as int64 ns (implementation dependent).
    for rg in range(meta.num_row_groups):
        col = meta.row_group(rg).column(ts_idx)
        stats = col.statistics
        if stats is None:
            continue
        if not stats.has_min_max:
            continue

        # pyarrow may expose min/max as python int for timestamps, or datetime-like.
        mn = stats.min
        mx = stats.max

        def to_ns(v):
            if v is None:
                return None
            if isinstance(v, int):
                return v
            if isinstance(v, datetime):
                # convert to ns since epoch
                v_utc = v.astimezone(timezone.utc) if v.tzinfo else v.replace(tzinfo=timezone.utc)
                return int(v_utc.timestamp() * 1_000_000_000)
            # fallback: try string parse
            try:
                dv = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
                dv = dv.astimezone(timezone.utc) if dv.tzinfo else dv.replace(tzinfo=timezone.utc)
                return int(dv.timestamp() * 1_000_000_000)
            except Exception:
                return None

        mn_ns = to_ns(mn)
        mx_ns = to_ns(mx)

        if mn_ns is not None:
            ts_min_ns = mn_ns if ts_min_ns is None else min(ts_min_ns, mn_ns)
        if mx_ns is not None:
            ts_max_ns = mx_ns if ts_max_ns is None else max(ts_max_ns, mx_ns)

    if ts_min_ns is None or ts_max_ns is None:
        return row_count, None, None

    # Convert ns to datetime ISOZ (microsecond precision in python datetime)
    dt_min = datetime.fromtimestamp(ts_min_ns / 1_000_000_000, tz=timezone.utc)
    dt_max = datetime.fromtimestamp(ts_max_ns / 1_000_000_000, tz=timezone.utc)
    return row_count, iso_z(dt_min), iso_z(dt_max)


@dataclass
class ManifestEntry:
    raw_path: str
    product_family: str
    date_yyyymmdd: str
    parquet_path: str
    row_count: int
    ts_event_min: Optional[str]
    ts_event_max: Optional[str]
    status: str  # OK / FAIL / SKIP_EXISTS
    error: Optional[str] = None


def write_manifest_line(manifest_path: Path, entry: ManifestEntry) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry.__dict__, ensure_ascii=False)
    with open(manifest_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()  # important
        # fsync per line is overkill; skip it


def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("stage2")
    logger.setLevel(logging.INFO)

    # avoid duplicate handlers if re-imported
    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger


def preflight_or_die(raw_root: Path, clean_root: Path, manifest_path: Path, logger: logging.Logger) -> None:
    logger.info(f"[PREFLIGHT] RAW_ROOT={raw_root}")
    logger.info(f"[PREFLIGHT] CLEAN_ROOT={clean_root}")
    logger.info(f"[PREFLIGHT] MANIFEST_PATH={manifest_path}")

    if not raw_root.exists():
        raise FileNotFoundError(f"RAW_ROOT does not exist: {raw_root}")

    # ensure clean root exists / can be created
    clean_root.mkdir(parents=True, exist_ok=True)

    # ensure clean is not inside raw
    raw_res = raw_root.resolve()
    clean_res = clean_root.resolve()
    try:
        clean_res.relative_to(raw_res)
        raise RuntimeError(f"CLEAN_ROOT must NOT be inside RAW_ROOT. CLEAN={clean_res} RAW={raw_res}")
    except ValueError:
        pass  # good


def vendor_folder_from_raw_path(raw_root: Path, file_path: Path) -> str:
    """
    Vendor folder = first path component under RAW_ROOT.
    This is the folder whose name must contain -MES or -MNQ.
    """
    rel = file_path.resolve().relative_to(raw_root.resolve())
    if not rel.parts:
        raise ValueError(f"Could not compute vendor folder for: {file_path}")
    return rel.parts[0]


def process_single_file(
    raw_root: Path,
    clean_root: Path,
    manifest_path: Path,
    logger: logging.Logger,
    raw_path: Path,
    smoke_mode: bool,
) -> ManifestEntry:
    filename = raw_path.name
    date_yyyymmdd = parse_yyyymmdd_from_filename(filename)

    vendor_folder = vendor_folder_from_raw_path(raw_root, raw_path)
    family = get_product_family(vendor_folder)

    out_path = build_output_path(clean_root, family, date_yyyymmdd)

    # idempotency
    if out_path.exists():
        status = "SKIP_EXISTS"
        logger.info(f"[SKIP] {family} {date_yyyymmdd} raw={raw_path} out={out_path}")
        return ManifestEntry(
            raw_path=str(raw_path),
            product_family=family,
            date_yyyymmdd=date_yyyymmdd,
            parquet_path=str(out_path),
            row_count=0,
            ts_event_min=None,
            ts_event_max=None,
            status=status,
            error=None,
        )

    # ensure parent dirs
    out_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"[START] {family} {date_yyyymmdd} raw={raw_path}")
    try:
        store = db.DBNStore.from_file(str(raw_path))

        # Non-negotiable: fixed price type, no floats
        store.to_parquet(
            str(out_path),
            price_type="fixed",
            map_symbols=True,
            # pretty_ts optional; if your databento version doesn't support it, remove it.
            pretty_ts=True,
        )

        row_count, ts_min, ts_max = parquet_rowcount_and_ts_event_range(out_path)

        entry = ManifestEntry(
            raw_path=str(raw_path),
            product_family=family,
            date_yyyymmdd=date_yyyymmdd,
            parquet_path=str(out_path),
            row_count=row_count,
            ts_event_min=ts_min,
            ts_event_max=ts_max,
            status="OK",
            error=None,
        )
        logger.info(f"[DONE] {family} {date_yyyymmdd} OK rows={row_count} out={out_path}")
        return entry

    except TypeError as te:
        # Most common: pretty_ts not supported on older databento versions
        msg = str(te)
        logger.error(f"[FAIL] {family} {date_yyyymmdd} raw={raw_path} error={msg}")
        return ManifestEntry(
            raw_path=str(raw_path),
            product_family=family,
            date_yyyymmdd=date_yyyymmdd,
            parquet_path=str(out_path),
            row_count=0,
            ts_event_min=None,
            ts_event_max=None,
            status="FAIL",
            error=msg,
        )
    except Exception as e:
        msg = str(e)
        logger.error(f"[FAIL] {family} {date_yyyymmdd} raw={raw_path} error={msg}")
        return ManifestEntry(
            raw_path=str(raw_path),
            product_family=family,
            date_yyyymmdd=date_yyyymmdd,
            parquet_path=str(out_path),
            row_count=0,
            ts_event_min=None,
            ts_event_max=None,
            status="FAIL",
            error=msg,
        )


def choose_smoke_files(
    raw_root: Path,
    clean_root: Path,
    files: List[Path],
) -> Tuple[Path, Path]:
    """
    Smoke test MUST WRITE, so we select earliest MES and MNQ whose out_path does NOT exist.
    If none exist for a family: stop.
    """
    # group by family with deterministic ordering
    mes_candidates: List[Path] = []
    mnq_candidates: List[Path] = []

    for p in files:
        vendor = vendor_folder_from_raw_path(raw_root, p)
        fam = get_product_family(vendor)
        if fam == "MES":
            mes_candidates.append(p)
        elif fam == "MNQ":
            mnq_candidates.append(p)

    mes_candidates = deterministic_sort(mes_candidates)
    mnq_candidates = deterministic_sort(mnq_candidates)

    def first_writable(fam: str, cands: List[Path]) -> Path:
        for p in cands:
            ymd = parse_yyyymmdd_from_filename(p.name)
            out = build_output_path(clean_root, fam, ymd)
            if not out.exists():
                return p
        raise RuntimeError(f"Smoke test cannot WRITE for {fam}: all earliest outputs already exist.")

    mes_file = first_writable("MES", mes_candidates)
    mnq_file = first_writable("MNQ", mnq_candidates)
    return mes_file, mnq_file


def run_pipeline(
    raw_root: Path,
    clean_root: Path,
    manifest_path: Path,
    log_path: Path,
    smoke_test: bool,
    run_all: bool,
) -> None:
    logger = setup_logging(log_path)
    preflight_or_die(raw_root, clean_root, manifest_path, logger)

    all_files = deterministic_sort(discover_dbn_files(raw_root))
    if not all_files:
        raise RuntimeError(f"No DBN files found under RAW_ROOT: {raw_root}")

    ok = fail = skip = 0

    if smoke_test:
        mes_file, mnq_file = choose_smoke_files(raw_root, clean_root, all_files)
        targets = [mes_file, mnq_file]

        for p in targets:
            entry = process_single_file(raw_root, clean_root, manifest_path, logger, p, smoke_mode=True)
            write_manifest_line(manifest_path, entry)

            if entry.status == "OK":
                ok += 1
            elif entry.status == "SKIP_EXISTS":
                # Smoke test is not allowed to skip; this indicates a logic error.
                raise RuntimeError("Smoke test produced SKIP_EXISTS; this must not happen.")
            else:
                fail += 1
                raise RuntimeError("Smoke test failed to write Parquet; stop-work authority engaged.")

        logger.info(f"[SUMMARY] smoke_test OK={ok} FAIL={fail} SKIP={skip}")
        print(f"SMOKE OK: wrote 2 files. OK={ok} FAIL={fail} SKIP={skip}")
        return

    if run_all:
        for p in all_files:
            entry = process_single_file(raw_root, clean_root, manifest_path, logger, p, smoke_mode=False)
            write_manifest_line(manifest_path, entry)

            if entry.status == "OK":
                ok += 1
            elif entry.status == "SKIP_EXISTS":
                skip += 1
            else:
                fail += 1

        logger.info(f"[SUMMARY] run_all OK={ok} FAIL={fail} SKIP={skip}")
        print(f"RUN_ALL DONE: OK={ok} FAIL={fail} SKIP={skip}")
        return

    raise ValueError("Must specify either smoke_test or run_all.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 2: Databento DBN(.dbn/.dbn.zst) -> Parquet (fixed price).")
    parser.add_argument("--raw-root", type=str, default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--clean-root", type=str, default=str(DEFAULT_CLEAN_ROOT))
    parser.add_argument("--manifest-path", type=str, default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument("--log-path", type=str, default=str(DEFAULT_LOG_PATH))
    parser.add_argument("--smoke-test", action="store_true")
    parser.add_argument("--run-all", action="store_true")

    args = parser.parse_args()

    if args.smoke_test and args.run_all:
        raise SystemExit("Choose only one: --smoke-test OR --run-all")

    run_pipeline(
        raw_root=Path(args.raw_root),
        clean_root=Path(args.clean_root),
        manifest_path=Path(args.manifest_path),
        log_path=Path(args.log_path),
        smoke_test=args.smoke_test,
        run_all=args.run_all,
    )


if __name__ == "__main__":
    main()
