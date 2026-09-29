"""Spot checks of the SCIP experiment claims (robust-branching.md Section 6) from the raw JSONL.
Review code only; it does not import the author's summarize.py or the study's analyze.py.

    python3 check_scip.py > check_scip.log
"""
import json
import math
import os
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import wilcoxon

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "bb-complexity")
RUNS = os.path.join(BASE, "robust-branching-points", "results", "minlplib.jsonl")
OLD = os.path.join(BASE, "minlplib-branching", "results", "runs.jsonl")
SEEDS = (0, 1, 2)
SHIFT = 10.0

runs = [json.loads(line) for line in open(RUNS)]
print(f"runs: {len(runs)}; settings: {len({r['setting'] for r in runs})}; instances: {len({r['inst'] for r in runs})}")
st = defaultdict(Counter)
for r in runs:
    st[r["setting"]][r["status"]] += 1
for s in sorted(st):
    print(f"  {s:12s} {dict(st[s])}")
crashes = [(r["inst"], r["setting"], r["seed"]) for r in runs if r["status"] not in ("optimal", "timelimit")]
print(f"non-optimal non-timelimit runs: {crashes}")

# ---- reproduction of the earlier study
old = [json.loads(line) for line in open(OLD)]
O = {(r["inst"], r["setting"], r["seed"]): r for r in old if r["setting"] in ("default", "lp")}
for s in ("default", "lp"):
    both = same = 0
    diffs = []
    for r in runs:
        if r["setting"] != s:
            continue
        o = O.get((r["inst"], s, r["seed"]))
        if o and r["status"] == "optimal" and o["status"] == "optimal":
            both += 1
            if o["nodes"] == r["nodes"]:
                same += 1
            else:
                diffs.append((r["inst"], r["seed"], o["nodes"], r["nodes"]))
    print(f"reproduction {s}: optimal in both {both}, identical node counts {same}; differences {diffs[:5]}")

# ---- pairwise node ratios
D = defaultdict(dict)
for r in runs:
    D[(r["inst"], r["setting"])][r["seed"]] = r
insts = sorted({r["inst"] for r in runs})


def inst_val(i, s):
    rs = D.get((i, s), {})
    if any(k not in rs or rs[k].get("nodes") is None for k in SEEDS):
        return None, None
    v = [rs[k]["nodes"] for k in SEEDS]
    return math.exp(np.mean([math.log(x + SHIFT) for x in v])) - SHIFT, v


def compare(s, ref, subset=None):
    lr, sep_w, sep_l, rows = [], 0, 0, []
    for i in insts if subset is None else subset:
        va, xa = inst_val(i, s)
        vb, xb = inst_val(i, ref)
        if va is None or vb is None:
            continue
        lr.append(math.log((va + SHIFT) / (vb + SHIFT)))
        sep_w += max(xa) + SHIFT < (min(xb) + SHIFT) / 1.1
        sep_l += min(xa) + SHIFT > 1.1 * (max(xb) + SHIFT)
        rows.append((i, va, vb))
    lr = np.array(lr)
    rng = np.random.default_rng(424242)
    bs = np.exp(np.sort(rng.choice(lr, size=(20000, lr.size), replace=True).mean(axis=1)))
    ci = (bs[int(0.025 * bs.size)], bs[int(0.975 * bs.size)])
    p = wilcoxon(lr[np.abs(lr) > 1e-12]).pvalue
    # alternative definition: ratio of shifted geometric means over instances
    sgm = lambda v: math.exp(np.mean([math.log(x + SHIFT) for x in v])) - SHIFT  # noqa: E731
    alt = sgm([r[1] for r in rows]) / sgm([r[2] for r in rows])
    wins = int((lr < -math.log(1.1)).sum())
    losses = int((lr > math.log(1.1)).sum())
    return dict(n=lr.size, ratio=math.exp(lr.mean()), ci=ci, p=p, wins=wins, losses=losses, sep=(sep_w, sep_l),
                alt=alt)


PAIRS = [("rclamp", "default"), ("c10", "default"), ("rclamp", "c10"), ("lp_rclamp", "lp"), ("lp", "default"),
         ("x_default", "default"), ("x_rclamp", "x_default"), ("x_lp_rclamp", "x_lp"), ("x_recenter", "x_lp"),
         ("x_inc", "x_lp"), ("x_noclamp", "x_lp"), ("x_recenter", "default"), ("x_recenter", "x_default")]
print("\nnode ratios (per-instance SGM over seeds, shift 10; exp mean log((a+10)/(b+10)); bootstrap 20000; scipy Wilcoxon)")
for s, ref in PAIRS:
    c = compare(s, ref)
    print(f"  {s:11s} / {ref:9s}: n={c['n']}, ratio {c['ratio']:.3f} (CI {c['ci'][0]:.2f}-{c['ci'][1]:.2f}), "
          f"p = {c['p']:.3g}, wins/losses {c['wins']}/{c['losses']}, separated {c['sep'][0]}/{c['sep'][1]}; "
          f"ratio of SGMs over instances {c['alt']:.3f}")

# ---- plugin counters
print("\nplugin counters")
for s in ("x_lp", "x_recenter", "x_inc", "x_noclamp"):
    t = Counter()
    for r in runs:
        if r["setting"] == s and "plugin" in r:
            t.update(r["plugin"])
    print(f"  {s}: cont {t['cont']}, lp_at_bound {t['lp_at_bound']} ({t['lp_at_bound'] / t['cont']:.1%}), "
          f"moved {t['clamped']} ({t['clamped'] / t['cont']:.1%}), recentred {t['recentred']} "
          f"({t['recentred'] / t['cont']:.1%}), inc {t['inc']}, child<1% {t['small_child']} "
          f"({t['small_child'] / t['cont']:.1%})")

# ---- synthetic sanity: statuses and eps
syn = [json.loads(line) for line in open(os.path.join(BASE, "robust-branching-points", "results", "synthetic.jsonl"))]
print(f"\nsynthetic runs: {len(syn)}; statuses {Counter(r['status'] for r in syn)}; "
      f"known optimum accepted in all: {all(r.get('knownopt_accepted') for r in syn)}; "
      f"max dual > 1e-9 below 0: {sum((r.get('dual') or 0) < -1e-9 - (r['eps'] or 0) for r in syn)}; "
      f"max primal: {max(abs(r.get('primal') or 0) for r in syn):.2e}")
gaps = [(r["primal"] - r["dual"]) for r in syn if r.get("primal") is not None and r.get("dual") is not None]
viol = sum((r["primal"] - r["dual"]) > r["eps"] * (1 + 1e-9) for r in syn
           if r.get("primal") is not None and r.get("dual") is not None)
print(f"  runs with primal - dual > eps: {viol}")
