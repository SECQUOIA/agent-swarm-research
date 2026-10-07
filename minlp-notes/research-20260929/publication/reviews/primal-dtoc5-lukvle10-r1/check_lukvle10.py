"""Reviewer check for the track's lukvle10 point.

Claim checked: with the exact rational seeds in points/lukvle10_seed.txt, solving the OSIL rows one
after another defines a real point x* that satisfies every row exactly (all variables are free and
continuous), and f(x*) lies in the track's enclosure; x* lies in the track's saved box.

Method (independent of the track's code):
 - model read by osil_rev.py (reviewer's reader, exact Fractions);
 - the elimination order is derived here: a row is usable when exactly one of its variables is
   still unknown and that variable occurs only linearly with a nonzero coefficient;
 - coordinates are enclosed by integer fixed-point interval arithmetic: an interval is a pair of
   integers (L, U) meaning [L 2^-P, U 2^-P]; every product and division is rounded outward with
   exact integer floor/ceil, so the enclosure needs no floating-point assumption;
 - the objective is evaluated from the parsed OSIL expression tree with mpmath.iv (assumption:
   mpmath.iv encloses +, *, exp and log outward); the iv precision exceeds P + 64 bits, so the
   conversion of the fixed-point intervals into iv intervals is exact (checked).
Usage: python3 check_lukvle10.py P
"""
import gzip, json, os, sys, time
from fractions import Fraction
import osil_rev
from mpmath import iv, mp, mpf

T0 = time.time()
P = int(sys.argv[1]) if len(sys.argv) > 1 else 3400
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/lukvle10.osil")
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
TRACK = _REPO + "/research-20260929/publication/primal/dtoc5-lukvle10"
NS = osil_rev.NS

M = osil_rev.read(OSIL)
V, cons, lin, quad, nl = M["vars"], M["cons"], M["lin"], M["quad"], M["nl"]
n, m = len(V), len(cons)
names = [v[0] for v in V]
assert all(v[1] is None and v[2] is None and v[3] == "C" for v in V), "not all variables free/continuous"
assert list(nl) == [-1], "nonlinear expressions only in the objective expected"
assert not M["obj"][1] and M["obj"][2] == 0 and M["obj"][0] == "min" and -1 not in quad
qrow = {}
for idx, terms in quad.items():
    qrow.setdefault(idx, []).extend(terms)
for r, (nm, lb, ub, const) in enumerate(cons):
    assert lb is not None and lb == ub, "only equality rows expected"

# ---------- elimination order ----------
seed_vals = {}
for line in open(TRACK + "/points/lukvle10_seed.txt"):
    if line.startswith("#") or not line.strip():
        continue
    nm, s = line.split()
    assert all(ch in "-.0123456789" for ch in s)
    seed_vals[names.index(nm)] = Fraction(s)
known = set(seed_vals)
rowvars = []
for r in range(m):
    lv = set(lin[r])
    qv = set()
    for i, k, c in qrow.get(r, []):
        qv |= {i, k}
    rowvars.append((lv, qv))
order = []
used = set()
progress = True
while progress:
    progress = False
    for r in range(m):
        if r in used:
            continue
        lv, qv = rowvars[r]
        unk = (lv | qv) - known
        if len(unk) == 1:
            p = unk.pop()
            assert p not in qv and lin[r][p] != 0, ("pivot not linear", r, p)
            order.append((r, p))
            used.add(r)
            known.add(p)
            progress = True
assert len(used) == m and known == set(range(n)), (len(used), len(known))
print("elimination order found:", len(order), "rows; seeds", sorted(names[j] for j in seed_vals), flush=True)

# structure statement of the report: row j: -x_j + 3x_{j+1} - 2x_{j+2} - 2x_{j+1}^2 = -1
form_ok = all(lin[j] == {j: -1, j + 1: 3, j + 2: -2} and qrow.get(j) == [(j + 1, j + 1, -2)]
              and cons[j][1] == -1 and cons[j][3] == 0 for j in range(m))
