"""Group-B independent checks for primal/dtoc5-lukvle10 minor fixes.

1. sci_up (new, from gaps.py; old, from git HEAD) against an independent integer
   ceiling formatter, on boundary cases and random values; recompute the six gaps.
2. f(p5) and the p5 row violation, from a generic OSIL evaluator (mpmath 60 dps).
3. x* from the 640-decimal seeds by forward row solving (1500 dps), its distance
   to logs/lukvle10_kkt_x.txt, and f(x*) against the reported enclosure.
"""
import ast, json, random, subprocess, xml.etree.ElementTree as ET
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp

T = Path(__file__).resolve().parents[3] / "primal/dtoc5-lukvle10"
REPO = Path(__file__).resolve().parents[5]
OSIL = Path.home() / ".cache/minlplib/minlplib/osil/lukvle10.osil"


def load_sci_up(src):
    mod = ast.parse(src)
    fn = next(x for x in mod.body if isinstance(x, ast.FunctionDef) and x.name == "sci_up")
    ns = {"Fraction": Q}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "gaps", "exec"), ns)
    return ns["sci_up"]


new = load_sci_up((T / "gaps.py").read_text())
old_src = subprocess.run(["git", "-C", str(REPO), "show",
                          "HEAD:research-20260929/publication/primal/dtoc5-lukvle10/gaps.py"],
                         capture_output=True, text=True, check=True).stdout
old = load_sci_up(old_src)


