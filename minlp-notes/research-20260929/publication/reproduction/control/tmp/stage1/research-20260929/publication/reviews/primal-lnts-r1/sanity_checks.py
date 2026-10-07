"""Sanity checks for verify_lnts_points.py (reviewer's own code).

Usage: python3 sanity_checks.py

1. Jacobian: my interval forward-mode Jacobian at the box centre vs central
   finite differences of my residual F (numerical, step 1e-35, 120 digits).
2. Mutations: the Krawczyk test of verify_lnts_points.py must fail on
   slightly wrong inputs (control + 1e-45; OSIL constant 100 -> 100 + 1e-40;
   fixed value 45 -> 45 + 1e-40; h centre + 2 radii) and pass on the
   unchanged input.
3. Earlier double vectors (open-instances/logs/lnts_lnts<N>_primal.txt) vs the
   new points: max |old - new| and number of coordinates equal to the new value
   rounded to double.
"""
import json
import os
import tempfile
from fractions import Fraction as Fr

from mpmath import iv, mp

import verify_lnts_points as V

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
OLD = _REPO + "/research-20260929/open-instances/logs/lnts_lnts{}_primal.txt"


def setup(N, osil=None, P=None):
    P = P or json.load(open(V.PT.format(N)))
    Vv, obj, C = V.read_osil(osil or P["osil"])
    names = [v["name"] for v in Vv]
    idx = {nm: j for j, nm in enumerate(names)}
    fixedpars = {idx[nm]: V.I(Fr(s)) for nm, s in P["fixed_controls"].items()}
    zvars = [idx[nm] for nm in P["unknowns_box"]]
    cen = [Fr(P["unknowns_box"][names[j]]["centre"]) for j in zvars]
    rad = [Fr(P["unknowns_box"][names[j]]["radius"]) for j in zvars]
    steps, resid = V.plan(Vv, C, set(fixedpars) | set(zvars))
    return Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid


def Fpoint(S, z):
    Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid = S
    V.ZERO3 = (iv.mpf(0),) * 3
    pv = {j: V.AD(q, V.ZERO3) for j, q in fixedpars.items()}
    pv.update({zvars[k]: V.AD(V.I(z[k]), V.ZERO3) for k in range(3)})
    X, F = V.evaluate(Vv, C, steps, resid, pv)
    out = []
    for f in F:
        a, b = V.ends(f.v)
        out.append((a + b) / 2)
    return out, X


def jac_check(N):
    S = setup(N)
    Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid = S
    Xb = [V.I(c) for c in cen]
    K, Fy, J = V.krawczyk(Vv, C, steps, resid, fixedpars, zvars, [V.I(c) for c in cen], Xb)
    Jm = [[sum(V.ends(J[i][j])) / 2 for j in range(3)] for i in range(3)]
    st = Fr(1, 10**35)
    worst = 0
    scale = max(abs(x) for r in Jm for x in r)
    for k in range(3):
        zp, zm = list(cen), list(cen)
        zp[k] += st
        zm[k] -= st
        Fp, _ = Fpoint(S, zp)
        Fm, _ = Fpoint(S, zm)
        for i in range(3):
            fd = (Fp[i] - Fm[i]) / (2 * st)
            worst = max(worst, abs(fd - Jm[i][k]) / scale)
    return float(worst)


def krawczyk_passes(N, osil=None, P=None):
    S = setup(N, osil, P)
    Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid = S
    Xb = [V.mk(V.I(c - r)._mpi_[0], V.I(c + r)._mpi_[1]) for c, r in zip(cen, rad)]
    K, _, _ = V.krawczyk(Vv, C, steps, resid, fixedpars, zvars, [V.I(c) for c in cen], Xb)
    return all(V.ends(K[k])[0] > V.ends(Xb[k])[0] and V.ends(K[k])[1] < V.ends(Xb[k])[1] for k in range(3))


def mutations(N=50):
    P0 = json.load(open(V.PT.format(N)))
    src = open(P0["osil"]).read()
    res = {}
    res["unchanged"] = krawczyk_passes(N)
    P = json.loads(json.dumps(P0))
    P["fixed_controls"]["x2"] = str(Fr(P["fixed_controls"]["x2"]) + Fr(1, 10**45))
    res["control x2 + 1e-45"] = krawczyk_passes(N, P=P)
    P = json.loads(json.dumps(P0))
    d = P["unknowns_box"]["x257"]
    d["centre"] = str(Fr(d["centre"]) + 2 * Fr(d["radius"]))
    res["h centre + 2 radii"] = krawczyk_passes(N, P=P)
    with tempfile.TemporaryDirectory() as td:
        for tag, a, b in (("OSIL first 100 -> 100+1e-40", '<number value="100"/>',
                           '<number value="100.0000000000000000000000000000000000000001"/>'),
                          ("OSIL vx_N 45 -> 45+1e-40", 'lb="45" ub="45"',
                           'lb="45.0000000000000000000000000000000000000001" ub="45.0000000000000000000000000000000000000001"')):
            assert src.count(a) >= 1
            p = os.path.join(td, "m.osil")
            open(p, "w").write(src.replace(a, b, 1))
            res[tag] = krawczyk_passes(N, osil=p)
    return res


def old_vectors(N):
    S = setup(N)
    Vv, obj, C, names, fixedpars, zvars, cen, rad, steps, resid = S
    _, X = Fpoint(S, cen)  # states at the centre; the zero is within 1e-50 of it
    new = [sum(V.ends(x.v)) / 2 for x in X]
    old = [Fr(float(s)) for s in open(OLD.format(N)).read().split()]
    assert len(old) == len(new)
    diffs = [abs(o - n) for o, n in zip(old, new)]
    j = max(range(len(diffs)), key=lambda k: diffs[k])
    eq = sum(1 for o, n in zip(old, new) if o == Fr(float(n)))
    neq = [names[k] for k, (o, n) in enumerate(zip(old, new)) if o != Fr(float(n))]
    return dict(max_abs_diff=float(diffs[j]), at=names[j], equal_to_double_rounding=eq, n=len(new), differing=neq)


if __name__ == "__main__":
    out = {}
    for N in (50, 100, 200, 400):
        out[f"lnts{N}"] = dict(jac_rel_diff_vs_fd=jac_check(N), old=old_vectors(N))
        print(N, out[f"lnts{N}"], flush=True)
    out["mutations_lnts50"] = mutations(50)
    print(out["mutations_lnts50"], flush=True)
    json.dump(out, open("sanity_checks.json", "w"), indent=1)
