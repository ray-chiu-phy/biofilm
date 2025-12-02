# Cross-Feeder Biofilm Simulation

Agent-based simulation of cross-feeding bacterial communities using NUFEB/LAMMPS, investigating how EPS secretion affects cross-feeder resilience against cheaters.

## Project Structure

```
.
├── src/
│   ├── cpp/growth_models/     # NUFEB growth model implementations
│   └── python/
│       ├── input_generation/  # Scripts to generate simulation inputs
│       └── analysis/          # Data analysis and visualization
├── config/                    # NUFEB input scripts and atom configs
├── docs/                      # Documentation and poster materials
├── biofilm/                   # NUFEB installation and simulation workspace
└── data_and_code/            # Archived experimental data and code
```

## Key Components

### Growth Models (C++)
- `fix_growth_cross1.cpp` / `fix_growth_cross2.cpp` - Cross-feeder growth with metabolite exchange
- `fix_growth_cheater.cpp` - Cheater growth (consumes but doesn't secrete)
- `fix_eps_secretion.cpp` - EPS particle secretion mechanism

### Simulation Configs
- `inputscript_EPS.nufeb` - With EPS secretion
- `inputscript_NEPS_ch.nufeb` - Without EPS (control)

### Analysis Tools
- `collect_lifetime.py` - Survival time analysis
- `growth curve.py` - Population dynamics visualization

## Quick Start

1. Install NUFEB (see `docs/Install NUFEB.md`)
2. Build with custom growth models from `src/cpp/growth_models/`
3. Run simulation:
   ```bash
   cd biofilm/crossfeeding
   mpirun -np 4 lmp_mpi -in inputscript_EPS.nufeb
   ```
4. Visualize results with ParaView

## Requirements

- NUFEB (built on LAMMPS)
- MPI runtime
- ParaView (optional, for visualization)
- Python 3.x with NumPy, Matplotlib

## References

- [NUFEB Documentation](https://github.com/nufeb/NUFEB)
- See `docs/poster.md` for research summary
