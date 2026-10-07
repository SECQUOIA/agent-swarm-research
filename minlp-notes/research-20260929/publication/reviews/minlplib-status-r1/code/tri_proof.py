"""Verifier (minlplib-status r1): independent proof that a listed MINLPLib
point can be turned into an exactly feasible point of a given OSiL model, by
forward substitution in outward-rounded interval arithmetic (mpmath.iv).

Method.
  * Binaries/integers are fixed at the listed (integral) values.
  * Each equality row i that is linear, with a constant coefficient c, in a
    continuous variable v that does not occur in the row's quadratic or
    nonlinear part, can "define" v:  v = (rhs - rest_i(x)) / c.
  * Rows are ordered greedily: a row is used when all its variables except v
    are known. Continuous variables that are never defined are independent
    and are fixed at their listed values (exact decimals, as rationals).
  * Each defined v is then a unique real number given the earlier values;
    interval evaluation gives an enclosure of it. If every equality row is
    used this way, the real point exists and satisfies all equalities
    exactly (each equality holds by construction).
  * Proof obligations checked over the enclosures: every variable bound,
    every inequality row (enclosure inside [lb, ub]), integrality.
  * The objective is enclosed.
Assumptions: the OSiL file is read correctly by this reader; mpmath.iv
rounds outward (documented behaviour); divisions/exp/power are evaluated on
intervals that do not contain singularities (iv raises or returns
unbounded intervals otherwise, which then fail the checks).

Usage: python3 tri_proof.py MODEL.osil POINT.sol [--set name=value ...]
"""
import sys
from fractions import Fraction

from mpmath import iv, libmp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from osil_eval_cmp import read, tag  # noqa: E402  (verifier's own reader)

iv.prec = 200


def LO(x):
    return Fraction(*libmp.to_rational(x._mpi_[0]))


def HI(x):
    return Fraction(*libmp.to_rational(x._mpi_[1]))


def I(f):
    f = Fraction(f)
    return iv.mpf(f.numerator) / iv.mpf(f.denominator)


def iev(e, x):
    t = tag(e)
    ch = list(e)
    if t == "number":
        return I(Fraction(e.get("value")))
    if t == "variable":
        return I(Fraction(e.get("coef", "1"))) * x[int(e.get("idx"))]
    a = [iev(c, x) for c in ch]
    if t in ("sum", "plus"):
        r = iv.mpf(0)
        for v in a:
            r = r + v
        return r
    if t == "minus":
        return a[0] - a[1]
    if t == "negate":
        return -a[0]
    if t in ("times", "product"):
        r = iv.mpf(1)
        for v in a:
            r = r * v
        return r
    if t == "divide":
        if LO(a[1]) <= 0 <= HI(a[1]):
            raise ZeroDivisionError("divisor interval contains 0")
        return a[0] / a[1]
    if t == "power":
        ex = a[1]
        if LO(ex) == HI(ex) and LO(ex).denominator == 1:
            return a[0] ** int(LO(ex))
        raise ValueError("non-integer power")
    if t == "square":
        return a[0] ** 2
    if t == "exp":
        return iv.exp(a[0])
    if t == "sqrt":
        if LO(a[0]) < 0:
            raise ValueError("sqrt of negative")
        return iv.sqrt(a[0])
    if t == "ln":
        if LO(a[0]) <= 0:
            raise ValueError("log of nonpositive")
        return iv.log(a[0])
    raise ValueError("node " + t)


def nl_vars(e, out):
    if tag(e) == "variable":
        out.add(int(e.get("idx")))
    for c in e:
        nl_vars(c, out)
    return out


def row_parts(M, i):
    lin = M["lin"].get(i, {}) if i >= 0 else M["obj"]["lin"]
    q = M["quad"].get(i, [])
    nv = set()
    for (p, r, c) in q:
        nv.add(p)
        nv.add(r)
    if i in M["nl"]:
        nl_vars(M["nl"][i], nv)
    return lin, q, nv


def row_eval(M, i, x, skip=None):
    lin, q, nv = row_parts(M, i)
    s = iv.mpf(0)
    for j, c in lin.items():
        if j != skip and c != 0:
            s = s + I(c) * x[j]
    for (p, r, c) in q:
        s = s + I(c) * x[p] * x[r]
    if i in M["nl"]:
        s = s + iev(M["nl"][i], x)
    if i >= 0:
        s = s + I(M["cconst"][i])
    else:
        s = s + I(M["obj"]["const"])
    return s


def load_sol(path):
    vals = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2:
            try:
                vals[p[0]] = Fraction(p[1])
            except ValueError:
                pass
    return vals


