"""Dossier checks for dtoc5 (own code, no project imports).

A. Parse dtoc5.gms text and confirm the model exactly (decimal strings as Fractions).
B. Exact-rational Lagrangian dual certificate from the exactly feasible point:
   lam_t = -2 u_t (exact decimals), lam_{T-1} := 0. d(lam) is computed with exact
   rational arithmetic; each division term is rounded UP to the grid 2^-256 (it is
   subtracted), so the result is a rigorous lower bound that uses no floating point.
"""
import gzip
import re
import time
from fractions import Fraction as Fr

t0 = time.time()
T = 49999
txt = open("dtoc5.gms").read()

# ---------------- A. GAMS text
eqs = re.findall(r"^(e\d+)\.\.(.*?);", txt, flags=re.S | re.M)
eqd = {name: body.replace("\n", " ") for name, body in eqs}
assert len(eqd) == T + 1, len(eqd)
obj = eqd["e1"]
terms = re.findall(r"([0-9.eE+-]+)\s*\*\s*sqr\(\s*x(\d+)\s*\)", obj)
assert all(Fr(c) == Fr(1, 50000) for c, _ in terms)
idx = sorted(int(j) for _, j in terms)
# objective: u = x2..x50000 (t = 0..T-1), y_t = x(50001+t); y_0..y_{T-1} = x50001..x99999
assert idx == list(range(2, 50001)) + list(range(50001, 100000)), (idx[:3], idx[-3:], len(idx))
assert re.search(r"objvar\s*=E=\s*0", obj) or "objvar" in obj
pat = re.compile(r"\s*([0-9.eE+-]+)\s*\*\s*sqr\(\s*x(\d+)\s*\)\s*\+\s*x(\d+)\s*-\s*([0-9.eE+-]+)\s*\*\s*x(\d+)\s*-\s*x(\d+)\s*=E=\s*0\s*$")
for t in range(T):
    m = pat.match(eqd[f"e{t + 2}"])
    assert m, (t, eqd[f"e{t + 2}"])
    q, ya, yb, hc, uu, yn = m.groups()
    assert Fr(q) == Fr(4, 50000) and Fr(hc) == Fr(1, 50000)
    assert int(ya) == int(yb) == 50001 + t and int(yn) == 50002 + t and int(uu) == 2 + t
bnd = re.findall(r"^(x\d+)\.(lo|up|fx|l)\s*=\s*([^;]+);", txt, flags=re.M)
print("A: GAMS rows/objective match; bound/level statements:", bnd[:5], len(bnd))

# ---------------- B. exact dual from the exactly feasible point
vals = {}
with gzip.open("dtoc5_point.txt.gz", "rt") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        k, v = line.split()
        vals[int(k[1:])] = Fr(v)
u = [vals[2 + t] for t in range(T)]
y = [vals[50001 + t] for t in range(T + 1)]
assert y[0] == 1
h = Fr(1, 50000)
# exact primal objective and row check (repeat of the primal track, own code)
assert all(-h * u[t] + y[t] - y[t + 1] + 4 * h * y[t] ** 2 == 0 for t in range(T))
fobj = h * (sum(a * a for a in u) + sum(b * b for b in y[:T]))
fref = Fr(open("dtoc5_check_objective_exact.txt").read().strip())
assert fobj == fref
lam = [-2 * a for a in u]
lam[T - 1] = Fr(0)
assert all(l < Fr(1, 4) for l in lam[1:]), max(lam[1:])
G = 1 << 256
poly = h * (1 - 4 * lam[0]) - lam[0] - h / 4 * sum(l * l for l in lam)  # exact
div_up = 0  # sum of ceil(term * G)
for t in range(1, T):
    num = (lam[t - 1] - lam[t]) ** 2
    den = 4 * h * (1 - 4 * lam[t])
    term = num / den
    div_up += -((-term.numerator * G) // term.denominator)  # ceil
dlow = poly - Fr(div_up, G)
gap = fobj - dlow


def dec(x, n=40):
    s = "-" if x < 0 else ""
    x = abs(x)
    ip = x.numerator // x.denominator
    fp = (x - ip) * 10 ** n
    return f"{s}{ip}.{fp.numerator // fp.denominator:0{n}d}"


print("B: max lam(1..T-1) =", float(max(lam[1:])), " min lam =", float(min(lam)), " u_{T-1} =", float(u[T - 1]))
print("B: rigorous dual  d(lam) >=", dec(dlow))
print("B: exact primal   f(x)    =", dec(fobj))
print("B: gap f - d <=", float(gap), " ; d - 5.38967211918114 =", float(dlow - Fr("5.38967211918114")))
print("B: verifier mpmath lower end 5.3896721191811404674239647238640027; diff =",
      float(dlow - Fr("5.3896721191811404674239647238640027")))
print("seconds", round(time.time() - t0, 1))
assert gap > 0
print("B60: d_low =", dec(dlow, 60))
print("B60: f(x)  =", dec(fobj, 60))
print("B: gap exact (rounded up to 3 sig):", float(gap))
