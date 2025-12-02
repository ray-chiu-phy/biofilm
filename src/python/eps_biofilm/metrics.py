"""Metrics for EPS / cheater experiments (collapse time etc.)."""

from __future__ import annotations

from typing import Sequence, Mapping
import numpy as np
import pandas as pd


def estimate_collapse_time(time: Sequence[float], total_biomass: Sequence[float], threshold: float) -> float:
    """Return first time where biomass falls below `threshold`.

    If the threshold is never crossed, return the last time point.
    """

    t = np.asarray(time)
    b = np.asarray(total_biomass)
    idx = np.where(b < threshold)[0]
    if len(idx) == 0:
        return float(t[-1])
    return float(t[idx[0]])


def summarise_replicate(df: pd.DataFrame, biomass_col: str = "biomass", time_col: str = "time") -> Mapping[str, float]:
    """Example aggregation over a single replicate's time series.

    Expect `df` with at least `time_col` and `biomass_col`.
    """

    collapse_time = estimate_collapse_time(df[time_col].values, df[biomass_col].values, threshold=1e-3)
    return {
        "collapse_time": collapse_time,
        "max_biomass": float(df[biomass_col].max()),
    }
