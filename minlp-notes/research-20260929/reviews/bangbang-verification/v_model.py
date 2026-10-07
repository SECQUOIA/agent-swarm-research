"""Independent parse of optcdeg2.osil and exact structure check (reviewer code, no project imports).

Writes logs/model_check.json. Asserts that the instance is exactly
  min 2e-4 * sum_{t=0}^{N} y_t^2
  Y_t: -y_t + y_{t+1} - 4e-4 v_t = 0                            (t = 0..N-1)
  V_t: -v_t + v_{t+1} - 4e-4 u_t + 8e-6 y_t + 8e-5 v_t^2 = 0      (t = 0..N-1)
  y_0 = 10, y_t free (t >= 1); v_0 = 0, v_N = 0, v_t >= -1 (1 <= t <= N-1); -.2 <= u_t <= .2,
with no other rows, terms, integer variables, or nonlinear expressions. The variable layout
is inferred from the rows, not assumed.
"""
import os
import json
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

PATH = os.path.expanduser("~/.cache/minlplib/minlplib/osil/optcdeg2.osil")
NS = "{os.optimizationservices.org}"


def expand(parent):
    """OSIL <el> lists with optional mult/incr attributes."""
    out = []
    for el in parent.findall(NS + "el"):
        mult = int(el.get("mult", "1"))
        incr = el.get("incr")
        txt = el.text.strip()
        if incr is None:
            out.extend([txt] * mult)
        else:
            base = int(txt); inc = int(incr)
            out.extend([str(base + k * inc) for k in range(mult)])
    return out


def main():
    root = ET.parse(PATH).getroot()
    data = root.find(NS + "instanceData")
    tags = [c.tag.replace(NS, "") for c in data]
    vars_ = data.find(NS + "variables").findall(NS + "var")
    n = len(vars_)
    lb = [v.get("lb", "0") for v in vars_]
    ub = [v.get("ub", "INF") for v in vars_]
    types = {v.get("type", "C") for v in vars_}
    objs = data.find(NS + "objectives").findall(NS + "obj")
    assert len(objs) == 1 and objs[0].get("maxOrMin") == "min"
    assert objs[0].get("numberOfObjCoef") in ("0", None) and len(objs[0]) == 0
    assert objs[0].get("constant") in (None, "0")
    cons = data.find(NS + "constraints").findall(NS + "con")
    m = len(cons)
    assert all(c.get("lb") == "0" and c.get("ub") == "0" and c.get("constant") in (None, "0") for c in cons)
    lcc = data.find(NS + "linearConstraintCoefficients")
    start = [int(s) for s in expand(lcc.find(NS + "start"))]
    assert lcc.find(NS + "rowIdx") is None, "column-major storage not expected"
    col = [int(s) for s in expand(lcc.find(NS + "colIdx"))]
    val = expand(lcc.find(NS + "value"))
    assert len(start) == m + 1 and start[-1] == len(col) == len(val)
    rows = [dict() for _ in range(m)]
    for i in range(m):
        for k in range(start[i], start[i + 1]):
            assert col[k] not in rows[i]
            rows[i][col[k]] = Fr(val[k])
    quad = data.find(NS + "quadraticCoefficients").findall(NS + "qTerm")
    objq = {}
    rowq = [dict() for _ in range(m)]
    for q in quad:
        i, a, b, c = int(q.get("idx")), int(q.get("idxOne")), int(q.get("idxTwo")), Fr(q.get("coef"))
        assert a == b
        if i == -1:
            assert a not in objq; objq[a] = c
        else:
            assert a not in rowq[i]; rowq[i][a] = c
    assert data.find(NS + "nonlinearExpressions") is None
    # ---- infer layout: the N rows with 3 linear terms are Y-rows, the N rows with a quadratic are V-rows
    Yrows = [i for i in range(m) if not rowq[i]]
    Vrows = [i for i in range(m) if rowq[i]]
    N = len(Yrows)
    assert len(Vrows) == N and m == 2 * N
    y = [None] * (N + 1); v = [None] * (N + 1); u = [None] * N
    # Y-row t: -1 y_t + 1 y_{t+1} - 4e-4 v_t ; V-row t: -1 v_t + 1 v_{t+1} - 4e-4 u_t + 8e-6 y_t + 8e-5 v_t^2
    for t, i in enumerate(Yrows):
        r = rows[i]
        assert sorted(r.values()) == [Fr(-1), Fr(-4, 10000), Fr(1)], (i, r)
        inv = {c: j for j, c in r.items()}
        yt, yt1, vt = inv[Fr(-1)], inv[Fr(1)], inv[Fr(-4, 10000)]
        if y[t] is None:
            y[t] = yt
        assert y[t] == yt, ("y chain", t)
        y[t + 1] = yt1; v[t] = vt
    for t, i in enumerate(Vrows):
        r, q = rows[i], rowq[i]
        assert len(r) == 4 and len(q) == 1, (i, r, q)
        (vq, cq), = q.items()
        assert cq == Fr(8, 10 ** 5) and vq == v[t], ("V-row quad", t)
        assert r.get(v[t]) == Fr(-1) and r.get(y[t]) == Fr(8, 10 ** 6), ("V-row", t, r)
        rest = {j: c for j, c in r.items() if j not in (v[t], y[t])}
        assert sorted(rest.values()) == [Fr(-4, 10000), Fr(1)], ("V-row rest", t, r)
        inv = {c: j for j, c in rest.items()}
        vn, ut = inv[Fr(1)], inv[Fr(-4, 10000)]
        if t + 1 < N:
            assert vn == v[t + 1], ("v chain", t)
        else:
            v[N] = vn
        u[t] = ut
    allv = y + v + u
    assert len(set(allv)) == len(allv) == n, "layout does not cover every variable exactly once"
    assert objq == {j: Fr(2, 10 ** 4) for j in y}, "objective"
    # ---- bounds (exact strings)
    B = lambda j: (lb[j], ub[j])  # noqa: E731
    assert B(y[0]) == ("10", "10")
    assert all(B(y[t]) == ("-INF", "INF") for t in range(1, N + 1))
    assert B(v[0]) == ("0", "0") and B(v[N]) == ("0", "0")
    assert all(B(v[t]) == ("-1", "INF") for t in range(1, N))
    assert all(B(u[t]) == ("-.2", ".2") for t in range(N))
    out = dict(N=N, n_vars=n, n_rows=m, sections=tags, var_types=sorted(types),
               first_Y_row=cons[Yrows[0]].get("name"), first_V_row=cons[Vrows[0]].get("name"),
               v_N_var=vars_[v[N]].get("name"), u_last_var=vars_[u[N - 1]].get("name"),
               y0_var=vars_[y[0]].get("name"), v0_var=vars_[v[0]].get("name"),
               layout_matches_first_wave=(u == list(range(0, N - 1)) + [50000]
                                          and y == list(range(50001, 50001 + N + 1))
                                          and v == list(range(100002, 100002 + N)) + [49999]),
               result="structure verified")
    print(json.dumps(out, indent=1))
    json.dump(out, open("logs/model_check.json", "w"), indent=1)


if __name__ == "__main__":
    main()
