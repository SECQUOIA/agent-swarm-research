import numpy as np, scipy.sparse as sp, clarabel, time
from sparse_bb import Relaxation, instance

def solve_clarabel(X, y, lam, k, S0, S1):
    """Perspective relaxation at a node via Clarabel. Variables: beta_A (A=S1 u F), z_F, t_F.
    min ||y - X_A beta||^2 + lam*||beta_S1||^2 + lam*sum t_F
    s.t. (t_i + z_i, 2 beta_i, t_i - z_i) in SOC  (i in F);  0<=z_F<=1; sum z_F <= k'."""
    n,p = X.shape
    S0=set(S0); S1=list(S1)
    F=[i for i in range(p) if i not in S0 and i not in S1]
    kp=k-len(S1)
    A = S1+F; na=len(A); nf=len(F)
    XA=X[:,A]
    # variable order: beta (na), z (nf), t (nf)
    N = na+2*nf
    P = np.zeros((N,N))
    P[:na,:na] = 2*(XA.T@XA)
    for j in range(len(S1)): P[j,j]+=2*lam
    q = np.zeros(N); q[:na] = -2*XA.T@y; q[na+nf:] = lam
    rows=[]; b=[]
    # nonneg cone: z>=0 -> -z <= 0 ; z<=1 ; sum z <= k'
    Ablocks=[]
    Az = sp.lil_matrix((2*nf+1, N)); bz=np.zeros(2*nf+1)
    for j in range(nf):
        Az[j, na+j] = -1.0; bz[j]=0
        Az[nf+j, na+j] = 1.0; bz[nf+j]=1
        Az[2*nf, na+j] = 1.0
    bz[2*nf]=kp
    # SOC: s = b - A x in SOC(3): s = (t+z, 2beta, t-z)
    Ac = sp.lil_matrix((3*nf, N)); bc=np.zeros(3*nf)
    for j in range(nf):
        bi = len(S1)+j; zi = na+j; ti = na+nf+j
        Ac[3*j, ti] = -1; Ac[3*j, zi] = -1
        Ac[3*j+1, bi] = -2
        Ac[3*j+2, ti] = -1; Ac[3*j+2, zi] = 1
    Amat = sp.vstack([Az.tocsc(), Ac.tocsc()]).tocsc()
    bvec = np.concatenate([bz,bc])
    cones=[clarabel.NonnegativeConeT(2*nf+1)]+[clarabel.SecondOrderConeT(3) for _ in range(nf)]
    s=clarabel.DefaultSettings(); s.verbose=False
    s.tol_gap_abs=1e-10; s.tol_gap_rel=1e-10; s.tol_feas=1e-10
    solver=clarabel.DefaultSolver(sp.triu(sp.csc_matrix(P)).tocsc(), q, Amat, bvec, cones, s)
    sol=solver.solve()
    x=np.array(sol.x)
    z=np.zeros(p); z[S1]=1; z[F]=x[na:na+nf]
    return sol.obj_val + y@y, np.clip(z,0,1)

rng=np.random.default_rng(3)
for trial in range(5):
    n,p,k=40,60,6
    X,y,lam,Ss=instance(n,p,k,seed=trial,sigma=0.5)
    S0=tuple(rng.choice(p,3,replace=False).tolist()); S1=()
    R=Relaxation(X,y,lam,k)
    t0=time.time(); LB,val,z=R.solve(S0,S1); t1=time.time()
    v,zc=solve_clarabel(X,y,lam,k,S0,S1); t2=time.time()
    # FW bound from clarabel z
    f,g=R.g_grad(zc)
    print("fista LB %.8f val %.8f (%.0fms) | clarabel %.8f g(z)=%.8f (%.0fms)"%(LB,val,1e3*(t1-t0),v,f,1e3*(t2-t1)))
