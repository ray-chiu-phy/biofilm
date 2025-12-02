import random
import os
# box size
x_max = 3e-4
y_max = 3e-4
z_max = 3e-4

# numbers of prticles for each atom type
counts = [500, 500]

rmins = [1e-6, 1e-6]

rmaxs = [2e-6, 2e-6]

# density (kg/m^3)
densities = [500, 500]

outfile = "atom.in"
os.chdir('C:/Users/User')
print(f"hi{os.getcwd()}")
def generate():
    n_types = len(counts)
    total_atoms = sum(counts)

    with open(outfile, "w") as f:
        f.write("NUFEB Simulation\n\n")
        f.write(f"     {total_atoms} atoms\n")
        f.write(f"     {n_types} atom types\n\n")
        f.write(f"  0.0e+00   {x_max:.2e}  xlo xhi\n")
        f.write(f"  0.0e+00   {y_max:.2e}  ylo yhi\n")
        f.write(f"  0.0e+00   {z_max:.2e}  zlo zhi\n\n")
        f.write("Atoms\n\n")
        #print("hi")

        atom_id = 1
        for tp in range(1, n_types+1):
            for _ in range(counts[tp-1]):
                
                r = random.uniform(rmins[tp-1], rmaxs[tp-1])
                x = random.uniform(r, x_max - r)
                y = random.uniform(r, y_max - r)
                z = r   # z = radius of particles
                # id type radius density x y z radius
                f.write(
                    f"{atom_id} {tp} "
                    f"{r:.2e} {densities[tp-1]:.0f} "
                    f"{x:.2e} {y:.2e} {z:.2e} "
                    f"{r:.2e}\n"
                )
                atom_id += 1


if __name__ == "__main__":
    generate()
