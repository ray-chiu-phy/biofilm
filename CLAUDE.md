# Cross-Feeder Biofilm Simulation

## Quick Reference

**Project**: Agent-based simulation of cross-feeding bacteria with EPS
**Tech**: NUFEB/LAMMPS, C++, Python
**Author**: 邱弈瑞 (Chiu, Yi-Jui)、 蔡秀吉（Hsiu-Chi Tsai）

## Directory Structure

```
src/cpp/growth_models/    # Custom NUFEB growth models
src/python/analysis/      # Data analysis scripts
src/python/input_generation/  # Input file generators
config/                   # NUFEB input scripts (.nufeb, .in)
docs/                     # Documentation, poster, install guide
biofilm/                  # NUFEB workspace and simulation outputs
```

## Key Files

- `src/cpp/growth_models/fix_growth_cross*.cpp` - Cross-feeder growth (Monod kinetics + metabolite exchange)
- `src/cpp/growth_models/fix_growth_cheater.cpp` - Cheater growth (consume only)
- `src/cpp/growth_models/fix_eps_secretion.cpp` - EPS particle creation
- `config/inputscript_EPS.nufeb` - With EPS secretion
- `config/inputscript_NEPS_ch.nufeb` - Control (no EPS)

## Commands

```bash
# Run simulation
cd biofilm/crossfeeding
mpirun -np 4 lmp_mpi -in inputscript_EPS.nufeb

# Generate initial atoms
python src/python/input_generation/atom_generate.py

# Analyze survival data
python src/python/analysis/collect_lifetime.py
```

## Development Guidelines

**CRITICAL**: Follow these rules when editing code:

- TDD: Write tests first, implement all planned tasks
- Boy Scout Rule: Leave code cleaner than found
- Small CLs: Keep changes focused and minimal
- **NEVER**: Over-generate, premature abstraction
- **NEVER**: Use flashy syntax unnecessarily
- Comments: 繁體中文, shorter than code itself
- Bug fixes: Analyze logs step-by-step, don't guess

## Excluded from Git

- `biofilm/` simulation outputs (VTK, HDF5)
- `ParaView-*/` (external software, 3.4GB)
- `*.vtu`, `*.vti`, `*.h5`, `*.zip`

開發計畫務必整合 "TDD Rule" 和 "Boy Scout Rule" 或是 "Small CLs"（不清楚就請上網查詢這些軟體開發的觀念和原則）。同時，請特別註記不可以出現生成 AI 常見的低級錯誤 "過度生成"、"過早抽象"，另外，也不可以出現任何與 claude 和 anthropic 有關的內容或是訊息。

計畫當中設計的 TDD 原則請你務必都要進行實作（所有的任務都要實作），不能有任何的任務被 SKIPED，通通都要 implementation。同時，程式碼的檔案的變量和變數命名，不要像是 AI 生成的異常完美，要像是人類撰寫的，實作時要確保有清晰的邏輯，同時請務必保持程式碼自然，不要讓人看出是 AI 生成，也請務必遵循 Code Readability，記住代碼是寫給人看的，所以要有自然的代碼流程（無論在任何階段通通不可以 push）。同時註解要用台灣的繁體中文口語邏輯還進行撰寫，程式碼的註解不得比程式碼本身還長。請注意決定不行在不需要的地方強行使用最新的炫技語法，同時不要一直嘗試 Refactor ，要保持專案程式碼的命名一致性，不要在不同檔案定義了五（數個）一樣功能的函數。同時，當遇到　BUG 時間，解決 BUG 的方式應該是一步一步的分析 Log 或 Stack Trace。


# CLAUDE.md – EPS Biofilm Cheater Project

This repository is for running and analysing **NUFEB-based individual-based simulations**
of cross-feeding microbial consortia with EPS production and cheater invasion.

Claude Code should use this file as the main reference for:
- Project goals and context
- Repository layout
- Coding conventions
- Recommended workflows and commands

---

## 1. Project overview

- **Goal**: Explore how EPS production and spatial structure affect the survival time of
  cross-feeding communities in the presence of metabolite cheaters, using NUFEB + LAMMPS
  as the simulator and Python for large-scale parameter sweeps, sensitivity analysis,
  and surrogate modelling.
- **Core idea**: Treat each NUFEB run as an expensive black-box function `f(theta)` that
  outputs metrics such as consortium collapse time, biomass trajectories, and spatial
  structure indicators. Python tooling (SALib, BoTorch, Ray, etc.) orchestrates and
  analyses many such runs.

---

## 2. Tech stack

