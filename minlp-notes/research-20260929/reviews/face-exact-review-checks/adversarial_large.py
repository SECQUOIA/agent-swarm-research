"""Referee: largest valid boxes at n = 6, 8 (kappa = 0, c = 0, b = +0.8, R = X0 = [-1,1]^n, eps = 1e-4),
versus the exact Lemma 2.1 supremum nu and the Theorem 1 closed form.  Starts: alternating slabs
(x_i in [-1,1] for i odd, x_i near +1 for i even, and the shifted pattern), the two unfrustrated
orthants, and random points.  Uses the search of adversarial_boxes.py.
Usage: python3 adversarial_large.py
"""
import math
import numpy as np
from multiprocessing import Pool
from adversarial_boxes import Inst, search, nu_exact, D


def main():
    rng = np.random.default_rng(11)
    jobs, meta = [], []
    for n in (6, 8):
        I = Inst(n, [0.8] * (n - 1), 0.0, np.zeros(n), 1e-4, 1.0, "A")
        S = []
        for off in (0, 1):
            for a in (0.2, 0.3, 0.4):
                l = np.array([-1.0 if (i + off) % 2 == 0 else a for i in range(n)])
                u = np.ones(n)
                S.append((l * 0 + np.where(l > -1, 0.999, -1e-6), u * 0 + np.where(l > -1, 1.0, 1e-6)))
        for sgn in (1, -1):
            S.append((np.where(sgn > 0, 0.0, -1e-3) * np.ones(n), np.where(sgn > 0, 1e-3, 0.0) * np.ones(n)))
        while len(S) < 40:
            z = rng.uniform(-1, 1, n) * rng.choice([0.2, 0.6, 1.0]); S.append((z - 1e-6, z + 1e-6))
        for st in S:
            if I.valid(*st):
                jobs.append((I, st, int(rng.integers(1 << 30)), 80)); meta.append(I)
    with Pool(34) as pool:
        res = pool.map(search, jobs, chunksize=1)
    rho = D / 1.6; Sg = math.sqrt(1 + rho); th = Sg / (1 + Sg); lam = (1 + Sg) / (2 * Sg * Sg)
    for n in (6, 8):
        rr = [x for I, x in zip(meta, res) if I.n == n]
        I = [I for I in meta if I.n == n][0]
        best = max(rr, key=lambda x: x[0])
        nu = nu_exact(I)
        cf = n * math.log(th) + lam * (1 + 1e-4 / 0.8)
        print(f"n={n}: best valid box fraction^(1/n) = {math.exp(best[0]/n):.4f} (1/fraction = {math.exp(-best[0]):.1f}); "
              f"exact Lemma 2.1 nu^(1/n) = {math.exp(nu/n):.4f} (1/nu = {math.exp(-nu):.1f}); closed form^(1/n) = "
              f"{math.exp(cf/n):.4f} (Thm 1 = {math.exp(-cf):.1f}); max center slack {max(x[3] for x in rr):.3e}; "
              f"min LB-f* {min(x[4] for x in rr):.2e}")
        print(f"   best box l={np.round(best[1], 3)} u={np.round(best[2], 3)}")
    # exact nu for larger n (Lemma 2.1 before the Lemma 3.1 relaxation)
    for n in (12, 16, 24):
        I = Inst.__new__(Inst); I.n, I.b, I.r, I.eps = n, np.full(n - 1, 0.8), 1.0, 1e-4
        nu = nu_exact(I)
        cf = n * math.log(th) + lam * (1 + 1e-4 / 0.8)
        print(f"n={n}: exact Lemma 2.1 nu^(1/n) = {math.exp(nu/n):.4f} (1/nu = {math.exp(-nu):.1f}) vs closed form (Thm 1 = {math.exp(-cf):.1f})")


if __name__ == "__main__":
    main()
