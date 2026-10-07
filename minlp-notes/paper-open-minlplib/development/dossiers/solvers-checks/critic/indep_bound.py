# Independent third implementation (critic): sympy parsing, presence check of required rows.
import re,sys,time
import sympy as sp
from fractions import Fraction as F
sys.set_int_max_str_digits(0)
def load(fn):
    txt=open(fn).read()
    assert re.search(r'Solve m using %\w+% minimizing objvar;',txt)
    names=re.findall(r'\b(objvar|x\d+)\b',txt.split('Equations')[0])
    syms={n:sp.Symbol(n) for n in set(names)}
    loc=dict(syms); loc['sqr']=lambda e:e**2
    rows={}
    for m in re.finditer(r'^(e\d+)\.\.(.*?);',txt,re.S|re.M):
        nm,body=m.groups()
        l,s,r=re.match(r'(.*)=([ELG])=(.*)$',body.replace('\n',' '),re.S).groups()
        ex=sp.expand(sp.parse_expr(l,local_dict=loc,transformations=sp.parsing.sympy_parser.standard_transformations+(sp.parsing.sympy_parser.rationalize,))-sp.parse_expr(r,local_dict=loc,transformations=sp.parsing.sympy_parser.standard_transformations+(sp.parsing.sympy_parser.rationalize,)))
        if s=='G': ex=-ex; s='L'
        d={}
        for term,coef in ex.as_coefficients_dict().items():
            key=tuple(sorted(str(f) for f in sp.Mul.make_args(term) for _ in range(1) ) ) if term!=1 else ()
            # expand powers
            kk=[]
            for f in sp.Mul.make_args(term):
                if f==1: continue
                b,e=f.as_base_exp(); kk+= [str(b)]*int(e)
            key=tuple(sorted(kk))
            d[key]=F(int(sp.Rational(coef).p),int(sp.Rational(coef).q))
        rows[nm]=(s,d)
    lo={};up={}
    for m in re.finditer(r'\b(\w+)\.(lo|up|fx)\s*=\s*([-+]?[\d.]+(?:[eE][+-]?\d+)?)\s*;',txt):
        v,k,val=m.group(1),m.group(2),F(m.group(3))
        if k in('lo','fx'): lo[v]=val
        if k in('up','fx'): up[v]=val
    return rows,lo,up
def find(rows,s,d):
    for nm,(ss,dd) in rows.items():
        if ss==s and dd==d: return nm
    return None
def run(fn):
    t=time.time()
    rows,lo,up=load(fn)
    # objective: E row containing objvar with coefficient -1 or +1, others radii with equal negative weight
    obj=[nm for nm,(s,d) in rows.items() if ('objvar',) in d]; assert len(obj)==1
    s,d=rows[obj[0]]; assert s=='E'
    a=d[('objvar',)]
    radii=[k[0] for k in d if k!=('objvar',)]
    assert all(len(k)==1 for k in d) and () not in d
    w={v:-d[(v,)]/a for v in radii}   # objvar = sum w_v v
    assert all(x<0 for x in w.values())
    # chain order via slope rows: E rows {ri:+-1, rj:-+1, dv:+-1}
    R=set(radii); slope={}
    for nm,(s,dd) in rows.items():
        if s!='E' or nm==obj[0]: continue
        ks=list(dd)
        if len(ks)==3 and all(len(k)==1 for k in ks):
            rv=[k[0] for k in ks if k[0] in R]; dv=[k[0] for k in ks if k[0] not in R]
            if len(rv)==2 and len(dv)==1 and dd[(rv[0],)]==-dd[(rv[1],)] and abs(dd[(rv[0],)])==1 and abs(dd[(dv[0],)])==1:
                slope[frozenset(rv)]=dv[0]
    # endpoint r1: radius with ub < 2 among chain ends
    deg={v:0 for v in R}
    for p in slope:
        for v in p: deg[v]+=1
    ends=[v for v in R if deg[v]==1]; assert len(ends)==2
    # identify r1 via the existence of the C1 row: c*r2 - r1*r2 - r1 <=0
    nb={v:[u for p in slope if v in p for u in p if u!=v] for v in R}
    chosen=None
    for e in ends:
        r2=nb[e][0]
        for nm,(s,dd) in rows.items():
            if s=='L' and set(dd)=={tuple(sorted((e,r2))),(e,),(r2,)} and dd[tuple(sorted((e,r2)))]==-1 and dd[(e,)]==-1:
                chosen=(e,r2,dd[(r2,)],nm)
    assert chosen; r1,r2,c,c1row=chosen
    order=[r1,r2]
    while len(order)<len(R):
        nxt=[u for u in nb[order[-1]] if u!=order[-2]]; assert len(nxt)==1; order.append(nxt[0])
    n=len(order)
    # presence check of C_j for j=2..n-1 with the same c
    for j in range(2,n):
        a_,b_,c_=order[j-2],order[j-1],order[j]
        want={tuple(sorted((a_,c_))):c, tuple(sorted((a_,b_))):F(-1), tuple(sorted((b_,c_))):F(-1)}
        assert find(rows,'L',want) is not None,(j,)
    lb=[lo[v] for v in order]; ub=[up[v] for v in order]
    assert all(x>=1 for x in lb)
    alpha=[]
    for j in range(n-1):
        dv=slope[frozenset((order[j],order[j+1]))]
        if dv in up or dv in lo:
            assert lo[dv]==-up[dv]; alpha.append(up[dv])
        else: alpha.append(None)
    # u_j=1/r_j ; u_0=1 ; u_{j-1}-c u_j+u_{j+1}>=0 ; lower bounds L_j on u_j
    L=[F(1),1/ub[0]]
    for j in range(1,n): L.append(c*L[j]-L[j-1])
    # check monotone nonneg Chebyshev weights up to n-1
    Uq=[F(1),c]
    for m in range(2,n): Uq.append(c*Uq[-1]-Uq[-2])
    assert min(Uq)>=0
    E=[]
    for j in range(1,n+1):
        if L[j]>0:
            q=1/L[j]
            # round up to 1e-30 grid
            Q=10**30; qq=F(-((-q.numerator*Q)//q.denominator),Q)
            E.append(min(ub[j-1],qq))
        else: E.append(ub[j-1])
    # shortest-path smoothing with slopes (full Bellman-Ford style, repeat to convergence)
    changed=True
    while changed:
        changed=False
        for j in range(n-1):
            if alpha[j] is None: continue
            if E[j]+alpha[j]<E[j+1]: E[j+1]=E[j]+alpha[j]; changed=True
            if E[j+1]+alpha[j]<E[j]: E[j]=E[j+1]+alpha[j]; changed=True
    val=sum(w[order[j]]*E[j] for j in range(n))
    print(fn,'n',n,'c',float(c),'C1row',c1row,'bound %.17g'%float(val),'floor-digits',val.numerator*10**20//val.denominator,'%.1fs'%(time.time()-t),flush=True)
for f in sys.argv[1:]: run(f)
