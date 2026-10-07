"""Campaign 4, Part S: the star oracle at scale.

Generates random constrained quadratic stars with a fixed generator and fixed
seeds, and times two exact oracles on each:

  * sweep_star     -- the O((m+k) log(m+k)) reference sweep of
                      ../../verification/M3_star_sweep.py;
  * support_star   -- the inherited oracle of
                      research-20261002-convexification/theory/quadratic_star.py
                      (imported read-only; no bytecode is written).

Problem (all data exact Fractions; M3_star_sweep.py notation):
    min a0 + a1*y + a2*y^2 + sum_i [d_i x_i^2 + (e_i y + f_i) x_i]
    s.t. ly <= y <= uy, center-only rows p*y <= c, l_i <= x_i <= u_i,
         two center-leaf rows p*y + b*x_i <= c (p != 0, b != 0) per leaf.

Generator (one random.Random per instance, seeded with the string
"campaign-v4-star:<k>:<index>"): objective coefficients a0, a1, a2, d_i, e_i,
f_i and row coefficients p, b are n/q with n uniform in [-9, 9] (nonzero for
p and b) and q uniform in [1, 4], so both signs and zero leaf curvature occur.
The center box is [ly, ly + w] with ly = n/q, n in [-16, 16], q in [1, 4],
and w in {2, 17/8, ..., 4}.  One to three center-only rows each cut the box
from above (y <= t, t in the top quarter or above uy) or from below (y >= t,
t in the bottom quarter or below ly).  Each leaf box is [l, l + v] with
l in {-3, -23/8, ..., 3} and v in {1/2, 5/8, ..., 3}.  Each leaf has two
rows, and both hold, with slack in {0, 1/16, ..., 1}, at the two ends of an
anchor segment from (ly, xa) to (uy, xb) with xa, xb on the grid
l + v*{0, 1/8, ..., 1}.  Every leaf polygon therefore projects onto the whole
center box, so every instance is feasible and the center interval does not
shrink as k grows.

For each instance the script records CPU and wall time of each oracle (the
inherited oracle's time excludes building its dense input), whether the two
minimum values are exactly equal, the number of center-partition pieces of
each oracle, the bit lengths of the minimum's numerator and denominator, and
an exact check that the sweep's minimizer is feasible and attains its value.
The inherited oracle is skipped at a k where its time, extrapolated
quadratically from the slowest run at the previous k, exceeds SKIP_SECONDS.

Usage: python star_bench.py   (writes star-bench.json next to this file and
prints the Markdown tables).  Single-threaded pure Python.
"""
import sys
sys.dont_write_bytecode = True

import json
import os
import platform
import random
import statistics
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
REPO = PAPER.parent
sys.path.insert(0, str(PAPER / "verification"))
sys.path.insert(0, str(REPO / "research-20261002-convexification" / "theory"))
from M3_star_sweep import sweep_star  # noqa: E402
from quadratic_star import support_star  # noqa: E402

KS = (10, 100, 1000, 10000)
INSTANCES = 5
ROWS_PER_LEAF = 2
SKIP_SECONDS = 600
OUT = HERE / "star-bench.json"


# ---------------------------------------------------------------- generator
def rq(rng, a, den):
    return F(rng.randint(-a, a), rng.randint(1, den))


def nonzero(rng, a, den):
    return F(rng.choice([v for v in range(-a, a + 1) if v]), rng.randint(1, den))


def generate(k, index):
    rng = random.Random(f"campaign-v4-star:{k}:{index}")
    ly = rq(rng, 16, 4)
    uy = ly + F(rng.randint(16, 32), 8)
    width = uy - ly
    center_rows = []
    for _ in range(rng.randint(1, 3)):
        p = nonzero(rng, 9, 4)
        t = ly + width * F(rng.randint(12, 18) if p > 0 else rng.randint(-2, 4), 16)
        center_rows.append((p, p * t))  # p > 0: y <= t;  p < 0: y >= t
    center = dict(ly=ly, uy=uy, a0=rq(rng, 9, 4), a1=rq(rng, 9, 4), a2=rq(rng, 9, 4),
                  rows=center_rows)
    leaves = []
    for _ in range(k):
        l = F(rng.randint(-24, 24), 8)
        u = l + F(rng.randint(4, 24), 8)
        xa = l + (u - l) * F(rng.randint(0, 8), 8)
        xb = l + (u - l) * F(rng.randint(0, 8), 8)
        rows = []
        for _ in range(ROWS_PER_LEAF):
            p, b = nonzero(rng, 9, 4), nonzero(rng, 9, 4)
            c = max(p * ly + b * xa, p * uy + b * xb) + F(rng.randint(0, 16), 16)
            rows.append((p, b, c))
        leaves.append(dict(l=l, u=u, d=rq(rng, 9, 4), e=rq(rng, 9, 4), f=rq(rng, 9, 4),
                           rows=rows))
    return center, leaves


# ---------------------------------------------------------------- oracles
def inherited_input(center, leaves):
    """Dense (bounds, rows, coefficients) for support_star, center index 0."""
    n = 1 + len(leaves)
    zero = F(0)
    bounds = [(center["ly"], center["uy"])] + [(lf["l"], lf["u"]) for lf in leaves]
    rows = []
    for p, c in center["rows"]:
        a = [zero] * n
        a[0] = p
        rows.append((a, c))
    coefficients = {}

    def put(entries, value):
        exponent = [0] * n
        for i, e in entries:
            exponent[i] = e
        key = tuple(exponent)
        coefficients[key] = coefficients.get(key, zero) + value

    put([], center["a0"])
    put([(0, 1)], center["a1"])
    put([(0, 2)], center["a2"])
    for i, lf in enumerate(leaves, start=1):
        for p, b, c in lf["rows"]:
            a = [zero] * n
            a[0], a[i] = p, b
            rows.append((a, c))
        put([(i, 2)], lf["d"])
        put([(i, 1)], lf["f"])
        put([(0, 1), (i, 1)], lf["e"])
    return bounds, rows, coefficients


