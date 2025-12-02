/* -*- c++ -*- ----------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

#ifdef FIX_CLASS

FixStyle(nufeb/growth/cross1,FixGrowthCross1)

#else

#ifndef LMP_FIX_GROWTH_CROSS1_H
#define LMP_FIX_GROWTH_CROSS1_H

#include "fix_growth.h"

namespace LAMMPS_NS {

class FixGrowthCross1 : public FixGrowth {
 public:
  FixGrowthCross1(class LAMMPS *, int, char **);
  virtual ~FixGrowthCross1() {}

  virtual void update_atoms();
  virtual void update_cells();

 protected:
  int imetab2;     // metabolite2
  int imetab1;     // metabolite1
  int eps_flag;

  double metab2_affinity;

  double growth;
  double yield;
  double maintain;
  double decay;
  double metab1_exp;
  double eps_yield;
  double eps_dens;
  
  class AtomVecBacillus *avec;
};

}

#endif
#endif

/* ERROR/WARNING messages:
*/
