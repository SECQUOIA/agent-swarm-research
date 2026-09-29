"""Independent recheck of Proposition 4.4(c): the connected spiral.

c(t) = rho(t) (cos t, sin t), rho(t) = r (1 + 1/(1+t)), t in (0, inf), B = [-2r, 2r]^2.
Checks: curvature bound 10/r (and the actual sup), injectivity via strictly decreasing rho,
gap between consecutive turns (reach 0), q_B <= 8 r^2 on the curve, and the
integral of q_B^(-1/2) over t in (0, T] for T = 10, 100, 1000 (note: 4.98, 40.0, 381).
"""
import numpy as np
from scipy.integrate import quad

for r in [1.0, 0.3]:
    rho = lambda t: r * (1 + 1 / (1 + t))
    rp = lambda t: -r / (1 + t) ** 2
    rpp = lambda t: 2 * r / (1 + t) ** 3
    t = np.concatenate([np.linspace(1e-9, 50, 2_000_001)[:-1], np.geomspace(50, 1e6, 200_001)])
    R, R1, R2 = rho(t), rp(t), rpp(t)
    kappa = np.abs(R**2 + 2 * R1**2 - R * R2) / (R**2 + R1**2) ** 1.5
    print(f"r={r}: sup curvature * r = {np.max(kappa) * r:.6f} (note bound: 10); "
          f"rho range ({R.min()/r:.6f} r, {R.max()/r:.6f} r); strictly decreasing: {bool(np.all(np.diff(R) < 0))}")
    x, y = R * np.cos(t), R * np.sin(t)
    q = (x + 2 * r) * (2 * r - x) + (y + 2 * r) * (2 * r - y)
    print(f"   q_B on curve in [{q.min()/r**2:.4f} r^2, {q.max()/r**2:.4f} r^2] (note: <= 8 r^2); inside B: "
          f"{bool(np.all(np.abs(x) < 2*r) and np.all(np.abs(y) < 2*r))}")
    for T in [10, 100, 1000]:
        gap = rho(T) - rho(T + 2 * np.pi)
        print(f"   radial gap between turns at t={T}: {gap/r:.3e} r  (-> 0, so reach 0)")

r = 1.0
rho = lambda t: r * (1 + 1 / (1 + t))
rp = lambda t: -r / (1 + t) ** 2


def integrand(t):
    R = rho(t)
    speed = np.sqrt(R * R + rp(t) ** 2)
    q = 8 * r * r - R * R  # q_B = 8 r^2 - |c|^2 on B = [-2r,2r]^2
    return speed / np.sqrt(q)


print("\nintegral of q_B^(-1/2) ds over t in (0,T], r = 1 (note: 4.98, 40.0, 381)")
for T in [10, 100, 1000, 10000]:
    val, err = quad(integrand, 0, T, limit=2000)
    print(f"   T={T:6d}: {val:.4f}  (lower bound length/(2 sqrt 2 r) = {quad(lambda s: np.sqrt(rho(s)**2+rp(s)**2), 0, T, limit=2000)[0]/(2*np.sqrt(2)):.4f})")
print("   asymptotic slope 1/sqrt(7) =", 1 / np.sqrt(7))
