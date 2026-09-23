import numpy as np  # noqa: consolidated regime checks: degenerate vertex, SDP face, curved disk
# degenerate vertex: min x3+x4+x5 s.t. x1+x4=1, x2+x5=1, x1+x2+2x3=2, x>=0
# optimum x*=(1,1,0,0,0), supp B={1,2} size 2 < m=3 -> primal degenerate vertex, dim(face)=0
c = np.array([0.,0.,1.,1.,1.])
A = np.array([[1.,0.,0.,1.,0.],
              [0.,1.,0.,0.,1.],
              [1.,1.,2.,0.,0.]])
b = np.array([1.,1.,2.])
print("rank A:", np.linalg.matrix_rank(A))
_,_,Vt = np.linalg.svd(A); Z = Vt[3:].T
x0 = np.array([0.5,0.5,0.5,0.5,0.5])
print("feasible start check:", A@x0 - b)
# fix start: solve for feasible interior point: x1=x2=t, x4=x5=1-t, x3=(2-2t)/2=1-t
t=0.6; x0=np.array([t,t,1-t,1-t,1-t]); print("start resid:", A@x0-b)
def central(mu, iters=400):
    x = x0.copy()
    for _ in range(iters):
        g = Z.T@(c - mu/x)
        H = Z.T@np.diag(mu/x**2)@Z
        d = np.linalg.solve(H,-g)
        lam = np.sqrt(d@H@d); step = 1.0 if lam<0.25 else 1/(1+lam)
        while np.any(x+step*(Z@d)<=0): step*=0.5
        x = x+step*(Z@d)
        if lam<1e-13: break
    return x
for mu in [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7]:
    x = central(mu)
    H = Z.T@np.diag(1/x**2)@Z
    w = np.linalg.eigvalsh(H)
    s = c - A.T@np.linalg.lstsq(np.diag(x)@A.T, np.diag(x)@c, rcond=None)[0] if False else mu/x
    print(f"mu={mu:.0e} x={np.round(x,6)} kappa={w[-1]/w[0]:.4f} s_N={np.round((mu/x)[2:],5)}")
import numpy as np  # noqa: consolidated regime checks: degenerate vertex, SDP face, curved disk
# SDP: min <C,X> over X psd, tr X = 1, C = diag(0,0,1).
# Optimal face = {X psd, X_3.=0, tr=1} = 2x2 trace-1 spectrahedron, dim 3-1=... (2x2 sym: 3 params, tr=1 -> 2) >= 1.
# Parameterize symmetric X by svec (6 coords), slice: tr X = 1 (1 constraint) -> V is 5-dim.
import itertools
idx = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def mat(v):
    X = np.zeros((3,3))
    for t,(i,j) in enumerate(idx):
        if i==j: X[i,i]=v[t]
        else: X[i,j]=X[j,i]=v[t]/np.sqrt(2)
    return X
def svec(X):
    return np.array([X[0,0],X[1,1],X[2,2],np.sqrt(2)*X[0,1],np.sqrt(2)*X[0,2],np.sqrt(2)*X[1,2]])
C = np.diag([0.,0.,1.]); c = svec(C)
A = svec(np.eye(3)).reshape(1,-1)  # trace
_,_,Vt = np.linalg.svd(A); Z = Vt[1:].T  # 6x5

def F_logdet(v):
    X = mat(v); return -np.linalg.slogdet(X)[1]
def barrier_grad_hess(v, extra=False):
    # numeric grad/hess of F = -logdet X  (+ optionally -log(1-X33))
    n = 6; h = 1e-5
    def F(v):
        X = mat(v); val = -np.linalg.slogdet(X)[1]
        if extra: val += -np.log(1.0 - X[2,2])
        return val
    g = np.zeros(n); H = np.zeros((n,n))
    for a in range(n):
        ea = np.zeros(n); ea[a]=h
        g[a] = (F(v+ea)-F(v-ea))/(2*h)
    for a in range(n):
        for b in range(a,n):
            ea=np.zeros(n); eb=np.zeros(n); ea[a]=h; eb[b]=h
            H[a,b]=H[b,a]=(F(v+ea+eb)-F(v+ea-eb)-F(v-ea+eb)+F(v-ea-eb))/(4*h*h)
    return g,H

