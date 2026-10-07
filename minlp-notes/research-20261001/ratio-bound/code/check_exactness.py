"""Consistency check of Theorem C (interval criterion for support-one minimizers) against the SDP
bisection for z_A, on random support-one corners with transversal edges at t*.
Instances: t* = 0, sbar and v2, v3 random with w-coordinate (= height h) > 0, rays p_j = v_j - sbar
(v1 = t* = 0), costs 1; kept if z_K = 1 with support {ray 1}.
Reports, per instance: min_alpha gap_A (<= 0 iff exact), H_cyl, z_A (certified / bisection upper value),
and the B-interval gap.  Also the threshold family of Proposition C3.  usage: python3 check_exactness.py SEED N"""
import sys
import numpy as np
import warnings
import rb
import exactness as ex

warnings.filterwarnings('ignore')
seed, nwant = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
n = agree = 0
rows = []
while n < nwant:
    V = rng.normal(size=(3, 3)) * np.exp(rng.normal(size=(3, 1)))
    V[:, 2] = np.abs(V[:, 2]) * np.exp(rng.normal(size=3))       # heights h > 0 (grad q(0) = e_w)
    sbar, v2, v3 = V
    if rb.q(sbar) <= 0:
        continue
    P = np.stack([-sbar, v2 - sbar, v3 - sbar], 1)
    if abs(np.linalg.det(P)) < 1e-6:
        continue
    c = np.ones(3)
    z, lam = rb.zK(sbar, P, c)
    if not (abs(z - 1) < 1e-9 and lam[0] > 1 - 1e-9 and lam[1] < 1e-12 and lam[2] < 1e-12):
        continue
    r = ex.analyze(sbar, P, c)
    if r is None:
        continue
    n += 1
    cert, hi, _ = rb.zA_ratio(sbar, rb.scaled_rays(P, c, z), iters=30)
    exact_int = r['gapA'] <= 0
    exact_sdp = cert >= 1 - 1e-6
    unclear = abs(r['gapA']) < 1e-6 or (1 - 1e-4 < hi < 1 - 1e-7)
    agree += (exact_int == exact_sdp) or unclear
    print('gapA=%+.4e gapB=%+.4e Hcyl=%.4f Hcrude=%.4f zA=%.6f/%.6f  interval:%s sdp:%s%s' % (
        r['gapA'], r['gapB'], r['Hcyl'], r['Hcrude'], cert, hi, 'exact' if exact_int else 'NOT', 'exact' if exact_sdp else 'NOT',
        '' if (exact_int == exact_sdp) else (' (borderline)' if unclear else ' DISAGREE')), flush=True)
    rows.append(r)
print('instances', n, 'agreeing (or borderline)', agree)
print('instances with Hcyl >= 1:', sum(r['Hcyl'] >= 1 for r in rows), '; of these exact by intervals:',
      sum(r['Hcyl'] >= 1 and r['gapA'] <= 0 for r in rows))
print('non-exact instances (gapA > 0):', sum(r['gapA'] > 0 for r in rows), '; max Hcyl among them: %.4f'
      % max([r['Hcyl'] for r in rows if r['gapA'] > 0] or [float('nan')]))
print('instances with gapB > gapA + 1e-9 (B harder than A, impossible):', sum(r['gapB'] > r['gapA'] + 1e-9 for r in rows))
