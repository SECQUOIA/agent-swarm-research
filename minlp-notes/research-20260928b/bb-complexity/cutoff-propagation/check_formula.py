"""Check Theorem 3.1 (flat separable sums of depth-one univariate terms): the
greatest hull-consistent box is nonempty iff some sub-box U' has
    Phi(U') = sum_j min_{U'} g_j + max_j [max(g_j(lo'), g_j(hi')) - min_{U'} g_j] <= c,
where lo', hi' are the endpoints of U' in the variable of term j (hull
consistency supports only interval endpoints, so a non-monotone term may drop
its interior maximum).

Random flat sums of univariate monomial terms a * x_i^k (k = 1..4).  For each
instance and random box, pi_grid = min of Phi over sub-boxes with endpoints on
a grid.  Theory: HC4 is nonempty at c = pi_grid + delta (a grid sub-box is a
witness, Lemma 3.2), and empty at c = pi_grid - delta whenever the grid is fine
enough that the true minimum exceeds pi_grid - delta.
Run: python3 check_formula.py > logs/check_formula.log
"""
import numpy as np
from fbbt import Builder, hc4

rng = np.random.default_rng(7)


def term_vals(terms, i, grid):
    """Values of the terms of variable i on the grid: array (nterms_i, G)."""
    return np.array([a * grid ** k for (a, var, k) in terms if var == i])


def interval_stats(vals):
    """For every sub-interval [p, q] of grid indices (p <= q): sum of term
    minima and max term width.  Returns arrays over pairs."""
    T, G = vals.shape
    p_idx, q_idx = np.triu_indices(G)
    mins = np.zeros(len(p_idx)); maxw = np.zeros(len(p_idx))
    for t in range(T):
        v = vals[t]
        # running min/max over [p, q] via sparse loops (G small)
        mn = np.empty((G, G))
        for p in range(G):
            mn[p, p:] = np.minimum.accumulate(v[p:])
        m = mn[p_idx, q_idx]
        M = np.maximum(v[p_idx], v[q_idx])      # max endpoint value
        mins += m
        maxw = np.maximum(maxw, M - m)
    return mins, maxw


def build(terms, nvar, const):
    b = Builder(nvar)
    ch, co = [], []
    for a, var, k in terms:
        ch.append(var if k == 1 else b.pow(var, k)); co.append(a)
    b.lin(ch, co, const)
    return b.dag()


def one(nvar, G):
    terms = []
    for i in range(nvar):
        for k in range(1, 5):
            if rng.random() < 0.8:
                terms.append((float(rng.normal()), i, k))
    if not terms:
        return None
    box = []
    for i in range(nvar):
        lo = rng.uniform(-1.5, 1.0); box.append((lo, lo + rng.uniform(0.3, 2.0)))
    const = 0.0
    grids = [np.linspace(lo, hi, G) for lo, hi in box]
    stats = []
    for i in range(nvar):
        vals = term_vals(terms, i, grids[i])
        if vals.size == 0:
            vals = np.zeros((1, G))
        stats.append(interval_stats(vals))
    if nvar == 1:
        phi = stats[0][0] + stats[0][1]
    else:
        m1, w1 = stats[0]; m2, w2 = stats[1]
        phi = (m1[:, None] + m2[None, :]) + np.maximum(w1[:, None], w2[None, :])
    pi_grid = float(phi.min())
    scale = 1.0 + sum(abs(a) for a, _, _ in terms)
    delta = 2e-3 * scale
    dag = build(terms, nvar, const)
    st_hi, _, r_hi = hc4(dag, box, pi_grid + delta, max_rounds=200000)
    st_lo, vb_lo, r_lo = hc4(dag, box, pi_grid - delta, max_rounds=200000)
    phi_fix = None if vb_lo is None else phi_exact(terms, vb_lo, const)
    return dict(pi_grid=pi_grid, hi=st_hi, lo=st_lo, r_hi=r_hi, r_lo=r_lo,
                c_lo=pi_grid - delta, phi_at_fixed_box=phi_fix)


def phi_exact(terms, box, const):
    """Phi on a box for monomial terms (exact minimum, endpoint maximum)."""
    from fbbt import ipow
    mins, widths = [], []
    for a, var, k in terms:
        lo, hi = ipow(box[var], k)
        m = min(a * lo, a * hi)
        e = max(a * box[var][0] ** k, a * box[var][1] ** k)
        mins.append(m); widths.append(e - m)
    return const + sum(mins) + max(widths)


if __name__ == '__main__':
    for nvar, G, N in ((1, 400, 300), (2, 50, 150)):
        cnt = dict(ok_hi=0, bad_hi=0, ok_lo=0, lo_nonempty=0, lo_limit=0)
        n = 0
        while n < N:
            r = one(nvar, G)
            if r is None:
                continue
            n += 1
            cnt['ok_hi' if r['hi'] != 'empty' else 'bad_hi'] += 1
            if r['lo'] == 'empty':
                cnt['ok_lo'] += 1
            elif r['lo'] == 'limit':
                cnt['lo_limit'] += 1
            else:
                cnt['lo_nonempty'] += 1
                ok = r['phi_at_fixed_box'] <= r['c_lo'] + 1e-9 * (1 + abs(r['c_lo']))
                cnt['fixed_box_phi_le_c' if ok else 'fixed_box_phi_gt_c'] = \
                    cnt.get('fixed_box_phi_le_c' if ok else 'fixed_box_phi_gt_c', 0) + 1
                print('  nonempty below grid minimum (grid too coarse); Phi(fixed box) <= c:',
                      ok, {k: r[k] for k in ('pi_grid', 'c_lo', 'phi_at_fixed_box', 'r_lo')})
        print(f'nvar={nvar} grid={G} instances={N}: {cnt}')
