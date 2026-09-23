"""Evaluate a point in the original OSiL model: objective and the largest violation of rows, bounds
and integrality (float arithmetic).  check(inst, xvals) -> dict; CLI: python check_point.py <instance> <json list>"""
import json, math, sys
import model


def ev(t, x):
    op = t[0]
    if op == "num":
        return t[1]
    if op == "var":
        return x[t[1]]
    k = [ev(c, x) for c in t[1:]]
    if op == "sum":
        return sum(k)
    if op == "negate":
        return -k[0]
    if op == "times":
        p = 1.0
        for c in k:
            p *= c
        return p
    if op == "divide":
        return k[0] / k[1]
    if op == "power":
        return k[0] ** k[1]
    if op == "square":
        return k[0] * k[0]
    if op == "abs":
        return abs(k[0])
    return getattr(math, op)(k[0])


def check(inst, x):
    worst, where = 0.0, None
    obj = None
    for r, row in enumerate(inst.rows):
        a = sum(c * x[i] for i, c in row["lin"].items()) + sum(c * x[i] * x[j] for i, j, c in row["quad"])
        if row["nl"] is not None:
            a += ev(row["nl"], x)
        if r == 0:
            obj = a + inst.obj_const
            continue
        v = max(row["lb"] - a, a - row["ub"], 0.0)
        if v > worst:
            worst, where = v, f"row {r}"
    for j, xv in enumerate(x):
        v = max(inst.var_lb[j] - xv, xv - inst.var_ub[j], 0.0)
        if inst.var_type[j] in "BI":
            v = max(v, abs(xv - round(xv)))
        if v > worst:
            worst, where = v, f"var {j}"
    return {"obj": obj, "max_violation": worst, "where": where}


if __name__ == "__main__":
    inst = model.read_osil(model.OSIL.format(sys.argv[1]))
    print(check(inst, json.load(open(sys.argv[2]))))
