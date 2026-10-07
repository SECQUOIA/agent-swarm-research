import numpy as np, sys, time
sys.path.insert(0,'..')
import catmix_model as cmx, catmix_bound as cb
N=int(sys.argv[1])
m,K=cmx.extract(N); fm=cmx.FloatModel(K,N)
a,b,c,ep,em=fm.a,fm.b,fm.c,fm.ep,fm.em
ustar=np.load('../logs/catmix%d_u.npy'%N)
def Mapply(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    x1=(P22*y1-P12*y2)/det; x2=(P11*y2-P21*y1)/det
    return (1-a*uu)*x1+b*uu*x2, a*uu*x1+(em-c*uu)*x2
def Pinv(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    return (P22*y1-P12*y2)/det,(P11*y2-P21*y1)/det
def vmin(f, shape, extra):
    us=np.unique(np.concatenate([np.linspace(0,1,201),extra]))
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
for cfg in sys.argv[2:]:
    dc,Kw,dw=cfg.split(','); dc=float(dc); Kw=int(Kw); dw=float(dw)
    t0=time.time()
    grids,thstar,Jref=cb.make_grids(N,K,ustar,dc,Kw,dw)
    th=grids[N-1]; w=vmin(lambda uu: sum(Pinv(uu,1-th,th)), th.shape, np.array([ustar[N]])); tot=len(th)
    for i in range(N-1,0,-1):
        thn=grids[i-1]
        def f(uu,w=w,th=th,thn=thn):
            z1,z2=Mapply(uu,1-thn,thn); s=z1+z2
            return s*np.interp(z2/s,th,w)
        w=vmin(f,thn.shape,np.array([ustar[i]])); th=thn; tot+=len(th)
    def f0(uu):
        z1=1-a*uu; z2=a*uu; s=z1+z2
        return s*np.interp(z2/s,th,w)
    bnd=vmin(f0,(),np.array([ustar[0]]))-1
    print(N,cfg,'avg rays %d bound %.15f gap %.3e (%.0fs)'%(tot//N,bnd,Jref-bnd,time.time()-t0),flush=True)
