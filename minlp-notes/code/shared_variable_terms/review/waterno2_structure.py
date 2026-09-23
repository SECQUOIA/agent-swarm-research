"""How x^2 and x^3 appear in waterno2_*: rows, coefficients, bounds of the variables (reviewer's reader)."""
import sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from osil_eval import Model, NS
for name in sys.argv[1:]:
    M = Model(name)
    cube, sq = {}, {}
    for i, node in M.nl.items():
        tag = node.tag.replace(NS, "")
        kids = list(node)
        assert tag == "power" and kids[0].tag.endswith("variable") and float(kids[1].get("value")) == 3.0 and float(kids[0].get("coef", "1")) == 1.0, (i, tag)
        cube.setdefault(int(kids[0].get("idx")), []).append(i)
    other_q = 0
    for i, q in M.quad.items():
        for a, b, c in q:
            if a == b: sq.setdefault(a, []).append((i, c))
            else: other_q += 1
    print(name, "nl rows:", len(M.nl), "all of the form x^3; vars with cube:", len(cube), "vars with square:", len(sq), "bilinear quad terms:", other_q, "objective nl/quad:", -1 in M.nl, len(M.quad[-1]))
    both = sorted(set(cube) & set(sq))
    print("  vars with both:", len(both), " cube only:", len(set(cube) - set(sq)), " square only:", len(set(sq) - set(cube)))
    print("  bounds of vars with both:", collections.Counter((M.lb[v], M.ub[v], M.vt[v]) for v in both))
    print("  bounds of square-only vars:", collections.Counter((M.lb[v], M.ub[v], M.vt[v]) for v in set(sq) - set(cube)))
    v = both[0]
    for i in cube[v][:1] + [r for r, _ in sq[v][:1]]:
        print(f"  row {i}: [{M.rlb[i]}, {M.rub[i]}] lin", {M.names[j]: c for j, c in M.lin[i].items()}, "quad", [(M.names[a], M.names[b], c) for a, b, c in M.quad[i]], "nl x^3" if i in M.nl else "")
    rowtypes = collections.Counter(("eq" if M.rlb[i] == M.rub[i] else "ineq") for v in both for i in cube[v])
    rowtypes2 = collections.Counter(("eq" if M.rlb[i] == M.rub[i] else "ineq") for v in both for i, _ in sq[v])
    print("  cube rows:", dict(rowtypes), " square rows:", dict(rowtypes2))
