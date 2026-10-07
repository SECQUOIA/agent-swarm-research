"""Verifier: exact comparison of a MINLPLib.jl file whose @constraint rows are
linear with a MINLPLib OSiL file: linear coefficients (exact rationals) and
right-hand sides of every @constraint; variable types/bounds; the single
@NLconstraint objective row (quadratic, sum c*(x)^2 + linear - objvar) is
compared exactly as a polynomial with the OSiL objective.
Usage: jl_lin_cmp.py FILE.jl FILE.osil"""
import re
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from poly_cmp_lib import read, rowpoly, padd  # noqa: E402
from jl_cmp import parse_jl  # noqa: E402

TERM = re.compile(r"([+-]?)\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?)\s*\*\s*)?\(?\s*([bxi])\[(\d+)\]\s*\)?(\^2)?")


def lin(expr):
    d = {}
    pos = 0
    e = expr.replace(" ", "")
    for m in TERM.finditer(e):
        if e[pos:m.start()].strip():
            raise ValueError("unparsed: " + e[pos:m.start()][:40])
        s = -1 if m.group(1) == "-" else 1
        c = Fraction(m.group(2)) if m.group(2) else Fraction(1)
        key = (m.group(3) + m.group(4), 2 if m.group(5) else 1)
        d[key] = d.get(key, 0) + s * c
        pos = m.end()
    rest = e[pos:]
    return d, rest


lb, ub, typ, rows, obj = parse_jl(sys.argv[1])
M = read(sys.argv[2])
cidx = {n: i for i, n in enumerate(M["cons"])}
nd = nc = 0
for (name, op, lhs, rhs) in rows:
    if name not in cidx:
        # objective row: lhs = sum c x^2 + ... - objvar  (op ==)
        e = lhs.replace(" ", "")
        e2 = e.replace("-objvar", "").replace("+objvar", "")
        d, rest = lin(e2)
        if rest.strip():
            print("objective row: unparsed tail", rest[:60])
        sign = -1 if "-objvar" in e else 1
        p = {}
        for (v, k), c in d.items():
            p[((v, k),)] = -sign * c
        r = Fraction(rhs.strip())
        if r:
            p[()] = p.get((), 0) + sign * r
        po, _ = rowpoly(M, -1)
        diff = padd({k: v for k, v in p.items() if v != 0}, po, -1)
        print(f"objective ({name}): terms {len(p)}; exact difference terms {len(diff)}")
        continue
    nc += 1
    d, rest = lin(lhs)
    if rest.strip():
        nd += 1
        print("unparsed", name, rest[:60])
        continue
    i = cidx[name]
    nm = M["vars"]
    lo = {(nm[j], 1): c for j, c in M["lin"].get(i, {}).items() if c != 0}
    dj = {k: v for k, v in d.items() if v != 0}
    r = Fraction(rhs.strip())
    k = M["cconst"][i]
    want = {"==": (r, r), "<=": (None, r), ">=": (r, None)}[op]
    have = (None if M["clb"][i] is None else M["clb"][i] - k, None if M["cub"][i] is None else M["cub"][i] - k)
    if dj != lo or want != have or M["quad"].get(i) or i in M["nl"]:
        nd += 1
        if nd <= 5:
            print("differs", name, want, have)
print(f"linear rows compared exactly {nc}; differing {nd}")
