"""Independent reader of the MINLPLib GAMS files of the eg_* instances (review check).

Reads data/<name>.gms (downloaded from https://www.minlplib.org/gms/<name>.gms on 2026-09-30),
extracts every equation as text, converts it to a Python expression and evaluates it with
mpmath at a requested precision.  It shares no code with osilx / eg_model / egdata.

Also extracts the per-term data (a, mu, gamma, scale) by a regular-expression pass over the
same text, for the independent bounding code (indep_tm.py); the extraction is cross-checked
against the direct evaluation of the expression text.
"""
import os
import re
from fractions import Fraction as Fr

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))


class GmsModel:
    def __init__(self, name):
        txt = open(os.path.join(HERE, "data", name + ".gms")).read()
        self.name = name
        m = re.search(r"^Variables\s+(.*?);", txt, re.M | re.S)
        self.vars = [v.strip() for v in m.group(1).replace("\n", " ").split(",")]
        m = re.search(r"^Integer Variables\s+(.*?);", txt, re.M | re.S)
        self.ints = set(v.strip() for v in m.group(1).replace("\n", " ").split(",")) if m else set()
        self.lb, self.ub = {}, {}
        for v, a in re.findall(r"\b(\w+)\.lo = ([-0-9.eE+]+);", txt):
            self.lb[v] = Fr(a)
        for v, a in re.findall(r"\b(\w+)\.up = ([-0-9.eE+]+);", txt):
            self.ub[v] = Fr(a)
        self.eqs = []
        for nm, body in re.findall(r"^(e\d+)\.\.(.*?);", txt, re.M | re.S):
            body = body.replace("\n", " ")
            for sense in ("=G=", "=L=", "=E="):
                if sense in body:
                    lhs, rhs = body.split(sense)
                    break
            else:
                raise ValueError(nm)
            lhs = re.sub(r"\s+", "", lhs)
            # numeric literals become exact decimal mpf constants (not Python floats)
            lhs_mp = re.sub(r"(?<![\w.])(\d+\.?\d*(?:[eE][-+]?\d+)?)", r'M("\1")', lhs)
            self.eqs.append(dict(name=nm, sense=sense, lhs=lhs, rhs=Fr(rhs.strip()),
                                 code=compile(lhs_mp, nm, "eval")))
        assert [e["name"] for e in self.eqs] == [f"e{k}" for k in range(1, len(self.eqs) + 1)]

    def lhs(self, k, point, dps=50):
        """value of the left-hand side of equation k (0-based) at point {var: str|Fraction|mpf}."""
        with mp.workdps(dps):
            env = {v: mp.mpf(point[v]) if not isinstance(point[v], Fr)
                   else mp.mpf(point[v].numerator) / point[v].denominator for v in self.vars}
            env["exp"] = mp.exp
            env["sqr"] = lambda z: z * z
            env["M"] = mp.mpf
            return eval(self.eqs[k]["code"], {"__builtins__": {}}, env)

    def violation(self, k, point, dps=50):
        e = self.eqs[k]
        with mp.workdps(dps):
            v = self.lhs(k, point, dps)
            r = mp.mpf(e["rhs"].numerator) / e["rhs"].denominator
            if e["sense"] == "=G=":
                return max(r - v, 0)
            if e["sense"] == "=L=":
                return max(v - r, 0)
            return abs(v - r)

    # ------------------------------------------------------------ term data (regex)
    def terms(self):
        """per equation: list of (a, {var: (scale, mu, gamma)}) and the linear part {var: coef},
        with lhs = -(sum_m a_m prod exp(gamma (mu + scale*var)^2) + sum lin*var) + objcoef*objvar.
        Returns (data, objcoef list)."""
        out = []
        NUM = r"[0-9.]+(?:[eE][-+]?\d+)?"
        tre = re.compile(r"exp\((-" + NUM + r")\*sqr\((?:\((-" + NUM + r")\)|(" + NUM + r"))\+"
                         r"(?:(0\.1)\*)?(\w+)\)\)")
        for e in self.eqs:
            s = e["lhs"]
            assert s.startswith("-(")
            # find the matching parenthesis of "-("
            depth = 0
            for p, ch in enumerate(s):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        end = p
                        break
            inner, tail = s[2:end], s[end + 1:]
            objc = {"": 0, "+objvar": 1}[tail]
            # split inner into signed products at top level
            items, depth, cur = [], 0, ""
            for ch in inner:
                if ch in "+-" and depth == 0 and cur and not cur.endswith(("e", "E", "*")):
                    items.append(cur)
                    cur = ch
                    continue
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                cur += ch
            items.append(cur)
            tl, lin = [], {}
            for it in items:
                m = re.fullmatch(r"([-+]?[0-9.]+(?:[eE][-+]?\d+)?)\*(\w+)", it)
                if m and m.group(2) in self.vars:
                    lin[m.group(2)] = lin.get(m.group(2), Fr(0)) + Fr(m.group(1))
                    continue
                m = re.match(r"([-+]?[0-9.]+(?:[eE][-+]?\d+)?)\*", it)
                a = Fr(m.group(1))
                rest = it[m.end():]
                fac = {}
                for g, mun, mup, sc, v in tre.findall(rest):
                    assert v not in fac
                    fac[v] = (Fr(sc) if sc else Fr(1), Fr(mun or mup), Fr(g))
                assert rest.count("exp(") == len(fac), (e["name"], it[:80])
                tl.append((a, fac))
            out.append(dict(name=e["name"], terms=tl, lin=lin, objc=objc, sense=e["sense"], rhs=e["rhs"]))
        return out


def eval_terms(T, point, dps=50):
    """evaluate -(sum terms + lin) + objc*objvar from the extracted data (for the cross-check)."""
    with mp.workdps(dps):
        P = {v: mp.mpf(x) if not isinstance(x, Fr) else mp.mpf(x.numerator) / x.denominator
             for v, x in point.items()}
        s = mp.mpf(0)
        for a, fac in T["terms"]:
            e = mp.mpf(0)
            for v, (sc, mu, g) in fac.items():
                t = mp.mpf(mu.numerator) / mu.denominator + (mp.mpf(sc.numerator) / sc.denominator) * P[v]
                e += (mp.mpf(g.numerator) / g.denominator) * t * t
            s += (mp.mpf(a.numerator) / a.denominator) * mp.exp(e)
        for v, c in T["lin"].items():
            s += (mp.mpf(c.numerator) / c.denominator) * P[v]
        return -s + T["objc"] * P["objvar"]
