"""M-limits checks: Prop lim:prop:messages (parts 2,3,4), Prop lim:prop:setgrowth (a),(b),(c)
and the n=2 certificate example, Prop prop:oraclebarrier (derivatives, counting)."""
from fractions import Fraction as Fr
from itertools import product
import random
import math
import sympy as sp

random.seed(11)
ok = True


def check(c, msg):
    global ok
    if not c:
        ok = False
        print("FAIL:", msg)


# ---------------- messages ----------------
for m in range(2, 8):
    def Psi(xi, z):
        xx = [Fr(0)] + xi
        rho = [xx[t] - 2 * xx[t - 1] - z[t - 1] for t in range(1, m + 1)]
        return xi[-1] ** 2 + sum(r * r for r in rho) + Fr(1, 8) * sum(t * (1 - t) for t in z)

    for _ in range(400):
        mode = random.random()
        if mode < 0.5:
            xi = [Fr(random.randint(0, (2 ** t - 1) * 50), 50) for t in range(1, m + 1)]
            z = [Fr(random.randint(0, 50), 50) for _ in range(m)]
        else:  # near the chain (rho ~ 0)
            z = [Fr(random.randint(0, 50), 50) for _ in range(m)]
            xi = []
            prev = Fr(0)
            for t in range(m):
                v = 2 * prev + z[t] + Fr(random.randint(-3, 3), 100)
                v = min(max(v, Fr(0)), Fr(2 ** (t + 1) - 1))
                xi.append(v)
                prev = v
        check(Psi(xi, z) >= Fr(1, 8) * (sum(t * t for t in xi) + sum(t * t for t in z)),
              f"messages growth m={m}")
    # zero set of V_0 at integers: binary digits give a zero
    for j in range(2 ** m):
        z = [Fr((j >> (m - t)) & 1) for t in range(1, m + 1)]
        xi = [Fr(j >> (m - t)) for t in range(1, m + 1)]
        check(all(0 <= xi[t - 1] <= 2 ** t - 1 for t in range(1, m + 1)), "digit states in box")
        check(Psi(xi, z) - xi[-1] ** 2 == 0 and xi[-1] == j, "V0(j)=0")

m = 4
xi = sp.symbols('xi1:5')
zz = sp.symbols('z1:5')
xx = [0] + list(xi)
Ps = xi[-1] ** 2 + sum((xx[t] - 2 * xx[t - 1] - zz[t - 1]) ** 2 for t in range(1, m + 1)) \
    + sp.Rational(1, 8) * sum(t * (1 - t) for t in zz)
diag = [sp.diff(Ps, v, 2) for v in list(xi) + list(zz)]
check(diag == [10, 10, 10, 4, sp.Rational(7, 4)] + [sp.Rational(7, 4)] * 3, f"diag {diag}")
H = sp.hessian(Ps, list(xi) + list(zz))
ev = [complex(e).real for e in sp.Matrix(H).evalf().eigenvals().keys()]
check(min(ev) >= -0.25 - 1e-12, "Hessian >= -1/4 I")
print("messages: min eigenvalue (m=4) =", min(ev))

# ---------------- set growth ----------------
def Lsmall(n):
    return [2] + [4] * (n - 2) + [2] if n >= 3 else [2, 2]


def minmarginals(G, L, n):
    def w(i, v):
        Gi = G[i]
        k = Gi.index(v)
        ws = []
        if k > 0:
            ws.append(Gi[k] - Gi[k - 1])
        if k < len(Gi) - 1:
            ws.append(Gi[k + 1] - Gi[k])
        return max(ws)

    def Q(y):
        return sum((y[i] - y[i + 1]) ** 2 for i in range(n - 1)) - sum(
            Fr(L[i], 8) * w(i, y[i]) ** 2 for i in range(n))

    mm = [dict() for _ in range(n)]
    beta = None
    for y in product(*G):
        q = Q(y)
        beta = q if beta is None or q < beta else beta
        for i in range(n):
            if y[i] not in mm[i] or q < mm[i][y[i]]:
                mm[i][y[i]] = q
    return mm, beta, w