for name, extra in [("-logdet (nu=3)", False), ("-logdet - log(1-X33) (nu=4)", True)]:
    print(f"\nbarrier: {name}")
    v = svec(np.eye(3)/3)
    for mu in [1e-1,1e-2,1e-3,1e-4]:
        for _ in range(300):
            g,H = barrier_grad_hess(v, extra)
            gr = Z.T@(c + mu*g); Hr = Z.T@(mu*H)@Z
            d = np.linalg.solve(Hr,-gr)
            lam = np.sqrt(max(d@Hr@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
            while True:
                vn = v + step*(Z@d); X = mat(vn)
                if np.all(np.linalg.eigvalsh(X)>0) and (not extra or X[2,2]<1): break
                step*=0.5
            v = vn
            if lam<1e-9: break
        g,H = barrier_grad_hess(v, extra)
        Hr = Z.T@H@Z; w = np.linalg.eigvalsh(Hr)
        X = mat(v)
        print(f"  mu={mu:.0e} X33={X[2,2]:.3e} kappa_red={w[-1]/w[0]:.4e} kappa*mu^2={w[-1]/w[0]*mu*mu:.4f}")
import numpy as np  # noqa: consolidated regime checks: degenerate vertex, SDP face, curved disk
# P = unit disk, min x1. Unique optimum (-1,0), boundary curved.
# F = -log(1 - x1^2 - x2^2). Chord law predicts kappa = Theta(1/mu) for every barrier.
def gh(v):
    x,y = v; r2 = x*x+y*y; d = 1-r2
    g = np.array([2*x/d, 2*y/d])
    H = np.array([[2/d + 4*x*x/d**2, 4*x*y/d**2],[4*x*y/d**2, 2/d + 4*y*y/d**2]])
    return g,H
c = np.array([1.0,0.0])
v = np.array([0.0,0.0])
for mu in [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6]:
    for _ in range(500):
        g,H = gh(v)
        gr = c + mu*g; Hr = mu*H
        d = np.linalg.solve(Hr,-gr)
        lam = np.sqrt(d@Hr@d); step = 1.0 if lam<0.25 else 1/(1+lam)
        while np.sum((v+step*d)**2)>=1: step*=0.5
        v = v+step*d
        if lam<1e-13: break
    g,H = gh(v)
    w = np.linalg.eigvalsh(H)
    gap = c@v - (-1.0)
    print(f"mu={mu:.0e} x={v[0]:.6f} gap={gap:.3e} kappa={w[-1]/w[0]:.4e} kappa*mu={w[-1]/w[0]*mu:.4f}")
import numpy as np
# SDP: min <C,X>, tr X=1, X psd, C=diag(0,1,2). Unique optimum X*=e1e1^T (rank 1, dim face = 0).
# log-det central path is explicit: X(mu) = mu*(C - lam I)^{-1} normalized... actually
# minimize <C,X> + mu*(-logdet X) s.t. trX=1 -> C - mu X^{-1} = lam I -> X = mu (C - lam I)^{-1}.
from scipy.optimize import brentq
C = np.diag([0.,1.,2.])
for mu in [1e-1,1e-2,1e-3,1e-4,1e-5]:
    f = lambda lam: mu*np.sum(1.0/(np.diag(C)-lam)) - 1.0
    lam = brentq(f, -1e8, -1e-12)
    d = mu/(np.diag(C)-lam)   # eigenvalues of X(mu)
    # reduced Hessian of -logdet on {trace 0}: eigen dirs: off-diag (i,j): 1/(d_i d_j);
    # diagonal traceless block: matrix Q = diag(1/d^2) restricted to sum=0
    offs = [1/(d[i]*d[j]) for i in range(3) for j in range(i+1,3)]
    D2 = np.diag(1/d**2)
    # restrict to traceless diagonal directions
    B = np.array([[1,-1,0],[1,1,-2]]).T.astype(float)
    B,_ = np.linalg.qr(B)
    W = np.linalg.eigvalsh(B.T@D2@B)
    evs = np.array(offs + list(W))
    print(f"mu={mu:.0e} X_eigs={np.round(d,5)} kappa_red={evs.max()/evs.min():.3e} kappa*mu^2={evs.max()/evs.min()*mu**2:.4f}")
import numpy as np
# min X22 s.t. tr X = 1, X33 - X12 = 0, X psd (3x3).
# Optimum X* = e1 e1^T unique. Error-bound chain: X22<=g => |X12|<=sqrt(g) => X33<=sqrt(g) => |X13|<=g^{1/4}.
# Chord law predicts kappa_red >= ~ (g^{1/4}/g)^2 = g^{-3/2} for EVERY barrier; test log-det.
idx = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def mat(v):
    X = np.zeros((3,3))
    for t,(i,j) in enumerate(idx):
        if i==j: X[i,i]=v[t]
        else: X[i,j]=X[j,i]=v[t]/np.sqrt(2)
    return X
def svec(X):
    return np.array([X[0,0],X[1,1],X[2,2],np.sqrt(2)*X[0,1],np.sqrt(2)*X[0,2],np.sqrt(2)*X[1,2]])
C = np.zeros((3,3)); C[1,1]=1.0; c = svec(C)
A1 = svec(np.eye(3))
M2 = np.zeros((3,3)); M2[2,2]=1.0; M2[0,1]=M2[1,0]=-0.5
A2 = svec(M2)
A = np.vstack([A1,A2])
_,_,Vt = np.linalg.svd(A); Z = Vt[2:].T  # 6x4
def F(v):
    X = mat(v); s,ld = np.linalg.slogdet(X)
    return -ld if s>0 else np.inf
def gh(v):
    n=6; h=1e-6
    g=np.zeros(n); H=np.zeros((n,n))
    for a in range(n):
        ea=np.zeros(n); ea[a]=h
        g[a]=(F(v+ea)-F(v-ea))/(2*h)
    for a in range(n):
        for b in range(a,n):
            ea=np.zeros(n); eb=np.zeros(n); ea[a]=h; eb[b]=h
            H[a,b]=H[b,a]=(F(v+ea+eb)-F(v+ea-eb)-F(v-ea+eb)+F(v-ea-eb))/(4*h*h)
    return g,H
# feasible start: X = I/3 satisfies X33 - X12 = 1/3 != 0 -> need feasible interior point.
# Find one: X = diag(a,b,c) + x12 sym: want c = x12, trace 1, psd. Take x12=0.2, c=0.2, a=b=0.4.
X0 = np.array([[0.4,0.2,0.0],[0.2,0.4,0.0],[0.0,0.0,0.2]])
print("check:", np.trace(X0), X0[2,2]-X0[0,1], np.linalg.eigvalsh(X0))
v = svec(X0)
print("resid:", A@v - np.array([1.0,0.0]))
for mu in [1e-1,3e-2,1e-2,3e-3,1e-3,3e-4,1e-4]:
    for _ in range(400):
        g,H = gh(v)
        gr = Z.T@(c + mu*g); Hr = Z.T@(mu*H)@Z
        try: d = np.linalg.solve(Hr,-gr)
        except np.linalg.LinAlgError: break
        lam = np.sqrt(max(d@Hr@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
        while True:
            vn = v + step*(Z@d)
            if np.all(np.linalg.eigvalsh(mat(vn))>1e-14): break
            step*=0.5
            if step<1e-16: break
        v = vn
        if lam<1e-8: break
    g,H = gh(v)
    Hr = Z.T@H@Z; w = np.linalg.eigvalsh(Hr)
    X = mat(v); gap = X[1,1]
    k = w[-1]/w[0]
    print(f"mu={mu:.0e} gap={gap:.3e} X13={X[0,2]:.3e} kappa={k:.3e} k*mu^1.5={k*mu**1.5:.4f} k*mu^2={k*mu**2:.5f} k*mu={k*mu:.2f}")
import numpy as np
# min x3 + theta*x2 on simplex slice: unique vertex optimum (1,0,0), but face {x3=0} is theta-nearly optimal.
# Chord law: D(g) ~ min(g/theta-ish, const) -> kappa ~ (D(g)/g)^2: 1/g^2 growth until g~theta, then plateau ~1/theta^2.
A = np.array([[1.,1.,1.]]); b=np.array([1.])
_,_,Vt = np.linalg.svd(A); Z = Vt[1:].T
for theta in [1e-2, 1e-3]:
    c = np.array([0., theta, 1.])
    x = np.ones(3)/3
    print(f"theta={theta:.0e}")
    for mu in [1e-1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7]:
        for _ in range(600):
            g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
            d = np.linalg.solve(H,-g)
            lam = np.sqrt(d@H@d); step = 1.0 if lam<0.25 else 1/(1+lam)
            while np.any(x+step*(Z@d)<=0): step*=0.5
            x = x+step*(Z@d)
            if lam<1e-13: break
        H = Z.T@np.diag(1/x**2)@Z
        w = np.linalg.eigvalsh(H)
        gap = c@x
        k = w[-1]/w[0]
        print(f"  mu={mu:.0e} gap={gap:.2e} kappa={k:.3e} kappa*gap^2={k*gap*gap:.3f} kappa*theta^2={k*theta*theta:.3f}")
