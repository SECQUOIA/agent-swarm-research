"""Why does the COCONUT benchmark list Fbest = -1612.1783 for pindyck, below the
certified MINLPLib optimum -1170.486...?  (Numerical evidence, not a proof.)

Takes the first 16 values of COCONUT's best point (../sources/coconut/lib1_pindyck.res,
these are the prices p_1..p_16) and re-runs the pindyck recursion
  td_t = 0.87 td_{t-1} - 0.13 p_t + c_t,  s_t = 0.75 s_{t-1} + (1.1+0.1 p_t) 1.02^(-K cs_t),
  cs_t = cs_{t-1} + s_t,  d_t = td_t - s_t,  R_t = R_{t-1} - d_t,  J = sum 1.05^-(t-1) d_t (p_t - 250/R_t)
with K = 0.142857142857143 (the GAMS/GLOBALLib/MINLPLib model) and with K = 1
(what COCONUT's dag2gams translation computes: exp(-0.0198026...*cs) = 1.02^(-cs)).
"""
import re, os
from mpmath import mp, mpf, findroot, log
mp.dps = 30
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, '..', 'sources', 'coconut')
mod = open(os.path.join(src, 'lib1_pindyck.mod')).read()
c = [mpf(m.group(1)) for m in re.finditer(r'\ne\d+:\s+0\.13\*x\d+ - 0\.87\*x\d+ \+ x\d+ = ([\d.]+);', mod)]
assert len(c) == 16
vals = [mpf(v) for v in re.findall(r'^x\(\d+\)\s*=\s*(\S+)', open(os.path.join(src, 'lib1_pindyck.res')).read(), re.M)]
p = vals[:16]
gms = open(os.path.join(src, 'lib1_pindyck.gms')).read()
k_dag = re.search(r'exp\(\((-[\d.]+)\) \* x', gms).group(1)
print('exponent coefficient in COCONUT pindyck.gms:', k_dag, ' ln(1.02) =', mp.nstr(log(mpf('1.02')), 16),
      ' ln(1.02)/7 =', mp.nstr(log(mpf('1.02')) / 7, 16))
for K in [mpf('0.142857142857143'), mpf(1)]:
    td, s, cs, R, J, dmin = mpf(18), mpf('6.5'), mpf(0), mpf(500), mpf(0), mpf(10) ** 9
    for t in range(16):
        td = mpf('0.87') * td - mpf('0.13') * p[t] + c[t]
        S = findroot(lambda S: S - (mpf('0.75') * s + (mpf('1.1') + mpf('0.1') * p[t]) * mpf('1.02') ** (-K * (cs + S))), s)
        s = S; cs += S; d = td - s; R -= d; dmin = min(dmin, d)
        J += d * (p[t] - 250 / R) / mpf('1.05') ** t
    print('K =', mp.nstr(K, 15), ': J(COCONUT prices) =', mp.nstr(J, 15), '  min d_t =', mp.nstr(dmin, 6))
