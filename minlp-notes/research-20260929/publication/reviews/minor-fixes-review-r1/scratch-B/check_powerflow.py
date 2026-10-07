"""Group-B independent checks for primal/powerflow minor fixes (own OSIL evaluator, mpmath 50 dps).

- p1 slacks of every inequality row; active (< 1e-9) list, next smallest slack, max violation;
- structure of rows e359 e360 e362 e363 e386 and voltage rows e307..e315 of 0039r;
- p1 objective vs. the reported enclosures;
- upward displays and summary relative gaps (exact rationals);
- SHA-256 of osilx.py.
"""
import hashlib, xml.etree.ElementTree as ET
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp

mp.mp.dps = 50
HERE = Path(__file__).resolve()
R = HERE.parents[5] / "research-20260929"
OSIL = Path.home() / ".cache/minlplib/minlplib/osil"
ns = "{os.optimizationservices.org}"


def expand_int(parent):
    out = []
    for el in parent.findall(f"{ns}el"):
        v, mult, inc = int(el.text), int(el.get("mult", 1)), int(el.get("incr", 0))
        out += [v + i * inc for i in range(mult)]
    return out


def expand_val(parent):
    out = []
    for el in parent.findall(f"{ns}el"):
        out += [el.text] * int(el.get("mult", 1))
    return out


def load(name):
    r = ET.parse(OSIL / f"{name}.osil").getroot()
    vars_ = r.findall(f".//{ns}variables/{ns}var")
    for v in vars_:
        assert v.get("lb") == "-INF" and v.get("ub") is None and v.get("type", "C") == "C", v.attrib
    names = [v.get("name") for v in vars_]
    cons = r.findall(f".//{ns}constraints/{ns}con")
    n = len(cons)
    lin = [dict() for _ in range(n)]
    lcc = r.find(f".//{ns}linearConstraintCoefficients")
    if lcc is not None:
        start = expand_int(lcc.find(f"{ns}start"))
        ci = lcc.find(f"{ns}colIdx")
        assert ci is not None
        idx, val = expand_int(ci), expand_val(lcc.find(f"{ns}value"))
        for row in range(len(start) - 1):
            for p in range(start[row], start[row + 1]):
                lin[row][idx[p]] = lin[row].get(idx[p], 0) + Q(val[p])
    quad = [[] for _ in range(n)]
    oquad = []
    for qt in r.findall(f".//{ns}quadraticCoefficients/{ns}qTerm"):
        t = (int(qt.get("idxOne")), int(qt.get("idxTwo")), Q(qt.get("coef", "1")))
        (oquad if qt.get("idx") == "-1" else quad[int(qt.get("idx"))]).append(t)
    nl = [None] * n
    onl = None
    for e in r.findall(f".//{ns}nonlinearExpressions/{ns}nl"):
        i = int(e.get("idx"))
        if i == -1:
            onl = e
        else:
            assert nl[i] is None
            nl[i] = e
    obj = r.find(f".//{ns}objectives/{ns}obj")
    assert obj.get("maxOrMin") == "min"
    olin = {int(c.get("idx")): Q(c.text) for c in obj.findall(f"{ns}coef")}
    return dict(names=names, cons=cons, lin=lin, quad=quad, nl=nl, olin=olin, oquad=oquad, onl=onl,
                oconst=Q(obj.get("constant", "0")))


def ev(e, x):
    t = e.tag[len(ns):]
    ch = list(e)
    if t == "nl":
        return ev(ch[0], x)
    if t == "sum":
        return mp.fsum(ev(c, x) for c in ch)
    if t == "product":
        p = mp.mpf(1)
        for c in ch:
            p *= ev(c, x)
        return p
    if t == "square":
        return ev(ch[0], x) ** 2
    if t == "sin":
        return mp.sin(ev(ch[0], x))
    if t == "cos":
        return mp.cos(ev(ch[0], x))
    if t == "number":
        return mp.mpf(e.get("value"))
    if t == "variable":
        return mp.mpf(e.get("coef", "1")) * x[int(e.get("idx"))]
    raise ValueError(t)


def frac(q):
    return mp.mpf(q.numerator) / q.denominator


def rowval(M, i, x):
    c = M["cons"][i]
    s = frac(Q(c.get("constant", "0")))
    s += mp.fsum(frac(a) * x[j] for j, a in M["lin"][i].items())
    s += mp.fsum(frac(a) * x[p] * x[q] for p, q, a in M["quad"][i])
    if M["nl"][i] is not None:
        s += ev(M["nl"][i], x)
    return s


def objval(M, x):
    s = frac(M["oconst"]) + mp.fsum(frac(a) * x[j] for j, a in M["olin"].items())
    s += mp.fsum(frac(a) * x[p] * x[q] for p, q, a in M["oquad"])
    if M["onl"] is not None:
        s += ev(M["onl"], x)
    return s


def bnd(s):
    if s is None or s in ("-INF", "INF", "-inf", "inf"):
        return None
    return mp.mpf(s)


ENC_UP = {"powerflow0030p": "576.8934134703742598676684",
          "powerflow0039p": "41869.0515113202038027683845",
          "powerflow0039r": "41869.0515113209830932768582"}
