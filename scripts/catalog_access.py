from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import duckdb


# Single source of truth for catalog location
DEFAULT_DUCKDB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
DEFAULT_TABLE = "mbp1_files"


def _yyyymmdd_to_date_str(yyyymmdd: str) -> str:
    if len(yyyymmdd) != 8 or not yyyymmdd.isdigit():
        raise ValueError(f"Invalid yyyymmdd: {yyyymmdd!r}")
    return f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


@dataclass(frozen=True)
class FileRecord:
    family: str
    yyyymmdd: str
    date: str
    parquet_path: str
    row_count: Optional[int]
    ts_event_min_utc: Optional[str]
    ts_event_max_utc: Optional[str]
    status: str
    error: Optional[str]


class Catalog:
    """
    DATA ACCESS CONTRACT (COLD HARD RULES)
    - Downstream code MUST NOT walk the filesystem to find data.
    - Downstream code MUST query DuckDB catalog and get parquet paths from it.
    - "OK only" is default. Anything not OK must be explicitly requested.
    """

    def __init__(self, db_path: Path = DEFAULT_DUCKDB_PATH, table: str = DEFAULT_TABLE):
        self.db_path = Path(db_path)
        self.table = table

    def connect(self) -> duckdb.DuckDBPyConnection:
        if not self.db_path.exists():
            raise FileNotFoundError(f"DuckDB catalog not found: {self.db_path}")
        return duckdb.connect(str(self.db_path), read_only=True)

    def get_parquet_paths(
        self,
        family: str,
        start_yyyymmdd: str,
        end_yyyymmdd: str,
        status: str = "OK",
    ) -> List[str]:
        """
        Returns parquet paths for a family in [start, end] inclusive, filtered by status (default OK).
        """
        fam = family.upper()
        start_date = _yyyymmdd_to_date_str(start_yyyymmdd)
        end_date = _yyyymmdd_to_date_str(end_yyyymmdd)

        con = self.connect()
        try:
            rows = con.execute(
                f"""
                SELECT parquet_path
                FROM {self.table}
                WHERE family = ?
                  AND date BETWEEN CAST(? AS DATE) AND CAST(? AS DATE)
                  AND status = ?
                ORDER BY date;
                """,
                [fam, start_date, end_date, status],
            ).fetchall()
            return [r[0] for r in rows]
        finally:
            con.close()

    def get_records(
        self,
        family: str,
        start_yyyymmdd: str,
        end_yyyymmdd: str,
        status: str = "OK",
    ) -> List[FileRecord]:
        """
        Returns full metadata rows for a family in [start, end] inclusive.
        """
        fam = family.upper()
        start_date = _yyyymmdd_to_date_str(start_yyyymmdd)
        end_date = _yyyymmdd_to_date_str(end_yyyymmdd)

        con = self.connect()
        try:
            rows = con.execute(
                f"""
                SELECT
                    family, yyyymmdd, CAST(date AS VARCHAR) AS date,
                    parquet_path, row_count, ts_event_min_utc, ts_event_max_utc,
                    status, error
                FROM {self.table}
                WHERE family = ?
                  AND date BETWEEN CAST(? AS DATE) AND CAST(? AS DATE)
                  AND status = ?
                ORDER BY date;
                """,
                [fam, start_date, end_date, status],
            ).fetchall()

            out: List[FileRecord] = []
            for r in rows:
                out.append(
                    FileRecord(
                        family=r[0],
                        yyyymmdd=r[1],
                        date=r[2],
                        parquet_path=r[3],
                        row_count=r[4],
                        ts_event_min_utc=r[5],
                        ts_event_max_utc=r[6],
                        status=r[7],
                        error=r[8],
                    )
                )
            return out
        finally:
            con.close()

    def get_date_range(self, family: str, status: str = "OK") -> Tuple[Optional[str], Optional[str]]:
        """
        Returns (min_yyyymmdd, max_yyyymmdd) for a family/status.
        """
        fam = family.upper()
        con = self.connect()
        try:
            row = con.execute(
                f"""
                SELECT MIN(yyyymmdd), MAX(yyyymmdd)
                FROM {self.table}
                WHERE family = ? AND status = ?;
                """,
                [fam, status],
            ).fetchone()
            return row[0], row[1]
        finally:
            con.close()