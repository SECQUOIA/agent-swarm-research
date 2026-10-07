"""Exact run of PROX (Algorithm alg:prox) on the instance of rem:falseguess.

F = x^2 + y^2 - 3xy + 63/128 (x+y) on [0,1]^2; L_i = 2.
Reports, for kappa_hat in {1,2,4} and stages 0..33, the set of minimizers of
Q_eta and the point returned with ties broken towards the current center.
Also checks the constants Delta, R, tau, J_kappa and the matrices of the remark.
"""
from fractions import Fraction as Fr
import math

def graded(lo, hi, c, h, th):
    nodes = {c}
    for sgn, R in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < R:
            t = min(t + h + th * t, R)
            nodes.add(c + sgn * t)
    return sorted(nodes)

def widths(G):
    w = {}
    for k, v in enumerate(G):
        cand = []
        if k > 0: cand.append(v - G[k - 1])
        if k + 1 < len(G): cand.append(G[k + 1] - v)
        w[v] = max(cand)
    return w

b = Fr(63, 128)
F = lambda x, y: x * x + y * y - 3 * x * y + b * (x + y)
L = Fr(2)
n = 2
ok = True
for kh in (1, 2, 4):
    mu = 2
    while Fr(kh, 4 ** mu) > Fr(1, 8):
        mu += 1
    th = Fr(1, 2 ** mu)
    eta = L * th * th / 4
    rho = 2 * math.ceil(math.sqrt(kh * n) - 1e-12)
    # exact ceil of sqrt(kh*n)
    r0 = math.isqrt(kh * n)
    rho = 2 * (r0 if r0 * r0 == kh * n else r0 + 1)
    c = (Fr(0), Fr(0))
    ties = []
    returned = []
    for j in range(34):
        h = Fr(1, 2 ** j)
        grids, ws = [], []
        for i in range(2):
            lo = max(Fr(0), c[i] - rho * h)
            hi = min(Fr(1), c[i] + rho * h)
            G = graded(lo, hi, c[i], h, th)
            grids.append(G); ws.append(widths(G))
        best, arg = None, []
        for x in grids[0]:
            for y in grids[1]:
                q = F(x, y) - L / 8 * (ws[0][x] ** 2 + ws[1][y] ** 2) + eta * ((x - c[0]) ** 2 + (y - c[1]) ** 2)
                if best is None or q < best:
                    best, arg = q, [(x, y)]
                elif q == best:
                    arg.append((x, y))
        if len(arg) > 1:
            ties.append((j, arg))
        nxt = c if c in arg else arg[0]
        returned.append(nxt)
        c = nxt
    allorigin = all(p == (0, 0) for p in returned)
    print("kappa_hat=%d mu=%d theta=%s rho=%d: origin at all stages 0..33: %s; ties: %s"
          % (kh, mu, th, rho, allorigin, [(j, [(str(p[0]), str(p[1])) for p in a]) for j, a in ties]))
    ok = ok and allorigin

# constants
Delta = 128
Hhat11 = Delta * 2
R = Delta * Hhat11 * Hhat11
tau = Fr(1, 4 * n * R)
print("R = 2^%d, tau = %s" % (R.bit_length() - 1, tau))
for kh in (1, 2, 4):
    J = 0
    while 4 ** J * tau ** 2 < 4 * kh * n:
        J += 1
    print("J_kappa(%d) = %d" % (kh, J))
lam0 = 2 * b
M0 = [[2 + lam0, -3], [-3, 2 + lam0]]
print("origin: H+Lambda diag", M0[0][0], "min eig", M0[0][0] - 3)
g11 = 2 - 3 + b
lam1 = 2 * abs(g11)
print("(1,1): grad", g11, "diag", 2 + lam1, "min eig", 2 + lam1 - 3)
print("OPT", F(Fr(1), Fr(1)), " g_S bound", (F(0, 0) - F(1, 1)) / 2)
print("ALL PASS" if ok else "SOME FAIL")
