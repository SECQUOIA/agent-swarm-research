"""The chiral chain (Part B of robust-chains.md).

  f_n(x) = sum_i a x_i^2 + b sum_i x_i x_{i+1} + (g/2) sum_i (x_i x_{i+1}^2 - x_i^2 x_{i+1}),   a = b + ev,
  on [-1,1]^n.  Balanced base split: bond W(x,y) = (a/2)(x^2+y^2) + b x y + (g/2)(x y^2 - x^2 y), plus
  (a/2) x_1^2 and (a/2) x_n^2 in the end factors.

Commands:
  python3 chiral.py certificate            symbolic check of the cubic sub-action identity (sympy)
  python3 chiral.py bulk B G EV [M]        per-bond bulk LP gaps g_inf(S) for S = P_1, ..., P_max(4,2M+2) and the
                                           holonomic LP (marginals equal), grid of 201 points; two-point fooling
                                           (M: chirality (g/2)(x y^{2M} - x^{2M} y), default 1)
  python3 chiral.py roots B G EV n1 n2 ..  root gaps of the n-chain for classes P_1..P_3 (column generation)
  python3 chiral.py dp B G EV n1 n2 ..     f*_n by grid DP + L-BFGS-B (checks x* = 0)
Floating point except 'certificate'.
"""
import sys
import json
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import linprog, minimize
from scipy import sparse
from polychain import PolyChain, RelaxPoly, poly_class, bivar


def chain(n, b, g, ev, m=1):
    """chirality (g/2)(x y^{2m} - x^{2m} y); m = 1 is the cubic chain of the note."""
    a = b + ev
    W = bivar({(2, 0): a / 2, (0, 2): a / 2, (1, 1): b, (1, 2 * m): g / 2, (2 * m, 1): -g / 2})
    return PolyChain(n, W, [0, 0, a / 2], [0, 0, a / 2])


def Wfun(b, g, ev, m=1):
    a = b + ev
    return lambda x, y: 0.5 * a * (x * x + y * y) + b * x * y + 0.5 * g * (x * y ** (2 * m) - x ** (2 * m) * y)


def certificate():
    import sympy as sp
    x, y, a, b, g, ev = sp.symbols("x y a b g ev", real=True)
    for m in (1, 2, 3):
        W = sp.Rational(1, 2) * (b + ev) * (x**2 + y**2) + b * x * y + g / 2 * (x * y**(2 * m) - x**(2 * m) * y)
        h = lambda t: -g / 2 * t**(2 * m + 1)
        lhs = sp.expand(W + h(x) - h(y))
        S = sum(x**(2 * j) * y**(2 * (m - 1 - j)) for j in range(m))
        rhs = sp.expand((x + y)**2 * (b / 2 + g / 2 * (y - x) * S) + ev / 2 * (x**2 + y**2))
        print(f"m={m}: W + h(x) - h(y) - [(x+y)^2 (b/2 + g/2 (y-x) S_m) + ev/2 (x^2+y^2)] =", sp.simplify(lhs - rhs))
    W = sp.Rational(1, 2) * (b + ev) * (x**2 + y**2) + b * x * y + g / 2 * (x * y**2 - x**2 * y)
    h = lambda t: -g / 2 * t**3
    # ends: (a/2) t^2 -/+ h(t) >= (a - |g|)/2 t^2 on [-1,1]
    t = sp.symbols("t", real=True)
    print("end terms: (b+ev)/2 t^2 - h(t) =", sp.factor((b + ev) / 2 * t**2 - h(t)), ";  (b+ev)/2 t^2 + h(t) =", sp.factor((b + ev) / 2 * t**2 + h(t)))
    # two-point antiferro fooling value per bond
    p = sp.symbols("p", real=True)
    print("W(p,-p) =", sp.factor(W.subs({x: p, y: -p})))


