"""Independent verifier code for the powerflow Lagrangian/SDP bounds (wave 3).

Own code: only the decimal-preserving OSIL reader (osilx.py) is shared.
The authors' model/certificate code is not imported.

Relaxation R built here from the OSIL:
  polar  : x = (e_k, f_k) per bus, e = v cos(th), f = v sin(th).  Each flow row
           y + expr(v, th) = 0 is converted to y + x^T Q x = 0 by a generic
           sympy expansion (expand_trig) and the identity expr(v,th) ==
           x^T Q x |_{e=v cos th, f=v sin th} is checked symbolically.
           Voltage rows lo <= v <= hi (lo >= 0) -> lo^2 <= e^2+f^2 <= hi^2.
           Angle-difference rows and the reference-angle row are dropped.
  rect   : rows kept as they are; the single-variable linear row on an x
           variable (f_ref = 0) is dropped.
  both   : single-variable linear rows on the remaining variables y become
           boxes of y (kept as constraints, not dualized).
Lagrangian: for multipliers w (free on equalities; vp, vm >= 0 on the upper
and lower sides of inequalities),
  obj(z) >= obj(z) + sum_eq w (h - rhs) + sum_ineq [vp (h - ub) + vm (lb - h)]
for every z in R, and the right side separates into
  const + sum_y (sigma_y y^2 + kappa_y y) + x^T A x.
"""
import os
import sys
from fractions import Fraction as Fr

import sympy as S

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def load(name):
    return osilx.read(os.path.join(OSIL, name + ".osil"))


def inf_or(s):
    return None if osilx.isinf(s) else Fr(s)


# ---------------------------------------------------------------- tree tools
def tree_vars(t, acc, in_trig=False):
    """collect (var, in_trig) occurrences"""
    if t[0] == "var":
        acc.add((t[1], in_trig))
        return
    if t[0] == "num":
        return
    for c in t[1:]:
        tree_vars(c, acc, in_trig or t[0] in ("sin", "cos"))


def to_sympy(t, sym):
    op = t[0]
    if op == "num":
        return S.Rational(Fr(t[1]).numerator, Fr(t[1]).denominator)
    if op == "var":
        c = Fr(t[2])
        return S.Rational(c.numerator, c.denominator) * sym[t[1]]
    a = [to_sympy(c, sym) for c in t[1:]]
    if op in ("sum", "plus"):
        return S.Add(*a)
    if op in ("product", "times"):
        return S.Mul(*a)
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "square":
        return a[0] ** 2
    if op == "sin":
        return S.sin(a[0])
    if op == "cos":
        return S.cos(a[0])
    raise NotImplementedError(op)


def s2f(c):
    c = S.Rational(c)
    return Fr(int(c.p), int(c.q))


