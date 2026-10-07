"""Forward construction of a point from a few free inputs, with an existence argument.

Given rational values for the free variables (network inputs; binaries are
chosen from the edge arguments when a model has interval binaries), every other
variable is DEFINED by one equality row in which it is the only unknown and
appears linearly with a coefficient that is provably nonzero:
    x_v := (rhs - rest(x)) / coef(x).
The real point x* given by these definitions satisfies each defining row
exactly.  The code encloses x* with outward-rounded interval arithmetic
(mpmath iv; tanh via 1 - 2/(exp(2s) + 1), so only iv's +, -, *, / and exp are
trusted) and keeps exact Fractions where a value is rational (no transcendental
function on its path).  Rows that are not used as definitions are checked
separately: exactly when all their values are rational, otherwise by intervals
(inequalities only; an unused transcendental equality row cannot be certified
and is reported).

Also provides the same computation in plain mpmath floating point (mode 'mp'),
used only to choose inputs (never as proof).
"""
from fractions import Fraction as Fr

import mpmath as mp
from mpmath import iv

import osil


def dec_out(q, digits=40, up=False):
    """Decimal string of the rational q rounded outward (down if not up) to `digits` significant digits."""
    q = Fr(q)
    if q == 0:
        return "0"
    import math
    e = len(str(abs(q.numerator))) - len(str(q.denominator))  # rough exponent
    k = digits - e
    t = q * Fr(10) ** k
    n = -((-t.numerator) // t.denominator) if up else t.numerator // t.denominator
    v = Fr(n) / Fr(10) ** k
    assert (v >= q) if up else (v <= q)
    return str(n) + "e" + str(-k)


def ivq(q):
    """Interval enclosing the rational q."""
    q = Fr(q)
    return iv.mpf(q.numerator) / q.denominator


def iv_tanh(s):
    return 1 - 2 / (iv.exp(2 * s) + 1)


IVF = {"num": ivq, "exp": iv.exp, "tanh": iv_tanh}
MPF = {"num": lambda q: mp.mpf(Fr(q).numerator) / Fr(q).denominator, "exp": mp.exp, "tanh": mp.tanh}


def _tup_to_frac(t):
    """Exact Fraction of a raw mpf tuple (sign, man, exp, bc); no rounding involved."""
    sign, man, exp, bc = t
    if man == 0:
        assert exp == 0, "special value (inf/nan) in an interval endpoint"
        return Fr(0)
    v = Fr(man) * (Fr(2) ** exp if exp >= 0 else Fr(1, 2 ** (-exp)))
    return -v if sign else v


def lo_frac(X):
    """Exact lower endpoint of an mpmath interval (read from the raw endpoint, not re-rounded)."""
    return _tup_to_frac(X._mpi_[0])


def hi_frac(X):
    return _tup_to_frac(X._mpi_[1])


class Forward:
    def __init__(self, M, skip_rows=(), log=print):
        self.M, self.log = M, log
        self.n = len(M["names"])
        self.skip = set(skip_rows)
        self.eqrows = [i for i, c in enumerate(M["cons"])
                       if c["lb"] is not None and c["lb"] == c["ub"] and c["name"] not in self.skip]
        self.isbin = [M["vtype"][j] in ("B", "I") for j in range(self.n)]
        self._groups()

    def _groups(self):
        """Binary groups: one-hot rows sum b = 1 over binaries; their argument z = the one
        continuous variable shared by the big-M rows of the group."""
        M = self.M
        self.groups = []
        for c in M["cons"]:
            if c["quad"] or c["nl"] is not None or not c["lin"]:
                continue
            if not all(self.isbin[j] for j in c["lin"]):
                continue
            if c["lb"] == 1 and c["ub"] == 1 and all(a == 1 for a in c["lin"].values()):
                bins = sorted(c["lin"])
                zs = set()
                rows = []
                bs = set(bins)
                for r in M["cons"]:
                    if r["lb"] is not None and r["lb"] == r["ub"]:
                        continue
                    if r["quad"] or r["nl"] is not None:
                        continue
                    if set(r["lin"]) & bs:
                        cont = [j for j in r["lin"] if not self.isbin[j]]
                        zs.update(cont)
                        rows.append(r)
                if len(zs) == 1:
                    self.groups.append(dict(bins=bins, z=zs.pop(), rows=rows))
        # inequality rows of a group's own binaries and argument (checked when choosing)

    def run(self, fixed, mode="iv", choose="first"):
        """fixed: {j: Fraction}.  Returns dict with X (values), exact (Fractions or None), defrow."""
        F = IVF if mode == "iv" else MPF
        X = [None] * self.n
        Q = [None] * self.n
        for j, v in fixed.items():
            Q[j] = Fr(v)
            X[j] = F["num"](v)
        defrow = {}
        used = set()
        prog = True
        while prog:
            prog = False
            for g in self.groups:
                if X[g["z"]] is not None and X[g["bins"][0]] is None:
                    k = self._choose(g, X, Q, F, mode, choose)
                    for i, b in enumerate(g["bins"]):
                        Q[b] = Fr(1 if i == k else 0)
                        X[b] = F["num"](Q[b])
                    prog = True
            for ri in self.eqrows:
                if ri in used:
                    continue
                c = self.M["cons"][ri]
                st = self._try(c, X, Q, F, mode)
                if st is None:
                    continue
                v, xv, qv = st
                X[v], Q[v] = xv, qv
                defrow[v] = c["name"]
                used.add(ri)
                prog = True
        return dict(X=X, Q=Q, defrow=defrow, used=used, F=F, mode=mode)

    def _choose(self, g, X, Q, F, mode, choose):
        """Index of the binary set to 1: every row of the group must hold for the assignment."""
        ok = []
        for k in range(len(g["bins"])):
            val = {b: Fr(1 if i == k else 0) for i, b in enumerate(g["bins"])}
            good = True
            for r in g["rows"]:
                if not all(j in val or j == g["z"] for j in r["lin"]):
                    continue
                s = r["const"] + sum(a * val[j] for j, a in r["lin"].items() if j in val)
                az = r["lin"].get(g["z"], Fr(0))
                # need lb <= s + az z <= ub
                if Q[g["z"]] is not None:
                    t = s + az * Q[g["z"]]
                    if (r["lb"] is not None and t < r["lb"]) or (r["ub"] is not None and t > r["ub"]):
                        good = False
                        break
                else:
                    T = F["num"](s) + F["num"](az) * X[g["z"]]
                    if mode == "iv":
                        if (r["lb"] is not None and lo_frac(T) < r["lb"]) or (r["ub"] is not None and hi_frac(T) > r["ub"]):
                            good = False
                            break
                    else:
                        if (r["lb"] is not None and T < F["num"](r["lb"])) or (r["ub"] is not None and T > F["num"](r["ub"])):
                            good = False
                            break
            if good:
                ok.append(k)
        assert ok, f"argument {self.M['names'][g['z']]} lies in no admissible interval (or straddles an end)"
        return ok[0] if choose == "first" else ok[-1]

    def _try(self, c, X, Q, F, mode):
        unk = set(j for j in c["lin"] if X[j] is None)
        for i, j, a in c["quad"]:
            if X[i] is None:
                unk.add(i)
            if X[j] is None:
                unk.add(j)
        nlv = osil.tree_vars(c["nl"]) if c["nl"] is not None else set()
        unk |= {j for j in nlv if X[j] is None}
        if len(unk) != 1:
            return None
        (v,) = unk
        if v in nlv:
            return None
        exact = True
        coefq, restq = Fr(0), c["const"]
        coef, rest = F["num"](0), F["num"](c["const"])
        for j, a in c["lin"].items():
            if j == v:
                coefq += a
                coef = coef + F["num"](a)
            else:
                rest = rest + F["num"](a) * X[j]
                if Q[j] is None:
                    exact = False
                else:
                    restq += a * Q[j]
        for i, j, a in c["quad"]:
            if i == v and j == v:
                return None
            if i == v or j == v:
                u = j if i == v else i
                coef = coef + F["num"](a) * X[u]
                if Q[u] is None:
                    exact = False
                else:
                    coefq += a * Q[u]
            else:
                rest = rest + F["num"](a) * X[i] * X[j]
                if Q[i] is None or Q[j] is None:
                    exact = False
                else:
                    restq += a * Q[i] * Q[j]
        if c["nl"] is not None:
            exact = False
            rest = rest + osil.eval_tree(c["nl"], X, F)
        rhs = c["lb"]
        if exact:
            if coefq == 0:
                return None
            qv = (rhs - restq) / coefq
            return v, F["num"](qv), qv
        if mode == "iv":
            if lo_frac(coef) <= 0 <= hi_frac(coef):
                return None
        elif coef == 0:
            return None
        return v, (F["num"](rhs) - rest) / coef, None

    def check(self, res, extra_skip=()):
        """Rigorous checks of everything not covered by the definitions (mode iv).
        Returns a report dict; raises on failure."""
        M = self.M
        X, Q = res["X"], res["Q"]
        assert res["mode"] == "iv"
        missing = [M["names"][j] for j in range(self.n) if X[j] is None]
        assert not missing, ("undetermined", missing[:10])
        rep = dict(unused_eq_exact=[], unused_eq_uncertified=[], skipped=[], ineq_exact=0, ineq_iv=0,
                   min_margin=None, bounds_checked=0, bound_viol=[])
        def margin(m, what):
            if rep["min_margin"] is None or m < rep["min_margin"][0]:
                rep["min_margin"] = (m, what)
        for ri, c in enumerate(M["cons"]):
            iseq = c["lb"] is not None and c["lb"] == c["ub"]
            if iseq and ri in res["used"]:
                continue
            if c["name"] in self.skip or c["name"] in extra_skip:
                rep["skipped"].append(c["name"])
                continue
            vs = osil.row_vars(c)
            if c["nl"] is None and all(Q[j] is not None for j in vs):
                t = osil.eval_row(c, Q, {"num": lambda q: q})
                if iseq:
                    assert t == c["lb"], ("unused equality row fails exactly", c["name"])
                    rep["unused_eq_exact"].append(c["name"])
                else:
                    assert (c["lb"] is None or t >= c["lb"]) and (c["ub"] is None or t <= c["ub"]), c["name"]
                    rep["ineq_exact"] += 1
                continue
            T = osil.eval_row(c, X, IVF)
            if iseq:
                rep["unused_eq_uncertified"].append(c["name"])
                continue
            if c["lb"] is not None:
                m = lo_frac(T) - c["lb"]
                assert m >= 0, ("inequality not proved", c["name"], float(m))
                margin(m, c["name"])
            if c["ub"] is not None:
                m = c["ub"] - hi_frac(T)
                assert m >= 0, ("inequality not proved", c["name"], float(m))
                margin(m, c["name"])
            rep["ineq_iv"] += 1
        return rep

    def check_bounds(self, res, which=None):
        """Variable bounds: exact for rational values, interval otherwise. which: set of
        variable indices to check (default all). Returns list of violations / unproved."""
        M = self.M
        X, Q = res["X"], res["Q"]
        bad = []
        minm = None
        for j in range(self.n):
            if which is not None and j not in which:
                continue
            lb, ub = M["lb"][j], M["ub"][j]
            if Q[j] is not None:
                if (lb is not None and Q[j] < lb) or (ub is not None and Q[j] > ub):
                    bad.append((M["names"][j], "exact value outside bounds"))
                continue
            if lb is not None:
                m = lo_frac(X[j]) - lb
                if m < 0:
                    bad.append((M["names"][j], f"lower bound not proved (margin {float(m):.3e})"))
                elif minm is None or m < minm[0]:
                    minm = (m, M["names"][j] + " lb")
            if ub is not None:
                m = ub - hi_frac(X[j])
                if m < 0:
                    bad.append((M["names"][j], f"upper bound not proved (margin {float(m):.3e})"))
                elif minm is None or m < minm[0]:
                    minm = (m, M["names"][j] + " ub")
        return bad, minm

    def objective(self, res):
        M = self.M
        o = M["obj"]
        assert o["sense"] == "min"
        X = res["X"]
        T = ivq(o["const"])
        for j, a in o["lin"].items():
            T = T + ivq(a) * X[j]
        for i, j, a in o["quad"]:
            T = T + ivq(a) * X[i] * X[j]
        if o["nl"] is not None:
            T = T + osil.eval_tree(o["nl"], X, IVF)
        return T
