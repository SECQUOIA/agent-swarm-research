"""Validate saved curve-hull cuts.
1. At the best known MINLPLib point (the bold primal bound's sol file, downloaded to sols/): slack c0 + c.phi(x*) of every cut,
   with phi evaluated in float at x*'s value, relative to 1 + |c|.|phi(x*)|.  Also reports whether x* lies
   in the curve interval (it must, for model bounds; for presolve bounds this is a check of those bounds).
2. At 2,000 random points of every distinct curve (and the interval ends).
python validate.py <instance> [cuts file]"""
import json, os, sys, urllib.request
import numpy as np
import sympy as sp
import model
from curvehull import T

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(0)


def sol_values(name):
    """Best known point listed on the MINLPLib page (listed_bounds.json, from listed.py); p1 otherwise."""
    lb = json.load(open(os.path.join(HERE, "listed_bounds.json")))
    pt = (lb.get(name) or {}).get("best_point") or "p1"
    os.makedirs(os.path.join(HERE, "sols"), exist_ok=True)
    f = os.path.join(HERE, "sols", f"{name}.{pt}.sol")
    if not os.path.exists(f):
        try:
            urllib.request.urlretrieve(f"https://www.minlplib.org/sol/{name}.{pt}.sol", f)
        except Exception as e:
            return None
    vals = {}
    for line in open(f):
        p = line.split()
        if len(p) >= 2:
            try:
                vals[p[0]] = float(p[1])
            except ValueError:
                pass
    return vals


def main(name, path=None):
    path = path or os.path.join(HERE, "cuts", f"{name}.json")
    cuts = json.load(open(path))
    inst = model.read_osil(model.OSIL.format(name))
    sol = sol_values(name)
    fn = {}
    worst_sol, worst_rand, outside = np.inf, np.inf, 0
    for c in cuts:
        key = tuple(c["funcs"])
        if key not in fn:
            fs = [sp.sympify(s, locals={"t": T}) for s in key]
            fn[key] = [sp.lambdify(T, f, "numpy") for f in fs]
        F = fn[key]
        phi = lambda t: np.vstack([np.atleast_1d(t)] + [np.broadcast_to(np.asarray(f(np.atleast_1d(t)), float), np.atleast_1d(t).shape) for f in F])
        cc = np.array(c["c"])
        tt = np.concatenate([rng.uniform(c["l"], c["u"], 2000), [c["l"], c["u"]]])
        P = phi(tt)
        worst_rand = min(worst_rand, float(((c["c0"] + cc @ P) / (1 + np.abs(cc) @ np.abs(P))).min()))
        if sol is not None:
            xv = sol.get(inst.var_names[c["v"]], 0.0)
            if not (c["l"] - 1e-9 <= xv <= c["u"] + 1e-9):
                outside += 1
                continue
            p = phi(xv)[:, 0]
            worst_sol = min(worst_sol, float((c["c0"] + cc @ p) / (1 + np.abs(cc) @ np.abs(p))))
    print(json.dumps({"name": name, "file": os.path.basename(path), "ncuts": len(cuts), "sol": sol is not None,
                      "sol_obj": None if sol is None else sol.get("objvar"),
                      "min_rel_slack_at_sol": None if sol is None else worst_sol,
                      "sol_outside_interval": outside, "min_rel_slack_random_curve": worst_rand}))


if __name__ == "__main__":
    main(*sys.argv[1:])
