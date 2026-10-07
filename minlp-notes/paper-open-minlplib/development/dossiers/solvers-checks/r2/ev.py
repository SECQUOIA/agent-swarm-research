import sys, re, subprocess
from fractions import Fraction as F
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,'../cam')
from gparse import parse_gms
def levels(gdx):
    out=subprocess.run(['gdxdump',gdx,'dFormat=hexponential'],capture_output=True,text=True).stdout
    L={}
    for m in re.finditer(r'(?:Positive |Free |Negative )?Variable (\w+)(?:\(\))? /(.*?)/;',out):
        name,body=m.groups()
        mm=re.search(r'\bL (-?0x[0-9a-fA-F.]+p[-+]?\d+)',body)
        L[name]=F(float.fromhex(mm.group(1))) if mm else F(0)
    return L
def ev(g,x): 
    s=F(0)
    for mon,c in g.items():
        t=c
        for v in mon: t*=x[v]
        s+=t
    return s
model,gdx,cert=sys.argv[1],sys.argv[2],F(sys.argv[3])
eqs,lo,up,pos=parse_gms(model); x=levels(gdx)
vars_=set(v for g,s in eqs.values() for m in g for v in m)
for v in vars_: x.setdefault(v,F(0))
worst=(F(0),None); wb=(F(0),None)
for k,(g,s) in eqs.items():
    val=ev(g,x)
    viol= abs(val) if s=='E' else (max(val,F(0)) if s=='L' else max(-val,F(0)))
    if viol>worst[0]: worst=(viol,k)
for v in vars_:
    if v in lo and x[v]<lo[v] and lo[v]-x[v]>wb[0]: wb=(lo[v]-x[v],v)
    if v in up and x[v]>up[v] and x[v]-up[v]>wb[0]: wb=(x[v]-up[v],v)
# objective from radii via objective row (objvar = const + sum w r)
objrow=[k for k,(g,s) in eqs.items() if ('objvar',) in g][0]; g=eqs[objrow][0]; a=g[('objvar',)]
f=sum(-c/a*x[m[0]] for m,c in g.items() if m and m[0]!='objvar') - g.get((),F(0))/a
print(f"{gdx}: f(r)={float(f):.15g} objvar={float(x['objvar']):.15g} cert-f={float(cert-f):.6e} maxrow={float(worst[0]):.4e} ({worst[1]}) maxbound={float(wb[0]):.4e} ({wb[1]})")
