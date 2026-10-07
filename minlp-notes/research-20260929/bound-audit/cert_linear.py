"""Exact repair of a listed point for models whose rows are all linear (objective may be
quadratic): integers rounded, chosen "decision" variables held at the listed decimals,
every other variable computed exactly (Fractions) by propagation through equality rows
with a single unknown. Then every row and bound is checked in exact rational arithmetic
and the objective is evaluated exactly. No floating point enters the result.

Decision variables: by default all variables with a finite bound that are not
determined by propagation from the integers alone (for watercontamination these are the
nonnegative source variables); propagation must then determine all other variables.

Usage: python3 cert_linear.py <name>.<pk>
"""
import json
import os
import sys
from collections import defaultdict, deque
from fractions import Fraction

import audit_eval as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def main(tag):
    name = tag.rsplit(".", 1)[0]
    m = A.load(name)
    vals = A.read_sol(os.path.join(HERE, "sol", tag + ".sol"))
    names, cons = m["names"], m["cons"]
    nv = len(names)
    assert all(not c["quad"] and c["nl"] is None for c in cons), "nonlinear rows"
    x = {}
    for j in range(nv):
        if m["vt"][j] in ("B", "I"):
            x[j] = Fraction(round(Fraction(vals.get(names[j], "0"))))
        elif m["lb"][j] == m["ub"][j]:
            x[j] = Fraction(m["lb"][j])
    decision = [j for j in range(nv) if j not in x and (m["lb"][j] != "-INF" or m["ub"][j] != "INF")]
    for j in decision:
        x[j] = Fraction(vals.get(names[j], "0"))
    eq = [r for r, c in enumerate(cons) if c["lb"] == c["ub"]]
    rows_of = defaultdict(list)
    for r in eq:
        for j in cons[r]["lin"]:
            rows_of[j].append(r)
    unk = {r: set(cons[r]["lin"]) - x.keys() for r in eq}
    used = set()
    q = deque(r for r in eq if len(unk[r]) == 1)
    while q:
        r = q.popleft()
        if r in used or len(unk[r]) != 1:
            continue
        j = next(iter(unk[r]))
        c = cons[r]
        s = Fraction(c["lb"]) - Fraction(c["constant"])
        for k, a in c["lin"].items():
            if k != j:
                s -= Fraction(a) * x[k]
        x[j] = s / Fraction(c["lin"][j])
        used.add(r)
        for r2 in rows_of[j]:
            unk[r2].discard(j)
            if len(unk[r2]) == 1:
                q.append(r2)
    missing = [j for j in range(nv) if j not in x]
    out = dict(tag=tag, n_decision=len(decision), n_propagated=len(used), n_undetermined=len(missing))
    if missing:
        # variables in no equality row: keep their decimals
        free_only = [j for j in missing if not rows_of.get(j)]
        for j in free_only:
            x[j] = Fraction(vals.get(names[j], "0"))
        missing = [j for j in range(nv) if j not in x]
        out["n_undetermined"] = len(missing)
    if missing:
        out["status"] = "fail: propagation incomplete"
        print(json.dumps(out))
        return
    xs = [x[j] for j in range(nv)]
    bad = []
    for r, c in enumerate(cons):
        v = V.row_frac(c, xs)
        if not V.row_ok_frac(c, v):
            bad.append((c["name"], float(v - Fraction(c["lb"] if c["lb"] != "-INF" else c["ub"]))))
    for j in range(nv):
        if (m["lb"][j] != "-INF" and xs[j] < Fraction(m["lb"][j])) or (m["ub"][j] != "INF" and xs[j] > Fraction(m["ub"][j])):
            bad.append((names[j], "bound"))
    o = m["obj"]
    f = Fraction(o["constant"]) + sum((Fraction(cf) * xs[j] for j, cf in o["lin"].items()), Fraction(0)) \
        + sum((Fraction(cf) * xs[i] * xs[j] for i, j, cf in o["quad"]), Fraction(0))
    assert o["nl"] is None
    out.update(n_bad=len(bad), bad=bad[:10], status="proved" if not bad else "fail",
               objective_exact_30=str((f.numerator * 10 ** 30) // f.denominator) + "e-30",
               objective=float(f),
               max_change=float(max(abs(xs[j] - Fraction(vals.get(names[j], "0"))) for j in range(nv))))
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "logs", f"cert_linear_{tag}.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
