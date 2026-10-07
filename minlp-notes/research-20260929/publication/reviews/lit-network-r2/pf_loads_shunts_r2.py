"""Reviewer r2: independent check that powerflow0030p (MINLPLib GAMS) has MATPOWER case30
loads and no bus shunts. Exact rationals (fractions) for coefficient comparisons."""
import re
from fractions import Fraction as F
from collections import Counter

def mat(path, name):
    s = open(path).read()
    blk = re.search(r'mpc\.%s = \[(.*?)\];' % name, s, re.S).group(1)
    return [[F(t) for t in ln.split(';')[0].split()] for ln in blk.strip().splitlines() if ln.strip() and not ln.strip().startswith('%')]

bus = mat('case30_matpower.m', 'bus'); br = mat('case30_matpower.m', 'branch')
print('buses', len(bus), 'branches', len(br), 'shunts (bus,Gs,Bs):', [(int(b[0]), b[4], b[5]) for b in bus if b[4] or b[5]])
gms = open('powerflow0030p.gms').read()
rows = [(n, ' '.join(b.split())) for n, b in re.findall(r'^(e\d+)\.\.(.*?);', gms, re.S | re.M)]
# balance rows: linear rows containing at least one flow variable x31..x194 and no theta var, sense E
def vars_(b): return [int(v) for v in re.findall(r'x(\d+)', b)]
lin = lambda b: not re.search(r'sqr|sin|cos|\*x|objvar', b)
bal = [(n, b) for n, b in rows if '=E=' in b and lin(b) and not re.fullmatch(r'x195 =E= 0', b)]
assert all(31 <= v <= 194 or 225 <= v <= 236 for n, b in bal for v in vars_(b)), 'unexpected var in balance row'
rhs = Counter(F(b.split('=E=')[1].strip()) for n, b in bal)
want = Counter([-b[2] / 100 for b in bus] + [-b[3] / 100 for b in bus])
print('balance rows found', len(bal), '; rhs multiset equals -Pd/100, -Qd/100 multiset:', rhs == want)
if rhs != want: print('diff', (rhs - want), (want - rhs))
nl_bal = [n for n, b in bal if re.search(r'sqr|sin|cos|\*x', b)]
print('balance rows with nonlinear terms:', len(nl_bal))
# sqr(V) coefficients in branch rows (V vars x1..x30)
coefs = []
for n, b in rows:
    for m in re.finditer(r'([-+]?)\s*([0-9.]+(?:[eE][-+]?\d+)?)\*sqr\(x(\d+)\)', b):
        if 1 <= int(m.group(3)) <= 30:
            coefs.append((n, F(m.group(1) + m.group(2)), int(m.group(3))))
for n, b in rows:  # coefficient-free sqr(V) terms
    for m in re.finditer(r'(?<![0-9.*])\s([-+])\s*sqr\(x(\d+)\)', ' ' + b):
        if 1 <= int(m.group(2)) <= 30: coefs.append((n, F(1 if m.group(1) == '+' else -1), int(m.group(2))))
cands = set()
for r in br:
    R, X, B = r[2], r[3], r[4]
    z2 = R * R + X * X
    g, bs = R / z2, -X / z2
    for v in (g, bs, bs + B / 2, -(bs + B / 2), -g, -bs, B / 2):
        cands.add(v)
def close(a, c): return abs(a - c) <= F(1, 10**12) * max(1, abs(c))
miss = [(n, float(c), v) for n, c, v in coefs if not any(close(c, k) for k in cands)]
print('sqr(V) terms in rows:', len(coefs), '; not equal to a pure branch quantity (1e-12 rel):', len(miss), miss[:5])
# would a shunt-folded coefficient match instead?
sh = [F(19, 10000), F(4, 10000)]
fold = [(n, float(c)) for n, c, v in coefs if any(close(abs(c), abs(k) + s) or close(abs(c), abs(abs(k) - s)) for k in cands for s in sh) and not any(close(c, k) for k in cands)]
print('coefficients matching branch +/- shunt only:', len(fold))
print('literal 0.0019 / 0.0004 in file:', bool(re.search(r'(?<![0-9])0\.0019(?![0-9])', gms)), bool(re.search(r'(?<![0-9])0\.0004(?![0-9])', gms)))
