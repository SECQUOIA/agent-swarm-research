import re,sys
from fractions import Fraction as F
def parse(fn):
    txt=open(fn).read()
    # equations
    body=txt.split('Model m')[0]
    eqs={}
    for m in re.finditer(r'^(e\d+)\.\.(.*?);',body,re.S|re.M):
        name=m.group(1); s=m.group(2).replace('\n',' ')
        mm=re.match(r'(.*)=([ELG])=(.*)',s)
        eqs[name]=(mm.group(1),mm.group(2),mm.group(3))
    lo={};up={}
    for m in re.finditer(r'(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+);',txt):
        v,k,val=m.groups()
        if k=='lo': lo[v]=F(val)
        elif k=='up': up[v]=F(val)
        else: lo[v]=up[v]=F(val)
    return eqs,lo,up
def pyexpr(e):
    e=re.sub(r'(?<![\w.])(\d+\.\d*|\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',lambda m:"F('%s')"%m.group(0),e)
    e=e.replace('sqr(','SQ(')
    return e
def SQ(a): return a*a
def evaluate(fn,solfn):
    eqs,lo,up=parse(fn)
    x={}
    for line in open(solfn):
        p=line.split()
        if len(p)==2: x[p[0]]=F(p[1])
    names=set(re.findall(r'\b(objvar|x\d+)\b',open(fn).read()))
    for n in names: x.setdefault(n,F(0))
    env=dict(x); env['F']=F; env['SQ']=SQ
    maxrow=(F(0),None)
    for name,(l,sense,r) in eqs.items():
        val=eval(pyexpr(l),env)-eval(pyexpr(r),env)
        viol = abs(val) if sense=='E' else (max(val,0) if sense=='L' else max(-val,0))
        if viol>maxrow[0]: maxrow=(viol,name)
    maxb=(F(0),None)
    for n in names:
        if n in lo and x[n]<lo[n] and lo[n]-x[n]>maxb[0]: maxb=(lo[n]-x[n],n)
        if n in up and x[n]>up[n] and x[n]-up[n]>maxb[0]: maxb=(x[n]-up[n],n)
    # objective from radii via e1: objvar + coeff*sum ... compute f(r)= value of objvar making e1 hold
    l,sense,r=eqs['e1']
    env2=dict(env); env2['objvar']=F(0)
    rest=eval(pyexpr(l),env2)-eval(pyexpr(r),env2)  # -objvar + rest =0 -> objvar = rest
    # check sign of objvar in e1
    env3=dict(env2); env3['objvar']=F(1)
    coef=eval(pyexpr(l),env3)-eval(pyexpr(r),env3)-rest
    fr=-rest/coef
    return x['objvar'],fr,maxrow,maxb
for g,s,b in [('QPLIB_2738.gms','QPLIB_2738.sol','-42841462678046116050206603'),('QPLIB_2480.gms','QPLIB_2480.sol','-42784904096736785827885646'),('QPLIB_2703.gms','QPLIB_2703.sol','-42756507125126529040486306'),('QPLIB_3177.gms','QPLIB_3177.sol','-42741871514717433905843708')]:
    ov,fr,mr,mb=evaluate(g,s)
    B=F(int(b),10**25)
    print(g,'objvar',float(ov),'f(r)=%.17g'%float(fr),'bound',float(B),'bound-f(r)=%.4g'%float(B-fr),'bound-objvar=%.4g'%float(B-ov),'maxrow %.4g %s'%(float(mr[0]),mr[1]),'maxbound %.4g %s'%(float(mb[0]),mb[1]))
