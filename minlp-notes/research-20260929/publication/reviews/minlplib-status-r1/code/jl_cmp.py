"""Verifier (minlplib-status r1): compare a MINLPLib.jl (JuMP 0.18) instance
file with a MINLPLib OSiL file, without going through GAMS.

  * variables: names b[k] -> bk, x[k] -> xk, i[k] -> ik, objvar; types from
    setcategory; bounds from setlowerbound/setupperbound (1e20 read as inf).
    Reported as they are (JuMP default is free; the GAMS source of these
    files gives integer/positive variables lower bound 0, which the JuMP
    writer omits for integers, so missing integer lower bounds are listed
    separately rather than called differences).
  * rows: for each jl constraint "lhs (==|<=|>=) rhs" the function
    g = lhs - rhs is evaluated at K random points in 50-digit mpmath and
    compared with the OSiL row value minus its bound (same sense).
  * objective: the jl row containing objvar is solved for objvar and
    compared with the OSiL objective.
Numerical evidence (random points), not a proof.
Usage: python3 jl_cmp.py FILE.jl FILE.osil [K]
"""
import random
import re
import sys
from fractions import Fraction

import mpmath
from mpmath import mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from osil_eval_cmp import read, row_value, mpf  # noqa: E402

mp.dps = 50
FUN = {"exp": mpmath.exp, "log": mpmath.log, "sqrt": mpmath.sqrt, "abs": abs,
       "sin": mpmath.sin, "cos": mpmath.cos, "tanh": mpmath.tanh}


def parse_jl(path):
    txt = open(path).read()
    stmts = re.findall(r"^(@\w+|set\w+)\((.*)\)\s*$", txt, flags=re.M)
    lb, ub, typ, rows, obj = {}, {}, {}, [], None
    for kind, body in stmts:
        if kind in ("setlowerbound", "setupperbound"):
            v, val = body.rsplit(",", 1)
            v = re.sub(r"(\w+)\[(\d+)\]", r"\1\2", v.strip())
            f = float(val)
            (lb if kind == "setlowerbound" else ub)[v] = None if abs(f) >= 1e20 else Fraction(val.strip())
        elif kind == "setcategory":
            v, c = body.split(",")
            typ[re.sub(r"(\w+)\[(\d+)\]", r"\1\2", v.strip())] = c.strip()
        elif kind in ("@constraint", "@NLconstraint"):
            _, name, expr = body.split(",", 2)
            m = re.match(r"(.*)(==|<=|>=)(.*)$", expr, flags=re.S)
            lhs, op, rhs = m.group(1), m.group(2), m.group(3)
            rows.append((name.strip(), op, lhs, rhs))
        elif kind == "@objective":
            obj = body
    return lb, ub, typ, rows, obj


def to_py(e):
    # numeric literals -> exact mpf (not Python doubles)
    e = re.sub(r"(?<![\w\[.])(\d+\.?\d*(?:[eE][-+]?\d+)?)", r"F('\1')", e)
    e = re.sub(r"\b([bxi])\[(\d+)\]", r"V['\1\2']", e)
    e = re.sub(r"\bobjvar\b", "V['objvar']", e)
    e = e.replace("^", "**")
    return e


def main(jl, osil, K=3):
    lb, ub, typ, rows, obj = parse_jl(jl)
    M = read(osil)
    idx = {n: j for j, n in enumerate(M["vars"])}
    # variable comparison
    diffs, intlb = [], []
    for n, j in idx.items():
        t = {"C": None, "B": ":Bin", "I": ":Int"}[M["type"][j]]
        if typ.get(n) != t:
            diffs.append((n, "type", typ.get(n), t))
        if t == ":Bin":
            continue
        jl_lb = lb.get(n, "free")
        if jl_lb == "free" and t == ":Int" and M["lb"][j] == 0:
            intlb.append(n)
        elif (None if jl_lb == "free" else jl_lb) != M["lb"][j]:
            diffs.append((n, "lb", jl_lb, M["lb"][j]))
        if ub.get(n) != M["ub"][j]:
            diffs.append((n, "ub", ub.get(n), M["ub"][j]))
    print(f"vars: osil {len(idx)}; type/bound differences {len(diffs)} {diffs[:5]}; integer lb omitted in jl: {len(intlb)}")
    cidx = {n: i for i, n in enumerate(M["cons"])}
    rng = random.Random(11)
    pts = []
    for k in range(K):
        V = {}
        for n, j in idx.items():
            lo, hi = M["lb"][j], M["ub"][j]
            if lo is not None and hi is not None:
                V[n] = mpf(lo) + mpmath.mpf(rng.random()) * mpf(hi - lo)
            elif lo is not None:
                V[n] = mpf(lo) + mpmath.mpf(rng.uniform(0.1, 2.0))
            elif hi is not None:
                V[n] = mpf(hi) - mpmath.mpf(rng.uniform(0.1, 2.0))
            else:
                V[n] = mpmath.mpf(rng.uniform(-2, 2))
        pts.append(V)
    env = dict(FUN)
    env["F"] = lambda t: mpf(Fraction(t))
    nrow = ndiff = nmiss = 0
    worst = mpmath.mpf(0)
    objrow = None
    for (name, op, lhs, rhs) in rows:
        code = compile(f"({to_py(lhs)}) - ({to_py(rhs)})", name, "eval")
        if ("objvar" in lhs or "objvar" in rhs) and name not in cidx:
            objrow = (name, code)
            continue
        if name not in cidx:
            nmiss += 1
            continue
        i = cidx[name]
        lo, hi = M["clb"][i], M["cub"][i]
        want = {"==": (True, True), "<=": (False, True), ">=": (True, False)}[op]
        have = (lo is not None, hi is not None)
        if want != have:
            ndiff += 1
            print("  sense differs", name, op, lo, hi)
            continue
        bnd = hi if hi is not None else lo
        nrow += 1
        for V in pts:
            x = [V[n] for n in M["vars"]]
            g_o = row_value(M, i, x) + mpf(M["cconst"][i]) - mpf(bnd)
            g_j = eval(code, env, {"V": V})
            d = abs(g_o - g_j)
            rel = d / max(1, abs(g_o), abs(g_j))
            worst = max(worst, rel)
            if rel > mpmath.mpf("1e-40"):
                ndiff += 1
                print("  row differs", name, mpmath.nstr(g_o, 12), mpmath.nstr(g_j, 12))
                break
    # objective
    od = None
    if objrow:
        name, code = objrow
        for V in pts:
            V0 = dict(V, objvar=mpmath.mpf(0))
            V1 = dict(V, objvar=mpmath.mpf(1))
            g0 = eval(code, env, {"V": V0})
            c = eval(code, env, {"V": V1}) - g0
            ov = -g0 / c
            x = [V[n] for n in M["vars"]]
            oo = row_value(M, -1, x) + mpf(M["obj"]["const"])
            od = max(od or 0, abs(ov - oo) / max(1, abs(oo)))
    print(f"rows compared {nrow}; rows differing {ndiff}; jl rows without OSiL row {nmiss}; "
          f"OSiL rows {len(cidx)}; worst rel {mpmath.nstr(worst, 3)}; objective row {objrow[0] if objrow else None} "
          f"worst rel {mpmath.nstr(od, 3) if od is not None else None}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3)
