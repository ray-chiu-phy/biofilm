/* ----------------------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

#include "fix_growth_cheater.h"

#include <cstdio>
#include <cstring>
#include <cmath>
#include "atom_vec_bacillus.h"
#include "atom.h"
#include "error.h"
#include "grid.h"
#include "group.h"
#include "grid_masks.h"
#include "math_const.h"
#include "update.h"

using namespace LAMMPS_NS;
using namespace FixConst;
using namespace MathConst;

/* ---------------------------------------------------------------------- */

FixGrowthCheater::FixGrowthCheater(LAMMPS *lmp, int narg, char **arg) :
  FixGrowth(lmp, narg, arg)
{
  avec = nullptr;
  avec = (AtomVecBacillus *) atom->style_match("bacillus");

  if (narg < 9)
    error->all(FLERR, "Illegal fix nufeb/growth/cheater command");

  if (!grid->chemostat_flag)
    error->all(FLERR, "fix nufeb/growth/cheater requires grid_style nufeb/chemostat");

  isub = -1;
  imetab2 = -1;

  sub_affinity = 0.0;
  metab1_affinity = 0.0;
  metab2_affinity = 0.0;

  growth = 0.0;
  yield = 1.0;
  maintain = 0.0;
  decay = 0.0;
  eps_yield = 0.0;
  eps_dens = 1.0;
  eps_flag = 0;

  isub = grid->find(arg[3]);
  if (isub < 0)
    error->all(FLERR, "Can't find substrate(sub) name");
  sub_affinity = utils::numeric(FLERR,arg[4],true,lmp);
  if (sub_affinity <= 0)
    error->all(FLERR, "substrate affinity must be greater than zero");

  imetab1 = grid->find(arg[5]);
  if (imetab1 < 0)
      error->all(FLERR, "Can't find substrate(metabolite1) name");
  metab1_affinity = utils::numeric(FLERR, arg[6], true, lmp);
  if (metab1_affinity <= 0)
      error->all(FLERR, "metabolite1 affinity must be greater than zero");

  imetab2 = grid->find(arg[7]);
  if (imetab2 < 0)
    error->all(FLERR, "Can't find substrate(metab2) name");
  metab2_affinity = utils::numeric(FLERR,arg[8],true,lmp);
  if (metab2_affinity <= 0)
    error->all(FLERR, "metabolite2 affinity must be greater than zero");


  int iarg = 9;
  while (iarg < narg) {
    if (strcmp(arg[iarg], "growth") == 0) {
      growth = utils::numeric(FLERR,arg[iarg+1],true,lmp);
      iarg += 2;
    } else if (strcmp(arg[iarg], "yield") == 0) {
      yield = utils::numeric(FLERR,arg[iarg+1],true,lmp);
      iarg += 2;
    } else if (strcmp(arg[iarg], "maintain") == 0) {
      maintain = utils::numeric(FLERR,arg[iarg+1],true,lmp);
      iarg += 2;
    } else if (strcmp(arg[iarg], "decay") == 0) {
      decay = utils::numeric(FLERR,arg[iarg+1],true,lmp);
      iarg += 2;
    } else if (strcmp(arg[iarg], "epsyield") == 0) {
      eps_yield = utils::numeric(FLERR, arg[iarg + 1], true, lmp);
      iarg += 2;
    } else if (strcmp(arg[iarg], "epsdens") == 0) {
      eps_flag = 1;
      eps_dens = utils::numeric(FLERR, arg[iarg + 1], true, lmp);
      iarg += 2;
    } else {
      error->all(FLERR, "Illegal fix nufeb/growth/cheater command");
    }
  }
}

/* ---------------------------------------------------------------------- */

void FixGrowthCheater::update_cells()
{
  double **conc = grid->conc;
  double **reac = grid->reac;
  double **dens = grid->dens;

  for (int i = 0; i < grid->ncells; i++) {
    if (grid->mask[i] & GRID_MASK) {
      // cheater growth rate based on substrate(sub), metabolite1 and metabolite2
      double tmp1 = growth * conc[isub][i] / (sub_affinity + conc[isub][i]) * conc[imetab1][i] / (metab1_affinity + conc[imetab1][i]) * conc[imetab2][i] / (metab2_affinity + conc[imetab2][i]);

      // nutrient utilization
      reac[isub][i] -= 1 / yield * tmp1 * dens[igroup][i];  //total sub consumption
      reac[imetab1][i] -= 1 / yield * tmp1 * dens[igroup][i];
      reac[imetab2][i] -= 1 / yield * tmp1 * dens[igroup][i];
    }
  }
}

/* ---------------------------------------------------------------------- */

void FixGrowthCheater::update_atoms()
{
  double** x = atom->x;
  double* radius = atom->radius;
  double* rmass = atom->rmass;
  double* biomass = atom->biomass;
  double* outer_radius = atom->outer_radius;
  double* outer_mass = atom->outer_mass;
  double **conc = grid->conc;

  const double three_quarters_pi = (3.0 / (4.0 * MY_PI));
  const double four_thirds_pi = 4.0 * MY_PI / 3.0;
  const double third = 1.0 / 3.0;

  for (int i = 0; i < grid->ncells; i++) {
    // cheater growth rate based on substrate(sub), metabolite1 and metabolite2
    double tmp1 = growth * conc[isub][i] / (sub_affinity + conc[isub][i]) * conc[imetab1][i] / (metab1_affinity + conc[imetab1][i]) * conc[imetab2][i] / (metab2_affinity + conc[imetab2][i]);

    grid->growth[igroup][i][0] = tmp1 - decay - maintain;
    grid->growth[igroup][i][1] = (eps_yield / yield) * (tmp1);
  }

  for (int i = 0; i < atom->nlocal; i++) {
      if (atom->mask[i] & groupbit) {
          const int cell = grid->cell(x[i]);
          const double density = rmass[i] /
              (four_thirds_pi * radius[i] * radius[i] * radius[i]);
          // forward Euler to update biomass and rmass
          rmass[i] = rmass[i] * (1 + grid->growth[igroup][cell][0] * dt);

          if (eps_flag) {
              outer_mass[i] = four_thirds_pi * (outer_radius[i] * outer_radius[i] * outer_radius[i] -
                  radius[i] * radius[i] * radius[i]) * eps_dens + grid->growth[igroup][cell][1] * rmass[i] * dt;

              outer_radius[i] = pow(three_quarters_pi * (rmass[i] / density + outer_mass[i] / eps_dens), third);
          }
          radius[i] = pow(three_quarters_pi * (rmass[i] / density), third);
      }
	// if (i==0) {
  	//	double rratio = outer_radius[i] / radius[i];
  	//	printf("timestep=%lld  atom0 outer/radius = %.8f\n",
    //     	update->ntimestep, rratio);
    //  }
  }

  if (!eps_flag) { 
    if (atom->coccus_flag) {
       update_atoms_coccus();
    } else {
             update_atoms_bacillus(avec);
    }
  }


}