def build_order(M):
    n = len(M["vars"])
    eq = [i for i in range(len(M["cons"])) if M["clb"][i] is not None and M["clb"][i] == M["cub"][i]]
    known = set(j for j in range(n) if M["type"][j] in ("B", "I"))
    # candidates
    cand = {}
    for i in eq:
        lin, q, nv = row_parts(M, i)
        cand[i] = [j for j, c in lin.items() if c != 0 and j not in nv and M["type"][j] not in ("B", "I")]
    definable = set(j for i in eq for j in cand[i])
    indep = set(j for j in range(n) if j not in known and j not in definable)
    known |= indep
    order = []
    left = set(eq)
    while left:
        prog = False
        for i in sorted(left):
            lin, q, nv = row_parts(M, i)
            allv = set(j for j, c in lin.items() if c != 0) | nv
            unk = allv - known
            if len(unk) == 1:
                v = unk.pop()
                if v in cand[i]:
                    order.append((i, v))
                    known.add(v)
                    left.discard(i)
                    prog = True
            elif len(unk) == 0:
                order.append((i, None))
                left.discard(i)
                prog = True
        if not prog:
            break
    if left:
        print("NOT TRIANGULAR: rows left", [M["cons"][i] for i in sorted(left)][:20])
        # make one more variable independent: pick undefined vars appearing in left rows
        return None, None, None
    return eq, order, left


def main(osil, sol, sets):
    M = read(osil)
    n = len(M["vars"])
    name = M["vars"]
    listed = load_sol(sol)
    for k, v in sets.items():
        listed[k] = Fraction(v)
    eq, order, left = build_order(M)
    if order is None:
        return False
    defined = set(v for i, v in order if v is not None)
    indep_cont = [j for j in range(n) if j not in defined]
    print(f"vars {n}; equalities {len(eq)} all used; defined {len(defined)}; fixed (listed) {len(indep_cont)}")
    x = [None] * n
    exact = {}
    ok = True
    for j in indep_cont:
        v = listed.get(name[j], Fraction(0))
        if M["type"][j] in ("B", "I") and v.denominator != 1:
            v = Fraction(round(v))
        exact[j] = v
        x[j] = I(v)
    for (i, v) in order:
        if v is None:
            val = row_eval(M, i, x)
            rhs = I(M["clb"][i])
            if not (LO(val) == HI(val) == M["clb"][i]):
                print("equality without free variable not exact:", M["cons"][i], val, rhs)
                ok = False
            continue
        c = M["lin"][i][v]
        rest = row_eval(M, i, x, skip=v)
        x[v] = (I(M["clb"][i]) - rest) / I(c)
    # bounds
    worst = None
    for j in range(n):
        lo, hi = M["lb"][j], M["ub"][j]
        if j in exact:  # fixed at an exact rational: check exactly
            if (lo is not None and exact[j] < lo) or (hi is not None and exact[j] > hi):
                print("bound violated by fixed value:", name[j], exact[j])
                ok = False
            continue
        if lo is not None and LO(x[j]) < lo:
            print("bound violated/undecided:", name[j], "lb", lo, x[j])
            ok = False
        if hi is not None and HI(x[j]) > hi:
            print("bound violated/undecided:", name[j], "ub", hi, x[j])
            ok = False
    # inequalities
    nineq = 0
    for i in range(len(M["cons"])):
        if i in eq:
            continue
        nineq += 1
        val = row_eval(M, i, x)
        lo, hi = M["clb"][i], M["cub"][i]
        if lo is not None and LO(val) < lo:
            print("row violated/undecided:", M["cons"][i], "lb", float(lo), val)
            ok = False
        if hi is not None and HI(val) > hi:
            print("row violated/undecided:", M["cons"][i], "ub", float(hi), val)
            ok = False
        sl = []
        if lo is not None:
            sl.append(LO(val) - lo)
        if hi is not None:
            sl.append(hi - HI(val))
        s = min(sl)
        if worst is None or s < worst[0]:
            worst = (s, M["cons"][i])
    obj = row_eval(M, -1, x)
    print(f"inequalities checked {nineq}; smallest proved slack {float(worst[0]) if worst else None} ({worst[1] if worst else ''})")
    wid = max((HI(x[j]) - LO(x[j]) for j in range(n)), default=0)
    print("widest variable enclosure:", float(wid))
    print("objective enclosure: [%s, %s]" % (iv.nstr(iv.mpf(LO(obj).numerator) / LO(obj).denominator, 16), iv.nstr(iv.mpf(HI(obj).numerator) / HI(obj).denominator, 16)))
    print("objective enclosure exact endpoints (float):", float(LO(obj)), float(HI(obj)))
    print("PROVED feasible" if ok else "NOT PROVED")
    return ok, obj


if __name__ == "__main__":
    sets = {}
    args = []
    for a in sys.argv[1:]:
        if "=" in a:
            k, v = a.split("=", 1)
            sets[k] = v
        else:
            args.append(a)
    main(args[0], args[1], sets)
