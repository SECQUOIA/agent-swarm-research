"""Soundness checks of rbb's building blocks at (nearly) feasible points.

For each period of a listed MINLPLib point (row violation ~1e-11):
  1. the point lies in the FBBT box of the root (up to 1e-8);
  2. the point, extended by w = monomial values, satisfies every relaxation
     row of the root box and of random sub-boxes containing it (up to 1e-8);
  3. the rigorous bound for random objectives c and random dual vectors is
     <= c.x (+1e-7).
Violations would indicate a bug in the relaxation or in the bound formula.

usage: python3 test_relax.py T point.sol [trials]
"""
import sys
import numpy as np

import period
import rbb
import evalpt


def extend(W, xg):
    x = np.array([xg[v] for v in W.gv] + [0.0] * W.naux)
    for k, (kind, args) in enumerate(W.auxdef):
        x[W.n0 + k] = rbb.mono_val(kind, args, x)
    return x


def row_viol(L, x):
    act = np.bincount(L["ri"], weights=L["am"] * x[L["ci"]], minlength=L["m"])
    le = L["sense"] == 0
    v_le = np.max(np.maximum(act[le] - L["bh"][le], 0.0)) if le.any() else 0.0
    v_eq = np.max(np.maximum(L["bl"][~le] - act[~le], act[~le] - L["bh"][~le])) if (~le).any() else 0.0
    return max(v_le, v_eq)


def main():
    T = int(sys.argv[1])
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    D = period.setup(T)
    xs, _ = evalpt.read_sol(sys.argv[2], D["M"]["names"])
    xg = [float(v) for v in xs]
    rng = np.random.default_rng(1)
    worst = dict(box=0.0, relax=0.0, bound=-np.inf)
    for t in range(T):
        W = rbb.Window(D, t, t + 1)
        x = extend(W, xg)
        lo, hi = W.fbbt(W.lo0, W.hi0)
        worst["box"] = max(worst["box"], np.max(lo - x), np.max(x - hi))
        for trial in range(trials):
            # random sub-box containing x (clipped to the root box)
            f = rng.uniform(0, 1, size=W.n) ** 3
            l2 = np.maximum(lo, x - f * (x - lo) - 1e-9)
            h2 = np.minimum(hi, x + rng.uniform(0, 1, size=W.n) ** 3 * (hi - x) + 1e-9)
            l2 = np.minimum(l2, x)
            h2 = np.maximum(h2, x)
            b = W.isbin
            l2[b], h2[b] = np.floor(l2[b]), np.ceil(h2[b])
            r = W.fbbt(l2, h2)
            if r is None:
                print(f"period {t} trial {trial}: FBBT declared a box containing the point infeasible")
                worst["box"] = np.inf
                continue
            l2, h2 = r
            worst["box"] = max(worst["box"], np.max(l2 - x), np.max(x - h2))
            L = W.relaxation(l2, h2)
            worst["relax"] = max(worst["relax"], row_viol(L, x))
            c = rng.normal(size=W.n) * (rng.uniform(size=W.n) < 0.3)
            nu = rng.normal(size=L["m"]) * (rng.uniform(size=L["m"]) < 0.2) * 10
            B = W.safe_bound(c, l2, h2, L, nu)
            worst["bound"] = max(worst["bound"], B - c @ x)
            xl, nu2, val = W.node_lp(c, l2, h2, L)
            if nu2 is not None:
                B2 = W.safe_bound(c, l2, h2, L, nu2)
                worst["bound"] = max(worst["bound"], B2 - c @ x)
        print(f"period {t}: max box violation {worst['box']:.2e}, max relaxation-row violation "
              f"{worst['relax']:.2e}, max (bound - c.x) {worst['bound']:.2e}", flush=True)
    ok = worst["box"] <= 1e-8 and worst["relax"] <= 1e-8 and worst["bound"] <= 1e-7
    print("PASS" if ok else "FAIL", worst)


if __name__ == "__main__":
    main()
