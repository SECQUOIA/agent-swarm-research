"""Reviewer's shared helpers: float data, reload map, equilibrium simulation, exact row evaluation."""
import numpy as np
from fractions import Fraction as F
from struct_nuc import analyze


class D:
    def __init__(self, name):
        S = analyze(name); self.S = S
        self.N, self.T = S.N, S.T
        self.G = np.array([[float(x) for x in r] for r in S.G])
        self.V = np.array([float(x) for x in S.V])
        cs = {x for r in S.c for x in r}; assert len(cs) == 1
        self.cF = cs.pop(); self.c = float(self.cF)
        self.a, self.KF = float(S.a), float(S.KF)
        self.ng = S.ntypes; self.fresh = S.fresh; self.pred = S.pred; self.age = S.age
        self.maxage = max(S.age.values())

    def reload(self, typ):
        """k_1 = KF f + R k_T for a complete F1 assignment typ[i] (type at node i)."""
        N = self.N; f = np.zeros(N); R = np.zeros((N, N))
        for i, g in enumerate(typ):
            if self.fresh[g]: f[i] = 1
            else:
                src = [j for j in range(N) if typ[j] == self.pred[g]]
                assert abs(sum(self.V[j] for j in src) - 1) < 1e-12
                for j in src: R[i, j] = self.V[j]
        return f, R

    def pattern_ok(self, typ):
        cnt = np.zeros(self.ng)
        for i, g in enumerate(typ): cnt[g] += self.V[i]
        return np.allclose(cnt, 1) and all(typ[i] == typ[j] for i, j in self.S.ties)


def perron_p(G, k, V):
    """Perron root of diag(k) G and its eigenvector p >= 0 normalized to V'p = 1 (power model)."""
    M = k[:, None] * G
    w, X = np.linalg.eig(M)
    m = np.argmax(w.real); p = np.abs(X[:, m].real); p /= V @ p
    return w[m].real, p


def cycle(d, k1):
    ks, ps, ls = [], [], []
    k = k1.copy()
    for t in range(d.T):
        lam, p = perron_p(d.G, k, d.V)
        ks.append(k); ps.append(p); ls.append(lam)
        k = k - d.a * p
    return ks, ps, ls


def equilibrium(d, typ, k1=None, tol=1e-13, maxit=2000):
    f, R = d.reload(typ)
    if k1 is None: k1 = np.full(d.N, d.KF)
    for it in range(maxit):
        ks, ps, ls = cycle(d, k1)
        new = d.KF * f + R @ ks[-1]
        if np.max(np.abs(new - k1)) < tol: k1 = new; break
        k1 = new
    ks, ps, ls = cycle(d, k1)
    res = np.max(np.abs(d.KF * f + R @ ks[-1] - k1))
    peak = max(p.max() for p in ps)
    return dict(lam=ls[-1], k1=k1, peak=peak, feasible=peak <= d.c, res=res, it=it, ks=ks, ps=ps, lams=ls)


def eval_rows_exact(S, x):
    """x: list of Fractions. Returns (max row violation, max bound violation, objective)."""
    worst = F(0); where = None
    for R in S.M["rows"]:
        v = sum(c * x[j] for j, c in R["lin"].items()) + sum(c * x[a] * x[b] for (a, b), c in R["quad"].items())
        viol = max(F(0), (R["lb"] - v) if R["lb"] is not None else F(0), (v - R["ub"]) if R["ub"] is not None else F(0))
        if viol > worst: worst, where = viol, R["name"]
    bw = F(0)
    for j, var in enumerate(S.M["vars"]):
        if var["lb"] is not None: bw = max(bw, var["lb"] - x[j])
        if var["ub"] is not None: bw = max(bw, x[j] - var["ub"])
        if var["type"] == "B": bw = max(bw, min(abs(x[j]), abs(x[j] - 1)))
    obj = sum(c * x[j] for j, c in S.M["obj"]["lin"].items())
    return worst, where, bw, obj


def typ_from_x(S, x):
    typ = []
    for i in range(S.N):
        gs = [g for g in range(S.ntypes) if x[S.y[i][g]] == 1]; assert len(gs) == 1; typ.append(gs[0])
    return typ