- **Simulation backend**
  - C++ / NUFEB / LAMMPS (compiled locally; not vendored in this repo)
  - Custom NUFEB fixes for EPS, cross-feeding and cheaters (your `fix_growth_*` code)
- **Orchestration & analysis (Python 3.10+)**
  - Snakemake or Ray for running parameter sweeps
  - SALib for global sensitivity analysis
  - PyTorch + BoTorch/GPyTorch for GP surrogates & Bayesian optimisation
  - NumPy / pandas / xarray / matplotlib for data handling & plotting

Assumptions:
- NUFEB/LAMMPS is installed and available as `lmp` or `lmp_nufeb` on `$PATH`.
- Python dependencies are installed via `pip install -r requirements.txt`.

---

## 3. Repository layout

- `CLAUDE.md` — This file (read me first).
- `README.md` — Quickstart and high-level overview.
- `TOOLS.md` — Curated list of external tools for this project.
- `requirements.txt` — Python dependencies.
- `Snakefile` — (optional) Snakemake workflow for large sweeps.
- `configs/`
  - `params_example.yaml` — Example parameter ranges for sweeps.
- `templates/`
  - `base_nufeb_input.in` — Minimal NUFEB/LAMMPS input template with placeholders.
- `scripts/`
  - `run_single_sim.py` — Run one NUFEB simulation.
  - `run_sweep.py` — Orchestrate many runs (local or Ray).
  - `aggregate_results.py` — Turn raw dumps into tidy tables.
  - `parse_outputs.py` — Low-level parsers and demos.
- `src/eps_biofilm/`
  - `parameter_space.py` — Parameter definitions & sampling.
  - `io_nufeb.py` — IO helpers for NUFEB outputs.
  - `metrics.py` — Compute collapse time, EPS fractions, etc.
  - `salib_sensitivity.py` — Global sensitivity analysis helpers.
  - `botorch_surrogate.py` — GP surrogates & Bayesian optimisation.
  - `plots.py` — Common plotting helpers.
- `notebooks/`
  - `00_exploration.ipynb` — EDA + quick plots (skeleton file).
  - `10_paper_figures.ipynb` — Reproducible figures for paper (skeleton file).
- `data/`
  - `raw/` — Raw NUFEB outputs (dumps, logs, VTK, CSV).
  - `processed/` — Aggregated metrics (Parquet/CSV, ready for analysis).
- `.github/workflows/ci.yml` — Minimal CI skeleton.

---

## 4. Coding conventions

**General**
- Prefer small, composable functions with clear names.
- Separate the concerns: simulation IO, analysis, and plotting should live in different modules.
- Avoid "god scripts" that mix everything together.

**Python**
- Use type hints where useful (`from __future__ import annotations` is okay).
- Light PEP 8: snake_case for variables/functions, PascalCase for classes.
- Put script entry points under `if __name__ == "__main__":`.

**C++ / NUFEB / LAMMPS**
- When editing or adding fixes, follow the existing NUFEB coding style.
- Keep biological rules (growth, EPS, cheaters) local to specific fixes.
- Try not to touch core LAMMPS unless absolutely necessary.

---

## 5. Typical workflows

### 5.1 Small local test

1. Create env and install deps:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Edit `configs/params_example.yaml` to a tiny space.
3. Run:
   - `python scripts/run_sweep.py --config configs/params_example.yaml --n-samples 4`
4. Check `data/raw/` and `data/processed/` for outputs.

### 5.2 Large sweep (Ray)

1. Ensure Ray is installed and Ray cluster is available (or run locally).
2. Run:
   - `python scripts/run_sweep.py --config configs/params_example.yaml --n-samples 512 --backend ray`
3. Use `scripts/aggregate_results.py` to summarise outputs.
4. Use `src/eps_biofilm/salib_sensitivity.py` and `botorch_surrogate.py` for analysis.

---

## 6. How Claude Code should help

- Extend existing patterns in `src/eps_biofilm` instead of inventing new ones.
- Propose **small, reviewable** changes (avoid huge refactors).
- Treat NUFEB runs as expensive – always think about caching and reusing results.
- Make suggestions that keep experiments reproducible (config-driven, not magic numbers).

---

## 7. Things to avoid

- Hard-coding absolute paths.
- Committing raw NUFEB dumps to git.
- Auto-generating large parts of NUFEB/LAMMPS source trees.

---

## 8. Future extensions

Potential future additions:
- `workflows/` for Nextflow / CWL / WDL pipelines.
- Container definitions (Docker/Singularity).
- MCP tools to launch runs directly from Claude Code.
