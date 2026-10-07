import numpy as np, sys, time
sys.path.insert(0,'..')
import catmix_model as cmx
N=int(sys.argv[1]); Jref=float(sys.argv[2])
m,K=cmx.extract(N); fm=cmx.FloatModel(K,N)
a,b,c,ep,em=fm.a,fm.b,fm.c,fm.ep,fm.em
def Mapply(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    x1=(P22*y1-P12*y2)/det; x2=(P11*y2-P21*y1)/det
    return (1-a*uu)*x1+b*uu*x2, a*uu*x1+(em-c*uu)*x2
def Pinv(uu,y1,y2):
    P11=1+a*uu;P12=-b*uu;P21=-a*uu;P22=ep+c*uu
    det=P11*P22-P12*P21
    return (P22*y1-P12*y2)/det,(P11*y2-P21*y1)/det
def vmin(f, shape):
    us=np.linspace(0,1,201)
    vals=np.stack([f(np.full(shape,uu)) for uu in us])
    k=np.argmin(vals,axis=0); best=vals.min(axis=0)
    lo=np.clip(us[k]-1/200,0,1); hi=np.clip(us[k]+1/200,0,1)
    gr=(np.sqrt(5)-1)/2
    x1=hi-gr*(hi-lo); x2=lo+gr*(hi-lo); f1=f(x1); f2=f(x2)
    for _ in range(45):
        m_=f1<f2
        hi=np.where(m_,x2,hi); lo=np.where(m_,lo,x1)
        x2n=np.where(m_,x1,lo+gr*(hi-lo)); x1n=np.where(m_,hi-gr*(hi-lo),x2)
        x1,x2=x1n,x2n; f1=f(x1); f2=f(x2)
    return np.minimum(best,np.minimum(f1,f2))
def run(grid_fn,label):
    t0=time.time()
    th=grid_fn(N-1); w=vmin(lambda uu: sum(Pinv(uu,1-th,th)), th.shape); tot=len(th)
    for i in range(N-1,0,-1):
        thn=grid_fn(i-1)
        def f(uu,w=w,th=th,thn=thn):
            z1,z2=Mapply(uu,1-thn,thn); s=z1+z2
            return s*np.interp(z2/s,th,w)
        w=vmin(f,thn.shape); th=thn; tot+=len(th)
    def f0(uu):
        z1=1-a*uu; z2=a*uu; s=z1+z2
        return s*np.interp(z2/s,th,w)
    bnd=vmin(f0,())-1
    print('%-40s avg grid %8d  bound %.15f  gap %.3e  (%.1fs)'%(label,tot//N,bnd,Jref-bnd,time.time()-t0),flush=True)
coarse=np.concatenate([np.linspace(0,0.1,1001),np.linspace(0.1,1,91)[1:]])
def uni(d): 
    g=np.concatenate([np.arange(0,0.1,d),np.linspace(0.1,1,91)]); return lambda i: g
ths=0.07061
band=lambda d,w: np.arange(ths-w,ths+w,d)
for d in [1e-5,3e-6]:
    run(uni(d),'uniform %g'%d)
g1=np.unique(np.concatenate([uni(1e-5)(0),band(1e-7,1e-3)]))
run(lambda i:g1,'uni 1e-5 + band 1e-7 +-1e-3')
g2=np.unique(np.concatenate([uni(1e-5)(0),band(1e-8,2e-4)]))
run(lambda i:g2,'uni 1e-5 + band 1e-8 +-2e-4')
g3=np.unique(np.concatenate([uni(1e-4)(0),band(1e-7,1e-3)]))
run(lambda i:g3,'uni 1e-4 + band 1e-7 +-1e-3')
