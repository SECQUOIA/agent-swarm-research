"""Exact rational repair of watercontamination0303 p2 (own implementation).

All rows are linear; the objective is quadratic. Keep the listed decimals of
every variable with a finite bound (binaries and the bounded continuous
variables; binaries must already be exactly 0/1). Then determine the free
variables by propagation: repeatedly take an equality row with exactly one
undetermined variable and solve it exactly. Finally check every row, bound and
integrality condition exactly and compute the objective exactly.
"""
import os
import sys
import time
from collections import defaultdict, deque
from fractions import Fraction as F

import evalpt
import osil

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "watercontamination0303"


def main(pk="p2"):
    t0 = time.time()
    M = evalpt.model(NAME)
    x0, missing, _ = osil.read_sol(os.path.join(HERE, "data", f"{NAME}.{pk}.sol"), M)
    for j in range(M.n):
        if M.vtype[j] == "B":
            assert x0[j] in (0, 1)
    known = [M.lb[j] is not None or M.ub[j] is not None for j in range(M.n)]
    x = [x0[j] if known[j] else None for j in range(M.n)]
    print("kept (bounded) variables:", sum(known), " free to determine:", M.n - sum(known))
    eqrows = [i for i in range(M.m) if M.clb[i] is not None and M.clb[i] == M.cub[i]]
    assert all(not M.quad[i] and M.nl[i] is None for i in range(M.m))
    unk = {i: sum(1 for j in M.lin[i] if x[j] is None) for i in eqrows}
    rows_of = defaultdict(list)
    for i in eqrows:
        for j in M.lin[i]:
            if x[j] is None:
                rows_of[j].append(i)
    q = deque(i for i in eqrows if unk[i] == 1)
    solved = 0
    while q:
        i = q.popleft()
        if unk[i] != 1:
            continue
        j = next(j for j in M.lin[i] if x[j] is None)
        rest = M.cconst[i] + sum(c * x[k] for k, c in M.lin[i].items() if k != j)
        x[j] = (M.cub[i] - rest) / M.lin[i][j]
        solved += 1
        for i2 in rows_of[j]:
            unk[i2] -= 1
            if unk[i2] == 1:
                q.append(i2)
    left = [j for j in range(M.n) if x[j] is None]
    print(f"propagated {solved} variables; undetermined {len(left)} ({time.time()-t0:.1f}s)")
    assert not left
    vi = evalpt.violations(M, x)
    worst = max(vi, key=lambda t: t[0])
    nv = sum(1 for t in vi if t[0] > 0)
    obj = osil.obj_exact(M, x)
    dmax = max(abs(x[j] - x0[j]) for j in range(M.n))
    print(f"exact check: violated conditions {nv}, worst {float(worst[0])} {worst[1:]}")
    print(f"max |x - listed| = {float(dmax):.3e}")
    print(f"objective = {float(obj)!r}  (denominator digits {len(str(obj.denominator))})")
    lo = obj
    for nm, d in (("BONMIN", "207.9850352"), ("LINDO", "207.9850353"), ("BARON", "207.9850346"),
                  ("CPLEX/GUROBI/SHOT", "207.9850348"), ("SCIP", "207.9850341")):
        d = F(d)
        print(f"  {nm}: dual {float(d)} - objective = {float(d - lo):.3e} (rel {float((d - lo) / d):.2e})")
    print(f"total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main(*(sys.argv[1:] or []))
