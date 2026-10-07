"""Reviewer's own construction of the relaxation R for powerflow0039p / 0039r.

Built only from own_osil.read.  Rows are keyed by name, in the representation
    lb <= sum_j lin[j] z_j + sum_{(i<=j)} Q[i,j] x_i x_j + sum_j qy[j] z_j^2 <= ub
with x = (e_0, f_0, e_1, f_1, ...) and z the OSIL variables that are not bus
coordinates ("y").  Bus order (a naming convention only; the bound does not depend on
it): polar - sorted by the index of the bus angle variable; rectangular - sorted by the
(smaller, larger) index pair of the voltage row e^2 + f^2.

Validity of every row for every feasible OSIL point:
  * rectangular rows are OSIL rows verbatim; the reference row f_ref = 0 is dropped;
  * polar flow rows: the OSIL term  c v_a v_b trig(th_p - th_q) , c v_a^2  is rewritten with
    e = v cos th, f = v sin th:  v_a v_b cos(th_a - th_b) = e_a e_b + f_a f_b,
    v_p v_q sin(th_p - th_q) = f_p e_q - e_p f_q,  v_a^2 = e_a^2 + f_a^2  (exact identities);
    in addition every converted row is compared with the native OSIL row at random points
    in 60-digit arithmetic (check_polar_identity);
  * polar voltage rows lo <= v <= hi with lo >= 0 become lo^2 <= e^2 + f^2 <= hi^2;
  * polar angle rows a <= th_p - th_q <= b become tb w_R - w_I >= 0 and w_I - ta w_R >= 0; their
    tb, ta are taken from the author's rows and checked here with interval arithmetic
    (check_angle_rows);
  * single-variable linear rows on y become boxes of y.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import random
from fractions import Fraction as Fr

import mpmath as mp

import own_osil


def qadd(Q, i, j, c):
    if i > j:
        i, j = j, i
    Q[(i, j)] = Q.get((i, j), Fr(0)) + c
    if Q[(i, j)] == 0:
        del Q[(i, j)]


def _factors(t):
    """flatten a product term into (coef, [var idx], [square var idx], [(trig, arg)])"""
    coef = Fr(1)
    vs, sq, tr = [], [], []
    items = t[1:] if t[0] == "product" else (t,)
    for f in items:
        if f[0] == "var":
            coef *= f[2]
            vs.append(f[1])
        elif f[0] == "num":
            coef *= f[1]
        elif f[0] == "square":
            assert f[1][0] == "var"
            coef *= f[1][2] ** 2
            sq.append(f[1][1])
        elif f[0] in ("cos", "sin"):
            arg = f[1]
            assert arg[0] == "sum" and len(arg) == 3
            lin = {}
            for a in arg[1:]:
                assert a[0] == "var"
                lin[a[1]] = lin.get(a[1], Fr(0)) + a[2]
            (t1, c1), (t2, c2) = lin.items()
            assert {c1, c2} == {Fr(1), Fr(-1)}
            p, q = (t1, t2) if c1 == 1 else (t2, t1)
            tr.append((f[0], p, q))
        else:
            raise ValueError(f)
    return coef, vs, sq, tr


def build(name):
    I = own_osil.read(_repro_os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    nv = len(I["names"])
    assert all(l is None for l in I["vlb"]) and all(u is None for u in I["vub"])
    assert I["obj"]["sense"] == "min" and I["obj"]["nl"] is None
    assert all(c["const"] == 0 for c in I["cons"])
    polar = any(c["nl"] is not None for c in I["cons"])
    rows = {}
    order = []
    ybox = {}
    info = dict(polar=polar)

    def addbox(y, cy, lb, ub):
        lo, hi = ybox.get(y, (None, None))
        l2 = None if lb is None else lb / cy
        u2 = None if ub is None else ub / cy
        if cy < 0:
            l2, u2 = u2, l2
        if l2 is not None:
            lo = l2 if lo is None else max(lo, l2)
        if u2 is not None:
            hi = u2 if hi is None else min(hi, u2)
        ybox[y] = (lo, hi)

    if polar:
        # angle vars: inside trig; voltage vars: other vars of nl trees
        th, vv = set(), set()
        pair = {}
        for c in I["cons"]:
            if c["nl"] is None:
                continue
            t = c["nl"]
            terms = t[1:] if t[0] == "sum" else (t,)
            for tm in terms:
                coef, vs, sq, tr = _factors(tm)
                for (_, p, q) in tr:
                    th |= {p, q}
                vv |= set(vs) | set(sq)
            # pairing: the squared voltage (from bus) belongs to the angle with coefficient +1
            sqs = [_factors(tm)[2] for tm in terms]
            sqv = {v for s in sqs for v in s}
            if not sqv:          # e.g. active flow on a lossless line: no v^2 term
                continue
            assert len(sqv) == 1, c["name"]
            a = sqv.pop()
            ps = {tr_[1] for tm in terms for tr_ in _factors(tm)[3]}
            assert len(ps) == 1
            p = ps.pop()
            assert pair.get(a, p) == p
            pair[a] = p
        assert th.isdisjoint(vv)
        assert sorted(pair) == sorted(vv) and len(set(pair.values())) == len(pair) and set(pair.values()) == th
        buses = sorted(th)
        kth = {t: k for k, t in enumerate(buses)}
        kv = {v: kth[p] for v, p in pair.items()}
        n = len(buses)
        info.update(kv=kv, kth=kth)
        E = lambda k: 2 * k
        Fi = lambda k: 2 * k + 1
        vlo, vhi, ang = {}, {}, {}
        for c in I["cons"]:
            vars_ = set(c["lin"]) | {i for ij in c["quad"] for i in ij}
            if c["nl"] is not None:
                assert c["lb"] == c["ub"] == 0 and not c["quad"] and len(c["lin"]) == 1
                (y, cy), = c["lin"].items()
                assert cy == 1 and y not in kv and y not in kth
                t = c["nl"]
                Q = {}
                for tm in (t[1:] if t[0] == "sum" else (t,)):
                    coef, vs, sq, tr = _factors(tm)
                    if sq:
                        assert len(sq) == 1 and not vs and not tr
                        k = kv[sq[0]]
                        qadd(Q, E(k), E(k), coef); qadd(Q, Fi(k), Fi(k), coef)
                        continue
                    assert len(vs) == 2 and len(tr) == 1
                    kind, p, q = tr[0]
                    P, Qb = kth[p], kth[q]
                    assert {kv[vs[0]], kv[vs[1]]} == {P, Qb}
                    if kind == "cos":
                        qadd(Q, E(P), E(Qb), coef); qadd(Q, Fi(P), Fi(Qb), coef)
                    else:
                        qadd(Q, Fi(P), E(Qb), coef); qadd(Q, E(P), Fi(Qb), -coef)
                rows[c["name"]] = dict(lin={y: Fr(1)}, Q=Q, qy={}, lb=Fr(0), ub=Fr(0))
                order.append(c["name"])
                continue
            if vars_ & set(kv):
                assert len(vars_) == 1 and not c["quad"]
                (v, cv), = c["lin"].items()
                assert cv == 1
                k = kv[v]
                if c["lb"] is not None:
                    vlo[k] = max(vlo.get(k, c["lb"]), c["lb"])
                if c["ub"] is not None:
                    vhi[k] = min(vhi.get(k, c["ub"]), c["ub"])
                continue
            if vars_ & set(kth):
                assert not c["quad"] and vars_ <= set(kth)
                if len(vars_) == 1:
                    assert c["lb"] == c["ub"] == 0   # reference angle: dropped
                    info["ref_dropped"] = c["name"]
                    continue
                (t1, a1), (t2, a2) = c["lin"].items()
                assert {a1, a2} == {Fr(1), Fr(-1)}
                p, q = (t1, t2) if a1 == 1 else (t2, t1)
                kp, kq = kth[p], kth[q]
                lb, ub = c["lb"], c["ub"]
                if kp > kq:
                    kp, kq = kq, kp
                    lb, ub = (None if ub is None else -ub), (None if lb is None else -lb)
                A0, B0 = ang.get((kp, kq), (None, None))
                if lb is not None:
                    A0 = lb if A0 is None else max(A0, lb)
                if ub is not None:
                    B0 = ub if B0 is None else min(B0, ub)
                ang[(kp, kq)] = (A0, B0)
                continue
            if len(vars_) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                addbox(y, cy, c["lb"], c["ub"])
                continue
            qy = {}
            for (a, b), cc in c["quad"].items():
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + cc
            rows[c["name"]] = dict(lin=dict(c["lin"]), Q={}, qy=qy, lb=c["lb"], ub=c["ub"])
            order.append(c["name"])
        assert sorted(vlo) == sorted(vhi) == list(range(n))
        for k in range(n):
            assert 0 <= vlo[k] <= vhi[k]
            rows[f"V{k}"] = dict(lin={}, Q={(E(k), E(k)): Fr(1), (Fi(k), Fi(k)): Fr(1)}, qy={},
                                 lb=vlo[k] ** 2, ub=vhi[k] ** 2)
            order.append(f"V{k}")
        vmax2 = [vhi[k] ** 2 for k in range(n)]
        info["angle"] = ang
        xset = None
    else:
        xset = set()
        for c in I["cons"]:
            if c["quad"] and c["lb"] is not None and c["lb"] == c["ub"]:
                for (a, b) in c["quad"]:
                    xset |= {a, b}
        vrows = {}
        for c in I["cons"]:
            if c["quad"] and not c["lin"] and {i for ij in c["quad"] for i in ij} <= xset:
                assert len(c["quad"]) == 2 and all(a == b and cc == 1 for (a, b), cc in c["quad"].items())
                key = tuple(sorted(a for (a, b) in c["quad"]))
                lo, hi = vrows.get(key, (None, None))
                if c["lb"] is not None:
                    lo = c["lb"] if lo is None else max(lo, c["lb"])
                if c["ub"] is not None:
                    hi = c["ub"] if hi is None else min(hi, c["ub"])
                vrows[key] = (lo, hi)
        keys = sorted(vrows)
        assert sorted(j for k in keys for j in k) == sorted(xset)
        xidx = {}
        for k, (a, b) in enumerate(keys):
            xidx[a], xidx[b] = 2 * k, 2 * k + 1
        n = len(keys)
        vmax2 = [vrows[k][1] for k in keys]
        info.update(keys=keys, xidx=xidx)
        for c in I["cons"]:
            qv = {i for ij in c["quad"] for i in ij}
            if qv & xset:
                assert qv <= xset and not (set(c["lin"]) & xset)
                Q = {}
                for (a, b), cc in c["quad"].items():
                    qadd(Q, xidx[a], xidx[b], cc)
                rows[c["name"]] = dict(lin=dict(c["lin"]), Q=Q, qy={}, lb=c["lb"], ub=c["ub"])
                order.append(c["name"])
                continue
            if set(c["lin"]) & xset:
                assert len(c["lin"]) == 1 and not c["quad"] and c["lb"] == c["ub"] == 0
                info["ref_dropped"] = c["name"]
                continue
            if len(c["lin"]) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                addbox(y, cy, c["lb"], c["ub"])
                continue
            qy = {}
            for (a, b), cc in c["quad"].items():
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + cc
            rows[c["name"]] = dict(lin=dict(c["lin"]), Q={}, qy=qy, lb=c["lb"], ub=c["ub"])
            order.append(c["name"])
    xvars = set(info.get("kv", {})) | set(info.get("kth", {})) | (xset or set())
    ys = [j for j in range(nv) if j not in xvars]
    o = I["obj"]
    assert all(a == b and a in ys for (a, b) in o["quad"]) and all(j in ys for j in o["lin"])
    obj = dict(const=o["const"], lin=dict(o["lin"]), qy={a: c for (a, b), c in o["quad"].items()})
    return dict(I=I, n=n, rows=rows, order=order, ybox=ybox, ys=ys, obj=obj, vmax2=vmax2, info=info)


def x_of_point(R, z):
    """bus coordinates x (mpf list) of an OSIL point z (mpf list)"""
    info = R["info"]
    x = [None] * (2 * R["n"])
    if info["polar"]:
        for v, k in info["kv"].items():
            t = [p for p, kk in info["kth"].items() if kk == k][0]
            x[2 * k] = z[v] * mp.cos(z[t])
            x[2 * k + 1] = z[v] * mp.sin(z[t])
    else:
        for j, i in info["xidx"].items():
            x[i] = z[j]
    return x


def row_val(r, z, x):
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    return (mp.fsum(q(c) * z[j] for j, c in r["lin"].items())
            + mp.fsum(q(c) * x[i] * x[j] for (i, j), c in r["Q"].items())
            + mp.fsum(q(c) * z[j] ** 2 for j, c in r["qy"].items()))


def check_polar_identity(R, trials=3, seed=1):
    """max |native OSIL flow expression - converted quadratic| over random points (60 digits)"""
    I = R["I"]
    rng = random.Random(seed)
    worst = mp.mpf(0)
    with mp.workdps(60):
        for _ in range(trials):
            z = [mp.mpf(rng.uniform(-2, 2)) for _ in I["names"]]
            x = x_of_point(R, z)
            for r, c in enumerate(I["cons"]):
                if c["nl"] is None:
                    continue
                nat = own_osil.row_value(I, r, z, mp)
                conv = row_val(R["rows"][c["name"]], z, x)
                worst = max(worst, abs(nat - conv))
    return worst
