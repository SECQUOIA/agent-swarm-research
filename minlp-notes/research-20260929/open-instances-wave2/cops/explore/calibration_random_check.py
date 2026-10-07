import numpy as np
rng=np.random.default_rng(1)
worst=np.inf
for trial in range(200):
    Hp=10**rng.uniform(-2,1); h=10**rng.uniform(-4,-0.5)
    tau=np.arcsinh(h/(2*Hp)); c=Hp*Hp*(tau+np.sinh(tau)*np.cosh(tau))
    G=lambda v: 0.5*(v*np.hypot(Hp,v)+Hp*Hp*np.arcsinh(v/Hp))
    a=rng.uniform(-5,5,20000); lam=h*(1+10**rng.uniform(-8,3,20000))
    b=a+lam
    F=G(b)-G(a)-c-np.abs((a+b)/2)*np.sqrt(lam*lam-h*h)
    worst=min(worst,(F/np.maximum(1,np.abs(G(b))+np.abs(G(a)))).min())
print('min relative F over random tests',worst)
