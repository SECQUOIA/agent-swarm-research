"""Runs for kappa-negative.md, Part 1 (kappa_tau < 0, one switch).

usage: OMP_NUM_THREADS=1 python3 run_kneg.py PART [PART ...]
PART in: lifted eps epsexact qneg
Each part prints JSON lines and writes logs/<part>.json.  "exact" = rational arithmetic.
"""
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ktoy import KToy, kkt, best_bang, exact_kkt, fam_const, bound, hess_exact  # noqa: E402
from lifted import certify, certify_multi, greedy_partition, fixed_bound, node_kkt, lifted_interval  # noqa: E402

LOG = os.path.join(HERE, "logs")
OUT = []


def emit(rec):
    print(json.dumps(rec, default=float), flush=True)
    OUT.append(rec)


def dump(name):
    with open(os.path.join(LOG, f"{name}.json"), "w") as f:
        json.dump(OUT, f, indent=1, default=float)
    OUT.clear()


def plus(k=0.5, phi2=0.0, R=2.0):
    """window-exactness.md's toy plus (k = 0.5), and variants: kappa_tau = -k, b = 1."""
    return KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, k),), phi1=1.0, phi2=phi2, R=R)


def weakest_stage(Z, k):
    """The interior stage if any, else the vertex stage with the smallest margin |sigma_t| / h - k."""
    if Z["frac"]:
        return Z["frac"][0], "interior"
    h = Z["h"]
    t = min(range(Z["N"]), key=lambda s: abs(Z["sig"][s]) / h)
    return t, "vertex"


# ---------------------------------------------------------------------------------------------- lifted
def part_lifted():
    cases = [(0.5, N) for N in (50, 100, 150, 200, 500, 1000, 2000, 4000, 8000)] + \
            [(1.0, N) for N in (200, 1000, 1003, 2000, 4000)]
    for k, N in cases:
        t0 = time.time()
        toy = plus(k, R=3.0 if k > 0.5 else 2.0)
        sw = best_bang(toy, 200, 1)
        kk = kkt(toy, N, sw)
        Z = exact_kkt(toy, kk)
        h = Z["h"]
        P = fam_const(N, -Fr(k))
        B0, L0, LN0 = bound(toy, Z, P)
        n, kind = weakest_stage(Z, k)
        rec = dict(k=k, kappa=-k, N=N, n=n, stage_kind=kind, u_n=float(Z["u"][n]),
                   sig_over_h=[float(Z["sig"][t] / h) for t in range(n - 2, n + 3)],
                   J=float(Z["J"]), transferred_gap_over_h2=float((Z["J"] - B0) / h ** 2),
                   transferred_exact=(B0 == Z["J"]))
        if B0 == Z["J"]:
            rec.update(certificate="transferred family alone (no branching)", n_nodes=1)
        else:
            res = certify(toy, Z, P, n, Z["J"])
            rec.update(certificate="branch on u_n: lifted + fixed nodes", ok=res["ok"], n_nodes=res["n_nodes"],
                       n_lifted=res["n_lifted"],
                       nodes=[dict(l=q["l"], r=q["r"], kind=q["kind"], V=q.get("V"),
                                   bound_minus_J_over_h2=q["bound_minus_target"] / float(h) ** 2)
                              for q in res["nodes"]])
        rec["time"] = time.time() - t0
        emit(rec)
    dump("lifted")


# ---------------------------------------------------------------------------------------------- eps
def predicted_count(q, kap, w0, a_plus, a_minus):
    """Leading-order count of the greedy partition: central node plus geometric nodes with ratio
    rho* = 1 + (q + sqrt(q^2 + q kap)) / kap on each side (kap = |kappa_tau|)."""
    rho = 1 + (q + math.sqrt(q * q + q * kap)) / kap
    c = 1
    for a in (a_plus, a_minus):
        if a > w0:
            c += math.ceil(math.log(a / w0) / math.log(rho))
    return c, rho


def part_eps():
    for k, Ns in ((0.5, (1000, 4000, 8000)), (1.0, (1000, 1001, 1002, 1003, 4000, 4001, 4002, 4003))):
        toy = plus(k, R=3.0 if k > 0.5 else 2.0)
        sw = best_bang(toy, 200, 1)
        for N in Ns:
            kk = kkt(toy, N, sw)
            if not kk["frac"]:
                continue
            n = kk["frac"][0]
            h = toy.T / N
            q = h * (N - 1 - n) + toy.phi2             # H_nn / h^2
            ub = kk["u"][n]
            for er in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-10):
                if er * h * h < 100 * 2.2e-16:      # below float resolution of J (about 1)
                    continue
                t0 = time.time()
                nodes = greedy_partition(toy, N, kk["u"], n, kk["J"], er * h * h, k, h * h)
                w0 = math.sqrt(2 * er / k)
                pc, rho = predicted_count(q, k, w0, 1 - ub, 1 + ub)
                ratios = []
                if any(len(q) != 3 for q in nodes):
                    emit(dict(k=k, N=N, eps_over_h2=er, stuck=True))
                    continue
                for (a, b, _) in nodes[1:]:
                    d_in = min(abs(a - ub), abs(b - ub))
                    d_out = max(abs(a - ub), abs(b - ub))
                    if d_in > 0 and abs(b) < 1 - 1e-12 and abs(a) < 1 - 1e-12:
                        ratios.append(d_out / d_in)
                emit(dict(k=k, N=N, n=n, u_n=ub, q=q, eps_over_h2=er, n_nodes=len(nodes), predicted=pc,
                          rho_star=rho, rho_exact_nodes=1 + 2 * q / k,
                          inner_ratios=[round(r, 3) for r in ratios],
                          min_margin_over_h2=min(m for (_, _, m) in nodes), time=time.time() - t0))
    dump("eps")


