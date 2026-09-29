"""T6: squared lengths in 1D with disjoint intervals on every edge (radial dispersion).

In 1D, REL = REL_H (intervals are simplices) and Euclidean lengths are exact on such
instances (T4(c)), but squared lengths can have gaps.  Corollary C with the exact radial
constant kappa^sq_e = (M_e + m_e)^2 / (4 M_e m_e), where [m_e, M_e] = {|w| : w in X_v - X_u},
must hold:  OPT <= E[round] <= sum_e kappa^sq_e * ltilde_e <= kappa^sq_max * REL_H.
Random search + local search maximizing (OPT/REL_H - 1)/(kappa^sq_max - 1).
Usage: python3 t6_squared1d.py [n_random] [local iters] [seed]
"""
import sys
import numpy as np
from gcslib import *

NR = int(sys.argv[1]) if len(sys.argv) > 1 else 60
IT = int(sys.argv[2]) if len(sys.argv) > 2 else 150
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 0)


def lohi(S):
    return (S.c[0], S.c[0]) if S.kind == "point" else (S.lo[0], S.hi[0])


def ksq(Su, Sv):
    a, b = lohi(Su), lohi(Sv)
    lo, hi = b[0] - a[1], b[1] - a[0]  # X_v - X_u = [lo, hi]
    if lo <= 0 <= hi:
        return np.inf
    m, M = min(abs(lo), abs(hi)), max(abs(lo), abs(hi))
    return (M + m) ** 2 / (4 * M * m)


def build(prm, E, nv):
    sets = {0: point([prm[0]]), nv - 1: point([prm[1]])}
    for v in range(1, nv - 1):
        c, w = prm[2 * v], abs(prm[2 * v + 1])
        sets[v] = box([c - w], [c + w])
    return GCS(sets, E, 0, nv - 1, SQ)


def evaluate(g):
    kap = {e: ksq(g.sets[e[0]], g.sets[e[1]]) for e in g.edges}
    km = max(kap.values())
    if not np.isfinite(km) or km > 3:
        return None
    rh, sol = relax(g, hull=True, return_sol=True)
    r = relax(g)
    o = opt(g)
    Er = expected_round(g, sol)
    y = sol["y"]
    kb = sum(kap[e] * y[e] * g.cost[e].val(sol["z"][e] / y[e], sol["zp"][e] / y[e]) for e in g.edges if y[e] > 1e-7)
    tol = 1e-5 * max(1.0, abs(o))
    ok = o <= Er + tol and Er <= kb + tol and kb <= km * rh + tol
    if not ok:
        print(f"  check failed: OPT={o:.8f} E={Er:.8f} sum k*l={kb:.8f} kmax*REL_H={km*rh:.8f}")
    return dict(r=r, rh=rh, o=o, Er=Er, kb=kb, km=km, ok=ok, score=(o / rh - 1) / (km - 1))


nv = 6
E = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (4, 5), (1, 2), (3, 4), (0, 3), (2, 5)]
viol, cnt, gaps, best, bp = 0, 0, 0, -1, None
for trial in range(NR * 20):
    if cnt >= NR:
        break
    prm = np.r_[0.0, rng.uniform(4, 8), [x for v in range(1, nv - 1) for x in (rng.uniform(0.5, 7), rng.uniform(0.05, 1.0))]]
    g = build(prm, E, nv)
    res = evaluate(g)
    if res is None:
        continue
    cnt += 1
    viol += not res["ok"]
    gaps += res["o"] - res["rh"] > 1e-5
    if abs(res["rh"] - res["r"]) > 1e-5:
        print("REL != REL_H in 1D?!", res)
    if res["score"] > best:
        best, bp = res["score"], prm
print(f"random: n={cnt} violations={viol} #gaps(OPT-REL_H>1e-5)={gaps} best score={best:.4f}")
for it in range(IT):
    p = bp + rng.standard_normal(len(bp)) * rng.choice([0.02, 0.1, 0.3])
    p[0] = 0.0
    res = evaluate(build(p, E, nv))
    if res is None:
        continue
    viol += not res["ok"]
    if res["score"] > best:
        best, bp = res["score"], p
res = evaluate(build(bp, E, nv))
print(f"local search: best (OPT/REL_H-1)/(kappa_sq_max-1)={best:.4f} OPT={res['o']:.5f} REL_H={res['rh']:.5f} "
      f"kappa_sq_max={res['km']:.4f} violations(total)={viol}")
print("best params (x_s, x_t, then centre/half-width per vertex):", np.round(bp, 4).tolist())

# explicit balanced fork (squared, 1D, disjoint intervals on every edge):
# s={0}, A=[1,3], P={3.5}, Q={4.5}, t={6};  both routes cost 12.375, relaxation mixes them.
sets = {"s": point([0.0]), "A": box([1.0], [3.0]), "P": point([3.5]), "Q": point([4.5]), "t": point([6.0])}
Ef = [("s", "A"), ("A", "P"), ("A", "Q"), ("P", "t"), ("Q", "t")]
gf = GCS(sets, Ef, "s", "t", SQ)
rf, of = relax(gf), opt(gf)
kf = max(ksq(sets[u], sets[v]) for u, v in Ef)
print(f"balanced fork: REL=REL_H={rf:.6f} (<= 12.3125) OPT={of:.6f} gap={(of-rf)/of:.4%} kappa_sq_max={kf:.4f}; "
      f"Euclidean lengths on same instance: REL={relax(GCS(sets, Ef, 's', 't', L2)):.6f} OPT={opt(GCS(sets, Ef, 's', 't', L2)):.6f}")
# local search on the fork geometry (parameters: A=[a1,a2], P, Q, t) for the score
def fork(p):
    a1, a2, P, Q, T = p
    if not (0 < a1 < a2 < min(P, Q) and max(P, Q) < T):
        return None
    S = {"s": point([0.0]), "A": box([a1], [a2]), "P": point([P]), "Q": point([Q]), "t": point([T])}
    return GCS(S, Ef, "s", "t", SQ)
bpf, bsc = np.array([1.0, 3.0, 3.5, 4.5, 6.0]), -1
for it in range(IT):
    p = bpf + (rng.standard_normal(5) * rng.choice([0.02, 0.1, 0.3]) if it else 0)
    g = fork(p)
    if g is None:
        continue
    res = evaluate(g)
    if res is None:
        continue
    viol += not res["ok"]
    if res["score"] > bsc:
        bsc, bpf, bres = res["score"], p, res
print(f"fork local search: best (OPT/REL_H-1)/(kappa_sq_max-1)={bsc:.4f}, OPT/REL_H-1={bres['o']/bres['rh']-1:.5f}, "
      f"kappa_sq_max={bres['km']:.4f}, params(A=[a1,a2],P,Q,t)={np.round(bpf,4).tolist()}, violations(total)={viol}")
