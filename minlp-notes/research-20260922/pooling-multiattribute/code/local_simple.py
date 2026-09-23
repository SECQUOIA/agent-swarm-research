"""Simplest K=2 family: box pool qualities, a single bypass quality vector beta (y = beta z)."""
import itertools, json, sys
import numpy as np
from local import run_case, summarize
rng = np.random.default_rng(int(sys.argv[1]))
for trial in range(int(sys.argv[2])):
    a = rng.uniform(-2, 0.5, 2); b = a + rng.uniform(0.5, 3, 2)
    G = np.array(list(itertools.product(*[(a[k], b[k]) for k in range(2)])))
    beta = -rng.uniform(0.2, 2.5, 2) if trial % 2 == 0 else rng.uniform(-2.5, 1.0, 2)
    Bv = beta.reshape(1, 2)
    s = summarize(run_case(G, Bv, ndir=80, seed=trial)); s.update(G=[a.round(3).tolist(), b.round(3).tolist()], beta=beta.round(3).tolist())
    print(json.dumps(s), flush=True)
