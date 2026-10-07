"""Evidence check (not a proof): is MINLPLib pricing050 the n = 50, #2 instance of
Davarnia & van Hoeve (Math. Program. 2021; preprint optimization-online 6512)?

Their pricing model (Sec. 6.2) uses integer price indices x in {0,...,10} with
price x/10.  MINLPLib pricing050 is the continuous version (x in [0,10]).  We
solve the integer version of pricing050 exactly (up to floating point) as a
MILP: one binary per (product, value), rows sum_j g_ij(v) z_jv >= b_i, and
compare the optimum with the integer-version UBs in their Table 6.1
(n = 50: 1592, 1825, 1891, 2403, 1800).  Row data are parsed from
../sources/minlplib_gms/pricing050.gms; row functions are evaluated in double.
"""
import re, math, os
import highspy
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, '..', 'sources', 'minlplib_gms', 'pricing050.gms')).read()
body = t[t.find('e1..'):t.find('x2.lo')]
eqs = re.findall(r'(e\d+)\.\.(.*?);', body, re.S)
obj = ' '.join(eqs[0][1].split())
c = {}
for m in re.finditer(r'([-+])\s*(?:(\d+(?:\.\d+)?)\s*\*\s*)?x(\d+)\b', obj.split('=E=')[0]):
    c[int(m.group(3))] = float(m.group(2) or 1)
# Row functions are evaluated with the generic GAMS-expression evaluator of
# compare_gms.py: the rows are separable and every term vanishes at x_j = 0,
# so g_ij(v) = row_i(x with x_j = v and all other x = 0).
src = open(os.path.join(here, 'compare_gms.py')).read().split("a, b = sys.argv[1]")[0]
cg = {}
exec(src, cg)
from mpmath import mpf
rows = []
for name, e in eqs[1:]:
    e = ' '.join(e.split())
    lhs, rhs = e.split('=L=')
    rows.append((lhs, float(rhs)))
vars_ = sorted(set(range(2, 52)))
print('objective coefficients:', len(c), ' rows:', len(rows))
# MILP: min sum_j c_j * sum_v v z_jv ; sum_v z_jv = 1 ; sum_j sum_v a*v*exp(g v^p) z_jv <= rhs
vals = list(range(11))
idx = {(j, v): k for k, (j, v) in enumerate((j, v) for j in vars_ for v in vals)}
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('mip_rel_gap', 0.0)
h.setOptionValue('threads', 1)
nv = len(idx)
for (j, v), k in idx.items():
    h.addVar(0.0, 1.0)
    h.changeColCost(k, c.get(j, 0.0) * v)
    h.changeColIntegrality(k, highspy.HighsVarType.kInteger)
for j in vars_:
    ks = [idx[(j, v)] for v in vals]
    h.addRow(1.0, 1.0, len(ks), np.array(ks, dtype=np.int32), np.ones(len(ks)))
for lhs, rhs in rows:
    coef = {}
    for j in vars_:
        for v in vals:
            xx = {'x%d' % i: mpf(0) for i in vars_}
            xx['x%d' % j] = mpf(v)
            val = float(cg['ev'](lhs, xx))
            if val != 0.0:
                coef[idx[(j, v)]] = val
    ks = sorted(coef)
    h.addRow(-highspy.kHighsInf, rhs, len(ks), np.array(ks, dtype=np.int32), np.array([coef[k] for k in ks]))
h.run()
info = h.getInfo()
print('MILP status:', h.modelStatusToString(h.getModelStatus()), ' integer optimum (min c.x):', info.objective_function_value,
      ' dual bound:', info.mip_dual_bound)
sol = h.getSolution().col_value
x = {j: sum(v * sol[idx[(j, v)]] for v in vals) for j in vars_}
print('price indices x2..x51:', [int(round(x[j])) for j in vars_])
