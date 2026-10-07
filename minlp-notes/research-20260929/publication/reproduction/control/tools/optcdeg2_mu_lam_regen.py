"""Test whether the tracked multiplier files open-instances/logs/optcdeg2_mu.npy and
optcdeg2_lam.npy (no script in the repository writes them) are exactly the multipliers that
optcdeg2_bound.main() computes. Run from open-instances/ (python3 - < this file).
Writes nothing; prints a JSON comparison."""
import json

import numpy as np

from optcdeg2_common import costates, load_minlplib

u, y, v = load_minlplib()
sw = np.where(np.diff(np.sign(u)) != 0)[0]
m0, l0 = costates(y, v, 0.0)
m1, l1 = costates(y, v, 1.0)
c = -l0[sw[1]] / (l1[sw[1]] - l0[sw[1]])
mu, lam = costates(y, v, c)
mu_s, lam_s = np.load("logs/optcdeg2_mu.npy"), np.load("logs/optcdeg2_lam.npy")
out = dict(lamN1=float(c), shapes=[list(mu.shape), list(mu_s.shape), list(lam.shape), list(lam_s.shape)],
           dtypes=[str(mu.dtype), str(mu_s.dtype)],
           mu_bitwise_equal=bool(mu.shape == mu_s.shape and mu.tobytes() == mu_s.tobytes()),
           lam_bitwise_equal=bool(lam.shape == lam_s.shape and lam.tobytes() == lam_s.tobytes()),
           mu_max_absdiff=float(np.max(np.abs(mu - mu_s))) if mu.shape == mu_s.shape else None,
           lam_max_absdiff=float(np.max(np.abs(lam - lam_s))) if lam.shape == lam_s.shape else None)
print(json.dumps(out, indent=1))
