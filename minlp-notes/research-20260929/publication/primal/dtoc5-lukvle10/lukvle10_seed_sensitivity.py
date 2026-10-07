"""lukvle10 (illustration, floating point, not a proof): how many seed digits does the forward
recursion need? Seeds x_0, x_1 = KKT point rounded to D decimals; the rows are solved forward in
1500-digit mpmath; we report the largest deviation from the KKT point and the objective."""
import json

import mpmath as mp

mp.mp.dps = 1500
kkt = [mp.mpf(line.split()[1]) for line in open("logs/lukvle10_kkt_x.txt")]
p5 = {}
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
for line in open(_REPO + "/research-20260929/open-instances/minlplib_sol/lukvle10.p5.sol"):
    nm, v = line.split()
    p5[nm] = mp.mpf(v)


def run(x0, x1):
    x = [x0, x1]
    for j in range(998):
        nxt = (1 - x[j] + 3 * x[j + 1] - 2 * x[j + 1] ** 2) / 2
        if abs(nxt) > 10:
            return dict(diverged_at_index=j + 2)
        x.append(nxt)
    dev = max(abs(x[k] - kkt[k]) for k in range(1000))
    obj = mp.fsum((x[2 * i] ** 2) ** (x[2 * i + 1] ** 2 + 1) + (x[2 * i + 1] ** 2) ** (x[2 * i] ** 2 + 1)
                  for i in range(500))
    first = next((k for k in range(1000) if abs(x[k] - kkt[k]) > mp.mpf("1e-6")), None)
    return dict(max_dev=mp.nstr(dev, 3), first_index_dev_above_1e_6=first, objective=mp.nstr(obj, 20))


out = {"p5_seeds_15_digits": run(p5["x1"], p5["x2"])}
for D in (50, 100, 200, 300, 400, 420, 440, 460, 500, 640):
    out[f"D={D}"] = run(mp.nint(kkt[0] * 10 ** D) / 10 ** D, mp.nint(kkt[1] * 10 ** D) / 10 ** D)
print(json.dumps(out, indent=1))
json.dump(out, open("logs/lukvle10_seed_sensitivity.json", "w"), indent=1)
