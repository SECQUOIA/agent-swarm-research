"""Test Theorem 3.1 of cutoff-propagation.md with the reviewer's propagator.

Instances: flat separable sums whose terms are general univariate polynomial
nodes phi(x_i) of degree 2..5 (non-monotone, interior maxima and minima), plus
monomial pow nodes and linear terms.  For each instance:

  Phi_min = min over sub-boxes U' of
            sum_j min_{U'} t_j + max_j [max(t_j(lo'), t_j(hi')) - min_{U'} t_j]
  (exact term minima via critical points; grid over sub-intervals, then
  Nelder-Mead refinement), and

  test (b): propagation at c = Phi_min + d must be nonempty, at c = Phi_min - d
            empty (d = 1e-6 * scale), for two schedules (hc4, chaotic);
  test (a): at c = Phi_min + d, the fixed box Z' must satisfy Phi(Z') <= c;
  also the full-range variant Phi_full (max over the interval instead of the
  endpoint max) to see how often it differs, and a chain-of-binary-sums
  representation (Remark 3.2).
Run: python3 t31_check.py > logs/t31_check.log
"""
import sys
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import minimize
from ifbbt import DAG, real_roots

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 11)


def rand_terms(nvar):
    terms = []  # (var, coeffs low->high, kind)
    for i in range(nvar):
        k = rng.integers(2, 4)
        for _ in range(k):
            r = rng.random()
            if r < 0.6:
                deg = rng.integers(2, 6)
                c = rng.normal(size=deg + 1); c[0] = 0.0
                terms.append((i, c, 'up'))
            elif r < 0.85:
                e = int(rng.integers(2, 5)); c = np.zeros(e + 1); c[e] = rng.normal()
                terms.append((i, c, 'pow'))
            elif not any(v == i and kd == 'lin' for v, _, kd in terms):
                terms.append((i, np.array([0.0, rng.normal()]), 'lin'))
    return terms


def build(terms, nvar, chain=False):
    d = DAG(nvar)
    ch, co = [], []
    for i, c, kind in terms:
        if kind == 'up':
            ch.append(d.up(i, c)); co.append(1.0)
        elif kind == 'pow':
            e = len(c) - 1
            ch.append(d.pow(i, e)); co.append(c[e])
        else:
            ch.append(i); co.append(c[1])
    if not chain:
        d.sum(ch, co, 0.0)
        return d
    # chain of binary sums s_k = s_{k-1} + a_k p_k (merge repeated variable children)
    acc = d.sum([ch[0]], [co[0]], 0.0)
    for c_, a_ in zip(ch[1:], co[1:]):
        acc = d.sum([acc, c_], [1.0, a_], 0.0)
    return d


def tmin(c, lo, hi):
    pts = [lo, hi] + real_roots(P.polyder(c), lo, hi)
    return min(P.polyval(p, c) for p in pts)


def tmax(c, lo, hi):
    pts = [lo, hi] + real_roots(P.polyder(c), lo, hi)
    return max(P.polyval(p, c) for p in pts)


def Phi(terms, box, full=False):
    mins, wid = [], []
    for i, c, _ in terms:
        lo, hi = box[i]
        m = tmin(c, lo, hi)
        top = tmax(c, lo, hi) if full else max(P.polyval(lo, c), P.polyval(hi, c))
        mins.append(m); wid.append(top - m)
    return sum(mins) + max(wid)


def grid_stats(terms, i, g):
    """For all grid sub-intervals of variable i: sum of exact term minima and
    max endpoint width.  Exact minima: min over endpoints and critical points."""
    G = len(g)
    p, q = np.triu_indices(G)
    M = np.zeros(len(p)); Wd = np.full(len(p), -np.inf)
    for var, c, _ in terms:
        if var != i:
            continue
        v = P.polyval(g, c)
        m = np.minimum(v[p], v[q])
        for r in real_roots(P.polyder(c), g[0], g[-1]):
            inside = (g[p] <= r) & (r <= g[q])
            m = np.where(inside, np.minimum(m, P.polyval(r, c)), m)
        M += m
        Wd = np.maximum(Wd, np.maximum(v[p], v[q]) - m)
    return M, np.where(np.isfinite(Wd), Wd, 0.0), g[p], g[q]


