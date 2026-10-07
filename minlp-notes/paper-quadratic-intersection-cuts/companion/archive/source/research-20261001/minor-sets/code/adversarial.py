"""Adversarial search: minimize z_orbit / z_K over full-dimensional tangent-edge minor corners
(note, Section 7.3).  w = 1, four rays, theta = (a0, b0, X, log alpha, log beta, sbar, v3, v4):
  t* = a0 b0^T,  D = X projected onto the tangent hyperplane at t*,  v1 = t* + alpha D,
  v2 = t* - beta D,  rays p_j = v_j - sbar.
Valid iff z_K = 1 with minimizer support {1, 2} and the non-degeneracy margins (all invariant under
the automorphisms M -> A M B^T of det, so the search measures intrinsic geometry) are >= MARGIN:
  ray non-grazing:   |B(sbar,p)^2 - det(sbar) det(p)| / (B^2 + |det sbar det p|)   for every ray;
  strict complementarity: KKT multipliers nu_3, nu_4 (w = 1);
  second order along the edge: det(d) det(sbar) / (B(d,sbar)^2 + det(d) det(sbar)), d = v1 - v2;
  apex away from the null cone relative to the rays: det(sbar) / max_j (|det p_j| + |B(sbar,p_j)|).
Starting points: the corners found by search_cex.py (logs/search_cex_*.log), plus random restarts.
Usage: python3 adversarial.py SEED NSTARTS MARGIN OUT.jsonl
"""
import sys
import json
import glob
import numpy as np
from scipy.optimize import minimize
from minor_core import zK, FamilySolver, precondition, det4

seed, NS, MARGIN, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
rng = np.random.default_rng(seed)


def polar_form(s, t):
    return 0.5 * (s[0] * t[3] + s[3] * t[0] - s[1] * t[2] - s[2] * t[1])


def build(th):
    a0, b0, X = th[0:2], th[2:4], th[4:8]
    al, be = np.exp(th[8]), np.exp(th[9])
    sb, v3, v4 = th[10:14], th[14:18], th[18:22]
    t0 = np.array([a0[0] * b0[0], a0[0] * b0[1], a0[1] * b0[0], a0[1] * b0[1]])
    g = np.array([t0[3], -t0[2], -t0[1], t0[0]])
    D = X - (g @ X) / (g @ g) * g
    v1, v2 = t0 + al * D, t0 - be * D
    return sb, [v1, v2, v3, v4], t0, D


def margins(sb, V, t0):
    P = [v - sb for v in V]
    ds = det4(sb)
    m = []
    for p in P:
        B = polar_form(sb, p); dp = det4(p)
        m.append(abs(B * B - ds * dp) / (B * B + abs(ds * dp)))
    g = np.array([t0[3], -t0[2], -t0[1], t0[0]])
    gp = [g @ p for p in P]
    sig = -1.0 / gp[0]
    nu = [1 + sig * x for x in gp]
    m += [nu[2], nu[3]]
    d = V[0] - V[1]
    dd = det4(d); Bd = polar_form(d, sb)
    m.append(dd * ds / (Bd * Bd + dd * ds) if dd > 0 else -1.0)
    m.append(ds / max(abs(det4(p)) + abs(polar_form(sb, p)) for p in P))
    return m


def ratio(th, iters=14, full=False):
    sb, V, t0, D = build(th)
    if det4(sb) <= 0 or not np.all(np.isfinite(th)):
        return 2.0
    P = np.stack([v - sb for v in V], 1)
    if abs(np.linalg.det(P)) < 1e-9 * (1 + np.abs(P).max() ** 4):
        return 2.0
    try:
        zk, lam = zK(sb, P, np.ones(4), return_point=True)
    except Exception:
        return 2.0
    if not (abs(zk - 1) < 1e-8 and lam[2] < 1e-10 and lam[3] < 1e-10 and min(lam[0], lam[1]) > 1e-6):
        return 2.0
    if min(margins(sb, V, t0)) < MARGIN:
        return 2.0
    sI, PI = precondition(sb, P)
    c, h, F = FamilySolver('orbit', sI, PI, np.ones(4)).best(1.0, iters=iters)
    return (c, h) if full else h


def starts():
    th0 = []
    for f in sorted(glob.glob('../logs/search_cex_*.log')):
        for line in open(f):
            if line.startswith('{'):
                r = json.loads(line)
                t0 = np.array(r['t0']); D = np.array(r['D'])
                M0 = t0.reshape(2, 2)
                U, s, Vt = np.linalg.svd(M0)
                a0 = U[:, 0] * np.sqrt(s[0]); b0 = Vt[0] * np.sqrt(s[0])
                th0.append((r['orbit'], np.concatenate([a0, b0, D, [0.0, np.log(r['k'])], r['sbar'], r['v3'], r['v4']])))
    th0.sort(key=lambda x: x[0])
    return [t for _, t in th0]


if __name__ == '__main__':
    S = starts()
    # seed 1: the four worst search corners first; other seeds: random search corners
    order = (list(range(min(4, len(S)))) + list(rng.permutation(np.arange(4, len(S))))) if seed == 1 \
        else list(rng.permutation(np.arange(4, len(S))))
    f = open(out, 'w')
    for k in order[:NS]:
        th = S[k]
        r0 = ratio(th)
        if r0 >= 2.0:
            f.write(json.dumps(dict(start=int(k), invalid_start=True)) + '\n')
            continue
        res = minimize(ratio, th, method='Nelder-Mead', options=dict(maxiter=700, xatol=1e-7, fatol=1e-7, adaptive=True))
        c, h = ratio(res.x, iters=40, full=True)
        sb, V, t0, D = build(res.x)
        rec = dict(start=int(k), start_ratio=r0, final_cert=c, final_upper=h, nfev=res.nfev,
                   margins=margins(sb, V, t0), sbar=sb.tolist(), V=[v.tolist() for v in V], t0=t0.tolist(),
                   theta=res.x.tolist())
        f.write(json.dumps(rec) + '\n')
        f.flush()
        print(json.dumps(dict(start=int(k), start_ratio=r0, final=c)), flush=True)
    f.close()
