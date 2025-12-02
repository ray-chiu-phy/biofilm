# TOOLS.md – Open-source stack for EPS / cheater NUFEB research

This file lists **open-source / free tools** that are directly useful for:

- Running and extending NUFEB simulations
- Orchestrating large parameter sweeps (10³–10⁴ runs)
- Doing global sensitivity analysis and surrogate modelling on GPU
- Analysing and visualising high-volume simulation outputs

Links and install commands are provided so you can set things up quickly in a
fresh environment.

---

## 1. Core IbM / biofilm simulators

### 1.1 NUFEB (primary backend)

- **What it is**: 3D individual-based / agent-based simulator for microbial systems,
  built on top of LAMMPS, with support for biofilms, EPS, nutrient diffusion,
  hydrodynamics (CFD coupling), etc.
- **Repo & docs**:
  - Stable release: https://github.com/nufeb/NUFEB
  - Development repo (newer features): https://github.com/nufeb/NUFEB-2
  - Software paper: "NUFEB: A massively parallel simulator for individual-based
    modelling of microbial communities" (PLOS Comp. Biol. 2019).
- **Install (from source, high-level)**:
  1. Install a recent **LAMMPS** with USER-NUFEB or build the NUFEB-patched LAMMPS
     as described in the NUFEB README.
  2. Clone the repo and follow the "Build from source" instructions
     (CMake + C++ toolchain, MPI recommended).
  3. Ensure the resulting `lmp` / `lmp_nufeb` binary is on your `$PATH`.
- **How it fits this project**:
  - This is the main simulator used by the C++ `fix_growth_*` implementations
    (EPS, cross-feeding, cheater). All large-scale experiments and datasets
    are ultimately composed of many NUFEB runs.

### 1.2 iDynoMiCS 2.0 (alternative IbM platform)

- **What it is**: Next-generation individual-based modelling framework for microbial
  communities (biofilms or chemostats), historically implemented in Java and now
  being modernised as "iDynoMiCS 2.0".
- **Resources**:
  - Project page: search "iDynoMiCS 2.0 – Kreft Lab, University of Birmingham".
  - Classic paper: "iDynoMiCS: next-generation individual-based modelling of biofilms",
    Environmental Microbiology 2011.
  - Example code / protocols: https://github.com/R-Wright-1/iDynoMiCS_1.5
- **Why it matters here**:
  - Useful as a **cross-model comparison** platform: some of the same EPS / cheater
    ideas could be tested in a different IbM implementation to check robustness
    of qualitative results.

---

## 2. Workflow orchestration & large sweeps

### 2.1 Snakemake

- **What it is**: A workflow management system for reproducible, scalable data analysis
  pipelines, using a Python-based rule language (similar spirit to GNU Make).
- **Docs**: https://snakemake.readthedocs.io/ and https://snakemake.github.io/
- **Install (recommended)**:
  - With mamba/conda (typical in scientific HPC):
    - `mamba install -c conda-forge -c bioconda snakemake`
  - Or via pip (if you control the environment):
    - `pip install snakemake`
- **How to use in this project**:
  - Encode "one NUFEB run" as a rule; parameter sweeps become expanding wildcards.
  - Easy to port from local runs to SLURM / SGE / Kubernetes without changing the
    Snakefile.

### 2.2 Nextflow (optional alternative)

- **What it is**: A DSL and engine for scalable, portable scientific workflows; heavily
  used in genomics and other data-intensive domains.
- **Site & docs**: https://www.nextflow.io/
- **Install**:
  - Requires Java; typical install is:
    - `curl -s https://get.nextflow.io | bash`
  - Or via conda: `mamba install -c bioconda nextflow`
- **Why consider it**:
  - If you already have a Nextflow-based pipeline ecosystem, you can wrap NUFEB runs
    as processes and re-use HPC/cloud execution profiles.

### 2.3 Ray

- **What it is**: A unified framework for scaling Python applications and AI workloads
  across many cores, many GPUs, and many nodes.
- **Docs**: https://docs.ray.io/
- **Install (Python)**:
  - Minimal: `pip install -U ray`
