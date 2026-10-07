"""Reviewer r1 (second reviewer): independent re-check of Section 7.1 (random corners).

Does not import the stream's code.  For every logged corner:
  * regenerates (sbar, P, w) from (seed, idx) with the generator described in the note;
  * computes z_K independently: for each direction mu in the simplex, t(mu) = first positive root of
    det(sbar + t * sum_j mu_j p_j / w_j) = 0; minimized over supports of size 1 (exact root), size 2
    (dense grid of 4001 points + golden-section refinement) and over 20000 random directions of the
    full simplex (a check that no support >= 3 direction is better);
  * computes SCIP's one-cut bound with the literal sepa_interminor.c formula (eigenvectors hard-coded,
    vars order (xik, xjl, xil, xjk));
  * recomputes the summary statistics of logs/analysis.log from the jsonl files.
Usage: python3 rev_random.py LOGDIR
"""
import json
import sys
import numpy as np

LOGDIR = sys.argv[1]


def det4(s):
    return s[0] * s[3] - s[1] * s[2]


def first_root(s, d):
    """smallest t > 0 with det(s + t d) = 0 (det(s) > 0), vectorized over columns of d."""
    a = d[0] * d[3] - d[1] * d[2]
    b = s[0] * d[3] + s[3] * d[0] - s[1] * d[2] - s[2] * d[1]
    c = det4(s)
    out = np.full(d.shape[1], np.inf)
    disc = b * b - 4 * a * c
    lin = np.abs(a) < 1e-14
    with np.errstate(all='ignore'):
        tl = np.where(lin & (b < 0), -c / b, np.inf)
        sq = np.sqrt(np.maximum(disc, 0))
        r1 = (-b - sq) / (2 * a)
        r2 = (-b + sq) / (2 * a)
    for r in (r1, r2):
        ok = (~lin) & (disc >= 0) & (r > 0)
        out = np.where(ok, np.minimum(out, r), out)
    out = np.where(lin, tl, out)
    return out


def zk_indep(s, P, w, rng):
    N = P.shape[1]
    Q = P / w
    best = np.inf
    supp = None
    t1 = first_root(s, Q)
    j = int(np.argmin(t1))
    best, supp = t1[j], (j,)
    grid = np.linspace(0, 1, 4001)
    gr = (np.sqrt(5) - 1) / 2
    for i in range(N):
        for k in range(i + 1, N):
            D = np.outer(Q[:, i], grid) + np.outer(Q[:, k], 1 - grid)
            t = first_root(s, D)
            m = int(np.argmin(t))
            if not np.isfinite(t[m]):
                continue
            lo, hi = grid[max(m - 1, 0)], grid[min(m + 1, len(grid) - 1)]
            f = lambda u: first_root(s, (u * Q[:, i] + (1 - u) * Q[:, k])[:, None])[0]
            for _ in range(80):
                m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
                if f(m1) <= f(m2):
                    hi = m2
                else:
                    lo = m1
            u = 0.5 * (lo + hi)
            v = min(t[m], f(u))
            if v < best - 1e-12:
                best = v
                uu = u if f(u) <= t[m] else grid[m]
                supp = (i, k) if 1e-7 < uu < 1 - 1e-7 else ((i,) if uu >= 1 - 1e-7 else (k,))
    mu = rng.dirichlet(np.ones(N), 20000).T
    tr = first_root(s, Q @ mu)
    rnd = float(np.min(tr))
    return best, supp, rnd


EIGVEC = np.array([[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0, 1.0], [-1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]])
EIGVAL = np.array([0.5, 0.5, -0.5, -0.5])
EC = 0.7071067811865475244008443621048490