def part_epsexact():
    """Exact rational re-check of greedy partitions (toy plus, N = 1000)."""
    toy = plus(0.5)
    N = 1000
    kk = kkt(toy, N, best_bang(toy, 200, 1))
    Z = exact_kkt(toy, kk)
    n = Z["frac"][0]
    h = Z["h"]
    P = fam_const(N, Fr(-1, 2))
    for er in (Fr(1, 10 ** 4), Fr(1, 10 ** 8)):
        nodes = greedy_partition(toy, N, kk["u"], n, kk["J"], float(er) * float(h) ** 2, 0.5, float(h) ** 2,
                                 safety=0.9)
        worst = None
        t0 = time.time()
        for (a, b, _) in nodes:
            l, r = Fr(a).limit_denominator(10 ** 12), Fr(b).limit_denominator(10 ** 12)
            A = node_kkt(toy, N, [float(v) for v in Z["u"]], n, l, r)
            Bn, _ = fixed_bound(toy, A, P, n)
            m = (Bn - Z["J"]) / h ** 2
            worst = m if worst is None or m < worst else worst
        # the rounded node ends overlap or leave gaps of at most 1e-12; report the cover
        emit(dict(N=N, eps_over_h2=float(er), n_nodes=len(nodes), exact_min_bound_minus_J_over_h2=float(worst),
                  all_within_eps=bool(worst >= -er), time=time.time() - t0))
    dump("epsexact")


# ---------------------------------------------------------------------------------------------- qneg
def part_qneg():
    """b^T Q b < 0 < eta_L: phi2 < -(T - tau).  Fractional KKT points are saddles (H_nn < 0); the global
    optimum is bang-bang.  Exact lifted certificate at the best vertex KKT point; the fractional KKT point
    (if one exists on the grid) is not optimal."""
    toy = KToy(a_pts=((0.0, 2.0), (1.0, -1.0)), k_pts=((0.0, 3.0),), phi1=1.0, phi2=-2.0, R=3.0)
    sw = best_bang(toy, 200, 1)
    for N in (200, 400, 1000, 2000):
        t0 = time.time()
        kk = kkt(toy, N, sw)
        Z = exact_kkt(toy, kk)
        h = Z["h"]
        n, kind = weakest_stage(Z, 3.0)
        Hnn = hess_exact(toy, N, [n])[0][0] / h ** 2
        P = fam_const(N, Fr(-3))
        B0, _, _ = bound(toy, Z, P)
        rec = dict(N=N, switch=sw, frac=Z["frac"], n=n, kind=kind, Hnn_over_h2=float(Hnn),
                   transferred_gap_over_h2=float((Z["J"] - B0) / h ** 2))
        if B0 != Z["J"]:
            res = certify_multi(toy, Z, P, Z["J"], max_nodes=150)
            inc = res["incumbent"]
            rec.update(ok=res["ok"], n_nodes=res["n_nodes"], n_leaves=res.get("n_leaves"),
                       incumbent_improved=inc["improved"],
                       incumbent_J_minus_J_over_h2=float((inc["J"] - Z["J"]) / h ** 2),
                       nodes=[(q["kind"], q.get("stages", q.get("stage")), q["box"]) for q in res["nodes"]])
        rec["time"] = time.time() - t0
        emit(rec)
    dump("qneg")


def part_lifted2():
    """kappa = -1 grids with an interior stage (exact, 1-D certificate as in part_lifted)."""
    for N in (1001, 1002):
        t0 = time.time()
        toy = plus(1.0, R=3.0)
        kk = kkt(toy, N, best_bang(toy, 200, 1))
        Z = exact_kkt(toy, kk)
        h = Z["h"]
        P = fam_const(N, -Fr(1))
        B0, _, _ = bound(toy, Z, P)
        n, kind = weakest_stage(Z, 1.0)
        res = certify(toy, Z, P, n, Z["J"])
        emit(dict(k=1.0, kappa=-1.0, N=N, n=n, stage_kind=kind, u_n=float(Z["u"][n]),
                  sig_over_h=[float(Z["sig"][t] / h) for t in range(n - 2, n + 3)],
                  transferred_gap_over_h2=float((Z["J"] - B0) / h ** 2), ok=res["ok"], n_nodes=res["n_nodes"],
                  nodes=[dict(l=q["l"], r=q["r"], kind=q["kind"], V=q.get("V"),
                              bound_minus_J_over_h2=q["bound_minus_target"] / float(h) ** 2) for q in res["nodes"]],
                  time=time.time() - t0))
    dump("lifted2")


if __name__ == "__main__":
    for part in sys.argv[1:]:
        dict(lifted=part_lifted, lifted2=part_lifted2, eps=part_eps, epsexact=part_epsexact, qneg=part_qneg)[part]()
