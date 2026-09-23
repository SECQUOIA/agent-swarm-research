import numpy as np
rng = np.random.default_rng(0)
n = 40
c = np.zeros(n); c[-1]=1.0; c[-2]=0.5
A = np.ones((1,n)); _,_,Vt = np.linalg.svd(A); Z = Vt[1:].T
def central(mu, x0):
    x = x0.copy()
    for _ in range(800):
        g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
        d = np.linalg.solve(H,-g)
        lam = np.sqrt(d@H@d); step = 1.0 if lam<0.25 else 1/(1+lam)
        while np.any(x+step*(Z@d)<=0): step*=0.5
        x = x+step*(Z@d)
        if lam<1e-12: break
    return x
def cg_iters(H, bb, tol=1e-8):
    xk = np.zeros_like(bb); r = bb.copy(); p = r.copy(); it=0; rs = r@r
    nb = np.linalg.norm(bb)
    while np.sqrt(rs) > tol*nb and it < 5000:
        Hp = H@p; al = rs/(p@Hp); xk+=al*p; r-=al*Hp
        rsn = r@r; p = r + (rsn/rs)*p; rs = rsn; it+=1
    return it
x = np.ones(n)/n
print(f"{'mu':>8} {'kappa':>10} {'#big':>5} {'ratio_lo':>9} {'ratio_hi':>9} {'CG its':>7}")
for mu in [1e-2,1e-4,1e-6,1e-8]:
    x = central(mu, x)
    H = Z.T@np.diag(1/x**2)@Z
    w = np.linalg.eigvalsh(H)
    thresh = np.sqrt(w[0]*w[-1])
    lo = w[w<=thresh]; hi = w[w>thresh]
    bb = rng.standard_normal(n-1); bb/=np.linalg.norm(bb)
    it = cg_iters(H, bb)
    print(f"{mu:>8.0e} {w[-1]/w[0]:>10.2e} {len(hi):>5} {lo[-1]/lo[0]:>9.3f} {hi[-1]/hi[0]:>9.3f} {it:>7}")