def ref(q, digits=4):
    """smallest d.ddd e E (d in [1000,9999]) >= q, by exhaustive exponent search"""
    best = None
    for E in range(-400, 400):
        # smallest integer d with d*10^(E-digits+1) >= q
        scale = Q(10) ** (E - digits + 1)
        d = -((-q.numerator * scale.denominator) // (q.denominator * scale.numerator))
        if 10 ** (digits - 1) <= d < 10 ** digits:
            v = d * scale
            if best is None or v < best[0]:
                best = (v, d, E)
    v, d, E = best
    s = str(d)
    return f"{s[0]}.{s[1:]}e{E}"


def wellformed(s, digits=4):
    m, e = s.split("e")
    return len(m) == digits + 1 and m[1] == "." and m[0] != "0"


cases = ["9.9999e-13", "9.9995e-13", "9.99950001e-13", "9.9994e-13", "1e-12", "1e0", "1e5",
         "1e-300", "9.999e3", "9.9990001e3", "0.99999", "99999", "1.00000001", "1.0001",
         "9.99999999999999999e-25", "1.2345e-7", "1.2340000001e-7"]
bad_new = bad_old = 0
print("case | new | old | reference")
for c in cases:
    q = Q(c)
    n, o, r = new(q), old(q), ref(q)
    okn = Q(n) >= q and wellformed(n) and n == r
    oko = Q(o) >= q and wellformed(o) and o == r
    bad_new += not okn
    bad_old += not oko
    print(c, "|", n, "|", o, "|", r, "| new ok" if okn else "| NEW BAD", "" if oko else "(old wrong)")
random.seed(1)
for _ in range(20000):
    k = random.randint(-60, 60)
    if random.random() < 0.5:
        q = Q(random.randint(1, 10 ** 12), 10 ** random.randint(0, 20)) * Q(10) ** k
    else:  # values just below 10^k or just below a 4-digit boundary
        base = Q(random.randint(1000, 9999)) * Q(10) ** (k - 3)
        q = base - Q(1, 10 ** random.randint(1, 30)) * Q(10) ** k
        if q <= 0:
            continue
    n, r = new(q), ref(q)
    if not (n == r and Q(n) >= q and wellformed(n)):
        bad_new += 1
        if bad_new < 5:
            print("random mismatch", q, n, r)
print("bad_new", bad_new, "(old wrong on listed cases:", bad_old, ")")

# six gaps, old vs new formatter
P = Q((T / "logs/dtoc5_check_objective_exact.txt").read_text().strip())
U = Q(json.load(open(T / "logs/lukvle10_enclose.json"))["objective_box"][1])
gaps = []
for D in [Q("5.38967211918114"), Q("5.38967211918114046742396472386")]:
    gaps += [P - D, (P - D) / D]
D = Q("352.2380254050784")
gaps += [U - D, (U - D) / D]
stored = json.load(open(T / "logs/gaps.json"))
stored_vals = [v for d in stored.values() for v in (d["abs_gap_upper"], d["rel_gap_upper"])]
for g, s in zip(gaps, stored_vals):
    print("gap", float(g), "new", new(g), "old", old(g), "ref", ref(g), "stored", s,
          "OK" if new(g) == old(g) == ref(g) == s else "DIFF")
print("lukvle10 enclosure upper end U =", U)

# ---- generic OSIL evaluation for lukvle10
r = ET.parse(OSIL).getroot()
ns = "{os.optimizationservices.org}"
nvar = int(r.find(f".//{ns}variables").get("numberOfVariables"))
ncon = int(r.find(f".//{ns}constraints").get("numberOfConstraints"))
cons = r.findall(f".//{ns}constraints/{ns}con")
lo = [c.get("lb") for c in cons]
up = [c.get("ub") for c in cons]


def expand(parent, tag):
    out = []
    for el in parent.findall(f"{ns}el"):
        v = int(el.text)
        mult = int(el.get("mult", 1))
        inc = int(el.get("incr", 0))
        out += [v + i * inc for i in range(mult)]
    return out


def expandf(parent):
    out = []
    for el in parent.findall(f"{ns}el"):
        mult = int(el.get("mult", 1))
        out += [el.text] * mult
    return out


lcc = r.find(f".//{ns}linearConstraintCoefficients")
start = expand(lcc.find(f"{ns}start"), "start")
rowcol = lcc.find(f"{ns}colIdx")
iscol = rowcol is not None
idx = expand(rowcol if iscol else lcc.find(f"{ns}rowIdx"), "")
val = expandf(lcc.find(f"{ns}value"))
lin = [[] for _ in range(ncon)]
for k in range(len(start) - 1):
    for p in range(start[k], start[k + 1]):
        if iscol:
            lin[k].append((idx[p], Q(val[p])))
        else:
            lin[idx[p]].append((k, Q(val[p])))
quad = [[] for _ in range(ncon)]
for qt in r.findall(f".//{ns}quadraticCoefficients/{ns}qTerm"):
    quad[int(qt.get("idx"))].append((int(qt.get("idxOne")), int(qt.get("idxTwo")), Q(qt.get("coef", "1"))))
nl = r.findall(f".//{ns}nonlinearExpressions/{ns}nl")
assert len(nl) == 1 and nl[0].get("idx") == "-1"
assert r.find(f".//{ns}objectives/{ns}obj").get("maxOrMin") == "min"


def ev(e, x):
    t = e.tag[len(ns):]
    ch = list(e)
    if t == "nl":
        return ev(ch[0], x)
    if t == "sum":
        return mp.fsum(ev(c, x) for c in ch)
    if t == "power":
        return mp.power(ev(ch[0], x), ev(ch[1], x))
    if t == "square":
        return ev(ch[0], x) ** 2
    if t == "number":
        return mp.mpf(e.get("value"))
    if t == "variable":
        return mp.mpf(e.get("coef", "1")) * x[int(e.get("idx"))]
    raise ValueError(t)


def rows(x):
    res = []
    for i in range(ncon):
        s = mp.fsum(mp.mpf(c.numerator) / c.denominator * x[j] for j, c in lin[i])
        s += mp.fsum(mp.mpf(c.numerator) / c.denominator * x[a] * x[b] for a, b, c in quad[i])
        res.append(s)
    return res


def maxviol(x):
    m = mp.mpf(0)
    for i, s in enumerate(rows(x)):
        if lo[i] is not None:
            m = max(m, mp.mpf(lo[i]) - s)
        if up[i] is not None:
            m = max(m, s - mp.mpf(up[i]))
    return m


mp.mp.dps = 60
sol = REPO / "research-20260929/open-instances/minlplib_sol/lukvle10.p5.sol"
v = dict(line.split() for line in sol.read_text().splitlines())
xp5 = [mp.mpf(v[f"x{i}"]) for i in range(1, nvar + 1)]
f5 = ev(nl[0], xp5)
Lx = mp.mpf("352.2380254064956226308712710293664647979978")
print("f(p5) =", mp.nstr(f5, 25), " f(p5)-f(x*)_lo =", mp.nstr(f5 - Lx, 6))
print("display 352.2380254064961 - f(x*)_lo =", mp.nstr(mp.mpf("352.2380254064961") - Lx, 6))
print("objvar", v["objvar"], " objvar - f(x*)_lo =", mp.nstr(mp.mpf(v["objvar"]) - Lx, 6))
print("p5 max row violation =", mp.nstr(maxviol(xp5), 6))

# ---- x* from seeds: each row is linear in its largest-index variable
mp.mp.dps = 1500
seeds = dict(l.split() for l in (T / "points/lukvle10_seed.txt").read_text().splitlines() if not l.startswith("#"))
x = [None] * nvar
x[0], x[1] = mp.mpf(seeds["x1"]), mp.mpf(seeds["x2"])
assert all(lo[i] == up[i] for i in range(ncon))
order = sorted(range(ncon), key=lambda i: max(j for j, _ in lin[i]))
for i in order:
    piv = max(j for j, _ in lin[i])
    assert all(piv not in (a, b) for a, b, _ in quad[i])
    cp = dict(lin[i])[piv]
    s = mp.fsum(mp.mpf(c.numerator) / c.denominator * x[j] for j, c in lin[i] if j != piv)
    s += mp.fsum(mp.mpf(c.numerator) / c.denominator * x[a] * x[b] for a, b, c in quad[i])
    assert x[piv] is None
    x[piv] = (mp.mpf(lo[i]) - s) / (mp.mpf(cp.numerator) / cp.denominator)
assert all(t is not None for t in x)
kkt = dict(l.split() for l in (T / "logs/lukvle10_kkt_x.txt").read_text().splitlines())
xk = [mp.mpf(kkt[f"x{i}"]) for i in range(1, nvar + 1)]
diffs = [abs(a - b) for a, b in zip(x, xk)]
imax = max(range(nvar), key=lambda i: diffs[i])
print("max |x* - x_kkt| =", mp.nstr(diffs[imax], 4), "at x%d" % (imax + 1),
      " digits ~", mp.nstr(-mp.log10(diffs[imax]), 5))
print("max row residual of x* (1500 dps) =", mp.nstr(max(abs(a - mp.mpf(lo[i])) for i, a in enumerate(rows(x))), 4))
print("min |x*| =", mp.nstr(min(abs(t) for t in x), 8))
fx = ev(nl[0], x)
print("f(x*) =", mp.nstr(fx, 50))
print("inside reported enclosure:", Lx <= fx <= mp.mpf("352.2380254064956226308712710293664647979979"))
print("f(p5) - f(x*) =", mp.nstr(f5 - fx, 6))
