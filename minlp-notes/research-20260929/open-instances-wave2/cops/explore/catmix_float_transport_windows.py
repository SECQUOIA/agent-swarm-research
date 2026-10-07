import numpy as np, sys, time
sys.path.insert(0,'..')
import catmix_model as cmx
N=int(sys.argv[1]); usrc=sys.argv[2]
m,K=cmx.extract(N); fm=cmx.FloatModel(K,N)
a,b,c,ep,em=fm.a,fm.b,fm.c,fm.ep,fm.em
ustar=np.load(usrc); Jref,_,xs=fm.J_grad(ustar)
ys=np.array([[(1-a*ustar[i])*xs[i,0]+b*ustar[i]*xs[i,1], a*ustar[i]*xs[i,0]+(em-c*ustar[i])*xs[i,1]] for i in range(N)])
thstar=ys[:,1]/ys.sum(1)
def Mapply(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    x1=(P22*y1-P12*y2)/det; x2=(P11*y2-P21*y1)/det
    return (1-a*uu)*x1+b*uu*x2, a*uu*x1+(em-c*uu)*x2
def Minv_theta(uu,th):
    # preimage ray of ray th under M(uu): solve M y' = (1-th,th) up to scale
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    Q=np.array([[1-a*uu,b*uu],[a*uu,em-c*uu]]); P=np.array([[P11,P12],[P21,P22]])
    Mm=Q@np.linalg.inv(P)
    y=np.linalg.solve(Mm,np.stack([1-th,th]))
    return y[1]/(y[0]+y[1])
def Pinv(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    return (P22*y1-P12*y2)/det,(P11*y2-P21*y1)/det
def vmin(f, shape, extra=None):
    us=np.linspace(0,1,201)
    if extra is not None: us=np.unique(np.concatenate([us,extra]))
    vals=np.stack([f(np.full(shape,uu)) for uu in us])
    k=np.argmin(vals,axis=0); best=vals.min(axis=0)
    lo=np.clip(us[k]-1/200,0,1); hi=np.clip(us[k]+1/200,0,1)
    gr=(np.sqrt(5)-1)/2
    x1=hi-gr*(hi-lo); x2=lo+gr*(hi-lo); f1=f(x1); f2=f(x2)
    for _ in range(50):
        m_=f1<f2
        hi=np.where(m_,x2,hi); lo=np.where(m_,lo,x1)
        x2n=np.where(m_,x1,lo+gr*(hi-lo)); x1n=np.where(m_,hi-gr*(hi-lo),x2)
        x1,x2=x1n,x2n; f1=f(x1); f2=f(x2)
    return np.minimum(best,np.minimum(f1,f2))
def run(dc, K_, delta, label):
    t0=time.time()
    base=np.concatenate([np.arange(0,0.1,dc),np.linspace(0.1,1,91)])
    # transported windows: window at stage N-1 around thstar[N-1]; stage i-1 window = preimage of stage i window under u_i*
    win=[None]*N
    win[N-1]=thstar[N-1]+delta*np.arange(-K_,K_+1)
    for i in range(N-1,0,-1):
        win[i-1]=Minv_theta(ustar[i],win[i])
    grid=lambda i: np.unique(np.concatenate([base,win[i]]))
    th=grid(N-1); w=vmin(lambda uu: sum(Pinv(uu,1-th,th)), th.shape, extra=np.array([ustar[N]])); tot=len(th)
    for i in range(N-1,0,-1):
        thn=grid(i-1)
        def f(uu,w=w,th=th,thn=thn):
            z1,z2=Mapply(uu,1-thn,thn); s=z1+z2
            return s*np.interp(z2/s,th,w)
        w=vmin(f,thn.shape,extra=np.array([ustar[i]])); th=thn; tot+=len(th)
    def f0(uu):
        z1=1-a*uu; z2=a*uu; s=z1+z2
        return s*np.interp(z2/s,th,w)
    bnd=vmin(f0,(),extra=np.array([ustar[0]]))-1
    print('%-45s avg grid %7d bound %.15f gap %.3e (%.1fs)'%(label,tot//N,bnd,Jref-bnd,time.time()-t0),flush=True)
print('Jref',Jref)
for dc in [1e-4,1e-5]:
    for K_,delta in [(0,0),(20,1e-6),(50,1e-7),(200,1e-7)]:
        run(dc,K_,delta,'uni %g + transported win K=%d d=%g'%(dc,K_,delta))
