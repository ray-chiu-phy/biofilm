#!/usr/bin/env python
"""Run a single NUFEB simulation from a prepared input file."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="NUFEB input file to run.")
    parser.add_argument(
        "--lmp-bin",
        type=str,
        default="lmp",
        help="LAMMPS/NUFEB binary name (must be on PATH)."
    )
    args = parser.parse_args()

    cmd = [args.lmp_bin, "-in", str(args.input)]
    print("[run_single_sim] Running:", " ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
