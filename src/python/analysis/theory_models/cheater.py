import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 論文參數
b, Q, b0, d = 0.6, 4, 0.7, 0.15

# 微分方程
def odes(t, y):
    N, C = y
    dN = N * (b * Q * N * (1 - 2 * N - C) - d)
    dC = C * (b0 * Q * N * (1 - 2 * N - C) - d)
    return [dN, dC]

# 計算 N 的平衡點 (C=0 時的非零平衡)
roots = np.roots([2*b*Q, -b*Q, d])
real_roots = np.sort(roots[np.isreal(roots)].real)
N_low, N_high = real_roots

# 初始條件：cross-feeders 取高根，cheater 給小量
N0, C0 = N_high, 1e-4
y0 = [N0, C0]

# 時間區間
t_span = (0, 500)
t_eval = np.linspace(*t_span, 1000)

# 求解
sol = solve_ivp(odes, t_span, y0, t_eval=t_eval, method='RK45')

# 繪圖
plt.figure(figsize=(8, 4.5))
plt.plot(sol.t, sol.y[0], color='teal', linewidth=2, label='cross-feeders')
plt.plot(sol.t, sol.y[1], color='red', linewidth=2, label='cheaters')

# 標示初始值
plt.scatter(0, N0, facecolors='none', edgecolors='black', s=100, zorder=5)
plt.scatter(0, C0, color='black', s=40, zorder=5)

# 平衡值虛線
plt.hlines([N_low, N_high], 0, 500, linestyles='--', colors='gray')

plt.xlabel('time (t)')
plt.ylabel('fraction of sites occupied')
plt.title('Time Evoluation of N with Cheater')
plt.legend(frameon=False)
plt.xlim(0, 500)
plt.ylim(0, 0.5)
plt.tight_layout()
plt.show()