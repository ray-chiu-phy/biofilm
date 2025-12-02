import numpy as np
import matplotlib.pyplot as plt


b = 0.6
Q = 4
d = 0.15

def dNdt(N):
    return N * (b * Q * N * (1 - 2 * N) - d)

# 求非零平衡点（解 bQ*N*(1-2N) - d = 0）
coeffs = [2 * b * Q, -b * Q, d]
quad_roots = np.roots(coeffs)
real_roots = np.sort(quad_roots[np.isreal(quad_roots)].real)

# 将 N=0 也作为平衡点
equilibria = np.concatenate(([0.0], real_roots))

# 生成绘图数据
N_vals = np.linspace(0, 0.5, 400)
dNdt_vals = dNdt(N_vals)

# 绘制相线图
plt.figure(figsize=(8, 4))
plt.plot(N_vals, dNdt_vals, linewidth=2)
plt.axhline(0, linestyle='--')

stable = [equilibria[0], equilibria[2]]
unstable = equilibria[1]
plt.scatter(stable, [0, 0], marker='o', color='black', s=80, zorder=5)
plt.scatter([unstable], [0], marker='o', facecolors='none', edgecolors='black', s=80, zorder=5)

# 添加流向箭头
for x in np.linspace(0.02, 0.48, 12):
    dx = 0.016 * np.sign(dNdt(x))
    plt.arrow(x, 0, dx, 0, head_width=0.003, head_length=0.005)

plt.xlabel('Fraction of sites occupied by cross-feeder (N)')
plt.ylabel('dN/dt')
plt.title('No Cheater')
plt.tight_layout()
plt.show()
