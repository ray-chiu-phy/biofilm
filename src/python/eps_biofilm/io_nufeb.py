"""I/O helpers for NUFEB/LAMMPS outputs.

This file intentionally stays very light: adapt it to
your actual output file formats (dumps, logs, etc.).
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import pandas as pd


def read_simple_tsv(path: Path) -> pd.DataFrame:
    """Example helper for reading a TSV table exported from NUFEB.

    Replace with a parser tailored to your own outputs.
    """

    return pd.read_csv(path, sep="\t")


def load_summary_table(path: Path) -> pd.DataFrame:
    """Load an aggregated summary table (e.g. collapse times)."""

    return pd.read_csv(path)
