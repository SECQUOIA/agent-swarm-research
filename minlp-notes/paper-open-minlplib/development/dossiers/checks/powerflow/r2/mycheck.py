"""Dossier re-check (own code): exact Lagrangian bound from stored multipliers, PD proof of
A + eps*I by integer Bareiss elimination (Sylvester: all leading principal minors > 0),
own vertex-plane validity check, and evaluation of the Lagrangian at the exactly feasible
primal centres.  Rows come from a /tmp copy of pf_model.decode (parsing and row order only).

    python3 mycheck.py root            # powerflow0030p root certificate (angle rows dropped)
    python3 mycheck.py leaves NAME TAG [noangle]
"""
import json
import sys
import time
from fractions import Fraction as Fr
from math import lcm

import mpmath as mp

sys.path.insert(0, "/tmp/pfd2")
import pf_model as pm  # noqa: E402
import leafcut as lc  # noqa: E402

D = "/tmp/pfd2/data/"
EPS = [Fr(0)] + [Fr(1, 10 ** k) for k in (10, 9, 8, 7, 6)]


def lagrangian(M, rows, raw, ybox):
    c = M["obj"]["const"]
    kap = {y: Fr(0) for y in M["ys"]}
    sig = {y: Fr(0) for y in M["ys"]}
    for y, v in M["obj"]["lin"].items():
        kap[y] += v
    for y, v in M["obj"]["qy"].items():
        sig[y] += v
    A = {}
    assert len(rows) == len(raw)
    for r, rv in zip(rows, raw):
        if rv[0] == "eq":
            assert r["lb"] == r["ub"]
            w = Fr(rv[1])
            c -= w * r["lb"]
        else:
            mp_ = Fr(rv[1]) if rv[1] is not None and rv[1] > 0 else Fr(0)
            mm_ = Fr(rv[2]) if rv[2] is not None and rv[2] > 0 else Fr(0)
            if mp_:
                assert r["ub"] is not None
                c -= mp_ * r["ub"]
            if mm_:
                assert r["lb"] is not None
                c += mm_ * r["lb"]
            w = mp_ - mm_
        if w == 0:
            continue
        for y, v in r["lin"].items():
            kap[y] += w * v
        for y, v in r["qy"].items():
            sig[y] += w * v
        for (i, j), v in r["Q"].items():
            if i == j:
                A[(i, i)] = A.get((i, i), Fr(0)) + w * v
            else:
                A[(i, j)] = A.get((i, j), Fr(0)) + w * v / 2
                A[(j, i)] = A.get((j, i), Fr(0)) + w * v / 2
    inner = Fr(0)
    for y in M["ys"]:
        s, k = sig[y], kap[y]
        assert s >= 0, ("sigma<0", y)
        lo, hi = ybox.get(y, (None, None))
        if lo is not None and hi is not None:
            cands = [lo, hi]
            if s > 0 and lo < -k / (2 * s) < hi:
                cands.append(-k / (2 * s))
            inner += min(s * t * t + k * t for t in cands)
        elif s > 0:
            t = -k / (2 * s)
            if lo is not None and t < lo:
                t = lo
            if hi is not None and t > hi:
                t = hi
            inner += s * t * t + k * t
        else:
            assert k == 0, ("unbounded y", y)
    return c, inner, kap, sig, A


