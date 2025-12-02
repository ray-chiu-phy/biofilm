#!/usr/bin/env python
"""Aggregate raw NUFEB outputs into a single tidy table.

This is a stub: adapt it to the real output layout of your runs.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    raw_dir = Path("data/raw/example_sweep")
    out_path = Path("data/processed/example_summary.csv")

    # TODO: implement your parsing logic here.
    # For now we emit a tiny dummy table just so downstream code has something to read.
    df = pd.DataFrame(
        {
            "sample_id": [0, 1],
            "collapse_time": [10.0, 20.0],
        }
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print("[aggregate_results] Wrote", out_path)


if __name__ == "__main__":
    main()
