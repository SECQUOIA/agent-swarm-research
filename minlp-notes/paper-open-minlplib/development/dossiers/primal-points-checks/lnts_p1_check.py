"""Objective N*h of MINLPLib's listed lnts p1 points versus the certified verifier duals N*h2.
Inputs: <name>.osil (cached) and <name>.p1.sol (lnts50 from R/open-instances/minlplib_sol/;
lnts100/200/400 fetched from https://www.minlplib.org/sol/<name>.p1.sol on 2026-10-04)."""
from fractions import Fraction as F
import xml.etree.ElementTree as ET
NS = '{os.optimizationservices.org}'
duals = {'lnts50': '0.5546687649381242', 'lnts100': '0.5545954011663565', 'lnts200': '0.5545770161025290', 'lnts400': '0.5545724137001325'}
for n in duals:
    sol = {}
    for l in open(n + '.p1.sol'):
        p = l.split()
        if len(p) >= 2:
            try: sol[p[0]] = F(p[1])
            except Exception: pass
    d = ET.parse(n + '.osil').getroot().find(NS + 'instanceData')
    V = [v.get('name') for v in d.find(NS + 'variables')]
    o = d.find(NS + 'objectives').find(NS + 'obj'); assert o.get('constant') is None
    f = sum(F(c.text) * sol[V[int(c.get('idx'))]] for c in o)
    print(f'{n}: f(p1) = N*h = {float(f)!r}; f(p1) - certified N*h2 = {float(f - F(duals[n])):+.3e}')
