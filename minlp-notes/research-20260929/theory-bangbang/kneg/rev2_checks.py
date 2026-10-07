"""Targeted checks for the revision of kappa-negative.md after review round 2
(reviews/kappa-negative-confirm-r1.md, items R1-R3 and nits).

usage: OMP_NUM_THREADS=1 python3 rev2_checks.py PART [PART ...]    PART in: two4000 eps01 tallies
  two4000  (R1)  Section 9.1, kappa = -0.5, N = 4000 (the three grids where the first revision did not run
                 the certificate): exact KKT point, plain gap, and the exact box branch and bound
                 certify_multi of run_multi.part_two (same settings, max_nodes = 150).
  eps01    (R2)  toy plus, kappa = -0.5: the float greedy partition at epsilon / h^2 = 1e-1 for
                 N = 1000, 4000, 8000 (node ends), as in run_kneg.part_eps.
  tallies  (R2, R3, nits)  read-only tallies of logs/eps.json and logs/sweep.json: per-side predicted
                 counts for kappa = -0.5; break times after theta_1 for the strong-drop configurations on
                 grids with a fractional second switch; layer-law ratios; e_2 and eta_hat_1 for -0.275.
Each part prints JSON lines and writes logs/rev2_<part>.json.
"""
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LOG = os.path.join(HERE, "logs")


def out(name, recs):
    with open(os.path.join(LOG, f"rev2_{name}.json"), "w") as f:
        json.dump(recs, f, indent=1, default=float)


def emit(recs, rec):
    print(json.dumps(rec, default=float), flush=True)
    recs.append(rec)


def part_two4000():
    from ktoy import kkt, exact_kkt, fam_const, bound
    from lifted import certify_multi
    from run_multi import toy2, structure, switching_stages
    recs = []
    N = 4000
    for (k, t1, t2) in ((0.5, 0.5, 1.5), (0.5, 0.7, 1.3), (0.5, 0.75, 1.25)):
        t0 = time.time()
        toy = toy2(((0.0, k),), t1, t2)
        sw = structure(toy)
        kk = kkt(toy, N, sw)
        Z = exact_kkt(toy, kk)
        h = Z["h"]
        P = fam_const(N, -Fr(k))
        B, L, _ = bound(toy, Z, P)
        rec = dict(kappa=-k, t1=t1, t2=t2, N=N, switch_stages=switching_stages(Z), frac=Z["frac"],
                   u_frac=[float(Z["u"][t]) for t in Z["frac"]], gap_over_h2=float((Z["J"] - B) / h ** 2),
                   failing=[(t, float(v / h ** 2)) for t, v in L.items() if v > 0])
        if B != Z["J"]:
            res = certify_multi(toy, Z, P, Z["J"], max_nodes=150)
            inc = res["incumbent"]
            rec.update(cert_ok=res["ok"], cert_nodes=res["n_nodes"], cert_leaves=res.get("n_leaves"),
                       incumbent_improved=inc["improved"],
                       incumbent_J_minus_J_over_h2=float((inc["J"] - Z["J"]) / h ** 2),
                       # leaves only: fixed nodes by their fixed bound, lifted nodes by their lifted bound
                       min_leaf_margin_over_h2=min(q["fixed_bound_minus_target"] if q["kind"] == "fixed"
                                                   else q["bound_minus_target"] for q in res["nodes"]
                                                   if q["kind"] in ("fixed", "lifted")) / float(h) ** 2,
                       cert_kinds=[(q["kind"], q.get("stages", q.get("stage")), q.get("box")) for q in res["nodes"]])
        rec["time"] = time.time() - t0
        emit(recs, rec)
        out("two4000", recs)


def part_eps01():
    from ktoy import kkt, best_bang
    from lifted import greedy_partition
    from run_kneg import plus, predicted_count
    recs = []
    k, er = 0.5, 1e-1
    toy = plus(k, R=2.0)
    sw = best_bang(toy, 200, 1)
    for N in (1000, 4000, 8000):
        kk = kkt(toy, N, sw)
        n = kk["frac"][0]
        h = toy.T / N
        q = h * (N - 1 - n) + toy.phi2
        ub = kk["u"][n]
        nodes = greedy_partition(toy, N, kk["u"], n, kk["J"], er * h * h, k, h * h)
        w0 = math.sqrt(2 * er / k)
        pc, rho = predicted_count(q, k, w0, 1 - ub, 1 + ub)
        emit(recs, dict(N=N, n=n, u_n=ub, w0=w0, dist_to_u_minus=1 + ub, dist_to_u_plus=1 - ub,
                        n_nodes=len(nodes), predicted=pc, nodes=[(round(a, 4), round(b, 4)) for (a, b, _) in nodes]))
    out("eps01", recs)


