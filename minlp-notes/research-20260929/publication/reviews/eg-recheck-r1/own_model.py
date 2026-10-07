"""Verifier's own reader of the cached MINLPLib OSIL file of eg_disc2_s (eg-recheck review r1).

Written from scratch for this review; it shares no code with the certificate author's modules,
the earlier review's indep_cert.py / gms_model.py, or the eg-recheck track's scripts.

Model (checked structurally while parsing; any other node type raises):
  minimize objvar  s.t.  row k (k = 0..27):  lb_k <= -(sum_m a_km prod_i exp(g_ki (mu_kmi + s_i x_i)^2)
                                                   + sum_i l_ki x_i) + [objvar for k < 24] <= ub_k
so with  h_k(x) = sum_m a_km exp(sum_i g_ki (mu_kmi + s_i x_i)^2) + l_k . x :
  objective rows k < 24 (lb only):   objvar >= lb_k + h_k(x)          -> F(x) = max_k (lb_k + h_k(x))
  side rows k >= 24:                 lb_k <= -h_k(x) <= ub_k           (one side finite)
All numbers are kept as exact Fractions of the decimal strings in the file.
"""
import os
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr

import mpmath as mp

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil")
NS = "{os.optimizationservices.org}"


def tag(e):
    return e.tag[len(NS):] if e.tag.startswith(NS) else e.tag


def num(s):
    return Fr(s)