def scip_step(s, p):
    z = np.array([s[0], s[3], s[1], s[2]]); r = np.array([p[0], p[3], p[1], p[2]])
    a = b = c = d = e = 0.0
    for i in range(4):
        vr = EC * EIGVEC[i] @ r; vz = EC * EIGVEC[i] @ z
        if EIGVAL[i] > 0:
            d += EIGVAL[i] * vz * vr; e += EIGVAL[i] * vz ** 2
        else:
            a -= EIGVAL[i] * vr ** 2; b -= 2 * EIGVAL[i] * vz * vr; c -= EIGVAL[i] * vz ** 2
    e = np.sqrt(e); d /= e
    # phi(t) = sqrt(a t^2 + b t + c) - (d t + e); first t > 0 with phi(t) = 0 (phi(0) < 0)
    if np.sqrt(a) <= d:
        return np.inf
    A2, A1, A0 = a - d * d, b - 2 * d * e, c - e * e
    if abs(A2) < 1e-300:
        return -A0 / A1 if A1 > 0 else np.inf
    disc = A1 * A1 - 4 * A2 * A0
    if disc < 0:
        return np.inf
    rts = sorted([(-A1 - np.sqrt(disc)) / (2 * A2), (-A1 + np.sqrt(disc)) / (2 * A2)])
    # keep only roots with d t + e >= 0 (on the branch sqrt(.) = d t + e)
    pos = [t for t in rts if t > 0 and d * t + e >= -1e-12]
    return pos[0] if pos else np.inf


stats = {}
for name, N in (('exp_random_N4_a.jsonl', 4), ('exp_random_N4_b.jsonl', 4), ('exp_random_N8.jsonl', 8)):
    recs = [json.loads(l) for l in open(LOGDIR + '/' + name)]
    seed = recs[0]['seed']
    byidx = {r['idx']: r for r in recs}
    rng = np.random.default_rng(seed)
    rr = np.random.default_rng(12345)
    tries = 0
    maxidx = max(byidx)
    worst_zk = 0.0; worst_rnd = 0.0; worst_scip = 0.0; nsupp_diff = 0; ninf_agree = 0; n = 0
    while tries < maxidx:
        tries += 1
        s = rng.normal(size=4)
        if det4(s) <= 0:
            continue
        P = rng.normal(size=(4, N))
        w = rng.uniform(0.2, 2.0, N)
        r = byidx.get(tries)
        if r is None:
            print('MISSING idx', tries, name)
            continue
        zk, supp, rnd = zk_indep(s, P, w, rr)
        if r['zK'] is None:
            ninf_agree += (not np.isfinite(zk))
            continue
        n += 1
        worst_zk = max(worst_zk, abs(zk - r['zK']) / r['zK'])
        worst_rnd = max(worst_rnd, (r['zK'] - rnd) / r['zK'])     # > 0 would mean a better random direction
        if sorted(supp) != sorted(r['support']):
            nsupp_diff += 1
        zs = min(w[j] * scip_step(s, P[:, j]) for j in range(N))
        worst_scip = max(worst_scip, abs(min(zs, r['zK']) / r['zK'] - r['ratios']['scip']))
    print('%s: %d finite corners; max rel |zK_indep - zK_log| = %.2e; max (zK_log - best random direction)/zK = %.2e;'
          ' support disagreements %d; infinite-zK records confirmed infinite: %d; max |scip ratio (literal C formula) - log| = %.2e'
          % (name, n, worst_zk, worst_rnd, nsupp_diff, ninf_agree, worst_scip), flush=True)

# recompute the summary statistics
A = 1 - 1e-5
for label, files in (('N = 4', ['exp_random_N4_a.jsonl', 'exp_random_N4_b.jsonl']), ('N = 8', ['exp_random_N8.jsonl'])):
    recs = [json.loads(l) for f in files for l in open(LOGDIR + '/' + f)]
    recs = [r for r in recs if r.get('zK') is not None]
    sup = [len(r['support']) for r in recs]
    print('%s: %d corners; supports 1/2/3+: %d/%d/%d; support-2 tangent (|cos|<1e-6): %d' % (
        label, len(recs), sup.count(1), sup.count(2), sum(x >= 3 for x in sup),
        sum(1 for r in recs if len(r['support']) == 2 and r['tangent_cos'] < 1e-6)))
    for fam in ('scip', 'bcm', 'pr', 'orbit'):
        x = np.array([r['ratios'][fam] for r in recs])
        s2 = np.array([len(r['support']) == 2 for r in recs])
        print('  %-5s attains %d (support 2: %d of %d); mean %.3f median %.3f q10 %.3f min %.3f' % (
            fam, (x >= A).sum(), ((x >= A) & s2).sum(), s2.sum(), x.mean(), np.median(x), np.quantile(x, 0.1), x.min()))
    miss = sorted(r['ratios']['orbit'] for r in recs if r['ratios']['orbit'] < A)
    print('  orbit misses:', [round(v, 5) for v in miss])
    # orbit ratio upper (bisection) for the misses vs lower
