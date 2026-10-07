"""Referee check: the author's N = 4000 partitions (logs/rev2_two4000.json, node ends read as floats) evaluated
with the referee's own bound formulas (c2_cert.py).  Lifted node = the part of the stage-n range not in the
two fixed nodes; it must lie inside the referee's exact V.  Fixed nodes anchored at z(e), e = the node end
nearest ubar_n (the author used node KKT points; any anchor gives a valid bound)."""
import json
from fractions import Fraction as Fr
import c2_cert as C

auth = json.load(open("../../theory-bangbang/kneg/logs/rev2_two4000.json"))
mine = {(r["t1"], r["t2"]): r for r in json.load(open("logs/cert4000.json"))}
cases = {("0.5", "1.5"): (503, 1495, 503), ("0.7", "1.3"): (1196, 1557, 1196), ("0.75", "1.25"): (1387, 1581, 1580)}
for a in auth:
    key = (repr(a["t1"]), repr(a["t2"]))
    s1, s2, n = cases[key]
    t1, t2 = Fr(key[0]), Fr(key[1])
    N = 4000
    h, ad = C.data(N, t1, t2)
    u = [Fr(1)] * N
    for t in range(s1, s2):
        u[t] = Fr(-1)
    u[n] = Fr(0)
    _, _, s0 = C.sim(u, h, ad)
    v = -h * s0[n] / C.Hij(n, n, h, N)
    u[n] = v
    x, J, sig = C.sim(u, h, ad)
    fixed = [q[2][str(n)] for q in a["cert_kinds"] if q[0] == "fixed"]
    Vm = mine[key]["V"]
    res = []
    for (l_, r_) in fixed:
        l_, r_ = Fr(l_), Fr(r_)
        e = l_ if l_ > v else r_
        ue = list(u); ue[n] = e
        xe, Je, sge = C.sim(ue, h, ad)
        other = max(C.stage_loss(sge[t], ue[t], Fr(-1), Fr(1), h) for t in range(N) if t != n)
        ln = C.stage_loss(sge[n], e, l_, r_, h)
        B = Je - ln - other
        res.append(dict(interval=[float(l_), float(r_)], anchor=float(e), other_loss_over_h2=float(other / h ** 2),
                        stage_n_loss_over_h2=float(ln / h ** 2), bound_minus_J_over_h2=float((B - J) / h ** 2), ok=B >= J))
    lifted = [max(f[1] for f in fixed if f[1] <= float(v) + 1e-12) if any(f[1] <= float(v) for f in fixed) else -1.0,
              min(f[0] for f in fixed if f[0] >= float(v)) if any(f[0] >= float(v) for f in fixed) else 1.0]
    inside = Vm[0] - 1e-15 <= lifted[0] and lifted[1] <= Vm[1] + 1e-15
    print(json.dumps(dict(t1=key[0], t2=key[1], author_fixed=res, author_lifted_range=lifted, referee_V=Vm,
                          lifted_range_inside_referee_V=inside)))
