# Scan MINLPLib OSIL files for rows y = x^k (k=2,3) whose decimal bounds are consistent at a bound
# (lb(y) = lb(x)^k or ub(y) = ub(x)^k exactly) but inconsistent after binary64 rounding:
#   fl(lb x)^k < fl(lb y)  (lower)   or   fl(ub x)^k > fl(ub y)  (upper).
# This is the data pattern behind the traced SCIP cutoff; it is necessary, not sufficient, for that defect.
import sys, os, glob, time
import xml.etree.ElementTree as ET
from fractions import Fraction as F
ns='{os.optimizationservices.org}'
INF=None
def expand(parent):
    out=[]
    for el in parent:
        mult=int(el.get('mult','1')); incr=el.get('incr')
        v=el.text.strip()
        if incr is None: out.extend([v]*mult)
        else:
            x=F(v); d=F(incr)
            for i in range(mult): out.append(str(x+i*d))
    return out
def scan(path):
    vars_=[]; cons=[]; start=colidx=vals=None; nls={}; qt={}; nlrows=set()
    for ev,el in ET.iterparse(path,events=('end',)):
        tag=el.tag.replace(ns,'')
        if tag=='var':
            m=int(el.get('mult','1'))
            for _ in range(m): vars_.append((el.get('lb','0'),el.get('ub','INF'),el.get('name')))
        elif tag=='con':
            m=int(el.get('mult','1'))
            for _ in range(m): cons.append((el.get('lb'),el.get('ub'),el.get('constant','0'),el.get('name')))
        elif tag=='start': start=[int(x) for x in expand(el)]
        elif tag in('colIdx','rowIdx'): colidx=(tag,[int(x) for x in expand(el)])
        elif tag=='value' and el.find(f'{ns}el') is not None and start is not None: vals=expand(el)
        elif tag=='qTerm':
            k=int(el.get('idx'))
            if k>=0: qt.setdefault(k,[]).append((int(el.get('idxOne')),int(el.get('idxTwo')),F(el.get('coef','1'))))
            el.clear()
        elif tag=='nl':
            k=int(el.get('idx'))
            if k>=0: nlrows.add(k)
            if k>=0:
                ch=list(el)
                if len(ch)==1:
                    e=ch[0]; t=e.tag.replace(ns,''); pat=None
                    if t=='power':
                        a,b=list(e)
                        if a.tag==ns+'variable' and b.tag==ns+'number' and b.get('value') in('2','3','2.0','3.0'):
                            pat=(int(a.get('idx')),F(a.get('coef','1')),int(float(b.get('value'))))
                    elif t=='square':
                        a=list(e)[0]
                        if a.tag==ns+'variable': pat=(int(a.get('idx')),F(a.get('coef','1')),2)
                    elif t=='product':
                        cs=list(e)
                        if all(c.tag==ns+'variable' for c in cs) and len({c.get('idx') for c in cs})==1 and len(cs) in(2,3):
                            co=F(1)
                            for c in cs: co*=F(c.get('coef','1'))
                            pat=(int(cs[0].get('idx')),co,len(cs))
                    if pat: nls[k]=pat
            el.clear()
        elif tag in('variables','constraints','linearConstraintCoefficients','nonlinearExpressions'):
            pass
        if tag in('linearConstraintCoefficients',): el.clear()
    for k,terms in qt.items():
        if len(terms)==1 and terms[0][0]==terms[0][1] and k not in nlrows:
            nls[k]=(terms[0][0],terms[0][2],2)
        elif k in nls: del nls[k]          # mixed quadratic + nl rows: skip
    if not nls: return []
    # row-wise linear part
    lin={}
    if colidx and colidx[0]=='colIdx' and start is not None:
        for r in range(len(start)-1):
            if r in nls:
                lin[r]=[(colidx[1][j],F(vals[j])) for j in range(start[r],start[r+1])]
    elif colidx and start is not None:   # column-wise
        for c in range(len(start)-1):
            for j in range(start[c],start[c+1]):
                r=colidx[1][j]
                if r in nls: lin.setdefault(r,[]).append((c,F(vals[j])))
    hits=[]
    for r,(x,co,k) in nls.items():
        L=lin.get(r,[])
        if len(L)!=1: continue
        y,a=L[0]
        lb,ub,const,cname=cons[r]
        if lb is None or ub is None or F(lb)!=F(ub) or F(lb)-F(const)!=0: continue
        if co/a!=-1: continue   # need y = x^k exactly
        xl,xu,xn=vars_[x]; yl,yu,yn=vars_[y]
        for side,(bx,by) in (('lb',(xl,yl)),('ub',(xu,yu))):
            if bx in('INF','-INF') or by in('INF','-INF'): continue
            Bx=F(bx); By=F(by)
            if Bx<=0 or Bx**k!=By: continue
            res=F(float(bx))**k-F(float(by))
            bad=(res<0) if side=='lb' else (res>0)
            hits.append((cname,xn,yn,k,side,bx,by,float(res),bad))
    return hits
if __name__=='__main__':
    files=sorted(glob.glob(os.path.expanduser('~/.cache/minlplib/minlplib/osil/*.osil')))
    t0=time.time(); n=0
    for f in files:
        try: h=scan(f)
        except Exception as e: print('ERR',os.path.basename(f),repr(e)[:120],flush=True); continue
        n+=1
        if h:
            bad=[x for x in h if x[-1]]
            print(f"{os.path.basename(f)[:-5]}: candidate rows {len(h)}, binary64-inconsistent {len(bad)}; L values {sorted({(x[4],x[5],x[3]) for x in bad})}",flush=True)
    print('scanned',n,'files in %.0f s'%(time.time()-t0))
