"""Regular n-gon (n odd) in the COPS 'largest small polygon' OSiL model, checked at high precision.

Model (verified by parsing): variables r_1..r_n (x1..xn), theta_1..theta_n (x_{n+1}..x_{2n});
r_n fixed to 0 (vertex n at the origin), theta_n fixed to 3.14159265358979 (a decimal, not pi),
0 <= r_i <= 1, 0 <= theta_i <= 3.14159265358979, theta_i <= theta_{i+1},
r_i^2 + r_j^2 - 2 r_i r_j cos(theta_j - theta_i) <= 1 for all i<j,
min -1/2 sum_i r_i r_{i+1} sin(theta_{i+1} - theta_i).

Construction: V_k = c (w^k - 1), w = exp(2 pi i/n), |c| = 1/(2 cos(pi/(2n))), rotated so that
r_k = sin(k pi/n)/cos(pi/(2n)), theta_k = k pi/n  (k = 1..n-1); r_n = 0.
"""
import sys, mpmath
from osil_eval import Model, mp_backend

LISTED = {  # name: (primal, dual) from MINLPLib open.csv
    "polygon25": (-0.7797510481, -5.799714178),
    "polygon50": (-0.7838751084, -15.26768502),
    "polygon75": (-0.7844637573, -24.87363815),
    "polygon100": (-0.7850561376, -33.9989141),
}
OS = __import__("os").path.expanduser("~/.cache/minlplib/minlplib/osil/")


def reg_area(n):  # area of regular n-gon with diameter 1 (n odd)
    R = 1 / (2 * mpmath.cos(mpmath.pi / (2 * n)))
    return n / 2 * R ** 2 * mpmath.sin(2 * mpmath.pi / n)


def gap(p, d):  # MINLPLib convention (reproduces listed gaps)
    return abs(p - d) / min(abs(p), abs(d))


def main():
    B = mp_backend(60)
    for name, (p, d) in LISTED.items():
        M = Model(OS + name + ".osil")
        n = M.n // 2
        line = f"{name}: n={n}"
        m = n if n % 2 == 1 else n - 1  # regular m-gon, m odd; for even n one vertex is duplicated
        x = [None] * (2 * n)
        pts = [(mpmath.sin(k * mpmath.pi / m) / mpmath.cos(mpmath.pi / (2 * m)), k * mpmath.pi / m)
               for k in range(1, m)]
        if m < n:
            pts = [pts[0]] + pts  # duplicate vertex 1 (zero-length edge)
        for i, (r, t) in enumerate(pts):
            x[i], x[n + i] = r, t
        x[n - 1] = mpmath.mpf(0)
        x[2 * n - 1] = mpmath.mpf("3.14159265358979")
        v = M.check(x, B)
        obj = M.objective(x, B)
        acts = sorted(M.row_value(r, x, B) for r in range(M.m) if r in M.nl)
        line += (f"\n  regular {m}-gon{' (one vertex duplicated)' if m < n else ''}: objective = {mpmath.nstr(obj, 20)}"
                 f" (exact -area {mpmath.nstr(-reg_area(m), 20)})"
                 f"\n  max bound viol = {mpmath.nstr(v['bound'][0], 3)}, max row viol = {mpmath.nstr(v['row'][0], 3)} ({v['row'][1]})"
                 f"\n  largest distance^2 = {mpmath.nstr(acts[-1], 25)}, #rows with |d^2-1|<1e-40: {sum(abs(a-1)<mpmath.mpf('1e-40') for a in acts)}"
                 f"\n  listed primal {p}: our value is lower by {mpmath.nstr(p - obj, 8)}")
        if m == n:
            db = -reg_area(n)
            line += f"\n  Reinhardt: optimal value = {mpmath.nstr(db, 15)} (primal = dual)"
        else:
            db = -reg_area(n + 1)
            line += f"\n  n-gon is a degenerate (n+1)-gon -> dual bound -A_reg(n+1) = {mpmath.nstr(db, 15)}"
        p = obj
        iso = -mpmath.pi / 4
        line += (f"\n  isodiametric bound -pi/4 = {mpmath.nstr(iso, 15)}; listed gap {gap(LISTED[name][0], d):.4g}; with our primal:"
                 f" gap with -pi/4: {mpmath.nstr(gap(p, iso), 4)}; gap with best bound above: {mpmath.nstr(gap(p, db), 4)}")
        print(line)


if __name__ == "__main__":
    main()
