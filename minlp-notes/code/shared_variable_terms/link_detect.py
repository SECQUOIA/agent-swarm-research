"""Detection shared by the SCIP and Gurobi pilots (same rules as link_pilot.py)."""
import math

def _walk(t, trig, pw):
    op = t[0]
    if op in ("sin", "cos") and t[1][0] == "var": trig.setdefault(t[1][1], set()).add(op)
    elif op == "power" and t[1][0] == "var" and t[2][0] == "num": pw.setdefault(t[1][1], set()).add(float(t[2][1]))
    elif op == "square" and t[1][0] == "var": pw.setdefault(t[1][1], set()).add(2.0)
    elif op == "sqrt" and t[1][0] == "var": pw.setdefault(t[1][1], set()).add(0.5)
    elif op == "divide" and t[1][0] == "num" and t[2][0] == "var": pw.setdefault(t[2][1], set()).add(-1.0)
    elif op == "times":
        vs = [c[1] for c in t[1:] if c[0] == "var"]
        for v in set(vs):
            if vs.count(v) >= 2: pw.setdefault(v, set()).add(float(vs.count(v)))
    if op not in ("num", "var"):
        for c in t[1:]: _walk(c, trig, pw)

def reference(ps_, rule="smallest"):
    """Reference exponent for the links t_k = t_ref^(p_k/p_ref).
    'smallest': smallest magnitude (first version).  'positive': the positive exponent closest to 1,
    so that the link is never a negative power of a near-zero variable."""
    if rule == "positive":
        pos = [p for p in ps_ if p > 0]
        if pos:
            return min(pos, key=lambda p: abs(math.log(p)))
    return min(ps_, key=abs)


def detect(inst):
    trig, pw = {}, {}
    for r in inst.rows:
        if r["nl"] is not None: _walk(r["nl"], trig, pw)
        for i, j, c in r["quad"]:
            if i == j: pw.setdefault(i, set()).add(2.0)
    trig = [v for v, k in trig.items() if len(k) == 2]
    pw = {v: sorted(p - {1.0, 0.0}) for v, p in pw.items()}
    pw = {v: p for v, p in pw.items() if len(p) >= 2 and inst.var_lb[v] >= 0 and math.isfinite(inst.var_ub[v])
          and (min(p) > 0 or inst.var_lb[v] > 0)}
    return trig, pw
