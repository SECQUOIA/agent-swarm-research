"""Exact term-by-term comparison of MINLPLib GAMS and OSIL files for the powerflow models.
Each row becomes a dict {monomial: Fraction coefficient}; a monomial is a sorted tuple of
factors ('x', name) / ('sin', p, q) / ('cos', p, q) (p < q after normalising
cos(q - p) = cos(p - q) and sin(q - p) = -sin(p - q))."""
import re, sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/pfdossier/code")
import osilx

def norm_trig(kind, p, q, coef):
    if p > q:
        p, q = q, p
        if kind == "sin":
            coef = -coef
    return (kind, p, q), coef

def add(d, mono, c):
    mono = tuple(sorted(mono))
    d[mono] = d.get(mono, Fr(0)) + c
    if d[mono] == 0:
        del d[mono]

def split_top(s):
    """split a GAMS expression into signed top-level terms"""
    terms, depth, cur, sign = [], 0, "", 1
    s = s.strip()
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and ch in "+-" and cur.strip() and not re.search(r"[eE]$", cur.strip()):
            terms.append((sign, cur.strip())); cur = ""; sign = 1 if ch == "+" else -1
        elif depth == 0 and ch in "+-" and not cur.strip():
            sign = sign * (1 if ch == "+" else -1)
        else:
            cur += ch
        i += 1
    if cur.strip():
        terms.append((sign, cur.strip()))
    return terms

def gms_rows(path):
    txt = open(path).read()
    eqs = re.findall(r"^(e\d+)\.\.(.*?);", txt, flags=re.S | re.M)
    rows = {}
    for name, body in eqs:
        body = "".join(body.split())
        m = re.match(r"(.*)=([EGL])=(.*)", body)
        lhs, rel, rhs = m.group(1), m.group(2), Fr(m.group(3).strip().replace(" ", ""))
        d = {}
        for sign, t in split_top(lhs):
            factors = re.findall(r"sqr\(\w+\)|sin\([^)]*\)|cos\([^)]*\)|[A-Za-z_]\w*|[\d.]+(?:[eE][-+]?\d+)?", t)
            coef = Fr(sign)
            mono = []
            for f in factors:
                if f.startswith("sqr("):
                    v = f[4:-1]; mono += [("x", v), ("x", v)]
                elif f.startswith(("sin(", "cos(")):
                    a, b = [z.strip() for z in f[4:-1].split("-")]
                    key, coef = norm_trig(f[:3], a, b, coef)
                    mono.append(key)
                elif re.match(r"[\d.]", f):
                    coef *= Fr(f)
                else:
                    mono.append(("x", f))
            add(d, mono, coef)
        rows[name] = (d, rel, rhs)
    return rows

def osil_rows(path):
    I = osilx.read(path)
    nm = I["names"]
    def expand(t):
        """polynomial-with-trig expansion: list of (coef, [factors])"""
        op = t[0]
        if op == "num":
            return [(Fr(t[1]), [])]
        if op == "var":
            return [(Fr(t[2]), [("x", nm[t[1]])])]
        if op == "sum":
            out = []
            for s in t[1:]:
                out += expand(s)
            return out
        if op == "product":
            out = [(Fr(1), [])]
            for s in t[1:]:
                e = expand(s)
                out = [(c1 * c2, f1 + f2) for c1, f1 in out for c2, f2 in e]
            return out
        if op == "square":
            e = expand(t[1])
            return [(c1 * c2, f1 + f2) for c1, f1 in e for c2, f2 in e]
        if op in ("sin", "cos"):
            arg = expand(t[1])
            assert len(arg) == 2 and all(len(f) == 1 for c, f in arg), arg
            (c1, f1), (c2, f2) = arg
            assert {c1, c2} == {Fr(1), Fr(-1)}
            p, q = (f1[0][1], f2[0][1]) if c1 == 1 else (f2[0][1], f1[0][1])
            key, c = norm_trig(op, p, q, Fr(1))
            return [(c, [key])]
        raise ValueError(op)
    rows = {}
    for con in I["cons"]:
        d = {}
        for j, c in con["lin"].items():
            add(d, [("x", nm[j])], Fr(c))
        for a, b, c in con["quad"]:
            add(d, [("x", nm[a]), ("x", nm[b])], Fr(c))
        if con["nl"] is not None:
            for c, f in expand(con["nl"]):
                add(d, f, c)
        assert con["constant"] == "0"
        rows[con["name"]] = (d, con["lb"], con["ub"])
    obj = {}
    for j, c in I["obj"]["lin"].items():
        add(obj, [("x", nm[j])], Fr(c))
    for a, b, c in I["obj"]["quad"]:
        add(obj, [("x", nm[a]), ("x", nm[b])], Fr(c))
    return rows, obj, Fr(I["obj"]["constant"])

for name in sys.argv[1:]:
    G = gms_rows(f"/tmp/pfdossier/gms/minlplib_{name}.gms")
    O, obj, oc = osil_rows(f"/tmp/pfdossier/osil/{name}.osil")
    # objective row e1: lhs - objvar = rhs  ->  objvar = lhs - rhs
    d1, rel, rhs = G.pop("e1")
    assert rel == "E" and d1.pop((("x", "objvar"),)) == -1
    objG = d1
    ok_obj = (objG == obj) and (oc == -rhs)
    nbad = 0; worst = Fr(0)
    for r, (d, rel, rhs) in G.items():
        od, lb, ub = O[r]
        # GAMS: lhs rel rhs
        exp_lb = rhs if rel in "EG" else None
        exp_ub = rhs if rel in "EL" else None
        olb = None if osilx.isinf(lb) else Fr(lb)
        oub = None if osilx.isinf(ub) else Fr(ub)
        if d != od or exp_lb != olb or exp_ub != oub:
            nbad += 1
            for k in set(d) | set(od):
                a, b = d.get(k, Fr(0)), od.get(k, Fr(0))
                if a != b:
                    worst = max(worst, abs(a - b) / max(abs(a), abs(b)))
    print(f"{name}: GAMS rows {len(G)} (+obj), OSIL rows {len(O)}; objective identical: {ok_obj}; "
          f"rows differing: {nbad}; max rel. coefficient difference {float(worst):.3g}")
