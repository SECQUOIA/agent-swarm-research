import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np, rb
rng=np.random.default_rng(1)
def psi(g,l):
    if g*l>=-2: return l*l/4
    return -(1+g*l)/(g*g)
def inB_closed(X,s):
    f1,f2,f3,f4 = X[0,0],X[0,1],X[1,0],X[1,1]
    d = f1*f4-f2*f3
    if d<=0: return None
    Xn = X/np.sqrt(d)
    f1,f2,f3,f4 = Xn[0,0],Xn[0,1],Xn[1,0],Xn[1,1]
    x,y,w = s
    qs = w-x*y; l = f1*x-f4*y-f3*w+f2; a22 = f3*x+f4
    return (a22>=0) and (qs-psi(f3,l)>=0), a22, qs-psi(f3,l)
bad=0;n=0
for k in range(20000):
    X=rng.normal(size=(2,2))
    if np.linalg.det(X)<=0: X[:,0]*=-1
    s=rng.normal(size=3)*rng.choice([0.5,2,5])
    r=inB_closed(X,s)
    a=rb.in_B_X(X,s,tol=1e-12)
    if r[0]!=a:
        if abs(r[1])>1e-6 and abs(r[2])>1e-6:
            bad+=1
            if bad<5: print(X,s,r,a)
    n+=1
print('n',n,'mismatch (non-borderline)',bad)
