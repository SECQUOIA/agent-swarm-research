"""Per-box constant in Theorem B (reviewer script).

For a box C with sides w, substitute y_i = l_i + w_i sin^2(theta_i).  Then
    int_C q_C^(-n/2) dy = 2^n int_{[0,pi/2]^n} prod(w_i s_i) / |w o s|^n dtheta,
with s_i = sin(2 theta_i).  AM-GM bounds the integrand by 2^n n^(-n/2), which
gives the scout's per-box bound pi^n n^(-n/2).  This script estimates the ratio
    L_n(w) = (int_C q_C^(-n/2)) / (pi^n n^(-n/2))  <= 1,
i.e. the loss of the AM-GM step, for cubes and elongated boxes.
"""
import numpy as np

rng = np.random.default_rng(1)


def ratio(w, samples=2_000_000):
    n = len(w)
    th = rng.uniform(0, np.pi / 2, size=(samples, n))
    x = np.asarray(w) * np.sin(2 * th)
    val = np.prod(x, axis=1) / (np.sum(x * x, axis=1) / n) ** (n / 2)
    return val.mean(), val.std() / np.sqrt(samples)


if __name__ == "__main__":
    print("cubes: n, L_n (mean +- s.e.), (2 sqrt2/pi)^n heuristic")
    for n in (1, 2, 3, 4, 6, 8, 12, 16):
        m, se = ratio([1.0] * n)
        print(f"  n={n:2d}  L_n={m:.4f} +- {se:.4f}   heuristic={(2*np.sqrt(2)/np.pi)**n:.4f}")
    print("2D boxes with aspect ratio rho (sides 1 x rho):")
    for rho in (1.0, 0.5, 0.2, 0.05, 0.01):
        m, se = ratio([1.0, rho])
        print(f"  rho={rho:5.2f}  L_2={m:.4f} +- {se:.4f}")
