"""Skeleton for BoTorch-based surrogate models and Bayesian optimisation."""

from __future__ import annotations

import torch
from botorch.fit import fit_gpytorch_mll
from botorch.models import SingleTaskGP
from botorch.acquisition import ExpectedImprovement
from botorch.optim import optimize_acqf
from gpytorch.mlls import ExactMarginalLogLikelihood


def fit_simple_gp(X: torch.Tensor, Y: torch.Tensor) -> SingleTaskGP:
    """Fit a basic GP to (X, Y)."""

    model = SingleTaskGP(X, Y)
    mll = ExactMarginalLogLikelihood(model.likelihood, model)
    fit_gpytorch_mll(mll)
    return model


def suggest_next_point(model: SingleTaskGP, bounds: torch.Tensor) -> torch.Tensor:
    """One-step EI-based suggestion under box constraints `bounds`."""

    model.eval()
    model.likelihood.eval()
    ei = ExpectedImprovement(model, best_f=model.train_targets.max())
    candidate, _ = optimize_acqf(
        ei,
        bounds=bounds,
        q=1,
        num_restarts=8,
        raw_samples=64,
    )
    return candidate
