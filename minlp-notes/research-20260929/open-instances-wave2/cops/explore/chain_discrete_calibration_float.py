import numpy as np, sys
sys.path.insert(0,'..')
import chain_model as cm
import mpmath as mp
from scipy.optimize import minimize, minimize_scalar
N=int(sys.argv[1])
z,mu,_=cm.solve(N)
fstar=float(cm.lag_grad_hess(z,mu,N,mp.mpf(1)/N,mp.mpf,mp.sqrt)[0]-mu*4)
mu=float(mu); h=1.0/N
y=np.array([1.0]+[float(v) for v in z]+[3.0])
dt=np.array([h/2]+[h]*(N-1)+[h/2])
dy=np.diff(y); lam=np.hypot(dt,dy); sig=np.concatenate([[0],np.cumsum(lam)])
a=np.array([1.0]+[0.5]*(N-1)+[0.0])
eta=np.concatenate([[1.0],(y[1:N]+y[2:N+1])/2,[3.0]])
T=eta+mu; V=T*dy/lam; Hk=T*dt/lam
H=np.mean(Hk[1:N]); Vb=V[0]-lam[0]; Vb2=Vb+lam[0]
k2=h/(2*H)
def m_of_v(v):
    m=v+k2*np.hypot(H,v)
    for _ in range(60): m=v+k2*np.hypot(H,m)
    return m
def Qm(m):
    Tm=np.hypot(H,m)
    return (m*Tm/2)*(1+k2*k2)+(H*H*np.arcsinh(m/H)/2)*(1-k2*k2)-k2*m*m
def Q(v): return Qm(m_of_v(v))
def Ld(v,vp):
    lamb=vp-v; return np.abs((v+vp)/2)*np.sqrt(np.maximum(lamb*lamb-h*h,0))
vk=Vb2+sig[1:N+1]-lam[0]  # start-of-piece tensions for interior pieces 1..N-1 and end
vk=np.array([Vb2+(sig[k]-sig[1]) for k in range(1,N+1)])
cs=[Q(vk[k+1])-Q(vk[k])-Ld(vk[k],vk[k+1]) for k in range(N-1)]
print('H',H,'c range',min(cs),max(cs),' -Hh',-H*h)
c=np.mean(cs)
# check S<=0 on grid
vs=np.linspace(-1.6,3.5,2001); ls=np.concatenate([h+np.logspace(-10,0,800)*0+np.linspace(0,0,1), h*np.linspace(1,300,3000)])
V_,L_=np.meshgrid(vs,ls)
S=Ld(V_,V_+L_)-Q(V_+L_)+Q(V_)+c
i=np.unravel_index(np.argmax(S),S.shape)
print('max S on grid',S[i],'at v',V_[i],'lam',L_[i])
# where positive
pos=S>1e-12
if pos.any(): print('positive region: v in',V_[pos].min(),V_[pos].max(),'lam in',L_[pos].min(),L_[pos].max())
# outer bound
def B(q,Vb2):
    z1,zN=q
    l0=np.hypot(h/2,z1-1); lN=np.hypot(h/2,3-zN); L=4-l0-lN
    return l0+3*lN+(Vb2+L)*zN-Vb2*z1+(N-1)*c+Q(Vb2)-Q(Vb2+L)
def Bmax(q):
    r=minimize_scalar(lambda vb:-B(q,vb),bracket=(Vb2-0.1,Vb2+0.1),tol=1e-14)
    return -r.fun
q0=np.array([y[1],y[N]])
print('B at opt with Vb2*',B(q0,Vb2),'f*',fstar,'diff',B(q0,Vb2)-fstar)
res=minimize(Bmax,q0,method='Nelder-Mead',options=dict(xatol=1e-12,fatol=1e-16,maxiter=4000))
print('min_q max_Vb B =',res.fun,'gap',fstar-res.fun,'q',res.x,'q*',q0)
