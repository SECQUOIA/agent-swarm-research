"""Random + hill-climbing search for instances maximizing T_rule / (2 N_opt - 1)."""
import sys
import numpy as np
from poly1d import Inst, convexify, RULES

def make(xs, lm, eps):
    xs = np.concatenate([[0.0, 1.0], xs])
    ms = np.concatenate([[1.0, 1.0], np.exp(lm)])
    X, M = convexify(xs, ms)
    M = M - M.min() + eps
    return Inst(X, M)

def score(I, rule):
    t = I.tree(RULES[rule], cap=200000)
    n = I.nopt()
    return (t if t is not None else 200000) / (2 * n - 1), t, n

def search(rule, K, eps, iters, seed):
    rng = np.random.default_rng(seed)
    best = None
    for rep in range(iters):
        xs = rng.uniform(0, 1, K)
        lm = rng.uniform(np.log(eps), 0, K)
        I = make(xs, lm, eps)
        s = score(I, rule)
        # local hill climb
        for it in range(200):
            xs2 = np.clip(xs + rng.normal(0, 0.02, K) * (rng.uniform(size=K) < 0.3), 1e-9, 1 - 1e-9)
            lm2 = np.clip(lm + rng.normal(0, 0.5, K) * (rng.uniform(size=K) < 0.3), np.log(eps), 0)
            I2 = make(xs2, lm2, eps)
            s2 = score(I2, rule)
            if s2[0] >= s[0]:
                xs, lm, s = xs2, lm2, s2
        if best is None or s[0] > best[0][0]:
            best = (s, xs.copy(), lm.copy())
        print(rule, K, eps, rep, "ratio %.3f T=%s N=%d" % s, flush=True)
    return best

if __name__ == "__main__":
    rule = sys.argv[1]; K = int(sys.argv[2]); eps = float(sys.argv[3]); iters = int(sys.argv[4])
    best = search(rule, K, eps, iters, 1)
    print("BEST", best[0])
    np.savez(f"search_{rule}_{K}_{eps:g}.npz", xs=best[1], lm=best[2])
