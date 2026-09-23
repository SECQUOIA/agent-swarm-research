import sys, math, numpy as np, pandas as pd, scipy.sparse as sp
sys.path.insert(0,'/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/code')
from qcqp import QCQP
import relax, gurobipy as gp
from gurobipy import GRB
from scipy.optimize import linprog
RES='/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/results'
inst=pd.read_csv(RES+'/instances.csv').set_index('name')
env=gp.Env(params={'OutputFlag':0})

def indep_lp(P, lb, ub, U, ntan=5):
    """Independent McCormick LP (scipy/HiGHS): returns function(objvec, sense)->value."""
    n=P.n; terms=list(P.terms); T={}
    col=n
    binsq=lambda i: P.isint[i] and lb[i]>=0 and ub[i]<=1
    for t in terms:
        if t[0]==t[1] and binsq(t[0]): T[t]=t[0]
        else: T[t]=col; col+=1
    N=col
    Aub=[];bub=[];Aeq=[];beq=[]
    def row(d): r=np.zeros(N); [r.__setitem__(k, r[k]+v) for k,v in d.items()]; return r
    for t in terms:
        i,j=t; v=T[t]
        if v==i and i==j: continue
        li,ui,lj,uj=lb[i],ub[i],lb[j],ub[j]
        if i==j:
            for k in range(ntan):
                p=li+(ui-li)*k/(ntan-1)          # v >= 2p x - p^2  ->  2p x - v <= p^2
                Aub.append(row({i:2*p, v:-1})); bub.append(p*p)
            Aub.append(row({v:1, i:-(li+ui)})); bub.append(-li*ui)  # v <= (l+u)x - lu
        else:
            # v >= lj xi + li xj - li lj ; v >= uj xi + ui xj - ui uj
            Aub.append(row({i:lj, j:li, v:-1})); bub.append(li*lj)
            Aub.append(row({i:uj, j:ui, v:-1})); bub.append(ui*uj)
            # v <= uj xi + li xj - li uj ; v <= lj xi + ui xj - ui lj
            Aub.append(row({v:1, i:-uj, j:-li})); bub.append(-li*uj)
            Aub.append(row({v:1, i:-lj, j:-ui})); bub.append(-ui*lj)
    A=P.A.tocsr()
    for r in range(P.m):
        d={}
        for k,a in zip(A.indices[A.indptr[r]:A.indptr[r+1]],A.data[A.indptr[r]:A.indptr[r+1]]): d[k]=d.get(k,0)+a
        for t,q in P.rq.get(r,{}).items(): d[T[t]]=d.get(T[t],0)+q
        rr=row(d); lo,hi=P.rlo[r],P.rhi[r]
        if lo==hi: Aeq.append(rr); beq.append(lo)
        else:
            if hi<math.inf: Aub.append(rr); bub.append(hi)
            if lo>-math.inf: Aub.append(-rr); bub.append(-lo)
    fd={k:P.sense*P.c[k] for k in range(n) if P.c[k]!=0}
    for t,q in P.oq.items(): fd[T[t]]=fd.get(T[t],0)+P.sense*q
    frow=row(fd); fc=P.sense*P.c0
    if math.isfinite(U): Aub.append(frow); bub.append(U-fc)
    bounds=[(lb[k] if lb[k]>-math.inf else None, ub[k] if ub[k]<math.inf else None) for k in range(n)]
    for t in terms:
        if T[t]>=n: bounds.append((0,None) if t[0]==t[1] else (None,None))
    Aub=sp.csr_matrix(np.array(Aub)) if Aub else None; Aeq=sp.csr_matrix(np.array(Aeq)) if Aeq else None
    def solve(c):
        res=linprog(c,A_ub=Aub,b_ub=bub if Aub is not None else None,A_eq=Aeq,b_eq=beq if Aeq is not None else None,bounds=bounds,method='highs')
        return res.fun if res.status==0 else (math.inf if res.status==2 else None)
    return solve, frow, fc, N