class OsilModel:
    def __init__(self, path=OSIL):
        root = ET.parse(path).getroot()
        vs = root.find(f".//{NS}variables")
        self.names, self.vlb, self.vub, self.vint = [], [], [], []
        for v in vs:
            self.names.append(v.get("name"))
            self.vint.append(v.get("type") == "I")
            lb, ub = v.get("lb", "0"), v.get("ub", "INF")
            self.vlb.append(None if lb == "-INF" else num(lb))
            self.vub.append(None if ub == "INF" else num(ub))
        assert self.names == ["x1", "x2", "x3", "x4", "i5", "i6", "i7", "objvar"], self.names
        obj = root.find(f".//{NS}objectives/{NS}obj")
        assert obj.get("maxOrMin") == "min"
        coefs = list(obj)
        assert len(coefs) == 1 and coefs[0].get("idx") == "7" and num(coefs[0].text) == 1
        cons = list(root.find(f".//{NS}constraints"))
        assert len(cons) == 28
        self.clb = [None if c.get("lb") is None else num(c.get("lb")) for c in cons]
        self.cub = [None if c.get("ub") is None else num(c.get("ub")) for c in cons]
        # linear part: objvar coefficient 1 in rows 0..23, nothing else (decoded by hand from the
        # start/colIdx/value arrays and asserted against the raw XML text here)
        lc = root.find(f".//{NS}linearConstraintCoefficients")
        assert lc.get("numberOfValues") == "24"
        st = [(e.get("mult"), e.get("incr"), e.text) for e in lc.find(f"{NS}start")]
        assert st == [("25", "1", "0"), ("4", None, "24")], st
        ci = [(e.get("mult"), e.text) for e in lc.find(f"{NS}colIdx")]
        assert ci == [("24", "7")], ci
        va = [(e.get("mult"), e.text) for e in lc.find(f"{NS}value")]
        assert va == [("24", "1")], va
        self.objcoef = [1 if k < 24 else 0 for k in range(28)]
        nls = root.find(f".//{NS}nonlinearExpressions")
        assert nls.get("numberOfNonlinearExpressions") == "28"
        self.xml_rows = {}
        self.rows = []
        for nl in nls:
            k = int(nl.get("idx"))
            self.xml_rows[k] = nl[0]
            self.rows.append(self._row(nl))
        assert sorted(self.xml_rows) == list(range(28))
        self.rows = [r for _, r in sorted(zip([int(nl.get("idx")) for nl in nls], self.rows))]

    # -- structured decoding
    def _row(self, nl):
        (neg,) = list(nl)
        assert tag(neg) == "negate"
        (sm,) = list(neg)
        assert tag(sm) == "sum"
        terms, lin = [], {}
        for ch in sm:
            if tag(ch) == "variable":
                i = int(ch.get("idx"))
                lin[i] = lin.get(i, Fr(0)) + num(ch.get("coef", "1"))
                continue
            assert tag(ch) == "product", tag(ch)
            kids = list(ch)
            if len(kids) == 2 and tag(kids[0]) == "number" and tag(kids[1]) == "variable" \
                    or len(kids) == 2 and tag(kids[1]) == "number" and tag(kids[0]) == "variable":
                nn = kids[0] if tag(kids[0]) == "number" else kids[1]
                vv = kids[1] if tag(kids[0]) == "number" else kids[0]
                i = int(vv.get("idx"))
                lin[i] = lin.get(i, Fr(0)) + num(nn.get("value")) * num(vv.get("coef", "1"))
                continue
            a = Fr(1)
            facs = {}
            for f in kids:
                if tag(f) == "number":
                    a *= num(f.get("value"))
                    continue
                assert tag(f) == "exp"
                (p,) = list(f)
                assert tag(p) == "product"
                sq, g = list(p)
                assert tag(sq) == "square" and tag(g) == "number"
                (s2,) = list(sq)
                assert tag(s2) == "sum"
                n0, v0 = list(s2)
                assert tag(n0) == "number" and tag(v0) == "variable"
                i = int(v0.get("idx"))
                assert i not in facs
                facs[i] = (num(v0.get("coef", "1")), num(n0.get("value")), num(g.get("value")))
            assert sorted(facs) == list(range(7)), sorted(facs)
            terms.append((a, facs))
        return dict(terms=terms, lin=lin)

    # -- generic evaluation of the raw XML tree (cross-check of the decoding)
    def eval_xml(self, k, x):
        def ev(e):
            t = tag(e)
            if t == "number":
                return mp.mpf(e.get("value"))
            if t == "variable":
                return mp.mpf(e.get("coef", "1")) * x[int(e.get("idx"))]
            vals = [ev(c) for c in e]
            if t == "sum":
                return mp.fsum(vals)
            if t == "product":
                r = mp.mpf(1)
                for v in vals:
                    r *= v
                return r
            if t == "negate":
                return -vals[0]
            if t == "square":
                return vals[0] ** 2
            if t == "exp":
                return mp.exp(vals[0])
            raise ValueError(t)
        return ev(self.xml_rows[k])

    def eval_struct(self, k, x):
        r = self.rows[k]
        s = mp.mpf(0)
        for a, facs in r["terms"]:
            e = mp.fsum(mp.mpf(g.numerator) / g.denominator * (mp.mpf(mu.numerator) / mu.denominator
                        + mp.mpf(sc.numerator) / sc.denominator * x[i]) ** 2 for i, (sc, mu, g) in facs.items())
            s += mp.mpf(a.numerator) / a.denominator * mp.exp(e)
        for i, l in r["lin"].items():
            s += mp.mpf(l.numerator) / l.denominator * x[i]
        return -s


if __name__ == "__main__":
    import random
    mp.mp.dps = 50
    M = OsilModel()
    print("variables", list(zip(M.names, M.vint, M.vlb, M.vub)))
    print("rows: terms per row", sorted(set(len(r["terms"]) for r in M.rows)),
          "linear parts", {k: {i: str(v) for i, v in r["lin"].items()} for k, r in enumerate(M.rows) if r["lin"]})
    print("row bounds", [(k, str(M.clb[k]), str(M.cub[k])) for k in range(28)])
    rnd = random.Random(1)
    worst = 0
    for trial in range(20):
        x = [mp.mpf(rnd.uniform(float(M.vlb[i]), float(M.vub[i]))) if not M.vint[i] else
             mp.mpf(rnd.randint(int(M.vlb[i]), int(M.vub[i]))) for i in range(7)]
        for k in range(28):
            a, b = M.eval_xml(k, x), M.eval_struct(k, x)
            worst = max(worst, abs(a - b) / (1 + abs(a)))
    print("max rel diff XML tree vs structured decoding over 20 points x 28 rows:", mp.nstr(worst, 5))
