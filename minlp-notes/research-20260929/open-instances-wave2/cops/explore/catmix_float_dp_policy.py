import numpy as np, sys
sys.path.insert(0,'..')
import catmix_model as cmx
N=int(sys.argv[1]); ng=int(sys.argv[2])
m,K=cmx.extract(N)
fm=cmx.FloatModel(K,N)
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
def vargmin(f, shape):
    us=np.linspace(0,1,201)
    vals=np.stack([f(np.full(shape,uu)) for uu in us])
    k=np.argmin(vals,axis=0); best=vals.min(axis=0); ub=us[k]
    lo=np.clip(us[k]-1/200,0,1); hi=np.clip(us[k]+1/200,0,1)
    gr=(np.sqrt(5)-1)/2
    x1=hi-gr*(hi-lo); x2=lo+gr*(hi-lo); f1=f(x1); f2=f(x2)
    for _ in range(45):
        m_=f1<f2
        hi=np.where(m_,x2,hi); lo=np.where(m_,lo,x1)
        x2n=np.where(m_,x1,lo+gr*(hi-lo)); x1n=np.where(m_,hi-gr*(hi-lo),x2)
        x1,x2=x1n,x2n; f1=f(x1); f2=f(x2)
    fb=np.minimum(f1,f2); xb=np.where(f1<f2,x1,x2)
    return np.where(fb<best,fb,best), np.where(fb<best,xb,ub)
th=np.linspace(0,0.1,ng); y1=1-th; y2=th
W=[None]*N
w,_=vargmin(lambda uu: sum(Pinv(uu,y1,y2)), th.shape); W[N-1]=w
for i in range(N-1,0,-1):
    def f(uu,w=w):
        z1,z2=Mapply(uu,y1,y2); s=z1+z2
        return s*np.interp(z2/s,th,w)
    w,_=vargmin(f,th.shape); W[i-1]=w
# forward policy extraction
def f0(uu):
    z1=1-a*uu; z2=a*uu; s=z1+z2
    return s*np.interp(z2/s,th,W[0])
v0,u0=vargmin(f0,())
print('DP bound',v0-1)
us=[float(u0)]; y=np.array([1-a*u0,a*u0])
for i in range(1,N):
    Wi=W[i]
    def fi(uu):
        z1,z2=Mapply(uu,y[0],y[1]); s=z1+z2
        return s*np.interp(z2/s,th,Wi)
    v,ui=vargmin(fi,()); us.append(float(ui)); y=np.array(Mapply(ui,y[0],y[1]))
_,uN=vargmin(lambda uu: sum(Pinv(uu,y[0],y[1])),()); us.append(float(uN))
us=np.array(us)
J,g,x=fm.J_grad(us)
print('policy J',repr(J))
np.save('/tmp/catmix%d_udp.npy'%N,us)
np.set_printoptions(linewidth=200,precision=4)
print(us)
