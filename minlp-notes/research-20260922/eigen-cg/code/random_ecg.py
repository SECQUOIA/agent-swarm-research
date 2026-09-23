"""Randomized test of Conjecture 1 on general (rounded) Eigen-CG cuts.

Samples rational (v0, v) near 'structured' points rho*(tau, sigma) (sigma integer) plus noise,
and fully random points; computes E-CG exactly (Fractions); discards cuts that are trivially
implied (support <= 5 -> P_BH = BQP there; v0^2 integer -> implied by SDP+nonnegativity);
then minimizes the cut over P_BH(n) by cutting planes (BH pool + MIQP + exact fallback).
Usage: python random_ecg.py n nsamples nworkers seed"""
import sys, time, math, json, random
import multiprocessing as mp
from fractions import Fraction as Fr
from bh import pairs


def sample(rng, n):
    kind = rng.random()
    if kind < 0.7:
        R = rng.choice([1, 2, 3])
        sigma = [rng.choice([k for k in range(-R, R + 1) if k]) for _ in range(n)]
        rho = math.sqrt(rng.uniform(0.2, 12))
        tau = rng.uniform(-sum(abs(s) for s in sigma) / 2 - 1, sum(abs(s) for s in sigma) / 2 + 1)
        noise = rng.choice([1e-4, 1e-3, 1e-2, 0.05, 0.2])
        vh = [rho * tau] + [rho * s for s in sigma]
        vh = [t + rng.gauss(0, noise) for t in vh]
    else:
        scale = rng.choice([0.5, 1, 2, 3])
        vh = [rng.gauss(0, scale) for _ in range(n + 1)]
    vh = [Fr(round(t * 10 ** 9), 10 ** 9) for t in vh]
    if vh[0] < 0:
        vh = [-t for t in vh]
    return vh


def ecg(vh):
    v0, v = vh[0], vh[1:]
    n = len(v)
    a = [math.ceil(v[i] * v[i] + 2 * v[i] * v0) for i in range(n)]
    a += [math.ceil(2 * v[i] * v[j]) for (i, j) in pairs(n)]
    return tuple(a), math.floor(v0 * v0)


_P = None


def init(n):
    global _P
    from bh import PBH
    _P = PBH(n, W0=1, exact=True)


def work(item):
    vh, a, c = item
    try:
        val, z = _P.minimize(list(a))
    except Exception as e:
        return (float('nan'), [str(t) for t in vh], a, c, "ERROR " + repr(e))
    return (val + c, [str(t) for t in vh], a, c, _P.last_certified is not None and val + c < -1e-9)


if __name__ == "__main__":
    n, N, nw, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    seen = set()
    items = []
    t = time.time()
    while len(items) < N:
        vh = sample(rng, n)
        if any(t == 0 for t in vh[1:]):
            continue
        a, c = ecg(vh)
        if (vh[0] * vh[0]).denominator == 1:
            continue
        # support of the cut must be all n variables (else P_BH = BQP on the support)
        sup = set()
        for k, (i, j) in enumerate(pairs(n)):
            if a[n + k]:
                sup |= {i, j}
        sup |= {i for i in range(n) if a[i]}
        if len(sup) < n or all(t >= 0 for t in a):
            continue
        if (a, c) in seen:
            continue
        seen.add((a, c))
        items.append((vh, a, c))
    print("distinct nontrivial cuts:", len(items), time.time() - t, flush=True)
    res = []
    with mp.Pool(nw, initializer=init, initargs=(n,)) as pool:
        for k, r in enumerate(pool.imap_unordered(work, items, chunksize=20)):
            res.append(r)
            if r[0] < -1e-7:
                print("VIOLATION", r, flush=True)
            if k % 5000 == 0:
                print(k, time.time() - t, flush=True)
    errs = [r for r in res if r[0] != r[0]]
    print("undetermined (errors):", len(errs), errs[:3])
    res = [r for r in res if r[0] == r[0]]
    res.sort(key=lambda r: r[0])
    print("done", len(res), "min", res[0][0], "violations", sum(r[0] < -1e-7 for r in res))
    json.dump(res[:50], open(f"random_ecg_n{n}_seed{seed}.json", "w"))