def part_tallies():
    recs = []
    eps = json.load(open(os.path.join(LOG, "eps.json")))
    # R2: per-side predicted counts, both toys
    for r in eps:
        if "n_nodes" not in r:
            continue
        kap, ub, er = r["k"], r["u_n"], r["eps_over_h2"]
        w0 = math.sqrt(2 * er / kap)
        side = {}
        for name, a in (("plus", 1 - ub), ("minus", 1 + ub)):
            side[name] = math.ceil(math.log(a / w0) / math.log(r["rho_star"])) if a > w0 else 0
        emit(recs, dict(check="R2_eps_side_counts", kappa=-kap, N=r["N"], u_n=round(ub, 4), eps_over_h2=er,
                        w0=round(w0, 4), observed=r["n_nodes"], predicted=r["predicted"], side_pred=side))
    sweep = json.load(open(os.path.join(LOG, "sweep.json")))
    # R3: strong drop (kappa 1 -> 0): break time after theta_1 on grids with a fractional second switch
    for (t1, t2) in ((0.5, 1.5), (0.55, 1.45), (0.45, 1.55)):
        rows = [r for r in sweep if r.get("kappa1") == 1.0 and r.get("t1") == t1 and r.get("t2") == t2]
        fr = [(r["N"], r["break_minus_s1"], r["break_time_minus_theta1"]) for r in rows if r["s2"] in r["frac"]]
        vx = [(r["N"], r["break_minus_s1"]) for r in rows if r["s2"] not in r["frac"]]
        emit(recs, dict(check="R3_break_times", t1=t1, t2=t2, frac_second_switch=fr, vertex_second_switch=vx))
    # R3: layer law s_b / s_1 = exp(-2 gamma / (Delta |eta|)), Delta = 2, and the implied matching scale s_1
    # Round-2 values, read off the round-2 sweep log whose theta_1 had the wrong sign of u[s1]; superseded by
    # rev3_checks.py tallies, which computes the ranges from the corrected log (kappa-negative.md, Sec. 15).
    obs = {(0.5, 1.5): (5.7e-4, 6.7e-4), (0.55, 1.45): (5.3e-4, 9.2e-4), (0.45, 1.55): (2.0e-4, 2.1e-4)}
    for (cfg, gam, eta) in (((0.5, 1.5), 3.70, 0.59), ((0.55, 1.45), 3.58, 0.69), ((0.45, 1.55), 3.81, 0.49),
                            ((0.6, 1.4), 3.5, 0.275)):
        ratio = math.exp(-2 * gam / (2 * eta))
        rec = dict(check="R3_layer_law", cfg=cfg, gamma=gam, abs_eta=eta, sb_over_s1=ratio)
        if cfg in obs:
            rec["implied_s1"] = [obs[cfg][0] / ratio, obs[cfg][1] / ratio]
        emit(recs, rec)
    # nits: -0.275 configuration, e_2 and eta_hat_1 on breaking and non-breaking grids
    rows = [r for r in sweep if r.get("kappa1") == 0.5 and r.get("kappa2") == 0.0 and r.get("t1") == 0.6]
    brk = [(r["N"], round(r["e2"], 4), round(r["eta_hat_1"], 4)) for r in rows if r["break_minus_s1"] is not None]
    nob = [(r["N"], round(r["e2"], 4), round(r["eta_hat_1"], 4)) for r in rows if r["break_minus_s1"] is None]
    emit(recs, dict(check="nits_-0.275", breaking=brk, not_breaking=nob,
                    max_eta_hat_1_breaking=max(x[2] for x in brk), max_e2_breaking=max(x[1] for x in brk),
                    min_e2_not_breaking=min(x[1] for x in nob), min_eta_hat_1_not_breaking=min(x[2] for x in nob)))
    out("tallies", recs)


if __name__ == "__main__":
    for part in sys.argv[1:]:
        dict(two4000=part_two4000, eps01=part_eps01, tallies=part_tallies)[part]()
