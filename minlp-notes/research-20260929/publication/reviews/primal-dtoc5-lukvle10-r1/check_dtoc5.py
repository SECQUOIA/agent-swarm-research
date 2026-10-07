"""Reviewer check: exact feasibility and exact objective of the track's dtoc5 point.

Uses only osil_rev.py (reviewer's reader) and Python Fractions. Reads the point file as text.
"""
import gzip, json, os, sys, time
from fractions import Fraction
import osil_rev

T0 = time.time()
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/dtoc5.osil")
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
TRACK = _REPO + "/research-20260929/publication/primal/dtoc5-lukvle10"
PT = TRACK + "/points/dtoc5_point.txt.gz"

M = osil_rev.read(OSIL)
V, cons, lin, quad, nl = M["vars"], M["cons"], M["lin"], M["quad"], M["nl"]
n, m = len(V), len(cons)
assert not nl, "dtoc5 unexpectedly has nonlinear expressions"
print("parsed", n, "vars", m, "rows", round(time.time() - T0, 1), "s", flush=True)

# point: exact decimal strings
val = {}
with gzip.open(PT, "rt") as f:
    for line in f:
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        assert len(parts) == 2, line
        assert parts[0] not in val
        s = parts[1]
        # must be a plain decimal (no exponent, no fraction bar) so the file is an exact decimal
        assert all(ch in "-.0123456789" for ch in s), s
        val[parts[0]] = Fraction(s)
names = [v[0] for v in V]
assert set(val) == set(names) and len(val) == n
x = [val[nm] for nm in names]


def check(x, label):
    bad_b = [j for j, (nm, lb, ub, ty) in enumerate(V)
             if (lb is not None and x[j] < lb) or (ub is not None and x[j] > ub)]
    bad_i = [j for j, (nm, lb, ub, ty) in enumerate(V)
             if ty in ("B", "I") and x[j].denominator != 1]
    qrow = {}
    for idx, terms in quad.items():
        if idx >= 0:
            qrow.setdefault(idx, []).extend(terms)
    bad_r = []
    for r, (nm, lb, ub, const) in enumerate(cons):
        g = const + sum(c * x[j] for j, c in lin[r].items())
        g += sum(c * x[i] * x[k] for i, k, c in qrow.get(r, []))
        if (lb is not None and g < lb) or (ub is not None and g > ub):
            bad_r.append(nm)
    sense, olin, oconst = M["obj"]
    f = oconst + sum(c * x[j] for j, c in olin.items())
    f += sum(c * x[i] * x[k] for i, k, c in quad.get(-1, []))
    return bad_b, bad_i, bad_r, f


bad_b, bad_i, bad_r, f = check(x, "track point")
types = sorted(set(v[3] for v in V))
fixed = [(nm, str(lb), str(ub)) for nm, lb, ub, ty in V if lb is not None or ub is not None]
print("types", types, "bounded vars", fixed)
print("bad bounds", len(bad_b), "bad integrality", len(bad_i), "bad rows", len(bad_r), flush=True)

# compare with the track's exact objective
ftrack = Fraction(open(TRACK + "/logs/dtoc5_check_objective_exact.txt").read().strip())
print("objective equals track's exact rational:", f == ftrack)


def floor_dec(q, k):
    return Fraction((q.numerator * 10 ** k) // q.denominator, 10 ** k)


def ceil_dec(q, k):
    return Fraction(-((-q.numerator * 10 ** k) // q.denominator), 10 ** k)


def up_sig(q, sig=4):
    """round q > 0 upward to `sig` significant digits; returns string"""
    from math import floor, log10
    e = floor(log10(float(q))) - sig + 1
    scale = Fraction(10) ** (-e)
    k = -((-q.numerator * scale.numerator) // (q.denominator * scale.denominator))
    return f"{k}e{e}"


duals = {
    "summary 5.38967211918114": Fraction("5.38967211918114"),
    "verifier lower end 5.3896721191811404674239647238640027": Fraction("5.3896721191811404674239647238640027"),
    "track's truncation 5.38967211918114046742396472386": Fraction("5.38967211918114046742396472386"),
}
gaps = {}
for k, d in duals.items():
    g = f - d
    gaps[k] = dict(abs_gap=up_sig(g), rel_gap=up_sig(g / abs(d)), positive=g > 0)

# negative test: perturb one control by 1e-60 and require exactly one failing row
xp = list(x)
jp = names.index("x500")
xp[jp] += Fraction(1, 10 ** 60)
nb_b, nb_i, nb_r, _ = check(xp, "perturbed")

# structural description in the track report
T = 49999
struct = {}
struct["n_free"] = sum(1 for nm, lb, ub, ty in V if lb is None and ub is None)
struct["fixed_var"] = [(j, nm) for j, (nm, lb, ub, ty) in enumerate(V) if lb is not None]
ok_rows = True
for t in range(T):
    r = lin[t]
    # expected: -(1/50000) u_t + y_t - y_{t+1} + (1/12500) y_t^2 = 0, u_t = var t, y_t = var T + t
    if r != {t: Fraction(-1, 50000), T + t: Fraction(1), T + t + 1: Fraction(-1)}:
        ok_rows = False
    if cons[t][1] != 0 or cons[t][2] != 0 or cons[t][3] != 0:
        ok_rows = False
qc = {idx: terms for idx, terms in quad.items() if idx >= 0}
ok_q = all(qc.get(t) == [(T + t, T + t, Fraction(1, 12500))] for t in range(T)) and len(qc) == T
obj_terms = sorted((i, k, c) for i, k, c in quad[-1])
exp_terms = sorted([(t, t, Fraction(1, 50000)) for t in range(T)] + [(T + t, T + t, Fraction(1, 50000)) for t in range(T)])
struct["rows_match_report_form"] = ok_rows and ok_q
struct["objective_matches_report_form"] = (obj_terms == exp_terms and not M["obj"][1] and M["obj"][2] == 0
                                           and M["obj"][0] == "min")

out = dict(
    n_vars=n, n_rows=m, var_types=types, bounded_vars=fixed,
    bad_bounds=len(bad_b), bad_integrality=len(bad_i), bad_rows=len(bad_r),
    objective_exact_equals_track=f == ftrack,
    objective_denominator_digits=len(str(f.denominator)),
    gaps=gaps,
    negative_test=dict(perturbed="x500 + 1e-60", bad_rows=nb_r, bad_bounds=len(nb_b)),
    structure=struct,
    seconds=round(time.time() - T0, 1),
)
fl, ce = floor_dec(f, 40), ceil_dec(f, 40)
out["objective_floor_40"] = str(fl.numerator * 10 ** 40 // fl.denominator) + "e-40"
out["objective_ceil_40"] = str(ce.numerator * 10 ** 40 // ce.denominator) + "e-40"
print(json.dumps(out, indent=1, default=str))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "check_dtoc5.json"), "w"),
          indent=1, default=str)
