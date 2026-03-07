from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root on sys.path so imports work if you keep module under src/
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# If you keep the module somewhere else, adjust this import to match your repo layout.
# For now, assume this script sits next to the module or you paste the module in same folder.
try:
    from stage2_dbn_to_parquet import main
except ImportError:
    # fallback if you placed module under src/project_1l/data_layer/
    from src.project_1l.data_layer.stage2_dbn_to_parquet import main  # type: ignore

if __name__ == "__main__":
    main()