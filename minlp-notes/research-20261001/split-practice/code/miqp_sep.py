"""Buchheim-Traversi style exact split separation: solve the integer QP
    min q(v) = v^T Y v + v^T Y e0,   v in Z^N,  -K <= v_i <= K
with an MIQP solver (Gurobi 13.0.2 command line, or SCIP 10 via PySCIPOpt).
B-T solve the unbounded problem with the convex IQP code of Buchheim,
Caprara and Lodi; general MIQP solvers need finite bounds, so K is a parameter
(the problem is convex for PSD Y; a tiny negative eigenvalue from the SDP
solver is removed by clipping before writing the model).
"""

import os
import re
import subprocess
import tempfile
import time

import numpy as np

GRB = "/opt/gurobi1302/linux64/bin/gurobi_cl"
GRB_ENV = dict(os.environ, LD_LIBRARY_PATH="/opt/gurobi1302/linux64/lib")


def psd_clip(Y, floor=0.0):
    w, V = np.linalg.eigh((Y + Y.T) / 2)
    w = np.maximum(w, floor)
    return (V * w) @ V.T


def write_lp(Y, K, path, eta=0.0):
    """q(v) + eta*|w|^2 ; LP format quadratic objective is [ ... ] / 2."""
    N = Y.shape[0]
    Yq = Y.copy()
    if eta:
        Yq[np.arange(1, N), np.arange(1, N)] += eta
    lin = Y[:, 0]
    terms = []
    for i in range(N):
        if abs(lin[i]) > 0:
            terms.append(f"{lin[i]:+.17g} v{i}")
    q = []
    for i in range(N):
        q.append(f"{2 * Yq[i, i]:+.17g} v{i} ^ 2")
        for j in range(i + 1, N):
            if Yq[i, j] != 0:
                q.append(f"{4 * Yq[i, j]:+.17g} v{i} * v{j}")
    with open(path, "w") as f:
        f.write("Minimize\n obj: " + " ".join(terms) + " + [ " + " ".join(q) + " ] / 2\n")
        f.write("Subject To\n")
        f.write("Bounds\n")
        for i in range(N):
            f.write(f" -{K} <= v{i} <= {K}\n")
        f.write("General\n " + " ".join(f"v{i}" for i in range(N)) + "\nEnd\n")


def gurobi_sep(Y, K=20, timelimit=60, threads=1, eta=0.0, cutoff=None, clip=True):
    N = Y.shape[0]
    Yc = psd_clip(Y) if clip else Y
    with tempfile.TemporaryDirectory() as td:
        lp = os.path.join(td, "s.lp"); sol = os.path.join(td, "s.sol"); log = os.path.join(td, "g.log")
        write_lp(Yc, K, lp, eta)
        args = [GRB, f"TimeLimit={timelimit}", f"Threads={threads}", "MIPGap=0",
                "MIPGapAbs=1e-9", f"ResultFile={sol}", f"LogFile={log}", "LogToConsole=0"]
        if cutoff is not None:
            args.append(f"Cutoff={cutoff}")
        args.append(lp)
        t = time.time()
        p = subprocess.run(args, env=GRB_ENV, capture_output=True, text=True)
        dt = time.time() - t
        txt = open(log).read() if os.path.exists(log) else p.stdout + p.stderr
        v = None
        if os.path.exists(sol):
            v = np.zeros(N, dtype=np.int64)
            for line in open(sol):
                m = re.match(r"v(\d+) ([-+0-9.eE]+)", line.strip())
                if m:
                    v[int(m.group(1))] = int(round(float(m.group(2))))
        status = "unknown"
        for key in ("Optimal solution found", "Time limit reached", "Model is infeasible",
                    "Cutoff", "Infeasible or unbounded"):
            if key in txt:
                status = key
                break
        bnd = re.findall(r"Best objective ([-+0-9.eE]+|-), best bound ([-+0-9.eE]+|-)", txt)
        nodes = re.findall(r"Explored (\d+) nodes", txt)
    q = None
    if v is not None:
        vf = v.astype(float)
        q = float(vf @ Y @ vf + vf @ Y[:, 0])
    return dict(v=v, q=q, time=dt, status=status,
                bound=(bnd[-1][1] if bnd else None), nodes=(int(nodes[-1]) if nodes else None))


def scip_sep(Y, K=20, timelimit=60, eta=0.0, clip=True):
    from pyscipopt import Model, quicksum
    N = Y.shape[0]
    Yc = psd_clip(Y) if clip else Y.copy()
    if eta:
        Yc[np.arange(1, N), np.arange(1, N)] += eta
    m = Model()
    m.hideOutput()
    m.setParam("limits/time", timelimit)
    m.setParam("parallel/maxnthreads", 1)
    v = [m.addVar(vtype="I", lb=-K, ub=K, name=f"v{i}") for i in range(N)]
    t = m.addVar(lb=None, name="t")
    expr = quicksum(Yc[i, j] * v[i] * v[j] for i in range(N) for j in range(N) if Yc[i, j] != 0) \
        + quicksum(Y[i, 0] * v[i] for i in range(N))
    m.addCons(expr <= t)
    m.setObjective(t, "minimize")
    t0 = time.time()
    m.optimize()
    dt = time.time() - t0
    st = m.getStatus()
    vv = None; q = None
    if m.getNSols() > 0:
        vv = np.array([int(round(m.getVal(x))) for x in v])
        vf = vv.astype(float)
        q = float(vf @ Y @ vf + vf @ Y[:, 0])
    return dict(v=vv, q=q, time=dt, status=st, bound=m.getDualbound(), nodes=m.getNNodes())
