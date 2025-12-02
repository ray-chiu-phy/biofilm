import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fname = "C:/Users/User/atom.in" #Desktop/分子研究/中研院物理所實習/biofilm/sim_result/co_NEPS/atom.in"

def read_atom_file(fname):
    xs, ys, zs = [], [], []
    radii, types = [], []
    with open(fname) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("Atoms"):
            start = i + 2
            break
    else:
        raise RuntimeError("Cannot find 'Atoms' section in file.")
    
    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        t = int(parts[1])             
        r = float(parts[2])           
        x = float(parts[4])
        y = float(parts[5])
        z = float(parts[6])
        types.append(t)
        radii.append(r)
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs, radii, types

def main():
    xs, ys, zs, radii, types = read_atom_file(fname)

    sizes = [(r * 1e6)**2 for r in radii]

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')

    lim = 3e-4
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_zlim(0, lim)
    ax.set_box_aspect((1,1,1))

    unique_types = sorted(set(types))
    cmap = plt.get_cmap('tab10') 
    for idx, t in enumerate(unique_types):
        xi = [x for x, tt in zip(xs, types) if tt == t]
        yi = [y for y, tt in zip(ys, types) if tt == t]
        zi = [z for z, tt in zip(zs, types) if tt == t]
        si = [s for s, tt in zip(sizes, types) if tt == t]
        ax.scatter(xi, yi, zi,
                   s=si,
                   color=cmap(idx),
                   label=f"Type {t}",
                   alpha=0.7,
                   edgecolors='w',
                   linewidths=0.3)

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title(f"Preview of {fname.split('/')[-1]}")
    ax.legend(loc="upper left", bbox_to_anchor=(1,1))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
