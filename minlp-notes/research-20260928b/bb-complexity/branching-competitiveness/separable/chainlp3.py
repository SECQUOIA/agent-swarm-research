"""Random search: longest chain D^1=[0,1] > D^2 > ... (parent-child) of split nodes
(F < -beta, w >= tau) inside l = [0,1] valid at beta + kappa*tau (LP in the values of m)."""
import sys, random
import numpy as np
from chainlp2 import lp

def rand_chain(r, rng):
    l, u = 0.0, 1.0
    nodes = []
    for k in range(r):
        L = u - l
        t = rng.random()
        mode = rng.random()
        if mode < 0.3:
            f = 10 ** (-rng.uniform(0, 4))
        elif mode < 0.6:
            f = 1 - 10 ** (-rng.uniform(0, 4))
        else:
            f = rng.uniform(0.05, 0.95)
        y = l + f * L
        nodes.append((l, u, y))
        if rng.random() < 0.5:
            u = y
        else:
            l = y
    return nodes

if __name__ == "__main__":
    kappa, trials, seed = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    best = 0
    for t in range(trials):
        r = rng.randint(best + 1, best + 3) if best < 12 else best + 1
        nodes = rand_chain(r, rng)
        s = lp(nodes, kappa)
        if s is not None and s > 1e-6:
            best = r
            print(f"kappa={kappa}: feasible chain length {r} slack {s:.3g}: " +
                  " ".join(f"[{l:.4g},{u:.4g}]@{y:.4g}" for l, u, y in nodes), flush=True)
    print("max feasible length found", best)
