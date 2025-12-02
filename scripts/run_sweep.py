#!/usr/bin/env python
"""Minimal skeleton for running a parameter sweep over NUFEB simulations."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="YAML config for the sweep.")
    parser.add_argument("--n-samples", type=int, default=8, help="Number of samples.")
    parser.add_argument(
        "--backend",
        choices=["local", "ray"],
        default="local",
        help="Execution backend (extend as needed).",
    )
    args = parser.parse_args()

    print("[run_sweep] This is a stub. Wire me up to your actual sweep logic.")
    print("Config:", args.config)
    print("n_samples:", args.n_samples)
    print("backend:", args.backend)


if __name__ == "__main__":
    main()
