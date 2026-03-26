import duckdb
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, Dict


class RegimeMachine:
    def __init__(self, db_path: Path):
        self.con = duckdb.connect(str(db_path), read_only=True)
        # cache logic: date_yyyymmdd -> symbol -> (poc, vah, val)
        self.cached_vp: Dict[str, Dict[str, Tuple[float, float, float]]] = {}
        
        self.current_day = None
        self.current_regime = None
        self.prev_vah = None
        self.prev_val = None
        self.pending_imbalance_dir = 0
        self.rth_open_price = None
        self.logged_today = False

    def get_previous_trading_day(self, current_date_yyyymmdd: str, symbol: str) -> Optional[str]:
        family = symbol.split('.')[0]
        query = f"""
            SELECT MAX(yyyymmdd) 
            FROM mbp1_ok_files 
            WHERE family='{family}' 
              AND yyyymmdd < '{current_date_yyyymmdd}'
        """
        row = self.con.execute(query).fetchone()
        return row[0] if row and row[0] else None

    def compute_previous_vp(self, current_date_yyyymmdd: str, symbol: str) -> Optional[Tuple[float, float, float]]:
        prev_date = self.get_previous_trading_day(current_date_yyyymmdd, symbol)
        if not prev_date:
            return None
            
        if prev_date in self.cached_vp and symbol in self.cached_vp[prev_date]:
            return self.cached_vp[prev_date][symbol]

        family = symbol.split('.')[0]
        row = self.con.execute(
            f"SELECT parquet_path FROM mbp1_ok_files WHERE family='{family}' AND yyyymmdd='{prev_date}'"
        ).fetchone()
        
        if not row:
            return None
        
        parquet_path = row[0]
        target_date = f"{prev_date[0:4]}-{prev_date[4:6]}-{prev_date[6:8]}"
        
        # SQL Query for Volume Profile (RTH 09:30 to 16:00 EST)
        query = f"""
            SELECT 
                FLOOR(price / 1e9) AS price_bin,
                SUM(size) AS bin_volume
            FROM read_parquet('{parquet_path}')
            WHERE symbol = '{symbol}'
              AND ts_event >= '{target_date} 09:30:00'
              AND ts_event <= '{target_date} 16:00:00'
            GROUP BY 1
            ORDER BY price_bin
        """
        
        df = self.con.execute(query).df()
        
        if df.empty:
            return None
            
        total_vol = df['bin_volume'].sum()
        if total_vol == 0:
            return None
            
        # 1) Prev_POC: the bin with highest volume
        poc_idx = df['bin_volume'].idxmax()
        poc = df.loc[poc_idx, 'price_bin']
        
        # 2) Expand around POC to find 70% bounds
        target_vol = total_vol * 0.70
        current_vol = df.loc[poc_idx, 'bin_volume']
        
        val_idx = poc_idx
        vah_idx = poc_idx
        
        while current_vol < target_vol:
            up_idx = vah_idx + 1 if (vah_idx + 1) in df.index else None
            down_idx = val_idx - 1 if (val_idx - 1) in df.index else None
            
            up_vol = df.loc[up_idx, 'bin_volume'] if up_idx is not None else -1
            down_vol = df.loc[down_idx, 'bin_volume'] if down_idx is not None else -1
            
            if up_vol == -1 and down_vol == -1:
                break
                
            if up_vol >= down_vol:
                vah_idx = up_idx
                current_vol += up_vol
            else:
                val_idx = down_idx
                current_vol += down_vol
                
        val_bin = df.loc[val_idx, 'price_bin']
        vah_bin = df.loc[vah_idx, 'price_bin']
        
        # The upper boundary of a 1.0 bin is bin + 1.0
        val = val_bin
        vah = vah_bin + 1.0
        
        if prev_date not in self.cached_vp:
            self.cached_vp[prev_date] = {}
        self.cached_vp[prev_date][symbol] = (poc, vah, val)
        
        return (poc, vah, val)

    def evaluate_regime(self, current_time: datetime, current_price: float, vp_levels: Tuple[float, float, float]) -> Optional[str]:
        # Fast path if already initialized
        if self.logged_today:
            if self.current_regime == "PENDING_IMBALANCE":
                if self.pending_imbalance_dir == 1 and current_price < self.prev_vah:
                    self.current_regime = "REJECTION_DOWN"
                elif self.pending_imbalance_dir == -1 and current_price > self.prev_val:
                    self.current_regime = "REJECTION_UP"
            return self.current_regime

        # Before 09:30:00
        if current_time.hour < 9 or (current_time.hour == 9 and current_time.minute < 30):
            return None  # Pre-market
            
        # First tick at or after 09:30:00 (Initialization)
        poc, vah, val = vp_levels
        self.current_regime = None
        self.prev_vah = vah
        self.prev_val = val
        self.rth_open_price = current_price
        self.logged_today = True  # We set this so we don't initialize again today
        
        if val <= current_price <= vah:
            self.current_regime = "BALANCE"
        else:
            self.current_regime = "PENDING_IMBALANCE"
            self.pending_imbalance_dir = 1 if current_price > vah else -1
            
        return self.current_regime

