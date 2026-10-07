"""Sanity tests of own_ia.py (evidence for the implementation; the proof is the error analysis):
exp enclosure vs mpmath at 50 digits; row enclosures at points vs mpmath; enclosures of random
boxes contain mpmath values at random points inside; timing."""
import time, random
import numpy as np, mpmath as mp
from fractions import Fraction as Fr
from own_ia import _exp_bound, IAModel, Cert
mp.mp.dps = 50
rng = np.random.default_rng(5)
x = np.concatenate([rng.uniform(-745, 1, 20000), rng.uniform(-1, 1, 5000) * 10.0 ** rng.uniform(-20, 0, 5000),
                    np.arange(-1000, 2) * 0.34657359027997264, [0.0, -0.0, 1.0, -700.0, -699.9999]])
x = x[x <= 1]
lo, hi = _exp_bound(x, False), _exp_bound(x, True)
bad = 0; wmax = 0
for xi, l, h in zip(x, lo, hi):
    e = mp.exp(mp.mpf(float(xi)))
    bad += not (mp.mpf(float(l)) <= e <= mp.mpf(float(h)))
    if xi > -690: wmax = max(wmax, float((mp.mpf(float(h)) - mp.mpf(float(l))) / e))
print(f"exp enclosure: {len(x)} arguments, violations {bad}, max relative width {wmax:.3g}")
M = IAModel()
O = M.O
rnd = random.Random(2)
bad = 0; wmax = 0
for t in range(30):
    p = np.array([rnd.uniform(float(O.vlb[i]), float(O.vub[i])) if not O.vint[i] else float(rnd.randint(int(O.vlb[i]), int(O.vub[i]))) for i in range(7)])
    hl, hh = M.rows(p[None], p[None], np.arange(28)[None], 0)
    for k in range(28):
        v = -O.eval_struct(k, [mp.mpf(float(q)) for q in p])
        bad += not (mp.mpf(float(hl[0, k])) <= v <= mp.mpf(float(hh[0, k])))
        wmax = max(wmax, float(hh[0, k] - hl[0, k]) / (1 + abs(float(v))))
print(f"point enclosures: 30 points x 28 rows, violations {bad}, max width/(1+|h|) {wmax:.3g}")
# random boxes
bad = 0
N = 64
clo = np.array([[rnd.uniform(float(O.vlb[i]), float(O.vub[i])) for i in range(4)] for _ in range(N)])
w = np.array([[rnd.uniform(0, 0.05) for i in range(4)] for _ in range(N)])
ilo = np.array([[float(rnd.randint(int(O.vlb[i]), int(O.vub[i]) - 2)) for i in range(4, 7)] for _ in range(N)])
lo = np.hstack([clo, ilo]); hi = np.hstack([clo + w, ilo + 2])
t0 = time.time(); hl, hh, gl, gh = M.bounds(lo, hi, np.tile(np.arange(28), (N, 1))); dt = time.time() - t0
for b in range(N):
    for s in range(3):
        p = [lo[b, i] + rnd.random() * (hi[b, i] - lo[b, i]) if i < 4 else float(rnd.randint(int(lo[b, i]), int(hi[b, i]))) for i in range(7)]
        for k in range(28):
            v = -O.eval_struct(k, [mp.mpf(q) for q in p])
            bad += not (mp.mpf(float(hl[b, k])) <= v <= mp.mpf(float(hh[b, k])))
print(f"box enclosures: {N} boxes x 3 points x 28 rows, violations {bad}; bounds() time for {N} boxes {dt:.2f}s")
C = Cert("5.642100574331458")
t0 = time.time(); st, mg, k, sm = C.test(lo, hi); print("test() time", time.time() - t0, "status counts", np.bincount(st + 1))

# derivative enclosures: gradient and Hessian at random points vs mpmath numerical differentiation
bad = 0
ridx = np.tile(np.arange(28), (8, 1))
out = M.rows(lo[:8], hi[:8], ridx, 2)
gl, gh, Hl, Hh = out[2], out[3], out[4], out[5]
mp.mp.dps = 40
for b in range(8):
    p = [mp.mpf(lo[b, i] + rnd.random() * (hi[b, i] - lo[b, i])) for i in range(7)]
    for k in (0, 5, 11, 24, 27):
        f = lambda *x: -O.eval_struct(k, list(x))
        for i in range(7):
            o = [0] * 7; o[i] = 1
            g = mp.diff(f, p, tuple(o))
            bad += not (mp.mpf(float(gl[b, k, i])) <= g <= mp.mpf(float(gh[b, k, i])))
            for j in range(i, 7):
                o2 = [0] * 7; o2[i] += 1; o2[j] += 1
                hval = mp.diff(f, p, tuple(o2))
                bad += not (mp.mpf(float(Hl[b, k, i, j])) <= hval <= mp.mpf(float(Hh[b, k, i, j])))
                bad += not (mp.mpf(float(Hl[b, k, j, i])) <= hval <= mp.mpf(float(Hh[b, k, j, i])))
print(f"gradient/Hessian enclosures over 8 boxes at random interior points, 5 rows: violations {bad}")
