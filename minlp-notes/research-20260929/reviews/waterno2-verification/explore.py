import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, collections
sys.path.insert(0, _RESEARCH + "/reviews/open-instances-verification")
import osilx
from fractions import Fraction as F
T = int(sys.argv[1])
m = osilx.read(_os.path.expanduser("~") + f"/.cache/minlplib/minlplib/osil/waterno2_{T:02d}.osil")
cons = m["cons"]
def vs(c):
    s = set(c["lin"])
    for i, j, a in c["quad"]: s |= {i, j}
    def walk(t):
        if t[0] == "var": s.add(t[1])
        elif t[0] != "num":
            for u in t[1:]: walk(u)
    if c["nl"] is not None: walk(c["nl"])
    return s
V = [vs(c) for c in cons]
copy = [i for i, c in enumerate(cons) if not c["quad"] and c["nl"] is None and len(c["lin"]) == 2
        and sorted(F(a) for a in c["lin"].values()) == [-1, 1] and F(c["lb"]) == 0 and c["ub"] != "INF" and F(c["ub"]) == 0]
hor = [i for i, c in enumerate(cons) if len(V[i]) == T and not c["quad"] and c["nl"] is None and all(F(a) == 1 for a in c["lin"].values()) and c["ub"] == "INF"]
print("copy rows", len(copy), "horizon", [cons[i]["name"] for i in hor])
n = len(m["names"])
par = list(range(n))
def f(a):
    while par[a] != a:
        par[a] = par[par[a]]; a = par[a]
    return a
rem = set(copy) | set(hor)
for i in range(len(cons)):
    if i in rem: continue
    l = sorted(V[i])
    for v in l[1:]:
        par[f(v)] = f(l[0])
comp = collections.Counter(f(v) for v in range(n))
print("atoms", len(comp), sorted(collections.Counter(comp.values()).items()))
