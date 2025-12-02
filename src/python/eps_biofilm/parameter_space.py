"""Parameter space definitions and simple helpers for EPS / cheater experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class UniformParam:
    name: str
    low: float
    high: float


def default_parameter_space() -> Dict[str, UniformParam]:
    """Return a toy parameter space to be customised."""

    return {
        "eps_yield_cooperator": UniformParam("eps_yield_cooperator", 0.0, 0.4),
        "eps_yield_cheater": UniformParam("eps_yield_cheater", 0.0, 0.2),
    }
