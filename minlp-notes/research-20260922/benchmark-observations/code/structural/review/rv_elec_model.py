"""Reviewer check: elec OSiL = Thomson problem on S^2 (exact, symbolic).

Converts the whole OSiL model to sympy expressions with a generic tree
converter and compares with an independently built expected model.
"""
import sys
import sympy as sp
from rv_osil import read, strip

path = "/home/sgusev/.cache/minlplib/minlplib/osil/{}.osil"


def to_sympy(node, X):
    t = strip(node.tag)
    ch = list(node)
    if t == "variable":
        assert not ch
        return sp.Rational(node.attrib.get("coef", "1")) * X[int(node.attrib["idx"])]
    if t == "number":
        assert not ch and set(node.attrib) <= {"value", "type"}
        return sp.Rational(node.attrib["value"])
    if t == "sum":
        return sp.Add(*[to_sympy(c, X) for c in ch])
    if t == "product":
        return sp.Mul(*[to_sympy(c, X) for c in ch])
    if t == "divide":
        assert len(ch) == 2
        return to_sympy(ch[0], X) / to_sympy(ch[1], X)
    if t == "sqrt":
        assert len(ch) == 1
        return sp.sqrt(to_sympy(ch[0], X))
    if t == "square":
        assert len(ch) == 1
        return to_sympy(ch[0], X) ** 2
    raise ValueError("unhandled node " + t)


for N in [int(a) for a in sys.argv[1:]] or [25, 50, 100, 200]:
    m = read(path.format(f"elec{N}"))
    n = len(m["vars"])
    assert n == 3 * N
    X = sp.symbols(f"x0:{n}", real=True)
    for v in m["vars"]:
        assert v["type"] == "C" and v["lb"] == "-INF" and v["ub"] == "INF", v
    # objective
    assert len(m["objs"]) == 1
    o = m["objs"][0]
    assert o["sense"] == "min" and o["constant"] == 0 and not o["lin"] and not m["objquad"]
    obj = to_sympy(m["nl"][-1], X)
    P = [(X[i], X[i + N], X[i + 2 * N]) for i in range(N)]
    exp_obj = sp.Add(*[1 / sp.sqrt(sum((P[a][c] - P[b][c]) ** 2 for c in range(3)))
                       for a in range(N) for b in range(a + 1, N)])
    assert obj == exp_obj, "structural mismatch"
    # constraints
    assert len(m["cons"]) == N
    exp_rows = {sp.Add(*[P[i][c] ** 2 for c in range(3)]) for i in range(N)}
    rows = set()
    for r, c in enumerate(m["cons"]):
        assert c["lb"] == 1 and c["ub"] == 1 and c["constant"] == 0 and not c["lin"], c
        assert r not in m["nl"]
        rows.add(sp.Add(*[coef * X[a] * X[b] for (a, b), coef in c["quad"].items()]))
    assert rows == exp_rows and len(rows) == N
    assert set(m["nl"]) == {-1}
    # count pairs in objective
    assert len(obj.args) == N * (N - 1) // 2
    print(f"elec{N}: vars 3N free, N rows |x_i|^2 = 1, objective = sum_(a<b) 1/|x_a-x_b| "
          f"({len(obj.args)} pairs) -- MATCH")
