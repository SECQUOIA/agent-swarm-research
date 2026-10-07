"""Model extraction for the Gibbs-energy instances ex6_2_5 and ex6_2_7.

- Splits the objective (a top-level sum) into per-phase functions G_p(n1, n2, n3);
  asserts that no term mixes phases and that the 3 rows are the mass balances
  sum_p n_{p,i} = b_i.
- Scaling analysis in exact rational arithmetic: every term T satisfies
  T(t n) = t T(n) + t ln(t) R_T(n) with R_T linear; returns R_p = sum of R_T.
  (Rules: linear forms scale by t; ln(linear) gains + ln t; ln(n_i / sum n) is
  scale invariant; products are handled only in the patterns that occur, and
  anything else raises.)
- Evaluators for G_p with pluggable arithmetic (float/numpy, mpmath).
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import osilx  # noqa: E402


def vars_of(t, acc=None):
    acc = set() if acc is None else acc
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            vars_of(c, acc)
    return acc


# ---------------- exact scaling classes ----------------
# class tuples:
#  ("const", q)                  constant q
#  ("lin", {i: q})               linear form, T(tn) = t T(n)
#  ("log", {i: q})               ln(L) with L linear: T(tn) = T(n) + ln t   (the dict is L, kept for positivity)
#  ("deg0",)                     scale-invariant function
#  ("hom", R)                    T(tn) = t T(n) + t ln t R(n), R linear ({i: q})

def lin_add(a, b, s=1):
    d = dict(a)
    for k, v in b.items():
        d[k] = d.get(k, 0) + s * v
    return {k: v for k, v in d.items() if v != 0}


def lin_scale(a, q):
    return {k: q * v for k, v in a.items() if q * v != 0}


def classify(t):
    op = t[0]
    if op == "num":
        return ("const", Fraction(t[1]))
    if op == "var":
        return ("lin", {t[1]: Fraction(t[2])})
    kids = [classify(c) for c in t[1:]]
    if op == "negate":
        k = kids[0]
        if k[0] == "const":
            return ("const", -k[1])
        if k[0] == "lin":
            return ("lin", lin_scale(k[1], -1))
        if k[0] == "hom":
            return ("hom", lin_scale(k[1], -1))
        raise ValueError(t)
    if op == "sum":
        kinds = {k[0] for k in kids}
        if kinds <= {"lin"}:
            d = {}
            for k in kids:
                d = lin_add(d, k[1])
            return ("lin", d)
        if kinds <= {"lin", "hom"}:
            R = {}
            for k in kids:
                if k[0] == "hom":
                    R = lin_add(R, k[1])
            return ("hom", R)
        if kinds <= {"deg0", "const"}:
            return ("deg0",)
        raise ValueError(("sum", kinds))
    if op == "ln":
        k = kids[0]
        if k[0] == "lin":
            assert all(v > 0 for v in k[1].values())  # positive combination of positive variables
            return ("log", k[1])
        if k[0] == "deg0":
            return ("deg0",)
        raise ValueError(t)
    if op == "divide":
        a, b = kids
        if a[0] == "lin" and b[0] == "lin":
            assert all(v > 0 for v in b[1].values())
            return ("deg0",)
        raise ValueError(t)
    if op == "product":
        consts = [k for k in kids if k[0] == "const"]
        rest = [k for k in kids if k[0] != "const"]
        q = Fraction(1)
        for k in consts:
            q *= k[1]
        kinds = sorted(k[0] for k in rest)
        if kinds == ["lin"]:
            return ("lin", lin_scale(rest[0][1], q))
        if kinds == ["lin", "log"]:
            L = [k for k in rest if k[0] == "lin"][0][1]
            return ("hom", lin_scale(L, q))          # q L ln(M): scaling adds t ln t * q L
        if kinds == ["deg0", "lin"]:
            return ("hom", {})
        raise ValueError(("product", kinds))
    raise ValueError(op)


def load(name):
    I = ev.load(name)
    o = I["obj"]
    assert o["sense"] == "min" and o["constant"] == "0" and not o["lin"] and not o["quad"]
    assert o["nl"][0] == "sum"
    names = I["names"]
    assert names == [f"x{k}" for k in range(2, 11)]
    # phases: (x2,x5,x8), (x3,x6,x9), (x4,x7,x10); rows e2,e3,e4: component balances
    phases = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    b = []
    for i, c in enumerate(I["cons"]):
        assert c["lb"] == c["ub"] and c["constant"] == "0" and not c["quad"] and c["nl"] is None
        assert c["lin"] == {phases[0][i]: "1", phases[1][i]: "1", phases[2][i]: "1"}
        b.append(c["lb"])
    for j in range(9):
        assert I["lb"][j] == "1e-7" and I["vt"][j] == "C"
        assert I["ub"][j] == b[j // 3]              # ub of every n_{p,i} equals b_i
    terms = [[] for _ in range(3)]
    for T in o["nl"][1:]:
        vs = vars_of(T)
        owner = [p for p in range(3) if vs <= set(phases[p])]
        assert len(owner) == 1, ("term mixes phases", T)
        terms[owner[0]].append(T)
    # R_p via exact scaling analysis
    R = []
    for p in range(3):
        Rp = {}
        for T in terms[p]:
            k = classify(T)
            assert k[0] in ("lin", "hom"), k
            if k[0] == "hom":
                Rp = lin_add(Rp, k[1])
        R.append([Rp.get(j, Fraction(0)) for j in phases[p]])
    return dict(I=I, phases=phases, b=b, terms=terms, R=R)


def remap(t, m):
    """Replace variable indices by local indices 0..2 (m: global -> local)."""
    if t[0] == "var":
        return ("var", m[t[1]], t[2])
    if t[0] == "num":
        return t
    return (t[0],) + tuple(remap(c, m) for c in t[1:])


def phase_trees(M):
    out = []
    for p in range(3):
        m = {g: l for l, g in enumerate(M["phases"][p])}
        out.append([remap(T, m) for T in M["terms"][p]])
    return out


def G_eval(trees, n, num, fns):
    s = None
    for T in trees:
        v = osilx.ev_tree(T, n, num, fns)
        s = v if s is None else s + v
    return s


if __name__ == "__main__":
    for name in ("ex6_2_7", "ex6_2_5"):
        M = load(name)
        tr = phase_trees(M)
        same = [tr[p] == tr[0] for p in range(3)]
        print(name, "b =", M["b"], "terms per phase", [len(t) for t in M["terms"]],
              "identical to phase 0:", same, "R_p =", [[str(v) for v in r] for r in M["R"]])
