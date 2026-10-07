"""KKT multipliers at a primal point with binaries fixed (least squares).

Stationarity of  f(x) + sum_i y_i g_i(x)  in the continuous variables, with
y_i free for equality rows and sign-constrained for active inequality rows
and active bounds.  Returns the multipliers of the link rows (lam[t][k]) and
of the horizon row (mu >= 0), in the sign convention of period.py:
    L = f + sum lam (x_b - x_a) + mu (c - sum h).
"""
import sys
import json

import numpy as np
from scipy.optimize import lsq_linear
from scipy.sparse import lil_matrix

import period
import evalpt


def grad_row(r, x):
    g = {}
    for mono, a in r["poly"].items():
        a = float(a)
        for p, v in enumerate(mono):
            term = a
            for q, w in enumerate(mono):
                if q != p:
                    term *= x[w]
            g[v] = g.get(v, 0.0) + term
    return g


def value_row(r, x):
    s = 0.0
    for mono, a in r["poly"].items():
        t = float(a)
        for v in mono:
            t *= x[v]
        s += t
    return s


def kkt(D, x, act_tol=1e-7):
    M, S = D["M"], D["S"]
    n = len(x)
    cont = [j for j in range(n) if M["vt"][j] != "B"]
    col = {j: k for k, j in enumerate(cont)}
    cols = []  # (kind, index, sign) ; sign: multiplier domain
    entries = []
    for i, r in enumerate(M["rows"]):
        val = value_row(r, x)
        lb, ub = r["lb"], r["ub"]
        eq = lb == ub
        if eq:
            dom = (-np.inf, np.inf)
        else:
            act_lo = lb.upper() != "-INF" and abs(val - float(lb)) <= act_tol
            act_up = ub.upper() not in ("INF", "+INF") and abs(val - float(ub)) <= act_tol
            if act_up:
                dom = (0.0, np.inf)   # + y g, y >= 0 for g <= ub
            elif act_lo:
                dom = (-np.inf, 0.0)  # + y g, y <= 0 for g >= lb
            else:
                continue
        cols.append(("row", i, dom))
        entries.append(grad_row(r, x))
    for j in cont:
        lb, ub = M["lb"][j], M["ub"][j]
        if lb == ub:
            dom = (-np.inf, np.inf)
        elif ub.upper() not in ("INF", "+INF") and abs(x[j] - float(ub)) <= act_tol:
            dom = (0.0, np.inf)
        elif lb.upper() != "-INF" and abs(x[j] - float(lb)) <= act_tol:
            dom = (-np.inf, 0.0)
        else:
            continue
        cols.append(("bnd", j, dom))
        entries.append({j: 1.0})
    A = lil_matrix((len(cont), len(cols)))
    for k, g in enumerate(entries):
        for v, a in g.items():
            if v in col:
                A[col[v], k] = a
    b = np.zeros(len(cont))
    for j, a in M["obj"].items():
        if j in col:
            b[col[j]] = -float(a)
    lo = np.array([c[2][0] for c in cols])
    hi = np.array([c[2][1] for c in cols])
    sol = lsq_linear(A.toarray(), b, bounds=(lo, hi), method="bvls", max_iter=100000, tol=1e-14)
    y = sol.x
    res = np.linalg.norm(A.tocsr() @ y - b, np.inf)
    ymap = {(c[0], c[1]): y[k] for k, c in enumerate(cols)}
    lam = []
    for t in range(D["T"] - 1):
        lam.append([float(ymap[("row", i)]) for (i, a, b_) in S["link"][t]])
    hrow = S["horizon"][0]
    yh = ymap.get(("row", hrow), 0.0)
    mu = -float(yh)  # row is sum h >= c: + y*sum h with y <= 0  ->  mu (c - sum h), mu = -y
    return lam, mu, res, sol.status


if __name__ == "__main__":
    T = int(sys.argv[1])
    D = period.setup(T)
    x, _ = evalpt.read_sol(sys.argv[2], D["M"]["names"])
    x = [float(v) for v in x]
    lam, mu, res, st = kkt(D, x)
    print("residual", res, "status", st)
    print("mu", mu)
    for t, l in enumerate(lam):
        print(t, l)
    json.dump(dict(lam=lam, mu=mu, residual=res), open(sys.argv[3], "w"), indent=1)