def exact_bounds(P, lb, ub, U, k, tl=30):
    m,xs=P.gurobi_model(env, lb, ub); m.Params.NonConvex=2; m.Params.TimeLimit=tl; m.Params.Threads=4
    obj=m.getObjective()
    m.addQConstr(P.sense*obj <= U)
    out=[]
    for sense in (GRB.MINIMIZE,GRB.MAXIMIZE):
        m.setObjective(xs[k]*1.0, sense); m.optimize()
        out.append(m.ObjBound if m.Status in (GRB.OPTIMAL,GRB.TIME_LIMIT) else None)
    m.dispose(); return out

for name in sys.argv[1:]:
    P=QCQP(name); f=np.load(RES+'/fbbt/%s.npz'%name); lb,ub=f['lb'],f['ub']
    fs=inst.loc[name,'fstar_min']; U=fs+1e-6*max(1,abs(fs))
    R=relax.Relaxation(P,lb,ub,env,math.inf); LB,_=R.bound()
    solve,frow,fc,N=indep_lp(P,lb,ub,math.inf)
    LBi=solve(frow)+fc
    print(f'== {name} sense={P.sense} n={P.n} nl={len(P.nlvars)} f*={fs:.6g}  relax LB={LB:.6g} indep LB={LBi:.6g}  LB<=f*: {LB<=fs+1e-6*max(1,abs(fs))}')
    # one Jacobi round without filtering, known cutoff
    RJ=relax.Relaxation(P,lb,ub,env,U); relax.obbt_round(RJ,list(P.nlvars),mode='J',filtering=False)
    solveU,_,_,_=indep_lp(P,lb,ub,U)
    maxdiff=0; worst=None; nt=0; exviol=0
    xref=P.load_sol(fs)
    for k in P.nlvars:
        c=np.zeros(N); c[k]=1
        lo=solveU(c); hi=-solveU(-c)
        # expected from relax (margin, rounding, acceptance threshold)
        for mine,theirs,old in ((lo,RJ.lb[k],lb[k]),(hi,RJ.ub[k],ub[k])):
            if theirs!=old: nt+=1
            if mine is None: continue
            d=abs(mine-theirs)/(1+abs(mine))
            if theirs!=old or abs(mine-old)/(1+abs(old))>1e-3*(ub[k]-lb[k]+1e-9):
                if d>maxdiff: maxdiff=d; worst=(P.names[k],mine,theirs,old)
    print(f'   Jacobi round: {nt} bounds tightened; max rel diff vs independent HiGHS LP = {maxdiff:.2e} {worst if maxdiff>1e-4 else ""}')
    if xref is not None:
        inside=np.all(xref>=RJ.lb-1e-6*(1+abs(xref))) and np.all(xref<=RJ.ub+1e-6*(1+abs(xref)))
        print('   reference solution (fmin=%.6g) inside Jacobi box:'%P.fmin(xref), inside)
    # exact bounds containment for a few variables
    bad=0; tight=[]
    for k in P.nlvars[:12]:
        el,eu=exact_bounds(P,lb,ub,U,k)
        if el is not None and RJ.lb[k]>el+1e-6*(1+abs(el)): bad+=1
        if eu is not None and RJ.ub[k]<eu-1e-6*(1+abs(eu)): bad+=1
        tight.append((P.names[k],round(RJ.lb[k],4),round(el,4) if el is not None else None,round(RJ.ub[k],4),round(eu,4) if eu is not None else None))
    print('   exact-bound containment violations:',bad)
    for t in tight[:6]: print('     ',t)
    # GS round with filtering as used in the experiment vs stored r1 box
    RG=relax.Relaxation(P,lb,ub,env,U); out=relax.iterate(RG,max_rounds=1,w0=None)
    b=np.load(RES+'/boxes/%s__known__r1.npz'%name)
    print('   rerun GS r1 == stored r1 box:', np.allclose(b['lb'],RG.lb,rtol=1e-6,atol=1e-6) and np.allclose(b['ub'],RG.ub,rtol=1e-6,atol=1e-6))
