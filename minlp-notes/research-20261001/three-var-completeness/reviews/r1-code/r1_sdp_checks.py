r"""Reviewer's floating-point checks, review round 1 (independent code;
uses only r1_common.py).

usage: python r1_sdp_checks.py {bnw|moments|stored} SEED N

bnw      Independent test of BNW Theorem 1 (n = 3): random submodular (Q, c);
         compare min over [0,1]^3 (exact face enumeration) with relaxation (2)
         {[[1,x^T],[x,X]] psd, X <= x e^T}.
moments  Points y of R_D and of R, obtained by minimizing random objectives
         (half supermodular-biased, half perturbed family copies).  For each y:
           s_all  = min q(y) over q in P3+ with q(uniform) = 1  (y in H3+ iff >= 0)
           s_pr<=0 = min over the four sign orthants with q12 q13 q23 <= 0
         Theorem 2.5 predicts s_pr<=0 >= 0 on R_D; Corollary 2.4 (iv) predicts
         that y in R_D \ H3+ satisfies all caps strictly and that setting any
         Y_ii = m_i gives a point of H3+; Conjecture 2.11 predicts s_all >= 0
         for points of R.
stored   Stored rays outside cl(D3) from the stream's logs: validity (cube
         minimum), value over R_D and over R (own implementation), and a direct
         fit to one of the 24 family copies (own fitting).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import glob
import json
import sys
import warnings
from itertools import product

import numpy as np

from r1_common import (QK, MinOver, SepP3plus, cube_min, family_copies, UNIFORM)

warnings.filterwarnings("ignore")
LOGS = (_PUBLIC_REPO + '/research-20261001/three-var-completeness/logs')


def poly_coeffs_compose(c, g):
    """Coefficients of p(u(x)) with u_i = x_perm[i] or 1 - x_perm[i]."""
    import sympy as sp
    xs = sp.symbols('x0:3')
    perm, comp = g
    u = [(1 - xs[perm[i]]) if comp[i] else xs[perm[i]] for i in range(3)]
    mons = [1, u[0], u[1], u[2], u[0]**2, u[1]**2, u[2]**2, u[0]*u[1], u[0]*u[2], u[1]*u[2]]
    P = sp.Poly(sp.expand(sum(float(a) * m for a, m in zip(c, mons))), *xs)
    out = []
    for kk in QK:
        out.append(float(P.coeff_monomial(xs[0]**kk[0] * xs[1]**kk[1] * xs[2]**kk[2])))
    return np.array(out)


def family_vec(h, d1, d2, d3, k):
    D = d1 + d2 - h
    # L^2 + 2 d3 k z (1 - x - y) + k (2D + k) x y, L = h - d1 x - d2 y + d3 z
    return np.array([h * h, -2 * h * d1, -2 * h * d2, 2 * h * d3 + 2 * d3 * k,
                     d1 * d1, d2 * d2, d3 * d3,
                     2 * d1 * d2 + k * (2 * D + k), -2 * d1 * d3 - 2 * d3 * k, -2 * d2 * d3 - 2 * d3 * k])


def norm(c):
    return c / np.abs(c).max()


# ---------------------------------------------------------------- bnw
def run_bnw(seed, n):
    import cvxpy as cp
    rng = np.random.default_rng(seed)
    xv = cp.Variable(3)
    Xv = cp.Variable((3, 3), symmetric=True)
    Mm = cp.bmat([[np.ones((1, 1)), cp.reshape(xv, (1, 3), order='F')],
                  [cp.reshape(xv, (3, 1), order='F'), Xv]])
    cons = [Mm >> 0] + [Xv[i, j] <= xv[i] for i in range(3) for j in range(3)]
    Qp = cp.Parameter((3, 3), symmetric=True)
    cpar = cp.Parameter(3)
    prob = cp.Problem(cp.Minimize(cp.trace(Qp @ Xv) + cpar @ xv), cons)
    worst = 0.0
    worst_other = 0.0
    for it in range(n):
        Q = np.zeros((3, 3))
        off = -np.abs(rng.normal(size=3)) * (rng.random(3) < 0.85)
        Q[0, 1] = Q[1, 0] = off[0]; Q[0, 2] = Q[2, 0] = off[1]; Q[1, 2] = Q[2, 1] = off[2]
        np.fill_diagonal(Q, rng.normal(size=3) * rng.choice([0.3, 1, 3]))
        c = rng.normal(size=3) * rng.choice([0.3, 1, 3])
        vec = np.array([0, c[0], c[1], c[2], Q[0, 0], Q[1, 1], Q[2, 2], 2 * Q[0, 1], 2 * Q[0, 2], 2 * Q[1, 2]])
        box = cube_min(vec)
        Qp.value = Q; cpar.value = c
        sdp = prob.solve(solver='CLARABEL', tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        scale = max(1.0, np.abs(vec).max())
        worst = max(worst, (box - sdp) / scale)
        # control: flip the sign of one off-diagonal pair (non-submodular) to see the relaxation fail
        Q2 = Q.copy(); Q2[0, 1] = Q2[1, 0] = abs(Q[0, 1]) + 0.5
        vec2 = vec.copy(); vec2[7] = 2 * Q2[0, 1]
        Qp.value = Q2
        sdp2 = prob.solve(solver='CLARABEL', tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        worst_other = max(worst_other, (cube_min(vec2) - sdp2) / max(1.0, np.abs(vec2).max()))
    # adversarial search: maximize the gap over submodular data (Nelder-Mead)
    from scipy.optimize import minimize

    def gap(theta, submodular=True):
        Q = np.zeros((3, 3))
        o = -np.abs(theta[:3]) if submodular else theta[:3]
        Q[0, 1] = Q[1, 0] = o[0]; Q[0, 2] = Q[2, 0] = o[1]; Q[1, 2] = Q[2, 1] = o[2]
        np.fill_diagonal(Q, theta[3:6])
        c = theta[6:9]
        vec = np.array([0, c[0], c[1], c[2], Q[0, 0], Q[1, 1], Q[2, 2], 2 * Q[0, 1], 2 * Q[0, 2], 2 * Q[1, 2]])
        s = np.abs(vec).max()
        Qp.value = Q / s; cpar.value = c / s
        sdp = prob.solve(solver='CLARABEL', tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        return -(cube_min(vec / s) - sdp)
    adv = 0.0
    for start in range(max(1, n // 25)):
        res = minimize(gap, rng.normal(size=9), method='Nelder-Mead', options=dict(maxfev=600))
        adv = max(adv, -res.fun)
    ctrl = 0.0
    for start in range(max(1, n // 100)):
        res = minimize(lambda t: gap(t, False), rng.normal(size=9), method='Nelder-Mead', options=dict(maxfev=600))
        ctrl = max(ctrl, -res.fun)
    print(f'bnw seed {seed}: control search without the sign condition finds normalized gap {ctrl:.2e}', flush=True)
    print(f'bnw seed {seed}: adversarial Nelder-Mead ({max(1, n // 25)} starts x 600 evaluations): '
          f'max normalized gap {adv:.2e}', flush=True)
    print(f'bnw seed {seed}: {n} submodular instances, max (box min - SDP(2)) / scale = {worst:.2e}; '
          f'control with one positive cross coefficient: max gap {worst_other:.2e}', flush=True)


# ---------------------------------------------------------------- moments
def random_objective(rng, copies):
    if rng.random() < 0.5:
        c = rng.normal(size=10)
        c[4:7] = np.abs(c[4:7]) + 0.05
        c[7:10] = np.abs(c[7:10])          # supermodular bias
        return c
    # perturbed family copy, five-contact-ish parameters
    d1, d2 = rng.uniform(0.3, 2, 2)
    h = rng.uniform(0, min(d1, d2))
    k = rng.uniform(0.1, 2)
    d3 = d1 + d2 - h + k + rng.uniform(0, 2)
    v = family_vec(h, d1, d2, d3, k)
    g = copies[rng.integers(len(copies))]
    v = poly_coeffs_compose(v, g)
    v = norm(v) + rng.normal(scale=0.03, size=10)
    v[4:7] = np.abs(v[4:7]) + 1e-3
    return v


def valid_gap_objective(rng, copies):
    """A family copy (five-contact regime) plus a small random element of
    D3^quad (affine square or x_i x_j-type generator): valid on the cube and,
    for small weight, outside cl(D3), so its minimizer over R_D lies outside H3+."""
    d1, d2 = rng.uniform(0.3, 2, 2)
    h = rng.uniform(0.05, 0.95) * min(d1, d2)
    k = rng.uniform(0.05, 2)
    d3 = (d1 + d2 - h + k) * rng.uniform(1.05, 3)
    v = norm(poly_coeffs_compose(family_vec(h, d1, d2, d3, k), copies[rng.integers(len(copies))]))
    a = rng.normal(size=4)
    sq = np.array([a[0]**2, 2*a[0]*a[1], 2*a[0]*a[2], 2*a[0]*a[3], a[1]**2, a[2]**2, a[3]**2,
                   2*a[1]*a[2], 2*a[1]*a[3], 2*a[2]*a[3]])
    i, j = rng.choice(3, 2, replace=False)
    gen = np.zeros(10)
    gen[{(0, 1): 7, (1, 0): 7, (0, 2): 8, (2, 0): 8, (1, 2): 9, (2, 1): 9}[(i, j)]] = 1   # x_i x_j
    return v + rng.uniform(0, 0.03) * norm(sq) + rng.uniform(0, 0.03) * gen


def run_moments(seed, n):
    rng = np.random.default_rng(seed)
    copies = family_copies()
    RD, RR = MinOver(False), MinOver(True)
    sep_all = SepP3plus()
    seps_pr = []
    for signs in [(-1, -1, -1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
        S = SepP3plus()
        import cvxpy as cp
        cons = list(S.prob.constraints) + [s * S.q[7 + j] >= 0 for j, s in enumerate(signs)]
        S.prob = cp.Problem(S.prob.objective, cons)
        seps_pr.append(S)
    stats = dict(n_RD=0, RD_outside_H=0, min_s_pr_RD=np.inf, min_cap_gap=np.inf, min_after_round=np.inf,
                 n_R=0, min_s_all_R=np.inf, min_s_all_RD=np.inf)
    for it in range(n):
        for which, rel in (('RD', RD), ('R', RR)):
            if which == 'RD':
                c = valid_gap_objective(rng, copies)
            else:
                c = random_objective(rng, copies) if rng.random() < 0.67 else valid_gap_objective(rng, copies)
            try:
                v, st = rel(c)
                if st not in ('optimal', 'optimal_inaccurate'):
                    continue
                y = rel.quad_moments()
                s_all = sep_all(y)[0]
            except Exception:
                continue
            if which == 'R':
                stats['n_R'] += 1
                stats['min_s_all_R'] = min(stats['min_s_all_R'], s_all)
                if s_all < -1e-6:
                    print('   R point outside H3+ ?', it, s_all, list(np.round(c, 4)), flush=True)
                continue
            stats['n_RD'] += 1
            stats['min_s_all_RD'] = min(stats['min_s_all_RD'], s_all)
            s_pr = min(S(y)[0] for S in seps_pr)
            stats['min_s_pr_RD'] = min(stats['min_s_pr_RD'], s_pr)
            if s_all < -1e-5:
                stats['RD_outside_H'] += 1
                caps = [y[1 + i] - y[4 + i] for i in range(3)]
                stats['min_cap_gap'] = min(stats['min_cap_gap'], min(caps))
                for i in range(3):
                    y2 = y.copy(); y2[4 + i] = y2[1 + i]
                    stats['min_after_round'] = min(stats['min_after_round'], sep_all(y2)[0])
    print(f'moments seed {seed}: ' + ', '.join(f'{k} {v:.3g}' if isinstance(v, float) else f'{k} {v}'
                                             for k, v in stats.items()), flush=True)


# ---------------------------------------------------------------- stored
def fit_family(p):
    """Best relative residual of p against a single member of one of the 24
    copies, found directly from the coefficients."""
    best = (np.inf, None)
    for g in family_copies():
        # g maps x -> u(x) and is an involution up to the permutation; compose
        # with all 48 images instead of inverting: test p o g' for every g'.
        pass
    for perm in __import__('itertools').permutations(range(3)):
        for comp in product((0, 1), repeat=3):
            pg = poly_coeffs_compose(p, (perm, comp))
            if min(pg[4:7]) <= 0:
                continue
            lam = 1.0
            d1, d2, d3 = np.sqrt(pg[4:7])
            k = -pg[8] / (2 * d3) - d1
            for hs in (1, -1):
                h = hs * np.sqrt(max(pg[0], 0))
                if k < -1e-9:
                    continue
                r = np.abs(family_vec(h, d1, d2, d3, max(k, 0)) - pg).max() / np.abs(pg).max()
                if r < best[0]:
                    best = (r, (perm, comp, h, d1, d2, d3, k))
    return best


def run_stored(seed, n):
    rays = []
    for f in sorted(glob.glob(LOGS + '/stratum_enum*_*.jsonl')):
        for line in open(f):
            r = json.loads(line)
            for ex in r.get('examples', []):
                rays.append(('stratum', np.array(ex['p'])))
    d = json.load(open(LOGS + '/signclass_sup_2.json'))
    for o in d['records']:
        if o['r_d3'] < -1e-6:
            rays.append(('signclass_sup', np.array(o['p'])))
    for f in sorted(glob.glob(LOGS + '/explore_psd_*.json')):
        for o in json.load(open(f)):
            if isinstance(o, dict) and (o.get('r0') or 0) < -1e-6 and 'p' in o:
                rays.append(('explore_psd', np.array(o['p'])))
    rng = np.random.default_rng(seed)
    if len(rays) > n:
        keep = sorted(rng.choice(len(rays), n, replace=False))
        # always keep all stratum and signclass examples
        keep = sorted(set(keep) | {i for i, (s, _) in enumerate(rays) if s != 'explore_psd'})
        rays = [rays[i] for i in keep]
    RD, RR = MinOver(False), MinOver(True)
    worst = dict(cubemin=np.inf, rd=-np.inf, rR=np.inf, fit=0.0)
    counts = {}
    for src, p in rays:
        p = norm(p)
        cm = cube_min(p)
        rd = RD(p)[0]
        rR = RR(p)[0]
        fit = fit_family(p)[0]
        counts[src] = counts.get(src, 0) + 1
        worst['cubemin'] = min(worst['cubemin'], cm)
        worst['rd'] = max(worst['rd'], rd)
        worst['rR'] = min(worst['rR'], rR)
        worst['fit'] = max(worst['fit'], fit)
        print(f'   {src:13s} cubemin {cm: .1e}  R_D {rd: .2e}  R {rR: .1e}  family fit {fit:.1e}', flush=True)
    print(f'stored: {counts}; min cube minimum {worst["cubemin"]:.2e}; largest R_D value {worst["rd"]:.2e}; '
          f'smallest R value {worst["rR"]:.2e}; worst family fit {worst["fit"]:.2e}', flush=True)


if __name__ == '__main__':
    mode, seed, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    dict(bnw=run_bnw, moments=run_moments, stored=run_stored)[mode](seed, n)
