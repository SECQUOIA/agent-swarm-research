"""Review r2: independent margins of the rounded adversarial corners (note Section 7.3).
Rounds sbar and V with limit_denominator(10^4) (as certify_ratio.py does), computes the grazing,
second-order and apex margins exactly from the definitions in the adversarial.py docstring, and the
KKT multipliers nu_3, nu_4 from an own 40-digit minimizer of the two-ray problem on rays {1, 2}
(golden section over the edge direction + exact quadratic root).  Also compares the two-ray cost
with the exact lower bound zK_lower_exact of certify_ratio_adv_*.log and with single rays and the
other pairs.  Usage: python3 r2_margins.py LOGDIR"""
import sys, json, itertools
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 40

def det(s): return s[0]*s[3] - s[1]*s[2]
def B(s, t): return (s[0]*t[3] + s[3]*t[0] - s[1]*t[2] - s[2]*t[1]) / 2

def first_root(sb, q):
    a, b, c = det(q), 2*B(sb, q), det(sb)          # det(sb + t q) = c + b t + a t^2
    roots = []
    if abs(a) < mp.mpf(10)**-35:
        if b < 0: roots = [-c/b]
    else:
        disc = b*b - 4*a*c
        if disc >= 0:
            r1, r2 = (-b - mp.sqrt(disc))/(2*a), (-b + mp.sqrt(disc))/(2*a)
            roots = [r for r in (r1, r2) if r > 0]
    return min(roots) if roots else mp.inf

def two_ray(sb, p, q):
    f = lambda th: first_root(sb, [th*x + (1-th)*y for x, y in zip(p, q)])
    # coarse scan then golden section
    grid = [mp.mpf(i)/400 for i in range(401)]
    vals = [f(t) for t in grid]
    i = min(range(401), key=lambda k: vals[k])
    lo, hi = grid[max(i-1, 0)], grid[min(i+1, 400)]
    gr = (mp.sqrt(5) - 1)/2
    for _ in range(160):
        a, b = hi - gr*(hi - lo), lo + gr*(hi - lo)
        if f(a) < f(b): hi = b
        else: lo = a
    th = (lo + hi)/2
    return f(th), th

LOG = sys.argv[1]
for tag in ('m01_s1', 'm01_s2', 'm05_s1'):
    certs = {json.loads(l)['start']: json.loads(l) for l in open('%s/certify_ratio_adv_%s.log' % (LOG, tag))}
    for line in open('%s/adversarial_%s.jsonl' % (LOG, tag)):
        r = json.loads(line)
        if 'V' not in r: continue
        sbF = [Fr(x).limit_denominator(10**4) for x in r['sbar']]
        VF = [[Fr(x).limit_denominator(10**4) for x in v] for v in r['V']]
        PF = [[v[i] - sbF[i] for i in range(4)] for v in VF]
        ds = det(sbF)
        graze = [abs(B(sbF, p)**2 - ds*det(p)) / (B(sbF, p)**2 + abs(ds*det(p))) for p in PF]
        dvec = [VF[0][i] - VF[1][i] for i in range(4)]
        dd, Bd = det(dvec), B(dvec, sbF)
        second = dd*ds/(Bd*Bd + dd*ds) if dd > 0 else Fr(-1)
        apex = ds / max(abs(det(p)) + abs(B(sbF, p)) for p in PF)
        sb = [mp.mpf(x.numerator)/x.denominator for x in sbF]
        P = [[mp.mpf(x.numerator)/x.denominator for x in p] for p in PF]
        tau, th = two_ray(sb, P[0], P[1])
        lam1, lam2 = tau*th, tau*(1-th)
        t0 = [s + lam1*a + lam2*b for s, a, b in zip(sb, P[0], P[1])]
        g = [t0[3], -t0[2], -t0[1], t0[0]]
        gp = [sum(x*y for x, y in zip(g, p)) for p in P]
        sig = -1/gp[0]
        nu = [1 + sig*x for x in gp]
        singles = [first_root(sb, p) for p in P]
        pairs = {pq: two_ray(sb, P[pq[0]], P[pq[1]])[0] for pq in itertools.combinations(range(4), 2) if pq != (0, 1)}
        zlo = Fr(certs[r['start']]['zK_lower_exact'])
        m = [float(x) for x in graze] + [float(nu[2]), float(nu[3]), float(second), float(apex)]
        print('%s start %3d: cost{1,2} %.12f (zlo %.10f, ratio %.9f) lam (%.4f, %.4f) gp1-gp2 %.1e | min single %.4f, min other pair %.4f'
              % (tag, r['start'], tau, float(zlo), float(tau/mp.mpf(zlo.numerator)*zlo.denominator), lam1, lam2,
                 float(gp[0]-gp[1]), float(min(singles)), float(min(pairs.values()))))
        print('     margins graze %s nu3 %.6f nu4 %.6f second %.6f apex %.6f -> min %.6f'
              % (['%.6f' % float(x) for x in graze], float(nu[2]), float(nu[3]), float(second), float(apex), min(m)))
