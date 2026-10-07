"""Sanity test of osil.py: exact evaluation of MINLPLib point p4 of waterno2_06 (expect objective 282.8880373869047 and max row violation 1.1e-11, as in the wave-2 report)."""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../../..'))
import sys, json, time
from fractions import Fraction as Fr
sys.path.insert(0, _RESEARCH + "/publication/primal/water-ann-kan/code")
import osil
F={'num':lambda c:c}
t=time.time()
M=osil.load('waterno2_06')
print('load',time.time()-t, len(M['names']), len(M['cons']))
idx={n:i for i,n in enumerate(M['names'])}
x=[Fr(0)]*len(M['names'])
for line in open(_RESEARCH + '/open-instances-wave2/waterno2/data/waterno2_06.p4.sol'):
    p=line.split()
    if len(p)<2 or p[0]=='objvar': continue
    x[idx[p[0]]]=Fr(p[1])
worst=0;wr=None
for c in M['cons']:
    v=osil.eval_row(c,x,F)
    vi=max((c['lb']-v) if c['lb'] is not None else 0,(v-c['ub']) if c['ub'] is not None else 0,0)
    if vi>worst: worst,wr=vi,c['name']
obj=M['obj']['const']+sum(a*x[j] for j,a in M['obj']['lin'].items())
print(float(obj), float(worst), wr)
