"""Decode the MINLPLib AC optimal power flow instances powerflow00XXp (polar) and
powerflow00XXr (rectangular) into one quadratic relaxation R.

R has bus coordinates x = (e_1, f_1, ..., e_n, f_n) and the remaining OSIL
variables y (branch flows, generator outputs).  Each kept row reads
    lb <= lin(y) + x^T Q x + sum_k qy_k y_k^2 <= ub.
Polar model: a polar-feasible point maps to e = v cos(theta), f = v sin(theta).
  * flow rows  y = c1 v_a v_b cos(th_a - th_b) + c2 v_a^2 + c3 v_a v_b sin(th_a - th_b)
    become exact quadratic identities in x;
  * voltage rows  lo <= v_k <= hi  (lo >= 0) are replaced by lo^2 <= e^2 + f^2 <= hi^2;
  * angle-difference rows a <= th_p - th_q <= b (|a|, |b| < pi/2) are replaced by
    w_I <= tb w_R and w_I >= ta w_R, tb >= tan(b), ta <= tan(a) rational, where
    w_R = e_p e_q + f_p f_q, w_I = f_p e_q - e_p f_q;
  * the reference-angle row theta_1 = 0 is dropped.
All these are valid consequences, so every polar-feasible point gives a point of R
with the same objective.  Rectangular model: rows are taken as they are.
Single-variable linear rows on y are kept as bounds of y.  All constants are
Fractions of the OSIL decimals.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def lin_of_sum(t):
    """linear combination {var: coef} of a sum of ('var', j, c) leaves"""
    assert t[0] == "sum", t
    out = {}
    for s in t[1:]:
        assert s[0] == "var", s
        out[s[1]] = out.get(s[1], Fr(0)) + Fr(s[2])
    return out


def parse_flow(t):
    """flow expression -> list of ('cos'|'sin', a, b, p, q, coef) (coef*v_a*v_b*trig(th_p - th_q))
    and ('sq', a, coef) (coef*v_a^2)."""
    terms = t[1:] if t[0] == "sum" else (t,)
    out = []
    for p in terms:
        if p[0] == "product" and p[1][0] == "square":
            (sq, num) = p[1:]
            assert num[0] == "num" and sq[1][0] == "var" and sq[1][2] == "1"
            out.append(("sq", sq[1][1], Fr(num[1])))
            continue
        assert p[0] == "product" and len(p) == 4, p
        va, vb, tr = p[1:]
        assert va[0] == "var" and vb[0] == "var" and vb[2] == "1" and tr[0] in ("cos", "sin")
        L = lin_of_sum(tr[1])
        (th1, c1), (th2, c2) = L.items()
        assert {c1, c2} == {Fr(1), Fr(-1)}
        pth, qth = (th1, th2) if c1 == 1 else (th2, th1)
        out.append((tr[0], va[1], vb[1], pth, qth, Fr(va[2])))
    return out


def tan_bounds(a):
    """rational (lo, hi) with lo <= tan(a) <= hi, a a Fraction, |a| < pi/2"""
    with mp.workdps(50):
        t = mp.tan(mp.mpf(a.numerator) / a.denominator)
        s = mp.nstr(t, 40)
    q = Fr(s)
    eps = Fr(1, 10**35)
    return q - eps, q + eps


def decode(name):
    I = osilx.read(os.path.join(OSIL, name + ".osil"))
    names, cons = I["names"], I["cons"]
    nv = len(names)
    assert all(I["lb"][j] == "-INF" and I["ub"][j] == "INF" for j in range(nv))
    for c in cons:
        assert c["constant"] == "0"
    o = I["obj"]
    assert o["sense"] == "min" and o["nl"] is None
    polar = any(c["nl"] is not None for c in cons)
    rows = []
    ybox = {}
    angle_info = {}
    busmap = None
    if polar:
        # bus mapping v <-> theta from the flow terms
        vt = {}
        for c in cons:
            if c["nl"] is None:
                continue
            for tm in parse_flow(c["nl"]):
                if tm[0] == "sq":
                    continue
                _, a, b, p, q, _ = tm
                assert {a, b} != set() and len({a, b}) == 2
                # v_a v_b trig(th_p - th_q): buses {a,b} = {p,q}; record candidates
                vt.setdefault(a, set()).update({p, q})
                vt.setdefault(b, set()).update({p, q})
        bus_of_v = {}
        for v, s in vt.items():
            pass
        # resolve: each v pairs with the theta common to all its candidate sets
        allv = sorted(vt)
        vpair = {}
        for c in cons:
            if c["nl"] is None:
                continue
            for tm in parse_flow(c["nl"]):
                if tm[0] == "sq":
                    continue
                _, a, b, p, q, _ = tm
                vpair.setdefault(a, []).append({p, q})
                vpair.setdefault(b, []).append({p, q})
        cand = {v: set.intersection(*vpair[v]) for v in allv}
        for v in allv:
            if len(cand[v]) == 1:
                bus_of_v[v] = next(iter(cand[v]))
        terms_ab = []
        for c in cons:
            if c["nl"] is None:
                continue
            for tm in parse_flow(c["nl"]):
                if tm[0] != "sq":
                    terms_ab.append((tm[1], tm[2], {tm[3], tm[4]}))
        changed = True
        while changed:
            changed = False
            for a, b, pq in terms_ab:
                for u, w in ((a, b), (b, a)):
                    if u in bus_of_v and w not in bus_of_v:
                        rest = pq - {bus_of_v[u]}
                        assert len(rest) == 1
                        bus_of_v[w] = rest.pop()
                        changed = True
        assert sorted(bus_of_v) == allv
        for a, b, pq in terms_ab:
            assert {bus_of_v[a], bus_of_v[b]} == pq
        th_of_bus = {th: k for k, th in enumerate(sorted(set(bus_of_v.values())))}
        vbus = {v: th_of_bus[bus_of_v[v]] for v in allv}
        thbus = {th: k for th, k in th_of_bus.items()}
        assert len(set(vbus.values())) == len(vbus) == len(thbus)
        n = len(vbus)

        def E(k):
            return 2 * k

        def F(k):
            return 2 * k + 1

        def qadd(Q, i, j, c):
            if i > j:
                i, j = j, i
            Q[(i, j)] = Q.get((i, j), Fr(0)) + c

        vlo, vhi = {}, {}
        angle = {}
        for c in cons:
            lb = None if osilx.isinf(c["lb"]) else Fr(c["lb"])
            ub = None if osilx.isinf(c["ub"]) else Fr(c["ub"])
            if c["nl"] is not None:
                assert lb == ub == 0 and not c["quad"] and len(c["lin"]) == 1
                (y, cy), = c["lin"].items()
                assert cy == "1" and y not in vbus and y not in thbus
                Q = {}
                for tm in parse_flow(c["nl"]):
                    if tm[0] == "sq":
                        _, a, cf = tm
                        k = vbus[a]
                        qadd(Q, E(k), E(k), cf); qadd(Q, F(k), F(k), cf)
                        continue
                    kind, a, b, p, q, cf = tm
                    kp, kq = thbus[p], thbus[q]
                    assert {vbus[a], vbus[b]} == {kp, kq}
                    if kind == "cos":      # e_p e_q + f_p f_q
                        qadd(Q, E(kp), E(kq), cf); qadd(Q, F(kp), F(kq), cf)
                    else:                  # sin(th_p - th_q) v_p v_q = f_p e_q - e_p f_q
                        qadd(Q, F(kp), E(kq), cf); qadd(Q, E(kp), F(kq), -cf)
                rows.append(dict(name=c["name"], lin={y: Fr(1)}, Q=Q, qy={}, lb=Fr(0), ub=Fr(0), kind="flow"))
                continue
            vars_ = set(c["lin"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
            if vars_ & set(vbus):
                assert len(vars_) == 1 and not c["quad"] and c["lin"][list(vars_)[0]] == "1"
                k = vbus[list(vars_)[0]]
                if lb is not None:
                    vlo[k] = max(vlo.get(k, lb), lb)
                if ub is not None:
                    vhi[k] = min(vhi.get(k, ub), ub)
                continue
            if vars_ & set(thbus):
                assert not c["quad"] and vars_ <= set(thbus)
                if len(vars_) == 1:
                    assert lb == ub == 0          # reference angle: dropped
                    continue
                assert len(vars_) == 2
                (t1, a1), (t2, a2) = c["lin"].items()
                a1, a2 = Fr(a1), Fr(a2)
                assert {a1, a2} == {Fr(1), Fr(-1)}
                p, q = (t1, t2) if a1 == 1 else (t2, t1)
                kp, kq = thbus[p], thbus[q]
                # store as interval for th_p - th_q with kp < kq
                if kp > kq:
                    kp, kq = kq, kp
                    lb, ub = (None if ub is None else -ub), (None if lb is None else -lb)
                A0, B0 = angle.get((kp, kq), (None, None))
                if lb is not None:
                    A0 = lb if A0 is None else max(A0, lb)
                if ub is not None:
                    B0 = ub if B0 is None else min(B0, ub)
                angle[(kp, kq)] = (A0, B0)
                continue
            # remaining rows: only y variables
            if len(vars_) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                cy = Fr(cy)
                lo_, hi_ = ybox.get(y, (None, None))
                l2 = None if lb is None else lb / cy
                u2 = None if ub is None else ub / cy
                if cy < 0:
                    l2, u2 = u2, l2
                if l2 is not None:
                    lo_ = l2 if lo_ is None else max(lo_, l2)
                if u2 is not None:
                    hi_ = u2 if hi_ is None else min(hi_, u2)
                ybox[y] = (lo_, hi_)
                continue
            qy = {}
            for a, b, cc in c["quad"]:
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + Fr(cc)
            rows.append(dict(name=c["name"], lin={j: Fr(a) for j, a in c["lin"].items()}, Q={}, qy=qy,
                             lb=lb, ub=ub, kind="limit" if qy else "linear"))
        # voltage rows -> quadratic
        assert sorted(vlo) == sorted(vhi) == list(range(n))
        for k in range(n):
            assert vlo[k] >= 0 and vhi[k] >= vlo[k]
            Q = {(E(k), E(k)): Fr(1), (F(k), F(k)): Fr(1)}
            rows.append(dict(name=f"V{k}", lin={}, Q=Q, qy={}, lb=vlo[k] ** 2, ub=vhi[k] ** 2, kind="volt"))
        vmax2 = [vhi[k] ** 2 for k in range(n)]
        # angle rows -> quadratic valid inequalities
        angle_info = {}
        for (kp, kq), (A0, B0) in sorted(angle.items()):
            assert A0 is not None and B0 is not None and -Fr(3, 2) < A0 <= B0 < Fr(3, 2)
            tb = tan_bounds(B0)[1]
            ta = tan_bounds(A0)[0]
            angle_info[(kp, kq)] = (A0, B0, ta, tb)
            WR = {}
            WI = {}
            qadd(WR, E(kp), E(kq), Fr(1)); qadd(WR, F(kp), F(kq), Fr(1))
            qadd(WI, F(kp), E(kq), Fr(1)); qadd(WI, E(kp), F(kq), Fr(-1))
            Q1 = {k_: tb * WR.get(k_, 0) - WI.get(k_, 0) for k_ in set(WR) | set(WI)}
            Q2 = {k_: WI.get(k_, 0) - ta * WR.get(k_, 0) for k_ in set(WR) | set(WI)}
            rows.append(dict(name=f"A{kp}_{kq}u", lin={}, Q=Q1, qy={}, lb=Fr(0), ub=None, kind="angle"))
            rows.append(dict(name=f"A{kp}_{kq}l", lin={}, Q=Q2, qy={}, lb=Fr(0), ub=None, kind="angle"))
        xvars = None
        ymap = [j for j in range(nv) if j not in vbus and j not in thbus]
        inv_v = {k: v for v, k in vbus.items()}
        inv_t = {k: t for t, k in thbus.items()}
        busmap = [(inv_v[k], inv_t[k]) for k in range(n)]
    else:
        # rectangular: x variables are those in quadratic terms of equality rows
        xset = set()
        for c in cons:
            if c["quad"] and c["lb"] == c["ub"]:
                for a, b, _ in c["quad"]:
                    xset |= {a, b}
        # bus pairs from voltage rows (e^2 + f^2 in [lo, hi], no linear part)
        pairs = []
        vrows = {}
        for c in cons:
            if c["quad"] and not c["lin"] and set(a for a, b, _ in c["quad"]) <= xset:
                q = c["quad"]
                assert len(q) == 2 and all(a == b and cc == "1" for a, b, cc in q)
                key = tuple(sorted(a for a, b, _ in q))
                lo_, hi_ = vrows.get(key, (None, None))
                if not osilx.isinf(c["lb"]):
                    lo_ = Fr(c["lb"]) if lo_ is None else max(lo_, Fr(c["lb"]))
                if not osilx.isinf(c["ub"]):
                    hi_ = Fr(c["ub"]) if hi_ is None else min(hi_, Fr(c["ub"]))
                vrows[key] = (lo_, hi_)
        keys = sorted(vrows)
        assert sorted(j for k in keys for j in k) == sorted(xset)
        xidx = {}
        for k, (a, b) in enumerate(keys):
            xidx[a] = 2 * k
            xidx[b] = 2 * k + 1
        n = len(keys)
        vmax2 = [vrows[k][1] for k in keys]
        for c in cons:
            lb = None if osilx.isinf(c["lb"]) else Fr(c["lb"])
            ub = None if osilx.isinf(c["ub"]) else Fr(c["ub"])
            xs = [a for a, b, _ in c["quad"] if a in xset] + [b for a, b, _ in c["quad"] if b in xset]
            if xs:
                assert all(a in xset and b in xset for a, b, _ in c["quad"])
                assert not (set(c["lin"]) & xset)
                Q = {}
                for a, b, cc in c["quad"]:
                    i, j = sorted((xidx[a], xidx[b]))
                    Q[(i, j)] = Q.get((i, j), Fr(0)) + Fr(cc)
                kind = "flow" if c["lin"] else "volt"
                rows.append(dict(name=c["name"], lin={j: Fr(a) for j, a in c["lin"].items()}, Q=Q, qy={}, lb=lb, ub=ub, kind=kind))
                continue
            if set(c["lin"]) & xset:
                # reference-angle row f_ref = 0: dropped (relaxation)
                assert len(c["lin"]) == 1 and not c["quad"] and lb == ub == 0
                continue
            if len(c["lin"]) == 1 and not c["quad"]:
                (y, cy), = c["lin"].items()
                cy = Fr(cy)
                lo_, hi_ = ybox.get(y, (None, None))
                l2 = None if lb is None else lb / cy
                u2 = None if ub is None else ub / cy
                if cy < 0:
                    l2, u2 = u2, l2
                if l2 is not None:
                    lo_ = l2 if lo_ is None else max(lo_, l2)
                if u2 is not None:
                    hi_ = u2 if hi_ is None else min(hi_, u2)
                ybox[y] = (lo_, hi_)
                continue
            qy = {}
            for a, b, cc in c["quad"]:
                assert a == b
                qy[a] = qy.get(a, Fr(0)) + Fr(cc)
            rows.append(dict(name=c["name"], lin={j: Fr(a) for j, a in c["lin"].items()}, Q={}, qy=qy,
                             lb=lb, ub=ub, kind="limit" if qy else "linear"))
        ymap = [j for j in range(nv) if j not in xset]
    # objective in y only
    for a, b, _ in o["quad"]:
        assert a == b and a in ymap
    assert all(j in ymap for j in o["lin"])
    obj = dict(const=Fr(o["constant"]), lin={j: Fr(c) for j, c in o["lin"].items()},
               qy={a: Fr(c) for a, b, c in o["quad"]})
    return dict(name=name, I=I, polar=polar, n=n, rows=rows, ybox=ybox, ys=ymap, obj=obj, vmax2=vmax2,
                angle=angle_info, busmap=busmap)
