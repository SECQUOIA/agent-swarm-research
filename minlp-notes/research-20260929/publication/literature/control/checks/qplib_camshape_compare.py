"""Compare QPLIB camshape copies with the MINLPLib camshape models.

Usage: python3 qplib_camshape_compare.py MINLPLIB.gms QPLIB.gms [MINLPLIB.sol QPLIB.sol]

Both inputs are GAMS scalar models written by GAMS CONVERT. QPLIB variable
x_k is MINLPLib variable x_{k-1} (QPLIB numbers the objective variable as
x1). The script
  1. parses every equation into {monomial: coefficient}, sense and rhs;
  2. matches equations of the two models by their monomial support and sense,
     allowing a common positive scale factor, and reports the largest
     relative coefficient difference and the largest bound difference;
  3. optionally evaluates both solution points in both models with exact
     rational arithmetic (fractions.Fraction on the decimal strings) and
     reports objective values and the largest constraint/bound violation.
Floating-point model data are compared as decimals; nothing here is a proof
about the QPLIB models' optimal values.
"""
import re
import sys
from fractions import Fraction as F



def parse_gms(path, shift):
    txt = open(path).read()
    lines = [l for l in txt.splitlines() if not l.startswith("*")]
    body = "\n".join(lines)
    eqs = {}
    for m in re.finditer(r"^(e\d+)\.\.(.*?);", body, re.S | re.M):
        name, expr = m.group(1), " ".join(m.group(2).split())
        sense = re.search(r"=([ELG])=", expr).group(1)
        lhs, rhs = re.split(r"=[ELG]=", expr)
        lhs = re.sub(r"sqr\((x\d+)\)", r"\1*\1", lhs)
        lhs = lhs.replace("(", "").replace(")", "").strip()
        if not lhs.startswith(("+", "-")):
            lhs = "+ " + lhs
        terms = {}
        pos = 0
        for t in re.finditer(r"([+-])\s*((?:\d+\.?\d*(?:[eE][+-]?\d+)?\*)?)([A-Za-z]\w*(?:\*[A-Za-z]\w*)*)", lhs):
            sign = -1 if t.group(1) == "-" else 1
            coef = F(t.group(2)[:-1]) if t.group(2) else F(1)
            vs = tuple(sorted(ren(v, shift) for v in t.group(3).split("*")))
            terms[vs] = terms.get(vs, 0) + sign * coef
            pos = t.end()
        assert lhs[pos:].strip() == "", (name, lhs[pos:])
        eqs[name] = (terms, sense, F(rhs.strip()))
    bounds = {}
    for m in re.finditer(r"(\w+)\.(lo|up|fx) = ([-0-9.eE+]+);", body, re.M):
        v = ren(m.group(1), shift)
        b = bounds.setdefault(v, [None, None])
        val = F(m.group(3))
        if m.group(2) in ("lo", "fx"):
            b[0] = val
        if m.group(2) in ("up", "fx"):
            b[1] = val
    pos_vars = set()
    pm = re.search(r"^Positive Variables(.*?);", body, re.S | re.M)
    if pm:
        pos_vars = {ren(v.strip(), shift) for v in pm.group(1).replace("\n", "").split(",") if v.strip()}
    for v in pos_vars:
        b = bounds.setdefault(v, [None, None])
        if b[0] is None:
            b[0] = F(0)
    return eqs, bounds


def ren(v, shift):
    if v == "objvar":
        return v
    k = int(v[1:])
    return "x%d" % (k - shift)


def normalize(terms, sense, rhs):
    # move rhs into the key, scale so that the largest |coef| is 1, sense L/E
    if sense == "G":
        terms = {k: -c for k, c in terms.items()}
        rhs = -rhs
        sense = "L"
    return terms, sense, rhs