def phi_min(terms, box, G):
    stats = [grid_stats(terms, i, np.linspace(lo, hi, G)) for i, (lo, hi) in enumerate(box)]
    if len(box) == 1:
        M, W, a, b = stats[0]
        k = int(np.argmin(M + W))
        x0 = [a[k], b[k]]
    else:
        (M1, W1, a1, b1), (M2, W2, a2, b2) = stats
        best = (np.inf, None)
        # case W1 >= W2: min over i of M1+W1 + min{M2 : W2 <= W1}
        for (Ma, Wa), (Mb, Wb), swap in (((M1, W1), (M2, W2), False), ((M2, W2), (M1, W1), True)):
            o = np.argsort(Wb); pref = np.minimum.accumulate(Mb[o])
            idx = np.searchsorted(Wb[o], Wa, side='right') - 1
            ok = idx >= 0
            val = np.where(ok, Ma + Wa + pref[np.maximum(idx, 0)], np.inf)
            i = int(np.argmin(val))
            if val[i] < best[0]:
                j = o[np.argmin(np.where(Wb[o][:idx[i] + 1] <= Wa[i], Mb[o][:idx[i] + 1], np.inf))]
                best = (val[i], (j, i) if swap else (i, j))
        i, j = best[1]
        x0 = [a1[i], b1[i], a2[j], b2[j]]
    n = len(box)

    def obj(z):
        bx = []
        for k in range(n):
            lo, hi = sorted((z[2 * k], z[2 * k + 1]))
            L, U = box[k]
            bx.append((min(max(lo, L), U), min(max(hi, L), U)))
        return Phi(terms, bx)
    v0 = obj(x0)
    r = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14, maxiter=4000))
    return min(v0, r.fun)


def run(nvar, N, G):
    stats = dict(n=0, b_hi_ok=0, b_lo_ok=0, b_lo_limit=0, b_lo_nonempty=0, a_ok=0, a_bad=0,
                 sched_agree=0, chain_agree=0, full_differs=0)
    worst = 0.0
    while stats['n'] < N:
        terms = rand_terms(nvar)
        box = []
        for _ in range(nvar):
            lo = rng.uniform(-1.5, 1.0); box.append((lo, lo + rng.uniform(0.3, 2.0)))
        d = build(terms, nvar)
        dc = build(terms, nvar, chain=True)
        pm = phi_min(terms, box, G)
        scale = 1.0 + sum(float(np.abs(c).sum()) for _, c, _ in terms)
        dl = 1e-6 * scale
        stats['n'] += 1
        st_hi, Z, _ = d.propagate(box, pm + dl, max_rounds=50000)
        st_lo, Zl, r_lo = d.propagate(box, pm - dl, max_rounds=50000)
        st_hi2, _, _ = d.propagate(box, pm + dl, max_rounds=50000, schedule='chaotic', seed=3)
        st_lo2, _, _ = d.propagate(box, pm - dl, max_rounds=50000, schedule='chaotic', seed=3)
        st_hic, _, _ = dc.propagate(box, pm + dl, max_rounds=50000)
        st_loc, _, _ = dc.propagate(box, pm - dl, max_rounds=50000)
        stats['b_hi_ok'] += st_hi != 'empty'
        if st_lo == 'empty':
            stats['b_lo_ok'] += 1
        elif st_lo == 'limit':
            stats['b_lo_limit'] += 1
        else:
            stats['b_lo_nonempty'] += 1
            print('  NONEMPTY below Phi_min:', dict(pm=pm, c=pm - dl, rounds=r_lo,
                                                  phi_fixed=Phi(terms, d.xbox(Zl))))
        stats['sched_agree'] += (st_hi != 'empty') == (st_hi2 != 'empty') and \
            (st_lo == 'empty') == (st_lo2 == 'empty')
        stats['chain_agree'] += (st_hi != 'empty') == (st_hic != 'empty') and \
            (st_lo == 'empty') == (st_loc == 'empty')
        if Z is not None:
            ph = Phi(terms, d.xbox(Z))
            if ph <= pm + dl + 1e-9 * scale:
                stats['a_ok'] += 1
            else:
                stats['a_bad'] += 1
                print('  (a) violated:', ph, pm + dl)
            worst = max(worst, ph - (pm + dl))
        # does the full-range variant give a different minimum over sub-boxes?
        full = Phi(terms, box, full=True) - Phi(terms, box)
        stats['full_differs'] += full > 1e-9
    print(f'nvar={nvar} grid={G}: {stats}; max Phi(fixed box) - c = {worst:.2e}')


if __name__ == '__main__':
    run(1, 120, 400)
    run(2, 80, 120)
