"""Helpers for running SALib-based global sensitivity analysis on NUFEB outputs."""

from __future__ import annotations

from typing import Dict

import numpy as np
from SALib.analyze import sobol
from SALib.sample import saltelli


def build_salib_problem(param_bounds: Dict[str, tuple[float, float]]) -> Dict:
    names = list(param_bounds.keys())
    bounds = [param_bounds[k] for k in names]
    return {"num_vars": len(names), "names": names, "bounds": bounds}


def demo_sobol() -> None:
    """Toy example showing how to run Sobol analysis.

    Replace the model call with a real surrogate or data-driven model.
    """

    problem = build_salib_problem(
        {
            "eps_yield_cooperator": (0.0, 0.4),
            "eps_yield_cheater": (0.0, 0.2),
        }
    )

    param_values = saltelli.sample(problem, 1024, calc_second_order=False)
    Y = np.random.rand(param_values.shape[0])  # fake outputs
    Si = sobol.analyze(problem, Y, calc_second_order=False, print_to_console=False)
    print("First-order indices:", Si["S1"])
