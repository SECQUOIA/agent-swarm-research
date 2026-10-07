"""Evaluate listed MINLPLib points exactly (algebraic rows) or by intervals.

Usage: python3 evalpt.py name.pK [...]
Prints objective (exact or enclosure), largest row/bound/integrality violation,
and the variables missing from the .sol file.
"""
import os
import sys
import time
from fractions import Fraction as F

import ivl
import osil

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
_cache = {}


def model(name):
    if name not in _cache:
        _cache[name] = osil.parse(os.path.join(D, name + ".osil"))
    return _cache[name]


def violations(M, x):
    """Return list of (viol, kind, index) exact or upper bounds."""
    out = []
    for i in range(M.m):
        if osil.is_algebraic(M.nl[i]):
            v = osil.row_exact(M, i, x)
            lo = hi = v
        else:
            iv = osil.row_iv(M, i, x)
            lo, hi = iv.lo, iv.hi
        viol = F(0)
        if M.clb[i] is not None and lo < M.clb[i]:
            viol = max(viol, M.clb[i] - lo)
        if M.cub[i] is not None and hi > M.cub[i]:
            viol = max(viol, hi - M.cub[i])
        out.append((viol, "row", i))
    for j in range(M.n):
        viol = F(0)
        if M.lb[j] is not None and x[j] < M.lb[j]:
            viol = M.lb[j] - x[j]
        if M.ub[j] is not None and x[j] > M.ub[j]:
            viol = max(viol, x[j] - M.ub[j])
        out.append((viol, "bound", j))
        if M.vtype[j] in ("B", "I") and x[j].denominator != 1:
            out.append((abs(x[j] - round(x[j])), "int", j))
    return out


def objective(M, x):
    if osil.is_algebraic(M.obj_nl):
        v = osil.obj_exact(M, x)
        return v, v
    iv = osil.obj_iv(M, x)
    return iv.lo, iv.hi


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        name, pk = arg.rsplit(".", 1)
        t0 = time.time()
        M = model(name)
        x, missing, extra = osil.read_sol(os.path.join(D, f"{name}.{pk}.sol"), M)
        vi = violations(M, x)
        vi.sort(key=lambda t: -t[0])
        lo, hi = objective(M, x)
        nviol = sum(1 for v in vi if v[0] > 0)
        print(f"{arg}: sense={M.sense} n={M.n} m={M.m} obj=[{float(lo)!r}, {float(hi)!r}] "
              f"objconst={float(M.obj_const)} missing={len(missing)} extra={extra[:3]}")
        print(f"   #violated={nviol}; worst:", [(float(v), k, (M.cname[i] if k == 'row' else M.vname[i])) for v, k, i in vi[:4]])
        miss_bad = [M.vname[j] for j in missing if (M.lb[j] is not None and M.lb[j] > 0) or (M.ub[j] is not None and M.ub[j] < 0)]
        print(f"   missing vars with 0 outside bounds: {miss_bad[:5]}  ({time.time()-t0:.1f}s)")
