"""Independent discrete check (example C; also B for the break times): explicit Euler transcription,
KKT point by enumeration (bang-bang with 0, 1 or 2 adjacent interior stages around the switch; all
KKT signs checked), then the discrete maximal recursion of Lemma 10 (own implementation).
Usage: python3 c_disc.py EX N1 N2 ..."""
import json
import sys

import numpy as np

from c_common import setup

b = np.array([0.0, 1.0])


def sim(P, N, u):
    h = 2.0 / N
    x1 = np.empty(N + 1); x2 = np.empty(N + 1)
    x1[0], x2[0] = 0.0, P["x20"]
    for t in range(N):
        x1[t + 1] = x1[t] + h * x2[t]
        x2[t + 1] = x2[t] + h * u[t]
    p1 = np.empty(N + 1); p2 = np.empty(N + 1)
    p1[N], p2[N] = -1.0, P["rho"] * x2[N]
    for t in range(N - 1, -1, -1):
        p1[t] = p1[t + 1] + h * (P["q"] * x1[t] + P["k1"] * u[t])
        p2[t] = p2[t + 1] + h * p1[t + 1] + h * (P["e"] - P["c"] * x2[t] + P["k2"] * u[t])
    sig = P["k1"] * x1[:N] + P["k2"] * x2[:N] + p2[1:]
    return x1, x2, sig


def kkt_viol(u, sig, free):
    v = 0.0
    for t in range(len(u)):
        if t in free:
            v = max(v, abs(sig[t]))
        elif u[t] > 0:
            v = max(v, sig[t])
        else:
            v = max(v, -sig[t])
    return v


def enumerate_kkt(P, N, tau):
    m0 = int(tau / (2.0 / N))
    found = []
    for m in range(m0 - 4, m0 + 5):
        # pure bang-bang, switch after stage m-1
        u = np.where(np.arange(N) < m, 1.0, -1.0)
        s = sim(P, N, u)[2]
        if kkt_viol(u, s, set()) <= 1e-13:
            found.append((u.copy(), set()))
        # one interior stage m
        base = np.where(np.arange(N) < m, 1.0, -1.0)
        ua, ub = base.copy(), base.copy()
        ua[m], ub[m] = -1.0, 1.0
        sa, sb = sim(P, N, ua)[2][m], sim(P, N, ub)[2][m]
        v = -1.0 + 2.0 * (0 - sa) / (sb - sa)
        if -1 < v < 1:
            u = base.copy(); u[m] = v
            s = sim(P, N, u)[2]
            if kkt_viol(u, s, {m}) <= 1e-12:
                found.append((u.copy(), {m}))
        # two adjacent interior stages m, m+1
        G = np.empty((2, 2)); u0 = base.copy(); u0[m] = 0.0; u0[m + 1] = 0.0
        s0 = sim(P, N, u0)[2][[m, m + 1]]
        for j, k in enumerate((m, m + 1)):
            uu = u0.copy(); uu[k] = 1.0
            G[:, j] = sim(P, N, uu)[2][[m, m + 1]] - s0
        vv = np.linalg.solve(G, -s0)
        if np.all(np.abs(vv) < 1):
            u = u0.copy(); u[m], u[m + 1] = vv
            s = sim(P, N, u)[2]
            if kkt_viol(u, s, {m, m + 1}) <= 1e-12:
                found.append((u.copy(), {m, m + 1}))
    return found


def rmax(P, N, x2N, sig, free, eps):
    h = 2.0 / N
    F = np.array([[1.0, h], [0.0, 1.0]])
    w = -np.array([P["k1"], P["k2"]])
    H = np.diag([P["q"], -P["c"]])
    X = np.diag([0.0, P["rho"]]) - 2 * eps * np.eye(2)
    mx = np.abs(X).max()
    ms = {}
    for t in range(N - 1, -1, -1):
        be = F.T @ X @ b - w
        kap = b @ X @ b
        m = kap + (0.0 if t in free else 2 * abs(sig[t]) / (h * 2.0))
        ms[t] = m
        if m <= 0:
            return dict(brk=t, maxP=mx, ms=ms)
        X = h * H + F.T @ X @ F - 2 * h * eps * np.eye(2) - np.outer(be, be) / m
        mx = max(mx, np.abs(X).max())
    return dict(brk=None, maxP=mx, ms=ms)


if __name__ == "__main__":
    name = sys.argv[1]
    d = setup(name)
    P, tau = d["P"], d["tau"]
    out = []
    for N in map(int, sys.argv[2:]):
        found = enumerate_kkt(P, N, tau)
        for u, free in found:
            x1, x2, sig = sim(P, N, u)
            for eps in (0.0, 0.02):
                r = rmax(P, N, x2[N], sig, free, eps)
                sw = int(np.argmax(u < 1.0))
                rec = dict(ex=name, N=N, nkkt=len(found), free=sorted(free), u_free=[float(u[k]) for k in sorted(free)],
                           switch_stage=sw, eps=eps, brk=r["brk"],
                           brk_time=None if r["brk"] is None else r["brk"] * 2.0 / N,
                           brk_after_switch=None if r["brk"] is None else (r["brk"] - sw),
                           maxP=float(r["maxP"]),
                           m_free=[float(r["ms"][k]) for k in sorted(free) if k in r["ms"]],
                           min_m_vertex=float(min(v for k, v in r["ms"].items() if k not in free)))
                print(rec, flush=True)
                out.append(rec)
    json.dump(out, open("logs/c_disc_%s.json" % name, "w"), indent=1)
