"""Rational interval/recovery checks with numerical coupled convex QPs."""
from fractions import Fraction as F
import mpmath as mp
import numpy as np
from scipy.optimize import minimize


def sign_term(x):return x*abs(x)


def profiles(q,lower,upper):
    flow=[q+1,q+1,q]
    lo=[l if x>=0 else u for x,l,u in zip(flow,lower,upper)]
    hi=[u if x>=0 else l for x,l,u in zip(flow,lower,upper)]
    return lo,hi


def value(q,beta):return sum(be*sign_term(x) for be,x in zip(beta,[q+1,q+1,q]))


def root_box(lower,upper,maximum,eta):
    left,right=F(-1),F(0)
    while right-left>eta:
        mid=(left+right)/2;lo,hi=profiles(mid,lower,upper)
        h=value(mid,lo if maximum else hi)
        if h==0:return mid,mid
        if h<0:left=mid
        else:right=mid
    return left,right


def physical(beta):
    def mpf(q):return mp.mpf(q.numerator)/q.denominator
    path=mpf(beta[0]+beta[1]);direct=mpf(beta[2])
    return -mp.sqrt(path)/(mp.sqrt(path)+mp.sqrt(direct))


def run():
    mp.mp.dps=90;rng=np.random.default_rng(593402)
    recoveries=frozen=0;worst_loss=0.;worst_bits=0
    for trial in range(12):
        cycles=1+trial%4;m=3*cycles
        lowers=[];uppers=[]
        for j in range(cycles):
            low=[F(int(x),2) for x in rng.integers(1,7,3)]
            width=[F(1,2**80)]*3 if j==0 and trial%2==0 else [F(int(x),4) for x in rng.integers(1,5,3)]
            lowers.append(low);uppers.append([a+b for a,b in zip(low,width)])
        R=rng.integers(-2,3,(m,m)).astype(float);Q=R.T@R;d=rng.integers(-4,5,m).astype(float)
        L=F(1+int(max(abs(d)+3*np.sum(abs(Q),axis=1))))
        epsilon=F(1,1000);eta=min(F(1),epsilon/(16*m*L))
        ell=[];uu=[];wide=[];true_bounds=[]
        for low,up in zip(lowers,uppers):
            lb=root_box(low,up,False,eta);ub=root_box(low,up,True,eta)
            if lb[1]<=ub[0]:ell.append(lb[1]);uu.append(ub[0]);wide.append(True)
            else:ell.append(lb[1]);uu.append(lb[1]);wide.append(False);frozen+=1
            true_bounds.append((float(physical([up[0],up[1],low[2]])),float(physical([low[0],low[1],up[2]]))))
        Z=np.zeros((m,cycles));x0=np.zeros(m)
        for j in range(cycles):Z[3*j:3*j+3,j]=1;x0[3*j:3*j+2]=1
        def cost(q):
            x=x0+Z@q;return .5*x@Q@x+d@x
        def grad(q):return Z.T@(Q@(x0+Z@q)+d)
        bounds=list(zip(map(float,ell),map(float,uu)))
        start=np.array([(a+b)/2 for a,b in bounds])
        result=minimize(cost,start,jac=grad,bounds=bounds,method='L-BFGS-B',options={'ftol':1e-15,'gtol':1e-12,'maxiter':2000})
        q_rat=[min(u,max(l,F(float(q)).limit_denominator(2**45))) for q,l,u in zip(result.x,ell,uu)]
        recovered=[]
        for q,low,up,is_wide in zip(q_rat,lowers,uppers,wide):
            if is_wide:
                lo,hi=profiles(q,low,up);hlo,hhi=value(q,lo),value(q,hi)
                assert hlo<=0<=hhi
                lam=-hlo/(hhi-hlo) if hhi!=hlo else F(0)
                beta=[a+lam*(b-a) for a,b in zip(lo,hi)]
                assert value(q,beta)==0
                assert abs(physical(beta)-mp.mpf(q.numerator)/q.denominator)<mp.mpf('1e-75')
                recoveries+=1
            else:beta=[up[0],up[1],low[2]]
            assert all(l<=b<=u for l,b,u in zip(low,beta,up))
            for b in beta:worst_bits=max(worst_bits,b.numerator.bit_length()+b.denominator.bit_length())
            recovered.append(float(physical(beta)))
        ref=minimize(cost,np.array([(a+b)/2 for a,b in true_bounds]),jac=grad,bounds=true_bounds,
                     method='L-BFGS-B',options={'ftol':1e-15,'gtol':1e-12,'maxiter':2000})
        loss=cost(np.array(recovered))-ref.fun;worst_loss=max(worst_loss,loss)
        assert loss<float(epsilon)
        assert np.sum(abs(Z@(np.array(recovered)-np.array(list(map(float,q_rat))))))<=m*float(eta)+1e-12
    print('PASS: 12 coupled convex QPs;',recoveries,'exact rational cycle recoveries;',frozen,'narrow frozen cycles')
    print('Largest observed reference loss',worst_loss,'largest resistance numerator+denominator bits',worst_bits)


if __name__=='__main__':run()