for _ in range(150):
    n = random.randint(2, 4)
    G = []
    for i in range(n):
        k = random.randint(0, 4 if n < 4 else 3)
        pts = sorted(set([Fr(0), Fr(1)] + [Fr(random.randint(1, 99), 100) for _ in range(k)]))
        G.append(pts)
    L = [Li + random.choice([0, 0, 1, Fr(1, 2)]) for Li in Lsmall(n)]
    mm, beta, w = minmarginals(G, L, n)
    for j in range(n):
        for v in G[j]:
            check(mm[j][v] <= -Fr(1, 8) * L[j] * w(j, v) ** 2, "(a) min-marginal bound")
        # (b) every interval retained at U = 0
        for a, b in zip(G[j], G[j][1:]):
            check(min(mm[j][a], mm[j][b]) <= 0, "(b) interval removed at U=0")
        Wj = max(b - a for a, b in zip(G[j], G[j][1:]))
        check(beta <= -Fr(1, 8) * L[j] * Wj ** 2, "(a) beta bound")

# example: n=2, eps=1/50
G0 = [[Fr(k, 5) for k in range(6)]] * 2
mm0, beta0, w0 = minmarginals(G0, [2, 2], 2)
check(all(mm0[i][v] == Fr(-1, 50) for i in range(2) for v in G0[i]), "example stage-0 mm")
G1 = [[Fr(0), Fr(1, 5)]] * 2
mm1, beta1, w1 = minmarginals(G1, [2, 2], 2)
check(beta1 == Fr(-1, 50), "example stage-1 beta")
eps = Fr(1, 50)
check(0 - Fr(-1, 50) == eps, "example gap")
check(1 + 1 / (2 * math.sqrt(1 / 50)) > 4, "example needs >= 5 nodes")
check(Fr(1, 5) ** 2 <= 4 * eps, "removed intervals <= 2 sqrt(eps)")
# set-growth constant 2/(n(n-1)) at random points (dist to diagonal is exact formula)
for _ in range(500):
    n = random.randint(2, 6)
    x = [Fr(random.randint(0, 100), 100) for _ in range(n)]
    mean = sum(x) / n
    d2 = sum((t - mean) ** 2 for t in x)  # mean in [0,1], so projection is feasible
    F = sum((x[i] - x[i + 1]) ** 2 for i in range(n - 1))
    check(F >= Fr(2, n * (n - 1)) * d2, "set growth constant")
print("setgrowth: random grids and example checked")

# ---------------- oracle barrier ----------------
n = 2
x = sp.symbols('x1:3')
c = sp.symbols('c1:3')
wv = sp.Symbol('w', positive=True)
zz = [(x[i] - c[i]) / wv for i in range(n)]
rho = sum(t ** 2 for t in zz)
f = -wv ** 2 / 6 * (1 - rho) ** 3
for i in range(n):
    check(sp.simplify(sp.diff(f, x[i]) - wv * zz[i] * (1 - rho) ** 2) == 0, "grad formula")
    for j in range(n):
        dij = sp.diff(f, x[i], x[j])
        target = (1 if i == j else 0) * (1 - rho) ** 2 - 4 * zz[i] * zz[j] * (1 - rho)
        check(sp.simplify(dij - target) == 0, "Hessian formula")
r = sp.Symbol('r')
check(sp.expand(1 - (1 - r) ** 3 - r - r * (1 - r) * (2 - r)) == 0, "cubic identity")
# counting: Q < (1/(2 sqrt(6 eps)) - 1)^n - 1  =>  M < 1/(2 sqrt(6 eps)) and M^n > Q+1
for nn in range(1, 4):
    for eps in [1e-2, 1e-3, 1e-4, 3e-5]:
        B = (1 / (2 * math.sqrt(6 * eps)) - 1) ** nn - 1
        for Q in range(0, int(max(0, B)) + 1, max(1, int(B) // 50 + 1)):
            if Q < B:
                M = math.floor((Q + 1) ** (1 / nn) + 1e-12) + 1
                check(M ** nn > Q + 1 and M < 1 / (2 * math.sqrt(6 * eps)), "barrier counting")
print("ALL OK" if ok else "SOME FAILURES")