def compare(a, b):
    ea, ba = a
    eb, bb = b
    keyb = {}
    for n, (t, s, r) in eb.items():
        t, s, r = normalize(t, s, r)
        keyb.setdefault((frozenset(t), s), []).append((n, t, r))
    worst = (0.0, None)
    unmatched = []
    for n, (t, s, r) in ea.items():
        t, s, r = normalize(t, s, r)
        cands = keyb.get((frozenset(t), s), [])
        best = None
        for nb, tb, rb in cands:
            # common scale: ratio of a reference coefficient (sign must agree for L rows)
            k0 = max(t, key=lambda k: abs(t[k]))
            lam = tb[k0] / t[k0]
            if s == "L" and lam <= 0:
                continue
            d = max(abs(float(tb[k] - lam * t[k])) / max(abs(float(lam * t[k])), 1e-300) for k in t)
            dr = abs(float(rb - lam * r))
            score = max(d, dr)
            if best is None or score < best[0]:
                best = (score, nb)
        if best is None:
            unmatched.append(n)
        elif best[0] > worst[0]:
            worst = (best[0], (n, best[1]))
    bd = 0.0
    bdw = None
    for v in set(ba) | set(bb):
        x, y = ba.get(v, [None, None]), bb.get(v, [None, None])
        for i in (0, 1):
            if (x[i] is None) != (y[i] is None):
                bdw = (v, i, x[i], y[i]); bd = float("inf")
            elif x[i] is not None:
                diff = abs(float(x[i] - y[i])) / max(abs(float(x[i])), 1.0)
                if diff > bd:
                    bd, bdw = diff, (v, i, x[i], y[i])
    return len(ea), len(eb), unmatched, worst, bd, bdw


def read_sol(path, shift):
    pt = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and re.match(r"^(x\d+|objvar)$", p[0]):
            pt[ren(p[0], shift)] = F(p[1])
    return pt


def evaluate(model, pt):
    """Return (objective implied by the objective row, worst violation, where).

    The objective row (the one containing objvar) defines objvar; it is
    used to compute the objective and is excluded from the violation."""
    eqs, bounds = model
    worst, where, obj = F(0), None, None
    for n, (t, s, r) in eqs.items():
        val = F(0)
        for vs, c in t.items():
            if vs == ("objvar",):
                continue
            prod = F(c)
            for v in vs:
                prod *= pt.get(v, F(0))  # .sol files omit zero values
            val += prod
        if ("objvar",) in t:
            obj = (r - val) / t[("objvar",)]
            continue
        viol = {"E": abs(val - r), "L": max(val - r, F(0)), "G": max(r - val, F(0))}[s]
        if viol > worst:
            worst, where = viol, n
    for v, (lo, up) in bounds.items():
        if v == "objvar":
            continue
        x = pt.get(v, F(0))
        if lo is not None and lo - x > worst:
            worst, where = lo - x, v + ".lo"
        if up is not None and x - up > worst:
            worst, where = x - up, v + ".up"
    return obj, worst, where


if __name__ == "__main__":
    mgms, qgms = sys.argv[1], sys.argv[2]
    M = parse_gms(mgms, 0)
    Q = parse_gms(qgms, 1)
    nm, nq, unm, worst, bd, bdw = compare(M, Q)
    print(f"MINLPLib {mgms}: {nm} rows; QPLIB {qgms}: {nq} rows")
    print(f"MINLPLib rows without a QPLIB row of the same support and sense: {unm}")
    print(f"largest relative coefficient/rhs difference after common scaling: {worst[0]:.3e} at {worst[1]}")
    print(f"largest relative bound difference: {bd:.3e} at {bdw}")
    if len(sys.argv) > 4:
        pm = read_sol(sys.argv[3], 0)
        pq = read_sol(sys.argv[4], 1)
        for lab, pt in (("MINLPLib point", pm), ("QPLIB point", pq)):
            om, wm, lm = evaluate(M, pt)
            oq, wq, lq = evaluate(Q, pt)
            print(f"{lab}: objective in MINLPLib model = {float(om):.13f}, in QPLIB model = {float(oq):.13f}; "
                  f"max violation in MINLPLib model = {float(wm):.3e} ({lm}); in QPLIB model = {float(wq):.3e} ({lq})")
