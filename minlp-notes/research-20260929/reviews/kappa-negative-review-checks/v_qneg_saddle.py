"""Search for KKT points of the q<0 toy (k=3, phi2=-2) at N=1000 with two fractional stages (exact)."""
import json
from fractions import Fraction as Fr
from vtoy import Toy, traj, H_entry, kkt_check
N = 1000
toy = Toy(a_pts=((0, 2), (1, -1)), k_pts=((0, 3),), phi1=1, phi2=-2, R=3)
fstar = Fr(118134616, 10**8)
h = Fr(2, N)
_, k = toy.data(N)
out = []
for i in range(270, 290):
    for gap in (1, 2, 3):
        j = i + gap
        u = [Fr(1)] * i + [Fr(0)] * (j - i + 1) + [Fr(-1)] * (N - j - 1)
        for t in range(i + 1, j):
            u[t] = Fr(0)  # placeholder, fixed below to -1 or +1 patterns
        for mid in ([Fr(1)] * (gap - 1), [Fr(-1)] * (gap - 1)):
            uu = list(u)
            for q, t in enumerate(range(i + 1, j)):
                uu[t] = mid[q]
            uu[i] = uu[j] = Fr(0)
            E0 = traj(toy, N, uu)
            a11, a12, a22 = H_entry(toy, N, k, i, i), H_entry(toy, N, k, i, j), H_entry(toy, N, k, j, j)
            b1, b2 = -h * E0["sig"][i], -h * E0["sig"][j]
            det = a11 * a22 - a12 * a12
            vi, vj = (b1 * a22 - a12 * b2) / det, (a11 * b2 - a12 * b1) / det
            if -1 < vi < 1 and -1 < vj < 1:
                uu[i], uu[j] = vi, vj
                E = traj(toy, N, uu)
                ok, frac = kkt_check(E)
                if ok:
                    out.append(dict(i=i, j=j, ui=float(vi), uj=float(vj), J_minus_fstar_h2=float((E["J"] - fstar) / h**2),
                                    detH=float(det / h**4)))
print(json.dumps(out))