form_ok = form_ok and m == 998 and n == 1000 and names == [f"x{k}" for k in range(1, 1001)]

# ---------- fixed-point interval arithmetic ----------
S = 1 << P


def sci(q):
    """decimal scientific string of a nonnegative Fraction (no float underflow)"""
    q = Fraction(q)
    if q == 0:
        return "0"
    e = len(str(q.numerator)) - len(str(q.denominator))
    while Fraction(10) ** e > q:
        e -= 1
    while Fraction(10) ** (e + 1) <= q:
        e += 1
    mant = q / Fraction(10) ** e
    return f"{float(mant):.3f}e{e}"


def fdiv(a, b):  # floor(a/b), b > 0
    return a // b


def cdiv(a, b):  # ceil(a/b), b > 0
    return -((-a) // b)


def const_iv(q):
    q = Fraction(q)
    return (fdiv(q.numerator * S, q.denominator), cdiv(q.numerator * S, q.denominator))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def scal(c, a):  # c Fraction
    c = Fraction(c)
    p, q = c.numerator, c.denominator
    lo, hi = (a[0], a[1]) if p >= 0 else (a[1], a[0])
    return (fdiv(lo * p, q), cdiv(hi * p, q))


def mul(a, b, same):
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    if same:  # square of one variable: tighter and still valid
        if a[0] >= 0:
            lo, hi = a[0] * a[0], a[1] * a[1]
        elif a[1] <= 0:
            lo, hi = a[1] * a[1], a[0] * a[0]
        else:
            lo, hi = 0, max(a[0] * a[0], a[1] * a[1])
    else:
        lo, hi = min(ps), max(ps)
    return (fdiv(lo, S), cdiv(hi, S))


X = [None] * n
for j, q in seed_vals.items():
    X[j] = const_iv(q)
    assert X[j][0] * Fraction(1, S) <= q <= X[j][1] * Fraction(1, S)
for r, p in order:
    nm, lb, ub, const = cons[r]
    acc = const_iv(lb - const)  # rhs
    for j, c in lin[r].items():
        if j != p:
            acc = add(acc, scal(-c, X[j]))
    for i, k, c in qrow.get(r, []):
        acc = add(acc, scal(-c, mul(X[i], X[k], i == k)))
    X[p] = scal(Fraction(1) / lin[r][p], acc)
    assert X[p][0] <= X[p][1]
wmax = max(Fraction(b - a, S) for a, b in X)
absmin = min(min(abs(Fraction(a, S)), abs(Fraction(b, S))) for a, b in X)
straddle = [names[j] for j, (a, b) in enumerate(X) if a <= 0 <= b]
print(f"propagated: max coordinate width {sci(wmax)}, min |x| {float(absmin):.6f}, "
      f"intervals containing 0: {straddle} ({time.time() - T0:.1f} s)", flush=True)

# ---------- objective over the coordinate intervals ----------
iv.prec = P + 128
mp.prec = P + 128


def to_iv(a):
    lo = mpf((a[0], -P))
    hi = mpf((a[1], -P))
    assert int(lo * S) == a[0] and int(hi * S) == a[1]  # exact conversion
    return iv.mpf([lo, hi])


XI = [to_iv(a) for a in X]


def ev(e):
    tag = e.tag[len(NS):]
    kids = list(e)
    if tag == "sum":
        out = iv.mpf(0)
        for k in kids:
            out = out + ev(k)
        return out
    if tag == "square":
        assert len(kids) == 1
        a = ev(kids[0])
        return a ** 2
    if tag == "variable":
        assert not kids
        c = Fraction(e.get("coef", "1"))
        assert c == 1
        return XI[int(e.get("idx"))]
    if tag == "number":
        assert e.get("type") in (None, "real")
        return iv.mpf(e.get("value"))  # exact for "1"
    if tag == "power":
        assert len(kids) == 2
        b, x = ev(kids[0]), ev(kids[1])
        assert b.a > 0, "base interval must be positive for exp(e log b)"
        return iv.exp(x * iv.log(b))
    raise ValueError(tag)


root = nl[-1]
assert root.tag == NS + "sum"
# objective form check: power(square(x_a), square(x_b)+1) for pairs (2i, 2i+1) both ways
terms = list(root)
pairs = []
for t in terms:
    b, e = list(t)
    a = int(list(b)[0].get("idx"))
    s, one = list(e)
    bb = int(list(s)[0].get("idx"))
    pairs.append((a, bb))
pair_ok = sorted(pairs) == sorted([(2 * i, 2 * i + 1) for i in range(500)] + [(2 * i + 1, 2 * i) for i in range(500)])
F = ev(root)
# exact rational ends of the iv enclosure
from mpmath.libmp import to_rational
flo = Fraction(*to_rational(F._mpi_[0]))
fhi = Fraction(*to_rational(F._mpi_[1]))
print(f"objective enclosure width {sci(fhi - flo)} ({time.time() - T0:.1f} s)", flush=True)

track_lo = Fraction("352.2380254064956226308712710293664647979978")
track_hi = Fraction("352.2380254064956226308712710293664647979979")
inside_track = track_lo <= flo and fhi <= track_hi

# ---------- saved box contains the enclosures ----------
box = {}
with gzip.open(TRACK + "/points/lukvle10_box.txt.gz", "rt") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        nm, c, rad = line.split()
        box[nm] = (Fraction(c), Fraction(rad))
assert set(box) == set(names)
inside_box = all(box[names[j]][0] - box[names[j]][1] <= Fraction(a, S) and
                 Fraction(b, S) <= box[names[j]][0] + box[names[j]][1] for j, (a, b) in enumerate(X))
max_rad = max(r for c, r in box.values())

# ---------- gaps ----------
DUAL = Fraction("352.2380254050784")
DUAL_CERT = Fraction("352.23802540507845563")  # certified end quoted in reviews/closing-confirm-r2.md


def up(q, sig=4):
    from math import floor, log10
    e = floor(log10(float(q))) - sig + 1
    num, den = q.numerator, q.denominator
    if e < 0:
        num *= 10 ** (-e)
    else:
        den *= 10 ** e
    return f"{cdiv(num, den)}e{e}"


def dec(q, k, rnd):
    v = q.numerator * 10 ** k
    i = fdiv(v, q.denominator) if rnd == "floor" else cdiv(v, q.denominator)
    s = str(abs(i)).rjust(k + 1, "0")
    return ("-" if i < 0 else "") + s[:-k] + "." + s[-k:]


out = dict(
    P_bits=P, elimination_rows=len(order), seeds=sorted(names[j] for j in seed_vals),
    report_row_form_matches_osil=form_ok, objective_pairs_match=pair_ok,
    max_coordinate_width=sci(wmax), min_abs_coordinate=f"{float(absmin):.9f}",
    objective_lo_45=dec(flo, 45, "floor"), objective_hi_45=dec(fhi, 45, "ceil"),
    objective_width=sci(fhi - flo),
    inside_track_enclosure=inside_track,
    inside_track_box=inside_box, track_box_max_radius=f"{float(max_rad):.3e}",
    gap_vs_summary_dual=dict(abs=up(fhi - DUAL), rel=up((fhi - DUAL) / DUAL)),
    gap_vs_certified_end=dict(abs=up(fhi - DUAL_CERT), rel=up((fhi - DUAL_CERT) / DUAL_CERT)),
    point_minus_p5_listed=f"{float(Fraction('352.2380254064961') - fhi):.4e}",
    seconds=round(time.time() - T0, 1),
)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", f"check_lukvle10_P{P}.json"), "w"),
          indent=1)
