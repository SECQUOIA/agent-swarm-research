"""Independent exact check of the witness points (second author; shares no code
with exact_check.py or spec_check.py and does not use SCIP).

For each (model CIP file, witness JSON) pair it
  1. parses the CIP file with its own tokenizer (every number -> Fraction from
     its decimal string),
  2. evaluates every row, every variable bound and binary integrality at the
     witness in exact rational arithmetic,
  3. prints the exact objective and its difference to the given SCIP claims.

It also proves the binary64 statements used in the report: for each listed
"pump-off" case (speed variable s with lower bound L forced to L when its
binary is 0, and a row  -p + s*s*s == 0  with lower bound lb(p) = L^3 in
decimal), it compares fl(L)^3 with fl(lb(p)) exactly, where fl() is the
nearest binary64 number (Python float of the decimal string, converted to an
exact Fraction).

usage: python3 indep_check.py
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def num(tok):
    return Fraction(tok)  # exact value of a decimal (or exponent) string


def parse(path):
    """Return (vars, rows): vars = {name: (kind, obj, lb, ub)},
    rows = [(name, [(coef, [var, ...]), ...], sense, rhs)]."""
    V, R, section = {}, [], None
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if line in ("STATISTICS", "OBJECTIVE", "VARIABLES", "CONSTRAINTS", "END"):
                section = line
                continue
            if section == "VARIABLES" and line.startswith("["):
                kind = line[1:line.index("]")]
                name = line[line.index("<") + 1:line.index(">")]
                rest = line[line.index(">:") + 2:]
                obj = num(rest.split("obj=")[1].split(",")[0].strip())
                lo, hi = rest.split("original bounds=[")[1].rstrip("]").split(",")
                lb = None if lo.strip().lower() in ("-inf", "-infinity") else num(lo.strip())
                ub = None if hi.strip().lower() in ("+inf", "inf", "infinity") else num(hi.strip())
                V[name] = (kind, obj, lb, ub)
            elif section == "CONSTRAINTS" and line.startswith("["):
                body = line[line.index("]") + 1:].strip()
                name = body[1:body.index(">")]
                expr = body[body.index(">:") + 2:].rstrip(";").strip()
                for sense in ("==", ">=", "<="):
                    if f" {sense} " in expr:
                        lhs, rhs = expr.rsplit(f" {sense} ", 1)
                        break
                else:
                    raise ValueError(line)
                terms = []
                for tok in lhs.split():
                    # token: (+|-)coef followed by <v> or *<v>*<w>..., optional [X] type tags
                    i = tok.index("<")
                    coef = num(tok[:i].rstrip("*"))
                    names = [p.split(">")[0] for p in tok[i:].split("<")[1:]]
                    terms.append((coef, names))
                R.append((name, terms, sense, num(rhs.strip())))
    return V, R


def check(model, witness, claims):
    V, R = parse(os.path.join(HERE, model))
    x = {k: Fraction(v) for k, v in json.load(open(os.path.join(HERE, witness))).items()}
    assert set(x) == set(V), "witness and model variables differ"
    bad = []
    for name, terms, sense, rhs in R:
        val = Fraction(0)
        for c, names in terms:
            t = c
            for n in names:
                t *= x[n]
            val += t
        ok = val == rhs if sense == "==" else (val >= rhs if sense == ">=" else val <= rhs)
        if not ok:
            bad.append(name)
    for n, (kind, obj, lb, ub) in V.items():
        if (lb is not None and x[n] < lb) or (ub is not None and x[n] > ub):
            bad.append(n)
        if kind == "binary" and x[n] not in (0, 1):
            bad.append(n)
    obj = sum(o * x[n] for n, (k, o, lb, ub) in V.items())
    print(f"{model}: {len(V)} vars, {len(R)} rows; violated rows/bounds: {bad or 'none'}; "
          f"objective = {float(obj):.12f} (exact {obj.numerator}/{obj.denominator})" if len(str(obj)) < 80 else
          f"{model}: {len(V)} vars, {len(R)} rows; violated rows/bounds: {bad or 'none'}; objective = {float(obj):.12f}")
    for c in claims:
        d = obj - Fraction(c)
        print(f"    objective - claim {c} = {float(d):+.9f}  ({'witness below claim: claim refuted' if d < 0 else 'NOT below claim'})")
    return not bad


def fl(s):
    return Fraction(float(s))  # exact rational value of the nearest binary64 number


CASES = [
    # model, witness, wrong claims (dual bounds reported as 'optimal'): for each model the smallest
    # wrong claim seen in any run (all versions, seeds and settings) and some typical ones
    ("models/p0.cip", "witness/p0.json", ["169.950250085232"]),
    ("models/p4.cip", "witness/p4.json", ["-6.72988938834578", "-6.72975433522885", "-5.72353518548678"]),
    ("models/p5.cip", "witness/p5.json", ["-231.905843299873", "-229.759027754299"]),
    ("models/pair2236.cip", "witness/pair2236.json", ["56.4920384487893", "65.1234"]),
    ("minimal/tiny2.cip", "minimal/tiny2_witness.json", ["-1.23108446311479"]),
    ("minimal/pumps_default.cip", "minimal/pumps_default_witness.json", ["1.19799998144798"]),
    # minimized fuzz reproducers (third author): smallest and typical wrong claims
    ("min/fm336_v1010.cip", "min/fm336_v1010.witness.json", ["0.814125", "1.50521312595154"]),
    ("min/fm318_master.cip", "min/fm318_master.witness.json", ["2.0"]),
    ("minimal/fuzz_master/fuzz_11_336.cip", "minimal/fuzz_master/fuzz_11_336.witness.json", ["1.50513151723365"]),
    ("minimal/fuzz_master/fuzz_11_318.cip", "minimal/fuzz_master/fuzz_11_318.witness.json", ["2.0"]),
]

if __name__ == "__main__":
    allok = True
    for m, w, c in CASES:
        allok &= check(m, w, c)
    print("ALL WITNESSES EXACTLY FEASIBLE:", allok)
    print("\nbinary64 residuals fl(L)^3 - fl(L^3) and fl(L)^2 - fl(L^2) (exact):")
    for L, L2, L3 in (("0.6", "0.36", "0.216"), ("0.7", "0.49", "0.343"), ("0.8", "0.64", "0.512"),
                      ("0.85", "0.7225", "0.614125")):
        assert Fraction(L) ** 2 == Fraction(L2) and Fraction(L) ** 3 == Fraction(L3)
        print(f"  L = {L}: cube {float(fl(L) ** 3 - fl(L3)):+.4e}, square {float(fl(L) ** 2 - fl(L2)):+.4e}")
    # pair2236: b47 = 0 is empty for the binary64 data with zero tolerance
    V, R = parse(os.path.join(HERE, "models/pair2236.cip"))
    rows = {name: (terms, sense, rhs) for name, terms, sense, rhs in R}
    assert rows["e471_up"] == ([(Fraction(-3, 10), ["b47"]), (Fraction(1), ["x545"])], "<=", Fraction(7, 10))
    assert rows["e1211"] == ([(Fraction(-1), ["x993"]), (Fraction(1), ["x545", "x545", "x545"])], "==", Fraction(0))
    assert V["x545"][2] == Fraction("0.7") and V["x993"][2] == Fraction("0.343")
    # with b47 = 0 and binary64 data: fl(0.7) <= x545 <= fl(0.7), x993 = x545^3 = fl(0.7)^3 < fl(0.343) = lb(x993)
    print("pair2236, binary64 data, zero tolerance: b47 = 0 forces x545 = fl(0.7) and x993 = fl(0.7)^3;"
          f" fl(0.7)^3 < fl(0.343): {fl('0.7') ** 3 < fl('0.343')}  -> the b47 = 0 branch is empty")
    sys.exit(0 if allok else 1)