def bulk(b, g, ev, N=201, m=1, dmax=4):
    Wf = Wfun(b, g, ev, m)
    G = np.linspace(-1, 1, N)
    X, Y = np.meshgrid(G, G, indexing="ij")
    cost = Wf(X, Y).ravel()
    out = {}
    for name, d in [(f"P{k}", k) for k in range(1, dmax + 1)] + [("holonomic", None)]:
        if d is None:
            # x-marginal = y-marginal: for each grid point k, sum_j nu[k, j] - sum_i nu[i, k] = 0
            rows = []
            I, J, V = [], [], []
            idx = np.arange(N * N).reshape(N, N)
            for k in range(N):
                I += [k] * N; J += list(idx[k, :]); V += [1.0] * N
                I += [k] * N; J += list(idx[:, k]); V += [-1.0] * N
            A = sparse.csr_matrix((V, (I, J)), shape=(N, N * N))
            A = sparse.vstack([A, sparse.csr_matrix(np.ones((1, N * N)))])
            beq = np.zeros(N + 1); beq[-1] = 1
        else:
            rowsA = [np.ones(N * N)]
            for k in range(1, d + 1):
                rowsA.append((X ** k - Y ** k).ravel())
            A = np.array(rowsA); beq = np.zeros(d + 1); beq[0] = 1
        res = linprog(cost, A_eq=A, b_eq=beq, bounds=(0, None), method="highs")
        nu = res.x.reshape(N, N)
        supp = np.argwhere(nu > 1e-9)
        out[name] = res.fun
        print(f"  {name:10s} per-bond LP value {res.fun:+.6f}; support {[(round(G[i],3), round(G[j],3), round(nu[i,j],4)) for i, j in supp[:8]]}", flush=True)
    # two-point antiferro fooling: p in {-1, q}, E p = 0
    qs = np.linspace(1e-3, 1, 1000)
    # law of p: mass q/(1+q) at -1 and 1/(1+q) at q (mean 0); W(p,-p) = ev p^2 + g p^(2m+1)
    v = (qs * (ev - g) + (ev * qs ** 2 + g * qs ** (2 * m + 1))) / (1 + qs)
    k = int(np.argmin(v))
    print(f"  two-point fooling p in {{-1, q}}: best q = {qs[k]:.3f}, value per bond {v[k]:+.6f}")
    return out


def dp(b, g, ev, n, N=801):
    Wf = Wfun(b, g, ev); a = b + ev
    G = np.linspace(-1, 1, N)
    M = Wf(G[:, None], G[None, :])
    V = 0.5 * a * G * G; back = []
    for _ in range(1, n):
        T = V[:, None] + M
        j = np.argmin(T, axis=0); back.append(j)
        V = T[j, np.arange(N)]
    V = V + 0.5 * a * G * G
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = G[np.array(path[::-1])]
    ch = chain(n, b, g, ev)
    r = minimize(ch.f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-12})
    # second-best: best grid-DP value among paths with |x|_inf >= 0.2 is not computed; report grid min
    return min(r.fun, ch.f(x0)), r.x, float(V[k])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "certificate":
        certificate()
    elif cmd == "bulk":
        b, g, ev = map(float, sys.argv[2:5])
        m = int(sys.argv[5]) if len(sys.argv) > 5 else 1
        print(f"bulk b={b} g={g} ev={ev} chirality degree {2*m+1}")
        bulk(b, g, ev, m=m, dmax=max(4, 2 * m + 2))
    elif cmd == "dp":
        b, g, ev = map(float, sys.argv[2:5])
        for n in map(int, sys.argv[5:]):
            fs, xs, vg = dp(b, g, ev, n)
            print(f"dp b={b} g={g} ev={ev} n={n} f*={fs:.3e} grid={vg:.3e} |x*|_inf={np.max(np.abs(xs)):.2e}", flush=True)
    elif cmd == "roots":
        b, g, ev = map(float, sys.argv[2:5])
        for n in map(int, sys.argv[5:]):
            res = {}
            for d in (1, 2, 3):
                rel = RelaxPoly(chain(n, b, g, ev), poly_class(d), K=7)
                lo, up, it = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=150, tol=1e-9)
                res[f"P{d}"] = (round(-up, 6), round(-lo, 6))
            print(json.dumps(dict(b=b, g=g, ev=ev, n=n, gap_range=res)), flush=True)
