"""How close does the C search of rule 1 (corner bound) get to the best lambda of SCIP's family?

For dumped corners with dim(lambda) = 2 and at most NMAX rays, scan the whole unit circle (NANG angles, then
golden-section refinement around the best angle) with the independent reference step lengths of check_dump.py
(bisection on the membership function), and compare the best corner bound found with the C choice.

Usage: python3 search_optimality.py DUMPFILE [MAXCORNERS] [NMAX] [NANG]
"""
import sys, os, json, gzip
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_dump import Corner   # noqa: E402


def crit(c, lam, wt):
    if not c.G(lam, c.sbar) < 0:
        return -np.inf
    al = [c.step(lam, c.P[:, j]) for j in range(c.P.shape[1])]
    v = [wt[j] * al[j] for j in range(len(al)) if np.isfinite(al[j])]
    return min(v) if v else np.inf


def main():
    path = sys.argv[1]
    maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    nang = int(sys.argv[4]) if len(sys.argv) > 4 else 360
    ratios, ratios0, outside = [], [], 0
    for line in (gzip.open(path, "rt") if path.endswith(".gz") else open(path)):
        d = json.loads(line.replace("-nan", "NaN").replace("nan", "NaN"))
        if d['type'] != 'corner' or d['dim'] != 2 or len(d['rays']) > nmax or d['rule'] != 1:
            continue
        c = Corner(d)
        wt = np.maximum(c.w, 1e-6 * max(c.w.max(), 1e-9))
        lam0 = np.array(d['lam0']); lamC = np.array(d['lam'])
        fC = crit(c, lamC, wt); f0 = crit(c, lam0, wt)
        th = np.linspace(-np.pi, np.pi, nang, endpoint=False)
        vals = np.array([crit(c, np.array([np.cos(t), np.sin(t)]), wt) for t in th])
        k = int(np.argmax(vals)); lo, hi = th[k] - 2 * np.pi / nang, th[k] + 2 * np.pi / nang
        g = (np.sqrt(5) - 1) / 2
        f = lambda t: crit(c, np.array([np.cos(t), np.sin(t)]), wt)
        for _ in range(30):
            m1, m2 = hi - g * (hi - lo), lo + g * (hi - lo)
            if f(m1) >= f(m2):
                hi = m2
            else:
                lo = m1
        tb = 0.5 * (lo + hi); fb = max(vals[k], f(tb))
        if not np.isfinite(fb) or fb <= 0:
            continue
        # is the best angle outside the half circle searched in C (|angle to lam0| < pi/2)?
        lb = np.array([np.cos(tb), np.sin(tb)])
        if lb @ lam0 <= 0:
            outside += 1
        ratios.append(min(fC, fb) / fb); ratios0.append(min(f0, fb) / fb)
        print(json.dumps(dict(n=len(d['rays']), f0=f0, fC=fC, fbest=fb, ratio_C=ratios[-1], ratio_scip=ratios0[-1])),
              flush=True)
        if len(ratios) >= maxc:
            break
    r = np.array(ratios); r0 = np.array(ratios0)
    print('SUMMARY', json.dumps(dict(n=len(r), C_mean=float(r.mean()), C_min=float(r.min()),
                                     C_within_1em4=int((r > 1 - 1e-4).sum()), scip_mean=float(r0.mean()),
                                     scip_within_1em4=int((r0 > 1 - 1e-4).sum()), best_outside_halfcircle=outside)))


if __name__ == '__main__':
    main()