- **How it helps here**:
  - Treat each NUFEB run as a Ray task or actor.
  - Schedule thousands of runs across multiple GPUs / nodes with very little
    boilerplate code.

---

## 3. GPU-accelerated ML & surrogates

### 3.1 PyTorch

- **What it is**: Widely used deep-learning / tensor library with strong GPU support.
- **Site**: https://pytorch.org/
- **Install (example, CPU-only)**:
  - `pip install torch`
  - For GPU builds, follow the selector on the PyTorch website for the right
    CUDA / OS combination.
- **Use in this project**:
  - Base tensor engine for Gaussian process surrogates and neural models of
    collapse time or other summary statistics.

### 3.2 BoTorch + GPyTorch

- **What they are**:
  - **BoTorch**: Bayesian optimisation library built on PyTorch, designed for
    Monte-Carlo acquisition functions and flexible GP models.
  - **GPyTorch**: Underlying framework for scalable Gaussian processes in PyTorch.
- **Resources**:
  - BoTorch site: https://botorch.org/
  - BoTorch GitHub: https://github.com/meta-pytorch/botorch
  - Tutorials: https://archive.botorch.org/tutorials/
- **Install**:
  - After PyTorch: `pip install botorch gpytorch`
- **Why they fit perfectly here**:
  - NUFEB runs are expensive → perfect use case for **Bayesian optimisation** to
    explore parameter space (e.g. find regimes where EPS extends survival time).
  - Also ideal for probabilistic surrogate modelling needed for global sensitivity
    and uncertainty analysis.

### 3.3 JAX (optional alternative backend)

- **What it is**: High-performance array computing library with JIT compilation and
  automatic differentiation, designed for CPU/GPU/TPU.
- **Docs**: https://docs.jax.dev/
- **Install (CPU)**:
  - `pip install jax`
  - For GPU/TPU, follow the official installation instructions to get a matching
    `jax` + `jaxlib` build.
- **Use case here**:
  - If you prefer the JAX ecosystem (Flax, BlackJAX, etc.) for probabilistic or
    differentiable modelling of NUFEB outputs, you can port the surrogate models
    from PyTorch to JAX.

---

## 4. Sensitivity analysis & UQ

### 4.1 SALib – Sensitivity Analysis Library in Python

- **What it is**: A Python library implementing standard global sensitivity analysis
  methods (Sobol, Morris, FAST, and more).
- **Repo**: https://github.com/SALib/SALib
- **Install**:
  - `pip install SALib`
- **How to use here**:
  - Treat the parameter vector (growth rates, EPS yield, diffusion coefficients, etc.)
    as inputs, and collapse time / survival indicators as outputs.
  - Compute Sobol or Morris indices to quantify how much EPS-related parameters
    contribute to variance in survival time.

---

## 5. Data handling & plotting

These are standard scientific Python tools, but are listed here for completeness:

- **NumPy** – array maths, basic numerics.
- **SciPy** – optimisation, interpolation, stats, etc.
- **pandas** – tabular data structures; convenient for storing aggregated metrics
  from many simulation runs.
- **xarray** – labelled n-dimensional arrays (excellent for storing parameter ×
  replicate × time grids).
- **matplotlib** (and optionally seaborn) – plotting.
- **ArviZ** – if you later add probabilistic models and want standard posterior /
  diagnostics plots.

Example combined installation (analysis environment):

```bash
pip install numpy scipy pandas xarray matplotlib seaborn arviz
```

---

## 6. Reproducibility & project hygiene

Recommended additional tooling for a more production-grade setup:

* **Poetry or uv** – for managing Python dependencies and virtualenvs.
* **pre-commit** – for code style checks (black, isort, flake8/ruff).
* **DVC or git-annex** – for versioning large simulation outputs without bloating
  the Git repository.
* **Docker / Singularity** – for containerised NUFEB + Python environments, useful
  on HPC and for sharing exact experimental setups.

These are not strictly required, but integrating them will make it much easier to
turn this work into a robust, shareable research artefact (and to re-run everything
when revising a paper).
