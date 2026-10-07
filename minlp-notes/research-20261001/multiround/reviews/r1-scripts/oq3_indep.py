# Independent exact check of Proposition 6 (Fractions only) + float LP cross-check with HiGHS (scipy)
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
def run(eps, xis, X, Y, W, R):
    rows=[((-1,0,0),0),((1,0,0),X),((0,-1,0),0),((0,1,0),Y),((0,0,-1),-1),((0,0,1),W)]
    c=(eps,Fr(1),Fr(1)); ok=True
    for r in range(R+1):
        xi, xn = xis[r], xis[r+1]; a = 2/xn
        v=(xi,Fr(0),Fr(1))
        dot=lambda g,p: sum(gi*pi for gi,pi in zip(g,p))
        if any(dot(g,v)>h for g,h in rows): ok=False; print('infeasible',r)
        act=[k for k,(g,h) in enumerate(rows) if dot(g,v)==h]
        if r==0: exp_act=[0,2,4]
        else: exp_act=[2,4,len(rows)-1]
        if sorted(act)!=exp_act: ok=False; print('active',r,act)
        # rays: solve A_act r_j = -e_j by Cramer (3x3)
        A=[rows[k][0] for k in exp_act]
        def det3(M): return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
        D=det3([[Fr(x) for x in row] for row in A]); assert D!=0
        rays=[]
        for j in range(3):
            rhs=[Fr(-1) if i==j else Fr(0) for i in range(3)]
            sol=[]
            for col in range(3):
                M=[[ (rhs[i] if cc==col else Fr(A[i][cc])) for cc in range(3)] for i in range(3)]
                sol.append(det3(M)/D)
            rays.append(sol)
        red=[dot(c,rj) for rj in rays]
        if not all(x>0 for x in red): ok=False; print('dual',r,red)
        Cval=lambda p: p[2]-(a*p[0]+p[1]/a)**2/4
        if not Cval(v)>0: ok=False
        coef=[]
        for rj in rays:
            # Cval(v+t r) = c0 + c1 t + c2 t^2 exactly
            c0=Cval(v); c2=-(a*rj[0]+rj[1]/a)**2/4
            c1=rj[2]-2*(a*v[0]+v[1]/a)*(a*rj[0]+rj[1]/a)/4
            if c2==0:
                coef.append(Fr(0) if c1>=0 else -c1/c0); continue
            # concave, c0>0: unique positive root; find it via rational candidates
            disc=c1*c1-4*c2*c0
            n,d=disc.numerator,disc.denominator
            import math
            sn,sd=math.isqrt(n),math.isqrt(d); assert sn*sn==n and sd*sd==d, 'irrational root'
            s=Fr(sn,sd); roots=[(-c1+s)/(2*c2),(-c1-s)/(2*c2)]
            pos=[t for t in roots if t>0]; assert len(pos)==1
            coef.append(1/pos[0])
        # cut sum coef_j*(b_act - A_act x) >= 1  ->  g x <= h
        g=[sum(coef[j]*A[j][i] for j in range(3)) for i in range(3)]
        h=sum(coef[j]*rows[exp_act[j]][1] for j in range(3))-1
        # expected cut: x/xn + xn*y/4 >= 1 i.e. (-1/xn, -xn/4, 0) x <= -1
        tgt=[-1/xn,-xn/4,Fr(0)]
        lam=-1/h
        if not (h<0 and all(gi*lam==ti for gi,ti in zip(g,tgt))): ok=False; print('cut',r,g,h)
        rows.append((tuple(tgt),-1))
        # float LP crosscheck
        Af=np.array([[float(x) for x in g_] for g_,_ in rows]); bf=np.array([float(h_) for _,h_ in rows])
        res=linprog([float(x) for x in c],A_ub=Af,b_ub=bf,bounds=[(None,None)]*3,method='highs')
        nxt=np.array([float(xn),0,1])
        if np.abs(res.x-nxt).max()>1e-7: ok=False; print('LP float mismatch',r,res.x,nxt)
    return ok, float(1+eps*xis[R+1])
e=Fr(1,4); xis=[2*(1-Fr(1,2**r)) for r in range(42)]
print('eps=1/4:',run(e,xis,10,10,10,40))
e=Fr(1,9); xis=[Fr(11,2)*(1-Fr(1,3**r)) for r in range(32)]  # xi_inf=5.5 < 6
print('eps=1/9 (xi_inf=5.5, z*=1+2/3, limit=1+5.5/9):',run(e,xis,12,1,3,30))
# boundary of hypotheses: X exactly 2/sqrt(eps)=6, Y = sqrt(eps)=1/3
print('eps=1/9, X=6, Y=1/3:',run(e,xis,6,Fr(1,3),2,30))
