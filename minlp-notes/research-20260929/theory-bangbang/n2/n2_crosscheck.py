"""Cross-check of the box minimization: for stage residuals of example A (N = 200), compare the
face-enumeration loss with the minimum over 2e5 random points plus a 31^3 grid of the box
(sampling can only overestimate the minimum, so sampled_loss <= enum_loss is required)."""
import json
import numpy as np
from model import Par
from discrete import solve_kkt, fam_rmax, fam_lyap, stage_quadratics, stage_losses, reach_box

EX = {"A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5),
      "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5)}
N = 200
rng = np.random.default_rng(0)
out = {}
for ex, p in EX.items():
  kk = solve_kkt(p, N)
  lo_b, hi_b = reach_box(p, N, kk["h"])
  for name, Ps in [(ex + ":rmax", fam_rmax(p, kk, 0.02)[0]), (ex + ":lyap", fam_lyap(p, kk, 0.02))]:
      loss, _ = stage_losses(p, kk, Ps)
      quads = stage_quadratics(p, kk, Ps)
      worst = -np.inf
      stages = sorted(set(list(range(1, N, 13)) + [kk["m"] - 1, kk["m"], kk["m"] + 1, kk["m"] + 2, N - 1]))
      for t in stages:
          g, hs, K, hb, hk = quads[t]
          lo = np.array([lo_b[t, 0] - kk["x"][t, 0], lo_b[t, 1] - kk["x"][t, 1], -1 - kk["u"][t]])
          hi = np.array([hi_b[t, 0] - kk["x"][t, 0], hi_b[t, 1] - kk["x"][t, 1], 1 - kk["u"][t]])
          Z = lo + (hi - lo) * rng.random((200000, 3))
          gr = [np.linspace(lo[i], hi[i], 31) for i in range(3)]
          Z = np.vstack([Z, np.stack(np.meshgrid(*gr, indexing="ij"), -1).reshape(-1, 3)])
          d, om = Z[:, :2], Z[:, 2]
          val = d @ g + hs * om + 0.5 * np.einsum("ni,ij,nj->n", d, K, d) + om * (d @ hb) + 0.5 * hk * om ** 2
          sampled_loss = -val.min()
          worst = max(worst, sampled_loss - loss[t])
      out[name] = dict(stages=len(stages), max_sampled_minus_enum=float(worst))
      print(name, out[name], flush=True)
json.dump(out, open("logs/n2_crosscheck.json", "w"), indent=1)
