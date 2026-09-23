import numpy as np
def deltas(n=64, a0=1.0, mu0=0.01, rho=(1.0,3.0,1.0), T=260):
    tau=a0/np.sqrt(n)
    A=np.zeros((1,n)); A[0,:3]=1.0
    Q,_=np.linalg.qr(np.array([[1.,-1.,0.],[1.,1.,-2.]]).T)
    V=np.zeros((n,n-1)); V[:3,:2]=Q; V[3:,2:]=np.eye(n-3)
    u=[np.array([1.,-1.,0.])/np.sqrt(2),np.array([0.,1.,-1.])/np.sqrt(2),np.array([-1.,0.,1.])/np.sqrt(2)]
    mus=[mu0*(1-tau)**t for t in range(T+2)]
    ds=[rho[t%3]*mus[t] for t in range(T+2)]
    psis=[];Ms=[]
    for t in range(T+1):
        j=t%3
        x=np.empty(n); x[:3]=1/3+ds[t]*u[j]; x[3:]=mus[t]
        s=np.empty(n); s[:3]=3*mus[t]; s[3:]=1.0
        Moss=np.hstack([-(np.diag(x)@A.T), np.diag(s)@V])
        f=(1-tau)*mus[t]*np.ones(n)-x*s
        z=np.linalg.solve(Moss,f); q=np.linalg.norm(z)
        psis.append(z/q); Ms.append(q/np.linalg.norm(f)*Moss)
    d=[np.linalg.norm(Ms[t+1]@(psis[t+1]-psis[t])) for t in range(T)]
    return np.array(d), np.array(mus)
for rho in [(1.,3.,1.),(1.,1.,1.)]:
    d,mus=deltas(rho=rho)
    print("rho",rho)
    print("  mu at t=60,120,180,240:", ["%.2e"%mus[t] for t in (60,120,180,240)])
    for t0 in (30,60,90,120,150):
        print(f"   delta_t t={t0}..{t0+2}: {d[t0]:.6f} {d[t0+1]:.6f} {d[t0+2]:.6f}   cum V_proj(t={t0+3}) = {d[:t0+3].sum():.3f}")
    # linear fit of cumulative over the numerically safe window
    import numpy.polynomial.polynomial as P
    w=slice(30,150); ts=np.arange(len(d))[w]; cum=np.cumsum(d)[w]
    slope=np.polyfit(ts,cum,1)[0]
    print(f"   linear growth rate of V_proj over t in [30,150]: {slope:.4f} per iteration")
