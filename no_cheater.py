import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parameters from paper
b = 0.6
Q = 4
d = 0.15

# ODE definition: dN/dt = N * (bQ * N * (1 - 2N) - d)
def dNdt(t, y):
    N = y[0]
    return N * (b * Q * N * (1 - 2 * N) - d)

# Compute fixed points by solving bQ*N*(1-2N) - d = 0
coeffs = [2 * b * Q, -b * Q, d]
roots = np.roots(coeffs)
real_roots = np.sort(roots[np.isreal(roots)].real)
N_unstable, N_stable = real_roots

# Define initial conditions near the unstable and stable fixed points
epsilon = 0.01
initial_conditions = [
    N_unstable - epsilon,
    N_unstable+ epsilon ,
    0.1, 0.3, 0.5]

# Time span for integration
t_eval = np.linspace(0, 60, 400)

# Solve ODE for each initial condition
solutions = [solve_ivp(dNdt, [0, 60], [ic], t_eval=t_eval) for ic in initial_conditions]

# Plotting
fig, ax = plt.subplots(figsize=(8, 5))

# Colors for each trajectory
colors = ['gold', 'orange', 'red', 'lightseagreen', 'teal']

# Plot trajectories and initial points
for sol, ic, color in zip(solutions, initial_conditions, colors):
    ax.plot(sol.t, sol.y[0], color=color, label=f'N(0)={ic:.3f}')
    #ax.scatter(0, ic, color=color, edgecolors='black', zorder=5)

# Move y-axis to x=0 and annotate fixed points
ax.spines['left'].set_position(('data', 0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))

# Mark fixed points on y-axis at x=0
ax.scatter([0, 0, 0], [0, N_unstable, N_stable],
           marker='o', facecolors=['black','none','black'],
           edgecolors='black', s=100, zorder=5)
# Annotate fixed points
ax.text(0.5, 0, '0.000', va='bottom', ha='left')
ax.text(0.5, N_unstable, f'{N_unstable:.3f}', va='bottom', ha='left')
ax.text(0.5, N_stable, f'{N_stable:.3f}', va='bottom', ha='left')

# Labels and legend
ax.set_xlabel('time (t)')
ax.set_ylabel('Fraction of sites occupied by cross-feeder (N)')
ax.set_title('Time Evoluation of N without Cheater')

plt.tight_layout()
plt.show()