# ---------------------------------------------------------------- model
def build(name, log=print):
    I = load(name)
    nv = len(I["names"])
    cons = I["cons"]
    assert all(I["lb"][j] == "-INF" and I["ub"][j] == "INF" for j in range(nv))
    assert all(c["constant"] == "0" for c in cons), "row constants"
    o = I["obj"]
    assert o["sense"] == "min" and o["nl"] is None and o["weight"] == "1"
    polar = any(c["nl"] is not None for c in cons)
    rows, box = [], {}
    dropped = {"angle": 0, "ref": 0}

    def add_box(y, cy, lb, ub):
        l2 = None if lb is None else lb / cy
        u2 = None if ub is None else ub / cy
        if cy < 0:
            l2, u2 = u2, l2
        lo, hi = box.get(y, (None, None))
        if l2 is not None:
            lo = l2 if lo is None else max(lo, l2)
        if u2 is not None:
            hi = u2 if hi is None else min(hi, u2)
        box[y] = (lo, hi)

    if polar:
        # variable classes from the trees
        V, TH = set(), set()
        for c in cons:
            if c["nl"] is not None:
                acc = set()
                tree_vars(c["nl"], acc)
                for j, it in acc:
                    (TH if it else V).add(j)
        assert not (V & TH)
        V, TH = sorted(V), sorted(TH)
        assert len(V) == len(TH)
        n = len(V)
        # pairing v_i <-> th_i by order; verified by the symbolic identities below
        pair = dict(zip(V, TH))
        bus_v = {v: k for k, v in enumerate(V)}
        r_ = {v: S.Symbol("r%d" % v, positive=True) for v in V}
        t_ = {t: S.Symbol("t%d" % t, real=True) for t in TH}
        sym = {**r_, **t_}
        cosT = {t: S.cos(t_[t]) for t in TH}
        sinT = {t: S.sin(t_[t]) for t in TH}
        vlo, vhi, nflow = {}, {}, 0
        for ri, c in enumerate(cons):
            lb, ub = inf_or(c["lb"]), inf_or(c["ub"])
            if c["nl"] is not None:
                assert lb == ub == 0 and not c["quad"] and len(c["lin"]) == 1
                (y, cy), = c["lin"].items()
                assert Fr(cy) == 1 and y not in V and y not in TH
                ex = S.expand(S.expand_trig(to_sympy(c["nl"], sym)))
                Q = {}
                for mono, coef in ex.as_coefficients_dict().items():
                    cf = s2f(coef)
                    pw = mono.as_powers_dict()
                    rs = {v: pw.get(r_[v], 0) for v in V if pw.get(r_[v], 0)}
                    trig = [(k, e) for k, e in pw.items() if k not in r_.values()]
                    if len(rs) == 1 and list(rs.values()) == [2] and not trig:
                        k = bus_v[next(iter(rs))]
                        for i in (2 * k, 2 * k + 1):
                            Q[(i, i)] = Q.get((i, i), Fr(0)) + cf
                        continue
                    assert len(rs) == 2 and set(rs.values()) == {1}, mono
                    a, b = sorted(rs)
                    idx = []
                    for v in (a, b):
                        t = pair[v]
                        hit = [(k, e) for k, e in trig if k in (cosT[t], sinT[t])]
                        assert len(hit) == 1 and hit[0][1] == 1, mono
                        idx.append(2 * bus_v[v] + (0 if hit[0][0] == cosT[t] else 1))
                    assert len(trig) == 2, mono
                    i, j = sorted(idx)
                    Q[(i, j)] = Q.get((i, j), Fr(0)) + cf
                # symbolic identity check: expr(v, th) == x^T Q x at e=r cos t, f=r sin t
                X = []
                for v in V:
                    X += [r_[v] * cosT[pair[v]], r_[v] * sinT[pair[v]]]
                rect = S.Add(*[S.Rational(q.numerator, q.denominator) * X[i] * X[j] for (i, j), q in Q.items()])
                d = S.expand(ex - rect)
                d = S.expand(d.subs({sinT[t] ** 2: 1 - cosT[t] ** 2 for t in TH}))
                assert d == 0, (c["name"], d)
                rows.append(dict(name=c["name"], kind="flow", lin={y: Fr(1)}, qy={}, Q=Q, lb=lb, ub=ub))
                nflow += 1
                continue
            vs = set(c["lin"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
            if vs & set(V):
                assert len(vs) == 1 and not c["quad"] and Fr(c["lin"][next(iter(vs))]) == 1
                k = bus_v[next(iter(vs))]
                if lb is not None:
                    vlo[k] = max(vlo.get(k, lb), lb)
                if ub is not None:
                    vhi[k] = min(vhi.get(k, ub), ub)
                continue
            if vs & set(TH):
                assert vs <= set(TH) and not c["quad"]
                if len(vs) == 1:
                    assert lb == ub == 0
                    dropped["ref"] += 1
                else:
                    dropped["angle"] += 1
                continue
            if len(vs) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                add_box(y, Fr(cy), lb, ub)
                continue
            qy = {}
            for a, b, cc in c["quad"]:
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + Fr(cc)
            rows.append(dict(name=c["name"], kind="limit" if qy else "linear",
                             lin={j: Fr(a) for j, a in c["lin"].items()}, qy=qy, Q={}, lb=lb, ub=ub))
        assert sorted(vlo) == sorted(vhi) == list(range(n))
        for k in range(n):
            assert vlo[k] >= 0 <= vhi[k] and vlo[k] <= vhi[k]
            rows.append(dict(name="V%d" % k, kind="volt", lin={}, qy={},
                             Q={(2 * k, 2 * k): Fr(1), (2 * k + 1, 2 * k + 1): Fr(1)},
                             lb=vlo[k] ** 2, ub=vhi[k] ** 2))
        xvars = None
        yvars = [j for j in range(nv) if j not in V and j not in TH]
        vmap = dict(V=V, TH=TH)
        log(f"{name}: polar, {n} buses, {nflow} flow rows verified symbolically; dropped angle rows {dropped['angle']}, ref {dropped['ref']}")
    else:
        X = set()
        for c in cons:
            if c["quad"] and c["lb"] == c["ub"]:
                for a, b, _ in c["quad"]:
                    X |= {a, b}
        X = sorted(X)
        xi = {j: q for q, j in enumerate(X)}
        n = len(X) // 2
        for c in cons:
            lb, ub = inf_or(c["lb"]), inf_or(c["ub"])
            qx = [(a, b, cc) for a, b, cc in c["quad"] if a in xi or b in xi]
            if qx:
                assert all(a in xi and b in xi for a, b, _ in c["quad"])
                assert not (set(c["lin"]) & set(X))
                Q = {}
                for a, b, cc in c["quad"]:
                    i, j = sorted((xi[a], xi[b]))
                    Q[(i, j)] = Q.get((i, j), Fr(0)) + Fr(cc)
                rows.append(dict(name=c["name"], kind="flow" if c["lin"] else "volt",
                                 lin={j: Fr(a) for j, a in c["lin"].items()}, qy={}, Q=Q, lb=lb, ub=ub))
                continue
            if set(c["lin"]) & set(X):
                assert len(c["lin"]) == 1 and not c["quad"] and lb == ub == 0
                dropped["ref"] += 1
                continue
            if len(c["lin"]) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                add_box(y, Fr(cy), lb, ub)
                continue
            qy = {}
            for a, b, cc in c["quad"]:
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + Fr(cc)
            rows.append(dict(name=c["name"], kind="limit" if qy else "linear",
                             lin={j: Fr(a) for j, a in c["lin"].items()}, qy=qy, Q={}, lb=lb, ub=ub))
        xvars = X
        yvars = [j for j in range(nv) if j not in xi]
        vmap = dict(X=X)
        log(f"{name}: rectangular, {len(X)} x-variables; dropped ref rows {dropped['ref']}")
    for a, b, _ in o["quad"]:
        assert a == b and a in yvars
    assert all(j in yvars for j in o["lin"])
    obj = dict(const=Fr(o["constant"]), lin={j: Fr(c) for j, c in o["lin"].items()},
               qy={a: Fr(c) for a, b, c in o["quad"]})
    return dict(name=name, I=I, polar=polar, n=n, rows=rows, box=box, ys=yvars, obj=obj,
                vmap=vmap, dropped=dropped)


def pattern(r):
    if r["lb"] is not None and r["ub"] is not None and r["lb"] == r["ub"]:
        return ("eq",)
    return ("ineq", r["ub"] is not None, r["lb"] is not None)


def raw_pattern(x):
    if x[0] == "eq":
        return ("eq",)
    return ("ineq", x[1] is not None, x[2] is not None)


# ---------------------------------------------------------------- Lagrangian
def ymin(s, k, lo, hi):
    """exact min of s y^2 + k y over [lo, hi] (None = infinite); None if -inf"""
    if s > 0:
        y = -k / (2 * s)
        if lo is not None and y < lo:
            y = lo
        if hi is not None and y > hi:
            y = hi
        return s * y * y + k * y
    if s == 0:
        if k == 0:
            return Fr(0)
        if k > 0:
            return None if lo is None else k * lo
        return None if hi is None else k * hi
    if lo is None or hi is None:
        return None
    return min(s * lo * lo + k * lo, s * hi * hi + k * hi)


def lagrangian(M, raw, log=print):
    rows = M["rows"]
    assert len(rows) == len(raw)
    for r, x in zip(rows, raw):
        assert pattern(r) == raw_pattern(x), (r["name"], pattern(r), x)
    w, const = [], M["obj"]["const"]
    nclip = 0
    for r, x in zip(rows, raw):
        if x[0] == "eq":
            m = Fr(x[1])                 # exact binary value of the float
            w.append(m)
            const -= m * r["lb"]
        else:
            vp = Fr(x[1]) if x[1] is not None else Fr(0)
            vm = Fr(x[2]) if x[2] is not None else Fr(0)
            if vp < 0 or vm < 0:
                nclip += 1
            vp, vm = max(vp, Fr(0)), max(vm, Fr(0))
            w.append(vp - vm)
            if vp:
                const -= vp * r["ub"]
            if vm:
                const += vm * r["lb"]
    kap = {y: M["obj"]["lin"].get(y, Fr(0)) for y in M["ys"]}
    sig = {y: M["obj"]["qy"].get(y, Fr(0)) for y in M["ys"]}
    defrow = {}
    for k, r in enumerate(rows):
        for y, c in r["lin"].items():
            kap[y] += w[k] * c
        for y, c in r["qy"].items():
            sig[y] += w[k] * c
        if r["kind"] == "flow" and len(r["lin"]) == 1 and r["lb"] == r["ub"] == 0:
            (y, c), = r["lin"].items()
            if c == 1:
                defrow[y] = k
    inner, nadj, nbox = Fr(0), 0, 0
    for y in M["ys"]:
        lo, hi = M["box"].get(y, (None, None))
        v = ymin(sig[y], kap[y], lo, hi)
        if v is None and sig[y] == 0 and y in defrow:
            k = defrow[y]
            w[k] -= kap[y]               # makes kappa_y = 0; row rhs is 0 so const is unchanged
            kap[y] = Fr(0)
            nadj += 1
            v = Fr(0)
        assert v is not None, ("unbounded y", y, sig[y], kap[y], lo, hi)
        inner += v
        nbox += (lo is not None or hi is not None)
    n2 = 2 * M["n"]
    A = [[Fr(0)] * n2 for _ in range(n2)]
    for k, r in enumerate(rows):
        if w[k] == 0:
            continue
        for (i, j), c in r["Q"].items():
            if i == j:
                A[i][i] += w[k] * c
            else:
                h = w[k] * c / 2
                A[i][j] += h
                A[j][i] += h
    log(f"  clipped negative ineq parts: {nclip}; flow multipliers adjusted: {nadj}; boxed y: {nbox}")
    return dict(const=const, inner=inner, A=A, w=w, kap=kap, sig=sig)


def ldl_psd(A):
    """exact symmetric elimination with diagonal pivoting; returns (is_psd, pivots, zero_pivots)"""
    n = len(A)
    M = [row[:] for row in A]
    alive = list(range(n))
    piv, zeros = [], 0
    while alive:
        # pick the largest remaining diagonal (any positive one is valid)
        p = max(alive, key=lambda i: M[i][i])
        d = M[p][p]
        if d < 0:
            return False, piv, zeros
        if d == 0:
            # all remaining diagonals are <= 0 -> must all be 0 with zero rows
            for i in alive:
                assert M[i][i] == 0
                if any(M[i][j] != 0 for j in alive):
                    return False, piv, zeros
            zeros += len(alive)
            break
        alive.remove(p)
        piv.append(d)
        rowp = {j: M[p][j] for j in alive if M[p][j] != 0}
        for i in rowp:
            f = rowp[i] / d
            Mi = M[i]
            for j, v in rowp.items():
                if j >= i:
                    Mi[j] -= f * v
        for i in rowp:
            for j in rowp:
                if j > i:
                    M[j][i] = M[i][j]
    return True, piv, zeros
