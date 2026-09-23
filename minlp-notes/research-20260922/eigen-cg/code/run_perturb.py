"""Parallel driver for the perturbation MILP search (perturb_milp.py) over exact base points
v* = rho*(tau, sigma) with sigma in {-R..R}^n \\ 0 (sorted, gcd 1), a = rho^2 = m/(2g), m <= amax,
and v0*^2 = b^2/(4a) a positive integer.  Usage: python run_perturb.py n R amax nworkers"""
import itertools, sys, time, json
import multiprocessing as mp
from f3_enum import subset_sums, b_coset, Fr, gcd, reduce, math


def bases(n, R, amax):
    for sigma in itertools.combinations_with_replacement([k for k in range(-R, R + 1) if k], n):
        if reduce(gcd, [abs(x) for x in sigma]) != 1:
            continue
        g = reduce(gcd, [abs(sigma[i] * sigma[j]) for i in range(n) for j in range(i + 1, n)])
        S_ = subset_sums(sigma)
        for m_ in range(1, amax + 1):
            a = Fr(m_, 2 * g)
            b0 = b_coset(list(sigma), a)
            if b0 is None:
                continue
            lo, hi = min(S_) - 2, max(S_) + 2
            for k in range(math.floor(-2 * a * hi - b0) - 1, math.ceil(-2 * a * lo - b0) + 2):
                b = b0 + k
                v02 = b * b / (4 * a)
                if v02.denominator != 1 or v02 == 0:
                    continue
                # BH in direction sigma give f*(z) >= a (tau - round(tau))^2 on P_BH, and the
                # perturbed cut is f*(z) - 1 + (nonneg): violation needs a (tau-k)^2 < 1.
                tau = b / (2 * a)
                kk = round(tau)
                if a * (tau - kk) ** 2 >= 1:
                    continue
                yield (list(sigma), a, b, int(v02))


_S = None


def init(n):
    global _S
    from bh import PBH
    from perturb_milp import PerturbSearch
    _S = PerturbSearch(PBH(n, W0=1))


def work(item):
    sigma, a, b, c = item
    try:
        r = _S.run(sigma, a, b, c)
    except Exception as e:  # recorded as undetermined
        return (sigma, str(a), str(b), c, "ERROR " + repr(e), None)
    hit = None
    if r and r[1] is not None:
        zv, dl, s = r[1]
        hit = dict(z=list(map(float, zv)), delta=list(map(float, dl)), S=s)
    return (sigma, str(a), str(b), c, None if r is None else r[0], hit)


if __name__ == "__main__":
    n, R, amax, nw = map(int, sys.argv[1:5])
    items = list(bases(n, R, amax))
    print("bases:", len(items), flush=True)
    t = time.time()
    out = []
    with mp.Pool(nw, initializer=init, initargs=(n,)) as pool:
        for k, res in enumerate(pool.imap_unordered(work, items, chunksize=4)):
            out.append(res)
            if res[5] is not None:
                print("HIT", res, flush=True)
            if k % 200 == 0:
                print(k, time.time() - t, flush=True)
    errs = [o for o in out if isinstance(o[4], str)]
    print("undetermined (errors):", len(errs), errs[:5])
    vals = sorted([o for o in out if o[4] is not None and not isinstance(o[4], str)], key=lambda o: o[4])
    print("done", len(out), "hits", sum(o[5] is not None for o in out), "none", sum(o[4] is None for o in out))
    print("lowest objective values:", vals[:5])
    json.dump(out, open(f"perturb_n{n}_R{R}_a{amax}.json", "w"))
