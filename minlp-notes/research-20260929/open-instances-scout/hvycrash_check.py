"""Structural check for hvycrash: is the objective constant on the feasible set?

Pattern asserted for every stage k (rows are matched by expression trees):
  accumulator row:  A_k = 0.00437 * cos(th) / ((0.486237 c^2 + 0.0162079) r^2)
                    (x201 = A_1, x_{j} = x_{j+1} + A_k, objective = x152)
  algebraic row:    -1/r - cos(th) / ((0.486237 c^2 + 0.0162079) r^3) = 0
The algebraic row needs r != 0 and gives cos(th)/(D r^2) = -1, so A_k = -0.00437
and the objective equals -50 * 0.00437 = -0.2185 at every feasible point.

Usage: python3 hvycrash_check.py
"""
import os, sys

from pathlib import Path
_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "research-20260922/scouting/minlplib-open-data"))
import osil

I = osil.read(os.path.expanduser("~/.cache/minlplib/minlplib/osil/hvycrash.osil"))
N = I["names"]
rows = I["rows"]
assert rows[-1]["lin"] == {N.index("x152"): 1.0} and rows[-1]["nl"] is None


def D(c):
    return ("sum", ("times", ("times", ("num", 0.486237), ("var", c)), ("var", c)), ("num", 0.0162079))


acc, alg = {}, {}
for r, R in rows.items():
    if r < 0:
        continue
    t = R["nl"]
    # accumulator: divide(times(cos(th), 0.00437), times(D(c), r, r))
    if t[0] == "divide" and t[1][0] == "times" and t[1][1][0] == "cos":
        th = t[1][1][1][1]; assert t[1][2] == ("num", 0.00437)
        den = t[2]; assert den[0] == "times" and len(den) == 4
        c = den[1][1][1][2][1]; rr = den[2][1]
        assert den[1] == D(c) and den[2] == den[3] == ("var", rr)
        acc[(th, c, rr)] = (r, R["lin"])
    # algebraic: sum(negate(divide(1, r)), negate(divide(cos(th), times(D(c), r, r, r))))
    elif t[0] == "sum" and len(t) == 3 and t[1][0] == "negate" and t[1][1][0] == "divide" \
            and t[1][1][1] == ("num", 1.0):
        rr = t[1][1][2][1]
        d = t[2][1]; assert t[2][0] == "negate" and d[0] == "divide" and d[1][0] == "cos"
        th = d[1][1][1]; den = d[2]
        c = den[1][1][1][2][1]
        assert den[1] == D(c) and den[2:] == (("var", rr),) * 3
        assert R["lin"] == {} and R["lb"] == R["ub"] == 0.0
        alg[(th, c, rr)] = r

assert len(acc) == 50 and set(acc) == set(alg), (len(acc), len(alg))
# accumulator chain: x201 = A_1; x_j - x_{j+1} = A (coefficients -1, +1), ending at x152
nxt = {}
for key, (r, lin) in acc.items():
    assert rows[r]["lb"] == rows[r]["ub"] == 0.0
    names = {N[k]: v for k, v in lin.items()}
    if len(names) == 1:
        assert names == {"x201": -1.0}; start = key
    else:
        (a, va), (b, vb) = sorted(names.items(), key=lambda kv: kv[1])
        assert va == -1.0 and vb == 1.0
        nxt[b] = a  # x_a = x_b + A
cur, steps = "x201", 1
while cur in nxt:
    cur = nxt[cur]; steps += 1
assert cur == "x152" and steps == 50
print("hvycrash: 50 stages match; objective x152 = sum of 50 terms, each = -0.00437 on the feasible set")
print("objective is constant = -0.2185 at every feasible point")
