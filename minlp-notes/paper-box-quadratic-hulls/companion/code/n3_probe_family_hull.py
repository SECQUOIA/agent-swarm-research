"""Probe: random points of PSD+RLT+TRI that satisfy all 24 family orientations
(StQP >= -tol) but lie outside QPB3 (hull depth < -dtol).
Sampling as in hardobj.py: x ~ U[0,1]^3, Y = xx' + G G', G ~ N(0, s^2) (3 x r).
Usage: python n3_probe_family_hull.py nbatches batchsize seed out.json"""
import sys, json, time
import numpy as np
sys.path.insert(0, '.')
from relax import family_AB, stqp_min, ORIENTS
import hullsep

def batch(rng, N):
    x = rng.random((N, 3))
    r = rng.integers(1, 4, size=N)
    s = rng.uniform(0.05, 0.5, size=N)
    G = rng.normal(size=(N, 3, 3)) * s[:, None, None]
    G = G * (np.arange(3)[None, None, :] < r[:, None, None])   # rank r
    Y = x[:, :, None] * x[:, None, :] + G @ G.transpose(0, 2, 1)
    tol = 1e-9
    ok = np.ones(N, bool)
    for i in range(3):
        ok &= Y[:, i, i] <= x[:, i] + tol
        for j in range(i + 1, 3):
            ok &= (Y[:, i, j] >= -tol) & (Y[:, i, j] >= x[:, i] + x[:, j] - 1 - tol) & (Y[:, i, j] <= np.minimum(x[:, i], x[:, j]) + tol)
    ok &= Y[:, 0, 1] + Y[:, 0, 2] - x[:, 0] - Y[:, 1, 2] <= tol
    ok &= Y[:, 0, 1] + Y[:, 1, 2] - x[:, 1] - Y[:, 0, 2] <= tol
    ok &= Y[:, 0, 2] + Y[:, 1, 2] - x[:, 2] - Y[:, 0, 1] <= tol
    ok &= x.sum(1) - Y[:, 0, 1] - Y[:, 0, 2] - Y[:, 1, 2] - 1 <= tol
    return x[ok], Y[ok]

def main():
    nb, bs, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = np.random.default_rng(seed)
    T = np.array([[0, 1, 2]])
    stats = {'sampled': 0, 'rlt_tri': 0, 'family_feasible': 0, 'family_violated': 0, 'tested': 0,
             'outside_hull': 0, 'min_depth': 0.0, 'examples': []}
    for b in range(nb):
        x, Y = batch(rng, bs)
        stats['sampled'] += bs
        stats['rlt_tri'] += len(x)
        worst = np.full(len(x), np.inf)
        for o in ORIENTS:
            bv, B = family_AB_batch(x, Y, o)
            A = B - bv[:, :, None] * bv[:, None, :]
            val, _ = stqp_min(A)
            worst = np.minimum(worst, val)
        feas = worst >= -1e-9
        stats['family_feasible'] += int(feas.sum())
        stats['family_violated'] += int((~feas).sum())
        for t in np.nonzero(feas)[0]:
            M = np.block([[np.ones((1, 1)), x[t][None]], [x[t][:, None], Y[t]]])
            d, C, st = hullsep.depth(M)
            stats['tested'] += 1
            stats['min_depth'] = min(stats['min_depth'], d)
            if d < -1e-6:
                stats['outside_hull'] += 1
                if len(stats['examples']) < 20:
                    stats['examples'].append({'x': x[t].tolist(), 'Y': Y[t].tolist(), 'depth': d})
        json.dump(stats, open(out, 'w'))

def family_AB_batch(x, Y, o):
    # family_AB takes a single (x, Y) and triple rows; emulate a batch by stacking
    N = len(x)
    c, s = o
    a, b = [r for r in range(3) if r != c]
    m = x.copy(); M2 = Y.copy()
    for k in range(3):
        if s[k]:
            mk = m[:, k].copy()
            for l in range(3):
                if l == k: continue
                M2[:, k, l] = m[:, l] - M2[:, k, l]; M2[:, l, k] = M2[:, k, l]
            M2[:, k, k] = 1 - 2 * mk + M2[:, k, k]
            m[:, k] = 1 - mk
    mx, my, mz = m[:, a], m[:, b], m[:, c]
    yxx, yyy, yzz = M2[:, a, a], M2[:, b, b], M2[:, c, c]
    yxy, yxz, yyz = M2[:, a, b], M2[:, a, c], M2[:, b, c]
    bv = np.stack([-mx, -my, mz, -yxy], 1)
    e34 = mz - yxz - yyz
    B = np.empty((N, 4, 4))
    B[:, 0] = np.stack([yxx, yxy, -yxz, yxy], 1)
    B[:, 1] = np.stack([yxy, yyy, -yyz, yxy], 1)
    B[:, 2] = np.stack([-yxz, -yyz, yzz, e34], 1)
    B[:, 3] = np.stack([yxy, yxy, e34, yxy], 1)
    return bv, B

if __name__ == '__main__':
    main()
