"""Evidence: inequality slacks of MINLPLib's p1 under the reviewer's OSIL reader, the two
smallest groups, and rows whose variables are all fixed but carry quadratic terms."""
import json, os, sys
from fractions import Fraction as Fr
import dyiv as V
import osil_read
from verify import Evaluator, OSIL, SOL, PTS

for name in sys.argv[1:]:
    M = osil_read.read(os.path.join(OSIL, name + ".osil"))
    names, cons = M["names"], M["cons"]
    p1 = {}
    for line in open(os.path.join(SOL, name + ".p1.sol")):
        p = line.split()
        if len(p) == 2:
            p1[p[0]] = p[1]
    E = Evaluator([V.of_frac(Fr(p1.get(v, "0"))) for v in names], False)
    sl = []
    for c in cons:
        if c["lb"] is not None and c["lb"] == c["ub"]:
            continue
        v, _ = E.body(c)
        mid = Fr(v[0] + v[1], 2 * V.ONE)
        for side in ("lb", "ub"):
            b = c[side]
            if b is not None:
                s = (mid - b) if side == "lb" else (b - mid)
                sl.append((s, c["name"], side, sorted(names[j] for j in osil_read.row_vars(c))))
    sl.sort()
    act = [t for t in sl if t[0] < Fr(1, 10**9)]
    print(name, "active (<1e-9):", [(t[1], t[2], f"{float(t[0]):.1e}", t[3] if len(t[3]) < 3 else len(t[3])) for t in act])
    rest = [t for t in sl if t[0] >= Fr(1, 10**9)]
    print("  smallest inactive slack:", f"{float(rest[0][0]):.4e}", rest[0][1], rest[0][2])
    P = json.load(open(os.path.join(PTS, name + ".json")))
    fixed = set(P["fixed"])
    fq = [c["name"] for c in cons if c["quad"] and c["nl"] is None and {names[j] for j in osil_read.row_vars(c)} <= fixed]
    print("  all-fixed rows with quadratic terms:", fq)
