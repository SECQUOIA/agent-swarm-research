"""Spatial branch-and-bound over the input box with LP relaxation R0 or R1.

Minimizes sense * net(x). Best-first node selection; branching on the input
coordinate with the largest width relative to the root box, at the midpoint.
Per node: interval bounds on the node box intersected with the parent's bounds,
LP with the parent's active cuts (initial 1-D tangent cuts at the root)
and the cut loop of relax.py (stopped at the prune cutoff or when two rounds
close less than tail_frac of the node gap). Primal: shared starting incumbent (multistart),
network value at every LP solution, and a short projected descent from it.
Gap closed when UB - LB <= max(ABS_GAP, REL_GAP * |UB|).
The time limit and the reported time are process CPU time (time.process_time,
which includes the single-threaded Gurobi LP solves), because the machine is
shared; wall time is recorded as well.
"""
import heapq
import itertools
import time

import numpy as np

from primal import local_descent
from relax import NodeLP, cut_loop, ibp, obbt, problems_to_cuts, r0_problems
from envelope import solve_batch

REL_GAP, ABS_GAP = 1e-4, 1e-6


def tol(ub):
    return max(ABS_GAP, REL_GAP * abs(ub))


def bnb(net, sense, mode, incumbent, time_limit=600.0, node_limit=10 ** 6, root_obbt=True, max_rounds=50,
        init_fracs=(1 / 6, 0.5, 5 / 6), tail_frac=0.01, log_every=0):
    t_start = time.process_time()
    w_start = time.time()
    lx0, ux0 = net.lo.copy(), net.hi.copy()
    w0 = ux0 - lx0
    ub_x = np.array(incumbent["x"], float)
    UB = float(incumbent["value"])  # in sense-transformed (minimization) units
    B = ibp(net, lx0, ux0)
    n_obbt = 0
    if root_obbt:
        B, n_obbt = obbt(net, B)
    counter = itertools.count()
    heap = [(-np.inf, next(counter), lx0, ux0, B, [], 0)]
    nodes = 0
    stats = dict(rounds=0, cuts_r0=0, cuts_r1=0, t_lp=0.0, t_sep=0.0, max_depth=0, pruned_by_bound=0)
    traj = []
    root_bound = None
    status = "open"
    while heap:
        key, _, lx, ux, Bp, cuts_in, depth = heap[0]
        LB = key
        if LB >= UB - tol(UB):
            status = "optimal"
            break
        if time.process_time() - t_start > time_limit:
            status = "time_limit"
            break
        if nodes >= node_limit:
            status = "node_limit"
            break
        heapq.heappop(heap)
        nodes += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        Bn = ibp(net, lx, ux, inherit=Bp)
        lp = NodeLP(net, sense, Bn)
        lp.set_output_objective()
        if depth == 0:  # children start from the parent's active cuts instead
            lp.add_cuts(problems_to_cuts(solve_batch(net.actname, r0_problems(net, Bn, range(lp.L), init_fracs))))
        lp.add_cuts(cuts_in)
        res = cut_loop(net, lp, Bn, mode, max_rounds=max_rounds, cutoff=UB - tol(UB), tail_frac=tail_frac)
        for k in ("rounds", "cuts_r0", "cuts_r1", "t_lp", "t_sep"):
            stats[k] += res[k]
        node_lb = max(res["bound"], key)
        if root_bound is None:
            root_bound = res["bound"]
        # primal: LP point and a short descent from it
        xs = np.clip(res["v"][lp.ix], lx0, ux0)
        Xd, fd = local_descent(net, sense, xs[None, :], lx0, ux0, iters=60, lr=0.01)
        fx = sense * float(net.forward(xs[None, :])[0])
        for val, xx in ((fx, xs), (float(fd[0]), Xd[0])):
            if val < UB:
                UB, ub_x = val, xx.copy()
        active = lp.active_cuts()
        lp.dispose()
        if node_lb >= UB - tol(UB):
            stats["pruned_by_bound"] += 1
        else:
            i = int(np.argmax((ux - lx) / w0))
            mid = 0.5 * (lx[i] + ux[i])
            u1 = ux.copy()
            u1[i] = mid
            l2 = lx.copy()
            l2[i] = mid
            heapq.heappush(heap, (node_lb, next(counter), lx.copy(), u1, Bn, active, depth + 1))
            heapq.heappush(heap, (node_lb, next(counter), l2, ux.copy(), Bn, active, depth + 1))
        glb = min(heap[0][0], UB) if heap else UB
        if log_every and nodes % log_every == 0:
            print(nodes, "LB %.6f UB %.6f open %d %.1fs" % (glb, UB, len(heap), time.process_time() - t_start), flush=True)
        if nodes <= 10 or nodes % 25 == 0:
            traj.append((round(time.process_time() - t_start, 3), nodes, glb, UB))
    else:
        status = "optimal"
    LB = min(heap[0][0], UB) if heap else UB
    elapsed = time.process_time() - t_start
    traj.append((round(elapsed, 3), nodes, LB, UB))
    return dict(status=status, nodes=nodes, time=elapsed, wall_time=time.time() - w_start, LB=float(LB), UB=float(UB), gap=float(UB - LB),
                closed=bool(UB - LB <= tol(UB)), x=ub_x.tolist(), root_bound=root_bound, open_nodes=len(heap),
                obbt_lps=n_obbt, traj=traj, **stats)
