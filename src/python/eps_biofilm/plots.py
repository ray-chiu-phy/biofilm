"""Common plotting helpers for NUFEB EPS / cheater experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt


def plot_survival_histogram(survival_times: Sequence[float], out: Path | None = None) -> None:
    plt.figure()
    plt.hist(survival_times, bins=30)
    plt.xlabel("Collapse / survival time (h)")
    plt.ylabel("Count")
    plt.title("Distribution of survival times across parameter samples")
    if out is not None:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, bbox_inches="tight")
    else:
        plt.show()