def attains(center, leaves, value, point):
    """Exact check that point is feasible and has objective value `value`."""
    y, xs = point[0], point[1:]
    feasible = center["ly"] <= y <= center["uy"] and all(p * y <= c for p, c in center["rows"])
    objective = center["a0"] + center["a1"] * y + center["a2"] * y * y
    for lf, x in zip(leaves, xs):
        feasible = feasible and lf["l"] <= x <= lf["u"] and all(
            p * y + b * x <= c for p, b, c in lf["rows"])
        objective += lf["d"] * x * x + (lf["e"] * y + lf["f"]) * x
    return feasible and objective == value


def timed(fn, *args):
    cpu, wall = time.process_time(), time.perf_counter()
    out = fn(*args)
    return out, time.process_time() - cpu, time.perf_counter() - wall


# ---------------------------------------------------------------- benchmark
def run():
    records = []
    previous = None  # (k, slowest inherited CPU seconds) of the last k where it ran
    for k in KS:
        estimate = None if previous is None else previous[1] * (k / previous[0]) ** 2
        run_inherited = estimate is None or estimate <= SKIP_SECONDS
        slowest = 0.0
        for index in range(INSTANCES):
            center, leaves = generate(k, index)
            sw, sw_cpu, sw_wall = timed(sweep_star, center, leaves)
            assert sw is not None, "generator produced an empty star"
            value = sw["value"]
            rec = dict(
                k=k, index=index, center_rows=len(center["rows"]),
                leaf_rows=sum(len(lf["rows"]) for lf in leaves),
                center_interval=[str(v) for v in sw["interval"]],
                value=str(value), value_num_bits=value.numerator.bit_length(),
                value_den_bits=value.denominator.bit_length(),
                sweep_pieces=sw["pieces"], sweep_cpu=sw_cpu, sweep_wall=sw_wall,
                sweep_point_attains=attains(center, leaves, value, sw["point"]),
            )
            if run_inherited:
                args = inherited_input(center, leaves)
                res, cpu, wall = timed(support_star, *args, 0)
                assert res["status"] == "complete", res["status"]
                rec.update(inherited_pieces=len(res["pieces"]), inherited_cpu=cpu,
                           inherited_wall=wall, equal=F(res["bound"]) == value)
                del res, args
                slowest = max(slowest, cpu)
            else:
                rec.update(inherited_pieces=None, inherited_cpu=None, inherited_wall=None,
                           equal=None, inherited_skipped=(
                               f"extrapolated CPU time {estimate:.0f} s > {SKIP_SECONDS} s"))
            records.append(rec)
            print(json.dumps(rec), flush=True)
        if run_inherited:
            previous = (k, slowest)
    return records


def fmt_time(t):
    return "skipped" if t is None else f"{t:.3g}"


def tables(records):
    head = ("| k | inst. | rows (center-leaf + center) | pieces sweep | pieces inherited "
            "| sweep CPU s | inherited CPU s | equal | min bits (num/den) | sweep point attains |\n"
            "|---:|---:|---:|---:|---:|---:|---:|:---:|---:|:---:|")
    lines = [head]
    for r in records:
        eq = "-" if r["equal"] is None else ("yes" if r["equal"] else "NO")
        lines.append(
            f"| {r['k']} | {r['index']} | {r['leaf_rows']} + {r['center_rows']} | {r['sweep_pieces']} "
            f"| {'-' if r['inherited_pieces'] is None else r['inherited_pieces']} "
            f"| {fmt_time(r['sweep_cpu'])} | {fmt_time(r['inherited_cpu'])} | {eq} "
            f"| {r['value_num_bits']}/{r['value_den_bits']} "
            f"| {'yes' if r['sweep_point_attains'] else 'NO'} |")
    summary = ["| k | median pieces sweep | median pieces inherited | median sweep CPU s "
               "| median inherited CPU s | values equal |",
               "|---:|---:|---:|---:|---:|---:|"]
    med = statistics.median
    for k in KS:
        rs = [r for r in records if r["k"] == k]
        ran = [r for r in rs if r["equal"] is not None]
        inh_pieces = f"{med(r['inherited_pieces'] for r in ran):g}" if ran else "-"
        inh_cpu = fmt_time(med(r["inherited_cpu"] for r in ran) if ran else None)
        equal = f"{sum(r['equal'] for r in ran)}/{len(ran)}" if ran else "not run"
        summary.append(
            f"| {k} | {med(r['sweep_pieces'] for r in rs):g} | {inh_pieces} "
            f"| {med(r['sweep_cpu'] for r in rs):.3g} | {inh_cpu} | {equal} |")
    return "\n".join(lines), "\n".join(summary)


def main():
    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    load = os.getloadavg()
    records = run()
    detail, summary = tables(records)
    OUT.write_text(json.dumps(dict(
        protocol="campaign-v4-protocol.md, Part S", script="star_bench.py",
        started=started, finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        python=sys.version, platform=platform.platform(), load_at_start=load,
        ks=KS, instances=INSTANCES, rows_per_leaf=ROWS_PER_LEAF, skip_seconds=SKIP_SECONDS,
        records=records), indent=1) + "\n")
    print(summary)
    print()
    print(detail)


if __name__ == "__main__":
    main()
