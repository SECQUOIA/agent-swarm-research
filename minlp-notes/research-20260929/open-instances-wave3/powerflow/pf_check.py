"""Sanity check of the power-flow Lagrangian certificates (independent of the certificate code
paths that compute the bound): at the MINLPLib point p1 (mapped to rectangular coordinates for
the polar model) evaluate, in 50-digit arithmetic,
    obj(p1)  and  L(p1) = obj + sum_r w_r (expr_r - rhs_r)  (sign-split multipliers),
and check  bound <= L(p1) <= obj(p1) + (row violations)*|w|.
Uses the multipliers saved by pf_cert.py in ../logs/<name>.sdpcert.json.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import json
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import ev  # noqa: E402

import pf_model as pm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main(name):
    mp.mp.dps = 50
    M = pm.decode(name)
    cert = json.load(open(os.path.join(HERE, "..", "logs", f"{name}.sdpcert.json")))
    rows = M["rows"]
    if cert["variant"] == "angle rows dropped":
        rows = [r for r in rows if r["kind"] != "angle"]
    raw = cert["raw"]
    assert len(raw) == len(rows)
    I = M["I"]
    vals = ev.read_sol(os.path.join(HERE, "..", "sol", f"{name}.p1.sol"))
    z = [mp.mpf(vals.get(v, "0")) for v in I["names"]]
    # bus coordinates x
    n = M["n"]
    x = [mp.mpf(0)] * (2 * n)
    if M["polar"]:
        for k, (vv, tt) in enumerate(M["busmap"]):
            v, th = z[vv], z[tt]
            x[2 * k] = v * mp.cos(th)
            x[2 * k + 1] = v * mp.sin(th)
    else:
        xset = sorted({a for c in I["cons"] if c["quad"] and c["lb"] == c["ub"] for a, b, _ in c["quad"]} |
                      {b for c in I["cons"] if c["quad"] and c["lb"] == c["ub"] for a, b, _ in c["quad"]})
        keys = []
        for c in I["cons"]:
            if c["quad"] and not c["lin"] and all(a == b for a, b, _ in c["quad"]) and {a for a, b, _ in c["quad"]} <= set(xset):
                keys.append(tuple(sorted(a for a, b, _ in c["quad"])))
        keys = sorted(set(keys))
        for k, (a, b) in enumerate(keys):
            x[2 * k] = z[a]; x[2 * k + 1] = z[b]
    q = lambda F: mp.mpf(F.numerator) / F.denominator

    def expr(r):
        s = mp.mpf(0)
        for j, c in r["lin"].items():
            s += q(c) * z[j]
        for (i, j), c in r["Q"].items():
            s += q(c) * x[i] * x[j]
        for j, c in r["qy"].items():
            s += q(c) * z[j] * z[j]
        return s
    obj = q(M["obj"]["const"]) + sum(q(c) * z[j] for j, c in M["obj"]["lin"].items()) + sum(q(c) * z[j] ** 2 for j, c in M["obj"]["qy"].items())
    L = obj
    maxviol = mp.mpf(0)
    for r, rv in zip(rows, raw):
        e = expr(r)
        if rv[0] == "eq":
            w = q(Fr(rv[1]))
            L += w * (e - q(r["lb"]))
            maxviol = max(maxviol, abs(e - q(r["lb"])))
        else:
            if rv[1] is not None and rv[1] > 0:
                L += q(Fr(rv[1])) * (e - q(r["ub"]))
                maxviol = max(maxviol, e - q(r["ub"]))
            if rv[2] is not None and rv[2] > 0:
                L += q(Fr(rv[2])) * (q(r["lb"]) - e)
                maxviol = max(maxviol, q(r["lb"]) - e)
    b = cert["bound"]
    print(f"{name}: obj(p1) {mp.nstr(obj, 17)}  L(p1) {mp.nstr(L, 17)}  certified bound {b!r}  "
          f"max relaxation-row violation at p1 {mp.nstr(maxviol, 3)}  bound <= L: {b <= L}  L - obj {mp.nstr(L - obj, 3)}")


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
