"""Driver for mc2d (review code): McCormick kink family, widest-side selection.
Runs the grid below with at most 4 processes and prints one line per entry, then summaries for
Proposition E / Conjecture E' and the keyed-randomization claim.

    python3 run_mc2d.py > run_mc2d.log
"""
import math
import subprocess
import zlib
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = __file__.rsplit("/", 1)[0]
EPS = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
A = {"1/6": 1 / 6, "3/238": 3 / 238, "0.25": 0.25, "0.1999": 0.1999, "1/3": 1 / 3, "0.0102": 0.0102}
N = 1_000_000

jobs = []
for an in ("1/6", "3/238", "0.25", "0.1999", "0.0102"):
    for rule in (("rclip", 0.1, 0.3), ("kvar", 0.1, 0.3), ("kshared", 0.1, 0.3)):
        for e in EPS:
            jobs.append((an, rule, e, N))
for rule in (("rclip", 0.05, 0.35), ("kvar", 0.05, 0.35), ("kshared", 0.05, 0.35)):
    for e in EPS:
        jobs.append(("1/3", rule, e, N))
for an in A:
    for rule in (("clip", 0.2), ("rc", 0.2)):
        for e in EPS:
            jobs.append((an, rule, e, 1))


def run(job):
    an, rule, e, n = job
    seed = zlib.crc32(repr((an, rule, e)).encode())
    cmd = [f"{HERE}/mc2d", "w", rule[0]] + [str(x) for x in rule[1:]] + [repr(A[an]), repr(e), str(n), str(seed)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.split()
    mean, sem = float(out[0]), float(out[1])
    q50, q90, q99, mx, capped = map(int, out[2:])
    return job, dict(mean=mean, sem=sem, q50=q50, q90=q90, q99=q99, max=mx, capped=capped)


res = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    for job, r in ex.map(run, jobs):
        an, rule, e, n = job
        res[(an, rule, e)] = r
        print(f"a={an:7s} {' '.join(map(str, rule)):18s} eps={e:.0e} n={n}: mean {r['mean']:.1f} +- {r['sem']:.1f}, "
              f"median {r['q50']}, q90 {r['q90']}, q99 {r['q99']}, max {r['max']}, capped {r['capped']}")
        sys.stdout.flush()

print("\nConjecture E': slope of log10(mean T) vs log10(1/eps) between 1e-4 and 1e-8")
for (an, rule, e), r in sorted(res.items()):
    if e == 1e-8 and rule[0] in ("rclip", "kvar", "kshared"):
        r4 = res[(an, rule, 1e-4)]
        s = (math.log10(r["mean"]) - math.log10(r4["mean"])) / 4
        print(f"  a={an} {rule}: {s:.3f}")

print("\nProposition E lower bound (a theta0/(2 theta1 D)) log(g theta0^1.5/eps^0.5) against simulated mean")
for an, (t0, t1) in (("1/6", (0.1, 0.3)), ("0.25", (0.1, 0.3)), ("0.1999", (0.1, 0.3)), ("1/3", (0.05, 0.35))):
    a = A[an]
    D = t1 - t0
    g = min(t0 / 2, 1 - a / t1)
    for e in EPS:
        if e < g * g * t0 ** 3:
            lb = a * t0 / (2 * t1 * D) * math.log(g * t0 ** 1.5 / math.sqrt(e))
            print(f"  a={an} [{t0},{t1}] eps={e:.0e}: bound {lb:.3f}; simulated mean {res[(an, ('rclip', t0, t1), e)]['mean']:.1f}")

print("\nKeyed randomization: independent vs keyed per (variable, interval) vs keyed shared across variables")
for (an, rule, e), r in sorted(res.items()):
    if rule[0] == "rclip":
        k1 = res[(an, ("kvar",) + rule[1:], e)]
        k2 = res[(an, ("kshared",) + rule[1:], e)]
        z = lambda k: (k["mean"] - r["mean"]) / max(math.hypot(k["sem"], r["sem"]), 1e-4)  # noqa: E731
        z1, z2 = z(k1), z(k2)
        print(f"  a={an} {rule[1:]} eps={e:.0e}: indep {r['mean']:.2f} (med {r['q50']}), kvar {k1['mean']:.2f} "
              f"(med {k1['q50']}, z={z1:+.1f}), kshared {k2['mean']:.2f} (med {k2['q50']}, z={z2:+.1f})")