def bareiss_pd(A, n, eps):
    """True iff every leading principal minor of A + eps I is > 0 (exact integers)."""
    ent = {}
    for i in range(n):
        for j in range(n):
            v = A.get((i, j), Fr(0)) + (eps if i == j else 0)
            if v:
                ent[(i, j)] = v
    den = 1
    for v in ent.values():
        den = lcm(den, v.denominator)
    M = [[0] * n for _ in range(n)]
    for (i, j), v in ent.items():
        M[i][j] = v.numerator * (den // v.denominator)
    prev = 1
    minors = []
    for k in range(n):
        p = M[k][k]
        if p <= 0:
            return False, k, minors
        minors.append(p)
        for i in range(k + 1, n):
            Mi, Mk = M[i], M[k]
            mik = Mi[k]
            for j in range(k + 1, n):
                Mi[j] = (Mi[j] * p - mik * Mk[j]) // prev
            Mi[k] = 0
        prev = p
    return True, n, minors


def certify(M, rows, raw, ybox, label):
    t = time.time()
    c, inner, kap, sig, A = lagrangian(M, rows, raw, ybox)
    n = 2 * M["n"]
    V2 = sum(M["vmax2"])
    for eps in EPS:
        ok, k, minors = bareiss_pd(A, n, eps)
        if ok:
            # smallest pivot of the LDL^T (ratio of consecutive leading minors), as a float
            piv = [Fr(minors[0])] + [Fr(minors[i], minors[i - 1]) for i in range(1, n)]
            den = 1
            # pivots above are scaled by the common denominator; report the unscaled minimum
            beta = c + inner - eps * V2
            print(f"  {label}: eps {eps} PD by Bareiss ({n} leading minors > 0); beta = {mp.nstr(mp.mpf(beta.numerator) / beta.denominator, 22)}  ({time.time()-t:.1f}s)")
            return beta, eps, (c, inner, kap, sig, A)
    print(f"  {label}: FAILED for all eps")
    return None, None, (c, inner, kap, sig, A)


def read_point(name):
    P = json.load(open(D + f"{name}.json"))
    vals = {}
    for v, d in P["fixed"].items():
        vals[v] = mp.mpf(Fr(d["value"]).numerator) / Fr(d["value"]).denominator
    for v, s in P["free"].items():
        vals[v] = mp.mpf(s)
    return vals


def point_xy(M, vals):
    names = M["I"]["names"]
    x = []
    if M["polar"]:
        for (vj, tj) in M["busmap"]:
            v, th = vals.get(names[vj], mp.mpf(0)), vals.get(names[tj], mp.mpf(0))
            x += [v * mp.cos(th), v * mp.sin(th)]
    else:
        for (a, b) in M["busmap"]:
            x += [vals.get(names[a], mp.mpf(0)), vals.get(names[b], mp.mpf(0))]
    y = {j: vals.get(names[j], mp.mpf(0)) for j in M["ys"]}
    return x, y


def lag_at(cert, x, y):
    c, inner, kap, sig, A = cert
    fr = lambda q: mp.mpf(q.numerator) / q.denominator
    val = fr(c)
    for j in kap:
        val += fr(sig[j]) * y[j] ** 2 + fr(kap[j]) * y[j]
    for (i, j), a in A.items():
        val += fr(a) * x[i] * x[j]
    return val


def obj_at(M, y):
    o = M["obj"]
    fr = lambda q: mp.mpf(q.numerator) / q.denominator
    return fr(o["const"]) + sum(fr(v) * y[j] for j, v in o["lin"].items()) + sum(fr(v) * y[j] ** 2 for j, v in o["qy"].items())


def root():
    mp.mp.dps = 60
    name = "powerflow0030p"
    M = pm.decode(name)
    S = json.load(open(D + f"{name}.sdpcert.json"))
    assert S["variant"] == "angle rows dropped"
    rows = [r for r in M["rows"] if r["kind"] != "angle"]
    from collections import Counter
    print(name, "rows", len(rows), Counter(r["kind"] for r in rows), "raw", len(S["raw"]), "boxed y", len(M["ybox"]), "ys", len(M["ys"]))
    beta, eps, cert = certify(M, rows, S["raw"], M["ybox"], "0030p root")
    print("  beta == stored bound_exact:", beta == Fr(S["bound_exact"]))
    print("  floor(beta*1e16)/1e16 =", (beta * 10 ** 16).numerator // (beta * 10 ** 16).denominator)
    x, y = point_xy(M, read_point(name))
    L, f = lag_at(cert, x, y), obj_at(M, y)
    print(f"  at exact primal centre: f = {mp.nstr(f, 25)}; L = {mp.nstr(L, 25)}; L - beta = {mp.nstr(L - mp.mpf(beta.numerator)/beta.denominator, 6)}; f - L = {mp.nstr(f - L, 6)}")


def node_rows(M, info, box):
    (p1, p2), (q1, q2), (s1, s2) = box
    ybox = dict(M["ybox"])
    ybox[info["Pg"]] = (p1, p2)
    ybox[info["Qg"]] = (q1, q2)
    L = info["L"]
    extra = [dict(name="VBL", lin={}, Q={(2 * L, 2 * L): Fr(1), (2 * L + 1, 2 * L + 1): Fr(1)}, qy={}, lb=s1, ub=s2, kind="volt")]
    planes = lc.planes3(info, box)
    # own validity check of each plane: H >= F at all 8 vertices, exact
    for (al, be, ga, de) in planes:
        for p in (p1, p2):
            for q in (q1, q2):
                for s in (s1, s2):
                    Fv = s - 2 * q / info["b"] + (q * q + p * p) / (info["b"] ** 2 * s)
                    assert al * p + be * q + ga * s + de >= Fv
    extra += lc.cut_rows3(info, box)
    return list(M["rows"]) + extra, ybox, planes


def leaves(name, tag, noangle=False):
    mp.mp.dps = 60
    M = pm.decode(name)
    info = lc.leaf_info(M)
    print(name, tag, "noangle" if noangle else "", "b =", info["b"], "Pg", M["I"]["names"][info["Pg"]], "Qg", M["I"]["names"][info["Qg"]])
    Dd = json.load(open(D + f"{name}.{tag}.json"))
    x, y = point_xy(M, read_point(name))
    N, Lb = info["N"], info["L"]
    WNN = x[2 * N] ** 2 + x[2 * N + 1] ** 2
    WLL = x[2 * Lb] ** 2 + x[2 * Lb + 1] ** 2
    Pg, Qg = y[info["Pg"]], y[info["Qg"]]
    b = mp.mpf(info["b"].numerator) / info["b"].denominator
    F = WLL - 2 * Qg / b + (Qg ** 2 + Pg ** 2) / (b ** 2 * WLL)
    print(f"  exact point: Pg {mp.nstr(Pg, 15)} Qg {mp.nstr(Qg, 15)} W_LL {mp.nstr(WLL, 15)} W_NN {mp.nstr(WNN, 15)}; W_NN - F = {mp.nstr(WNN - F, 3)}")
    fx = obj_at(M, y)
    best = None
    for Lf in Dd["leaves"]:
        box = tuple((Fr(a), Fr(c)) for a, c in Lf["box"])
        rows, ybox, planes = node_rows(M, info, box)
        raw = Lf["raw"]
        if noangle:
            raw = [rv if r["kind"] != "angle" else ("ineq", 0.0, 0.0) for r, rv in zip(rows, raw)]
        lab = str([[round(float(a), 5), round(float(c), 5)] for a, c in box])
        beta, eps, cert = certify(M, rows, raw, ybox, lab)
        assert beta is not None
        stored = Fr(Lf["bound"])
        inside = all(lo <= v <= hi for v, (lo, hi) in zip((Pg, Qg, WLL), [(mp.mpf(a.numerator) / a.denominator, mp.mpf(c.numerator) / c.denominator) for a, c in box]))
        msg = f"    own - stored = {float(beta - stored):.3e}; planes {len(planes)}"
        if inside:
            Lx = lag_at(cert, x, y)
            bf = mp.mpf(beta.numerator) / beta.denominator
            slack = [al * Pg + be * Qg + ga * WLL + de - WNN for (al, be, ga, de) in [tuple(mp.mpf(t.numerator) / t.denominator for t in H) for H in planes]]
            msg += f"; CONTAINS exact point: L(x*) - beta = {mp.nstr(Lx - bf, 6)}, f(x*) - L(x*) = {mp.nstr(fx - Lx, 6)}, plane slacks H-W_NN at x*: {[mp.nstr(s_, 3) for s_ in slack]}"
        print(msg)
        best = beta if best is None else min(best, beta)
    print(f"  minimum over leaves = {mp.nstr(mp.mpf(best.numerator) / best.denominator, 22)}; floor(min*1e12) = {(best * 10**12).numerator // (best * 10**12).denominator}")
    print(f"  stored LB_exact = {mp.nstr(mp.mpf(Fr(Dd['LB_exact']).numerator) / Fr(Dd['LB_exact']).denominator, 22)}; f(x*) = {mp.nstr(fx, 25)}")


if __name__ == "__main__":
    if sys.argv[1] == "root":
        root()
    else:
        leaves(sys.argv[2], sys.argv[3], len(sys.argv) > 4)
