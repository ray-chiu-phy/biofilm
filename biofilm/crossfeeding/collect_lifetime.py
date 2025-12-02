#!/usr/bin/env python3
"""
Self-contained script (no command-line args) to scan ./data/*.log,
label files by name (eps -> 1, neps -> 2), and record the first Step
where BOTH v_ncross1 and v_ncross2 are strictly below THRESHOLD.
Writes lifetimes.csv in the working directory.
"""

from pathlib import Path
import re
import csv
from typing import Optional

# ---- User-editable constants (inside file) ----
DATA_DIR = Path("C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\exp_data")
OUT_CSV = Path("C:\\Users\\User\\Desktop\\分子研究\\中研院物理所實習\\biofilm\\crossfeeding\\data\\lifetimes.csv")
THRESHOLD = 50.0           # strictly below this value
# -----------------------------------------------

def parse_log_first_below_both(log_path: Path, thr: float = 50.0) -> Optional[int]:
    """
    Return the first 'Step' where BOTH v_ncross1 and v_ncross2 are strictly below `thr`.
    If never reached, return None.
    """
    idx_step = idx_n1 = idx_n2 = None
    header_found = False

    with log_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Find header line containing column names
            if not header_found and ("Step" in line and "v_ncross1" in line and "v_ncross2" in line):
                headers = line.strip().split()
                try:
                    idx_step = headers.index("Step")
                    idx_n1 = headers.index("v_ncross1")
                    idx_n2 = headers.index("v_ncross2")
                except ValueError:
                    continue
                header_found = True
                continue

            if header_found:
                parts = line.strip().split()
                if len(parts) <= max(idx_step, idx_n1, idx_n2):
                    continue

                # The value at idx_step should be integer-like
                if not re.fullmatch(r"-?\d+", parts[idx_step]):
                    continue

                try:
                    step = int(parts[idx_step])
                    n1 = float(parts[idx_n1])
                    n2 = float(parts[idx_n2])
                except ValueError:
                    continue

                if n1 < thr and n2 < thr:
                    return step
    return None

def label_from_name(name: str) -> Optional[int]:
    """
    Return 1 if filename contains 'eps' (case-insensitive),
    2 if it contains 'neps' (takes precedence),
    else None.
    """
    lname = name.lower()
    if "neps" in lname:
        return 2
    if "eps" in lname:
        return 1
    return None

def main():
    data_dir: Path = DATA_DIR
    out_csv: Path = OUT_CSV
    rows = []

    # Create data dir if missing (no error if empty)
    data_dir.mkdir(parents=True, exist_ok=True)

    for log_path in sorted(data_dir.glob("*.log")):
        label = label_from_name(log_path.name)
        if label is None:
            continue

        lifetime = parse_log_first_below_both(log_path, thr=THRESHOLD)
        rows.append({
            "filename": log_path.name,
            "label": label,
            "lifetime_step": "" if lifetime is None else lifetime
        })

    # Write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "label", "lifetime_step"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Scanned {len(list(DATA_DIR.glob('*.log')))} .log files; wrote {len(rows)} rows to {out_csv}")

if __name__ == "__main__":
    main()
