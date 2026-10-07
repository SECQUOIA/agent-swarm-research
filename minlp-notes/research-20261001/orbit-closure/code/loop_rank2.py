"""Rounds of orbit cuts inside one corner: does re-basing at the new LP vertex (a "second round")
close the closure gap of the first round?  (Section 8 of the note; compare Proposition 9 of the
sfree note.)

The LP is the corner itself, Pi_0 = {lam >= 0} (lambda-space of the original corner), with the
objective w.  Rule 'rebase': in round k, take the LP optimum v_k of min w^T lam over Pi_k, its basis
(three tight constraints G lam >= h, G invertible), the new corner (sbar' = sbar + P v_k,
P' = P G^{-1}, reduced costs w' = G^{-T} w), compute the best single orbit cut there for w'
(LMI bisection, family A) and add it to Pi_k.  Rule 'closure': in round k add all cuts generated for the orbit closure of the corner at v_k
(cut generation for objective w'); round 0 is the closure of the original corner, so the bound
after round 0 is z_cl(w), and later rounds measure the gain from re-basing.

Usage: python3 loop_rank2.py INSTANCE ROUNDS [RULE]      (RULE = closure (default) or single)
Output: JSON lines with the LP bound after each round (numerical evidence).
"""
import sys, json
import numpy as np
from scipy.optimize import linprog
import orbit_lib
from orbit_lib import qval, corner_bound
import core
from closure_survey import INST
from closure import closure_value
from orbit_lib import Corner


def lp(w, cuts):
    N = len(w)
    if cuts:
        A = -np.array([c[0] for c in cuts]); b = -np.array([c[1] for c in cuts])
    else:
        A = np.zeros((0, N)); b = np.zeros(0)
    res = linprog(w, A_ub=A if len(cuts) else None, b_ub=b if len(cuts) else None,
                  bounds=[(0, None)] * N, method='highs')
    return res


def basis(v, cuts, N, tol=1e-9):
    """Three tight constraints with linearly independent normals (rows of G, rhs h)."""
    rows = []
    for j in range(N):
        if v[j] <= tol * (1 + abs(v).max()):
            e = np.zeros(N); e[j] = 1.0
            rows.append((e, 0.0))
    for a, rhs in cuts:
        if abs(a @ v - rhs) <= 1e-7 * (1 + abs(rhs)):
            rows.append((np.asarray(a, float), rhs))
    # greedy selection of an invertible subset (prefer the most recent cuts last)
    G, h = [], []
    for a, rhs in rows:
        if np.linalg.matrix_rank(np.array(G + [a])) == len(G) + 1:
            G.append(a); h.append(rhs)
        if len(G) == N:
            break
    return (np.array(G), np.array(h)) if len(G) == N else (None, None)


def run(name, rounds, rule='closure'):
    sb, P = INST[name]()
    N = P.shape[1]
    w = np.ones(N)
    zK, _ = corner_bound(sb, P, w)
    print(json.dumps(dict(name=name, zK=float(zK))), flush=True)
    cuts = []
    for k in range(rounds):
        res = lp(w, cuts)
        v = res.x
        bound = float(w @ v)
        G, h = basis(v, cuts, N)
        if G is None:
            print(json.dumps(dict(round=k, bound=bound, note='degenerate basis')), flush=True)
            break
        Gi = np.linalg.inv(G)
        sbp = sb + P @ v
        Pp = P @ Gi
        wp = Gi.T @ w
        qv = qval(sbp)
        rec = dict(round=k, bound=bound, lam=v.tolist(), q_vertex=qv, reduced_costs=wp.tolist())
        if qv <= 1e-10:
            rec['note'] = 'LP vertex satisfies the bilinear constraint'
            print(json.dumps(rec), flush=True)
            break
        if np.any(wp <= 1e-12):
            rec['note'] = 'zero reduced cost'
        wpp = np.maximum(wp, 1e-9)
        zKp, lamKp = corner_bound(sbp, Pp, wpp)
        if rule == 'closure':
            cn = Corner(sbp, Pp)
            zc, lamc, ccuts, th, hist = closure_value(cn, wpp, fam='A', maxit=40, tol=1e-7)
            for coef in ccuts:
                a_lam = np.asarray(coef) @ G
                cuts.append((a_lam, 1.0 + a_lam @ v))
            rec.update(zK_new_corner=float(zKp), closure_new_corner=float(zc), ncuts_added=len(ccuts))
            print(json.dumps(rec), flush=True)
            if zc >= zKp * (1 - 1e-9):
                pass
            continue
        cert, hi, F = core.best_orbit_bound('+', sbp, Pp, wpp, zKp, iters=40)
        rec.update(zK_new_corner=float(zKp), orbit_cut_new_corner=float(cert))
        if F is None or not np.isfinite(cert) or cert <= 0:
            rec['note'] = 'no orbit cut'
            print(json.dumps(rec), flush=True)
            break
        _, al = core.orbit_bound_of(F, '+', sbp, Pp, wpp)
        # cut sum_k mu_k / alpha_k >= 1 with mu = G (lam - v)
        coef = np.array([0.0 if not np.isfinite(a) else 1.0 / a for a in al])
        a_lam = coef @ G
        rhs = 1.0 + a_lam @ v
        cuts.append((a_lam, rhs))
        print(json.dumps(rec), flush=True)
    res = lp(w, cuts)
    print(json.dumps(dict(final_bound=float(w @ res.x), ncuts=len(cuts))), flush=True)


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    run(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'closure')
