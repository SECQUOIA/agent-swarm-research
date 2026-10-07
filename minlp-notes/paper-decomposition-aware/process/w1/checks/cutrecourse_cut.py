"""Exact checks of the signed endpoint / minimum-cut residual oracle.

For random rational instances of
    F(x) = c + sum_i (a_i x_i^2 + b_i x_i) + sum_{i<j} c_ij x_i x_j
with residual a_i <= 0 and c_ij o_i o_j <= 0 on residual edges, we check:
  * the cut identity  F = K + sum min(0,rho_i) + cut(y)  for every label y;
  * an exact Edmonds-Karp max flow equals the brute-force endpoint minimum,
    and its flow is a valid certificate (capacity, conservation, value=cut);
  * endpoint lemma: no point of a fine residual grid (or of the integer
    residual domain) beats the endpoint minimum.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from collections import deque

def rnd(rng, lo=-4, hi=4, den=(1, 2, 3, 4, 5)):
    return Fr(rng.randint(lo * 6, hi * 6), rng.choice(den))

def make_instance(rng, k, r):
    n = k + r
    a = [rnd(rng) for _ in range(n)]
    for i in range(k, n):
        a[i] = -abs(a[i]) if rng.random() < 0.8 else Fr(0)
    b = [rnd(rng) for _ in range(n)]
    o = [rng.choice((-1, 1)) for _ in range(n)]
    c = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.7:
                v = rnd(rng)
                if i >= k and j >= k:  # residual edge: enforce c_ij o_i o_j <= 0
                    v = -abs(v) * o[i] * o[j]
                c[(i, j)] = v
    lo, hi, integer = [], [], []
    for i in range(n):
        if i < k:
            lo.append(Fr(0)); hi.append(Fr(1)); integer.append(False)
        else:
            isint = rng.random() < 0.3
            l = rnd(rng, -2, 1); u = l + abs(rnd(rng, 0, 3))
            if isint:
                import math
                l2, u2 = Fr(math.ceil(l)), Fr(math.floor(u))
                if l2 > u2:
                    l2 = u2 = Fr(math.floor(u))
                l, u = l2, u2
            lo.append(l); hi.append(u); integer.append(isint)
    return dict(n=n, k=k, a=a, b=b, c=c, o=o, lo=lo, hi=hi, integer=integer, c0=rnd(rng))

def F(inst, x):
    v = inst["c0"]
    for i in range(inst["n"]):
        v += inst["a"][i] * x[i] ** 2 + inst["b"][i] * x[i]
    for (i, j), cij in inst["c"].items():
        v += cij * x[i] * x[j]
    return v

def energy(inst, core):
    """Return (K, mu, omega, alpha, d) for the binary energy at core point."""
    k, n = inst["k"], inst["n"]
    R = list(range(k, n))
    alpha = {i: (inst["lo"][i] if inst["o"][i] == 1 else inst["hi"][i]) for i in R}
    d = {i: inst["o"][i] * (inst["hi"][i] - inst["lo"][i]) for i in R}
    # evaluate F at y = 0, y = e_i, y = e_i + e_j to read off coefficients exactly
    def xval(y):
        x = list(core) + [alpha[i] + d[i] * y.get(i, 0) for i in R]
        return F(inst, x)
    K = xval({})
    mu = {i: xval({i: 1}) - K for i in R}
    omega = {}
    for p, i in enumerate(R):
        for j in R[p + 1:]:
            w = xval({i: 1, j: 1}) - K - mu[i] - mu[j]
            if w != 0:
                omega[(i, j)] = w
    return K, mu, omega, alpha, d

def maxflow(nodes, cap, s, t):
    flow = {e: Fr(0) for e in cap}
    adj = {u: [] for u in nodes}
    for (u, v) in cap:
        adj[u].append(v); adj[v].append(u)
    def res(u, v):
        return cap.get((u, v), Fr(0)) - flow.get((u, v), Fr(0)) + flow.get((v, u), Fr(0))
    while True:
        par = {s: None}; q = deque([s])
        while q and t not in par:
            u = q.popleft()
            for v in adj[u]:
                if v not in par and res(u, v) > 0:
                    par[v] = u; q.append(v)
        if t not in par:
            return flow, set(par)
        path = []; v = t
        while par[v] is not None:
            path.append((par[v], v)); v = par[v]
        aug = min(res(u, v) for u, v in path)
        for u, v in path:
            back = flow.get((v, u), Fr(0))
            use = min(back, aug)
            if use > 0:
                flow[(v, u)] = back - use
            if aug - use > 0:
                flow[(u, v)] = flow.get((u, v), Fr(0)) + aug - use

def solve(inst, core):
    K, mu, omega, alpha, d = energy(inst, core)
    R = list(range(inst["k"], inst["n"]))
    rho = {i: mu[i] + sum(w / 2 for (p, q), w in omega.items() if i in (p, q)) for i in R}
    cap = {}
    for i in R:
        if rho[i] > 0: cap[(i, "t")] = rho[i]
        if rho[i] < 0: cap[("s", i)] = -rho[i]
    for (i, j), w in omega.items():
        assert w <= 0
        cap[(i, j)] = -w / 2; cap[(j, i)] = -w / 2
    nodes = ["s", "t"] + R
    flow, S = maxflow(nodes, cap, "s", "t")
    y = {i: (1 if i in S else 0) for i in R}
    def cutval(y):
        side = lambda u: 1 if u == "s" else (0 if u == "t" else y[u])
        return sum(cv for (u, v), cv in cap.items() if side(u) == 1 and side(v) == 0)
    const = K + sum(min(Fr(0), rho[i]) for i in R)
    # flow certificate checks
    for e, f in flow.items():
        assert 0 <= f <= cap[e]
    for u in R:
        assert sum(f for (p, q), f in flow.items() if q == u) == sum(f for (p, q), f in flow.items() if p == u)
    value = sum(f for (p, q), f in flow.items() if p == "s") - sum(f for (p, q), f in flow.items() if q == "s")
    assert value == cutval(y)
    return y, const, cutval, alpha, d, R

def check(rng, trials=150):
    cnt = 0
    for _ in range(trials):
        k = rng.randint(0, 2); r = rng.randint(0, 5)
        inst = make_instance(rng, k, r)
        core = [Fr(rng.randint(0, 8), 8) for _ in range(k)]
        y, const, cutval, alpha, d, R = solve(inst, core)
        # identity for every label, and brute-force endpoint minimum
        best = None
        for bits in product((0, 1), repeat=len(R)):
            yy = dict(zip(R, bits))
            x = list(core) + [alpha[i] + d[i] * yy[i] for i in R]
            val = F(inst, x)
            assert val == const + cutval(yy)
            best = val if best is None else min(best, val)
        xopt = list(core) + [alpha[i] + d[i] * y[i] for i in R]
        assert F(inst, xopt) == best
        # endpoint lemma against a grid of the residual box / integer domain
        pts = []
        for i in R:
            lo, hi = inst["lo"][i], inst["hi"][i]
            if inst["integer"][i]:
                pts.append([Fr(z) for z in range(int(lo), int(hi) + 1)])
            else:
                pts.append([lo + (hi - lo) * Fr(t, 4) for t in range(5)])
        for z in product(*pts):
            assert F(inst, list(core) + list(z)) >= best
        cnt += 1
    return cnt

if __name__ == "__main__":
    rng = random.Random(20261003)
    n = check(rng)
    print("cut oracle: %d random instances passed (identity, max-flow = endpoint min, flow certificate, endpoint lemma)" % n)
