"""Search for instances with a rigid breakpoint a (N_opt <= 2) maximizing the
minimizer rule's tree.  H = max(chord of y^2 on [0,a], chord on [a,1], extra
lines tangent to y^2 + mu_i at p_i)."""
import sys
import numpy as np
from poly1d import Inst, from_lines, RULES

EPS0 = 1e-12

def build(a, ps, lmus):
    lines = [(a, 1e-13), (1 + a, -a + 1e-13), (2 * a, -a * a + EPS0), (0.0, 1e-3), (2.0, -1.0 + 1e-3)]
    for p, lm in zip(ps, lmus):
        mu = (a - p) ** 2 / (1 + np.exp(-lm))
        lines.append((2 * p, -p * p + mu))
    xs, ms = from_lines(lines)
    return Inst(xs, ms)

def evaluate(a, ps, lmus, rule="min"):
    try:
        I = build(a, ps, lmus)
    except ValueError:
        return None
    eps = I.m.min()
    t = I.tree(RULES[rule], cap=100000)
    return t, I.nopt(), eps

if __name__ == "__main__":
    rule = sys.argv[1]; K = int(sys.argv[2]); iters = int(sys.argv[3]); seed = int(sys.argv[4])
    epsmin = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-30
    rng = np.random.default_rng(seed)
    a = 1.0 / 3.0
    best_overall = None
    for rep in range(iters):
        ps = a + rng.normal(0, 0.1, K) * np.exp(rng.uniform(-8, 0, K))
        lmus = rng.normal(0, 3, K)
        cur = evaluate(a, ps, lmus, rule)
        for it in range(400):
            msk = rng.uniform(size=K) < 0.3
            ps2 = ps + msk * rng.normal(0, 1, K) * np.abs(ps - a) * 0.3
            lm2 = lmus + (rng.uniform(size=K) < 0.3) * rng.normal(0, 1.0, K)
            r = evaluate(a, ps2, lm2, rule)
            if r is None:
                continue
            if r[0] >= cur[0]:
                ps, lmus, cur = ps2, lm2, r
        print(rule, rep, "T=%d N=%d eps=%.3g" % cur, flush=True)
        if best_overall is None or cur[0] > best_overall[0][0]:
            best_overall = (cur, ps.copy(), lmus.copy())
    print("BEST", best_overall[0])
    np.savez(f"n2_{rule}_{K}_{seed}.npz", ps=best_overall[1], lmus=best_overall[2])