ENC_LO = {"powerflow0030p": "576.8934134703742598676683",
          "powerflow0039p": "41869.0515113202038027683844",
          "powerflow0039r": "41869.0515113209830932768581"}

for name in ["powerflow0030p", "powerflow0039p", "powerflow0039r"]:
    M = load(name)
    idx = {v: j for j, v in enumerate(M["names"])}
    x = [mp.mpf(0)] * len(idx)
    missing = set(idx)
    for line in (R / f"open-instances-wave3/sol/{name}.p1.sol").read_text().splitlines():
        p = line.split()
        if len(p) >= 2 and p[0] in idx:
            x[idx[p[0]]] = mp.mpf(p[1])
            missing.discard(p[0])
    ineq, maxviol = [], (mp.mpf(0), None)
    for i, c in enumerate(M["cons"]):
        v = rowval(M, i, x)
        lb, ub = bnd(c.get("lb")), bnd(c.get("ub"))
        for side, b in (("lb", lb), ("ub", ub)):
            if b is None:
                continue
            slack = v - b if side == "lb" else b - v
            if -slack > maxviol[0]:
                maxviol = (-slack, c.get("name"))
            if lb is not None and ub is not None and lb == ub:
                continue
            ineq.append((slack, c.get("name"), side))
    ineq.sort()
    act = [t for t in ineq if t[0] < mp.mpf("1e-9")]
    nxt = [t for t in ineq if t[0] >= mp.mpf("1e-9")][:2]
    print(f"== {name}: {len(missing)} vars missing in p1 (set 0); max row violation {mp.nstr(maxviol[0], 4)} at {maxviol[1]}")
    print("  active (slack<1e-9):", [(n, s, mp.nstr(sl, 3)) for sl, n, s in act])
    print("  max |active slack| =", mp.nstr(max(abs(t[0]) for t in act), 4),
          "; max positive active slack =", mp.nstr(max(t[0] for t in act), 4))
    print("  next smallest inactive slacks:", [(n, s, mp.nstr(sl, 4)) for sl, n, s in nxt])
    f = objval(M, x)
    print("  obj(p1) =", mp.nstr(f, 20), "; enclosure lower - obj(p1) =", mp.nstr(mp.mpf(ENC_LO[name]) - f, 4))
    if name == "powerflow0039r":
        byname = {c.get("name"): i for i, c in enumerate(M["cons"])}
        for rn in ["e359", "e360", "e362", "e363", "e386", "e307", "e308", "e309", "e310", "e311", "e312", "e313", "e314", "e315"]:
            i = byname[rn]
            c = M["cons"][i]
            terms = [f"{a}*{M['names'][j]}" for j, a in M["lin"][i].items()]
            terms += [f"{a}*{M['names'][p]}*{M['names'][q]}" for p, q, a in M["quad"][i]]
            print(f"  {rn}: {' + '.join(terms)} in [{c.get('lb')}, {c.get('ub')}]  nl={M['nl'][i] is not None}  "
                  f"value-ub={mp.nstr(rowval(M, i, x) - (bnd(c.get('ub')) or 0), 4)}")

# ---- displays and gaps (exact rationals)
print("== displays")
def up_display(u, decimals):
    k = -((-u.numerator * 10 ** decimals) // u.denominator)
    return Q(k, 10 ** decimals)
checks = [
    ("dtoc5", Q((R / "publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt").read_text().strip()),
     "5.38967211918114", Q("5.38967211918114")),
    ("lukvle10", Q("352.2380254064956226308712710293664647979979"), "352.2380254064961", Q("352.2380254050784")),
    ("powerflow0030p", Q(ENC_UP["powerflow0030p"]), "576.8934134704", Q("576.8934122988004")),
    ("powerflow0039p old", Q(ENC_UP["powerflow0039p"]), "41869.0515113202", Q("41869.05148485014")),
    ("powerflow0039p new", Q(ENC_UP["powerflow0039p"]), "41869.0515113203", Q("41869.05148485014")),
    ("powerflow0039r old", Q(ENC_UP["powerflow0039r"]), "41869.0515113208", Q("41869.05148327243")),
    ("powerflow0039r new", Q(ENC_UP["powerflow0039r"]), "41869.0515113210", Q("41869.05148327243")),
]
for lab, U, disp, D in checks:
    d = Q(disp)
    ndec = len(disp.split(".")[1])
    print(f"  {lab}: display {disp} - upper end = {float(d - U):.4e} -> {'UPPER BOUND' if d >= U else 'NOT an upper bound'};"
          f" upward rounding of upper end at {ndec} decimals = {up_display(U, ndec)} ({up_display(U, ndec) == d});"
          f" at {ndec-1} decimals = {up_display(U, ndec-1)};"
          f" rel gap (display-dual)/dual = {float((d - D) / D):.4e}; rigorous (U-D)/D = {float((U - D) / D):.4e}")
print("  dtoc5 shortest upward displays:", [str(up_display(checks[0][1], k)) for k in (14, 15)],
      "exact", float(checks[0][1]))
print("  dtoc5 verifier lower end vs display: ", Q("5.3896721191811404674239647238640027") > Q("5.38967211918114"))

print("== osilx.py sha256", hashlib.sha256((R / "reviews/open-instances-verification/osilx.py").read_bytes()).hexdigest())
