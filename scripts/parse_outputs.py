#!/usr/bin/env python
"""Demonstration script for parsing NUFEB output files.

Adapt this to your preferred output format (dump, VTK, CSV, logs, ...).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from eps_biofilm.io_nufeb import read_simple_tsv


def main() -> None:
    example_path = Path("data/raw/example.tsv")
    if not example_path.exists():
        print("[parse_outputs] No example file at", example_path)
        return

    df = read_simple_tsv(example_path)
    print(df.head())


if __name__ == "__main__":
    main()
