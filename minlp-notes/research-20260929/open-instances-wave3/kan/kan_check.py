"""Independent checks of the KAN decoding and bounds.

1. full_point(M, u): builds every OSIL variable from the inputs u by generic row
   propagation (an equality row with exactly one unknown variable, appearing
   linearly, determines it; when an edge argument becomes known its interval
   binary is set).  This does not use the decoded spline polynomials; success
   for all variables shows that inputs + interval binaries determine the point.
2. The point is evaluated on the raw OSIL rows (ev.py, 60 digits): objective,
   max row violation, max bound violation.
3. Random-point test: the OSIL objective at random inputs lies inside the B&B
   box enclosures of f~ widened by Delta.

    python3 kan_check.py <name> [u1 u2 ...]
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import ev  # noqa: E402
import osilx  # noqa: E402

import kan_model as km  # noqa: E402

DPS = 60


def full_point(M, u, dps=DPS, choose="first"):
    """u: list of mp numbers (or strings) for the input roots. Returns x (list of mpf)."""
    I = M["I"]
    cons = I["cons"]
    nv = len(I["names"])
    with mp.workdps(dps):
        x = [None] * nv
        for i, R in enumerate(M["inputs"]):
            x[R] = mp.mpf(u[i])
        edge_of_z = {E["z"]: E for E in M["edges"]}
        rows = [c for c in cons if c["lb"] == c["ub"]]
        progress = True
        while progress:
            progress = False
            for E in M["edges"]:
                z = E["z"]
                if x[z] is not None and x[E["bins"][0]] is None:
                    zq = x[z]
                    ks = [k for k in range(len(E["bins"])) if mp.mpf(E["lo"][k].numerator) / E["lo"][k].denominator <= zq
                          <= mp.mpf(E["hi"][k].numerator) / E["hi"][k].denominator]
                    assert ks, f"edge argument {I['names'][z]} = {zq} lies in no interval"
                    k = ks[0] if choose == "first" else ks[-1]
                    for kk, b in enumerate(E["bins"]):
                        x[b] = mp.mpf(1 if kk == k else 0)
                    progress = True
            for c in rows:
                unk = [v for v in c["lin"] if x[v] is None]
                qv = {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
                if len(unk) != 1 or unk[0] in qv:
                    continue
                if any(x[a] is None or x[b] is None for a, b, _ in c["quad"]):
                    continue
                v = unk[0]
                rest = dict(c)
                rest = dict(c, lin={j: a for j, a in c["lin"].items() if j != v})
                if c["nl"] is not None:
                    # nl must not involve v
                    def vars_of(t):
                        if t[0] == "var":
                            return {t[1]}
                        if t[0] == "num":
                            return set()
                        return set().union(*[vars_of(s) for s in t[1:]])
                    if v in vars_of(c["nl"]) or any(x[w] is None for w in vars_of(c["nl"])):
                        continue
                s = osilx.ev_row(rest, x, mp.mpf, ev.MPFNS)
                x[v] = (mp.mpf(c["lb"]) - s) / mp.mpf(c["lin"][v])
                progress = True
        missing = [I["names"][j] for j in range(nv) if x[j] is None]
        assert not missing, f"undetermined: {missing[:10]}"
        return x


def evaluate(M, x, dps=DPS):
    r = ev.evaluate(M["I"], x, dps)
    return r


def row_violations_by_kind(M, x, dps=DPS):
    """max violation over partition rows and over all other rows."""
    I = M["I"]
    part = set()
    for E in M["edges"]:
        part |= set(E.get("partition_rows", []))
    worst = {"partition": mp.mpf(0), "other": mp.mpf(0)}
    with mp.workdps(dps):
        for c in I["cons"]:
            v = osilx.ev_row(c, x, mp.mpf, ev.MPFNS)
            viol = mp.mpf(0)
            if not osilx.isinf(c["lb"]):
                viol = max(viol, mp.mpf(c["lb"]) - v)
            if not osilx.isinf(c["ub"]):
                viol = max(viol, v - mp.mpf(c["ub"]))
            kk = "partition" if c["name"] in part else "other"
            worst[kk] = max(worst[kk], viol)
    return worst


def point_report(M, u, label=""):
    x = full_point(M, u)
    r = evaluate(M, x)
    w = row_violations_by_kind(M, x)
    print(f"{label} obj {mp.nstr(r['obj'], 20)}  max row viol {mp.nstr(r['row_viol'], 3)} ({r['worst_row']})"
          f"  [partition rows {mp.nstr(w['partition'], 3)}, other rows {mp.nstr(w['other'], 3)}]"
          f"  max bound viol {mp.nstr(r['bound_viol'], 3)} ({r['worst_var']})")
    return x, r


def write_sol(M, x, path, digits=30):
    with open(path, "w") as f:
        for nm, v in zip(M["I"]["names"], x):
            f.write(f"{nm} {mp.nstr(v, digits, min_fixed=-10**9, max_fixed=10**9)}\n")


def random_test(name, nsamp=40, seed=1):
    """OSIL objective at random inputs vs rigorous enclosures of f~ on small boxes."""
    import kan_bb as kb
    net = kb.Net(name)
    M = net.M
    rng = np.random.default_rng(seed)
    worst = 0.0
    nfeas = 0
    Delta = float(net.Delta)
    for _ in range(nsamp):
        u = net.ulo + (net.uhi - net.ulo) * rng.random(net.d)
        x = full_point(M, [mp.mpf(float(v)) for v in u])
        r = evaluate(M, x)
        f = float(r["obj"])
        for w in (0.0, 1e-6, 1e-3):
            lo = np.maximum(u - w, net.ulo)[None, :]
            hi = np.minimum(u + w, net.uhi)[None, :]
            Ph = net.layer1(lo, hi, need=(0,))
            H = net.hsum(Ph)
            Fb = net.fval_box(H)
            assert Fb.lo[0] - Delta <= f <= Fb.hi[0] + Delta, (u, f, Fb.lo, Fb.hi)
            R = net.bound(lo, hi)
            hmod = np.array([float(x[Hd["h"]]) for Hd in M["hidden"]])
            feas = np.all((hmod >= net.hlo) & (hmod <= net.hhi))
            if feas:
                assert R["lb"][0] - Delta <= f, (u, f, R["lb"])
        if w == 0.0:
            pass
        fv, _ = net.point(u[None, :])
        worst = max(worst, abs(f - 0.5 * (fv.lo[0] + fv.hi[0])))
        nfeas += 1
    print(f"random test {name}: {nsamp} points, max |OSIL obj - f~| = {worst:.3e} (Delta = {Delta:.3e}); all enclosures hold")


if __name__ == "__main__":
    name = sys.argv[1]
    M = km.decode(name)
    if len(sys.argv) > 2 and sys.argv[2] == "random":
        random_test(name)
    elif len(sys.argv) > 2:
        u = sys.argv[2:]
        point_report(M, u, "point")
