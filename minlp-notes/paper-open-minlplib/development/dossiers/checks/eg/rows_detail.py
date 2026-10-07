import sys
sys.argv=[sys.argv[0]]
exec(open('primal_iv.py').read().split("for name in sys.argv[1:]:")[0])
import xml.etree.ElementTree as ET
for name in ['eg_int_s','eg_disc_s','eg_disc2_s']:
    idata = ET.parse(f'{name}.osil').getroot().find(NS+'instanceData')
    vn=[v.get('name') for v in idata.find(NS+'variables')]
    sol=dict(l.split() for l in open(f'{name}.retry.sol') if l.strip())
    x=[iv.mpf(sol[n]) for n in vn]
    nls={int(n.get('idx')): n[0] for n in idata.find(NS+'nonlinearExpressions')}
    cons=list(idata.find(NS+'constraints'))
    vals=[]
    for k,c in enumerate(cons):
        g=ev(nls[k],x)
        if k<24: vals.append((k+1, iv.mpf(c.get('lb'))-g))
    Fm=max(v.b for _,v in vals)
    act=[(k, mp.nstr(Fm - v.b, 3)) for k,v in vals if Fm - v.b < 1e-6]
    side=[]
    for k in range(24,28):
        c=cons[k]; g=ev(nls[k],x)
        s = (g - iv.mpf(c.get('lb'))) if c.get('lb') else (iv.mpf(c.get('ub'))-g)
        side.append((k+1, mp.nstr(s.a,4)))
    print(name, 'objective rows within 1e-6 of max (F - row):', act, '; side-row slacks:', side)
