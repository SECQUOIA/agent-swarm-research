# Numerical comparison of MINLPLib .gms (unmodified copies) and .osil for the six instances (50 digits, random points).
import re, random, sys
from mpmath import mp
import osil_own as O
mp.dps = 50
MPF = dict(exp=mp.exp, log=mp.log, cos=mp.cos, sqrt=mp.sqrt)
def gms_equations(path):
    txt = open(path).read()
    txt = "\n".join(l for l in txt.splitlines() if not l.startswith("*"))
    eqs = {}
    for m_ in re.finditer(r"^(e\d+)\.\.(.*?);", txt, re.S | re.M):
        name, body = m_.group(1), " ".join(m_.group(2).split())
        sense = re.search(r"=([ELG])=", body, re.I).group(1).upper()
        lhs, rhs = re.split(r"=[ELGelg]=", body)
        eqs[name] = (lhs, rhs, sense)
    return eqs
def to_py(expr):
    e = expr.replace("**", "^")
    e = re.sub(r"\bsqr\s*\(", "SQR(", e)
    e = re.sub(r"\bpower\s*\(", "POW(", e)
    e = e.replace("^", "**")
    e = re.sub(r"(?<![\w.])(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)", r"mpf('\1')", e)
    return e
ENV = dict(mpf=mp.mpf, log=mp.log, exp=mp.exp, cos=mp.cos, sqrt=mp.sqrt, SQR=lambda a: a * a, POW=lambda a, b: a ** b)
def compare(name, sampler, npts=5):
    m = O.read(name + ".osil")
    eqs = gms_equations("gms/" + name + ".gms")
    idx = {n: i for i, n in enumerate(m["names"])}
    cons = {c["name"]: i for i, c in enumerate(m["cons"])}
    objeq = [k for k, (l, r, s) in eqs.items() if "objvar" in l + r]
    assert len(objeq) == 1
    worst = mp.mpf(0); worst_o = mp.mpf(0)
    random.seed(1)
    for _ in range(npts):
        x = sampler(m)
        env = dict(ENV); env.update({n: x[i] for n, i in idx.items()})
        env["objvar"] = O.objective(m, x, mp.mpf, MPF)
        for k, (l, r, s) in eqs.items():
            vg = eval(to_py(l), env) - eval(to_py(r), env)
            if k in objeq:
                worst_o = max(worst_o, abs(vg) / (1 + abs(env["objvar"])))
                continue
            i = cons[k]
            c = m["cons"][i]
            rhs = c["lb"] if c["lb"] != "-INF" else c["ub"]
            vo = O.row(m, i, x, mp.mpf, MPF) - mp.mpf(rhs)
            d = min(abs(vg - vo), abs(vg + vo)) / (1 + abs(vg))
            worst = max(worst, d)
    print(f"{name}: rows {len(cons)} (gms {len(eqs)-1}+obj), max rel row diff {mp.nstr(worst, 3)}, objective-row residual {mp.nstr(worst_o, 3)}")
U = lambda a, b: mp.mpf(random.uniform(a, b))
def s_hvy(m):
    x = []
    for n, lb, ub in zip(m["names"], m["lb"], m["ub"]):
        if ub != "INF": x.append(U(float(lb), float(ub)))
        else: x.append(U(0.5, 3.0))
    return x
def s_box(lo_default, hi_default):
    def f(m):
        x = []
        for lb, ub in zip(m["lb"], m["ub"]):
            lo = float(lb) if lb != "-INF" else -1.0
            hi = float(ub) if ub != "INF" else max(lo, 0) * 2 + hi_default
            if lo == hi: x.append(mp.mpf(lb)); continue
            x.append(U(max(lo, lo_default) if lb != "-INF" else lo, hi))
        return x
    return f
compare("hvycrash", s_hvy)
compare("ex6_2_7", s_box(1e-7, 1.0))
compare("ex6_2_5", s_box(1e-7, 1.0))
compare("etamac", s_box(0.0, 5.0))
compare("pindyck", s_box(0.0, 5.0))
compare("pricing050", s_box(0.0, 10.0))
