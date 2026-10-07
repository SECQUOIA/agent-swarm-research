import numpy as np
rng=np.random.default_rng(3)
mx=0
for k in range(2000):
    X=rng.normal(size=(2,2)); rho=rng.uniform(1,50)
    d=np.linalg.det(X)
    if d<=0 or abs(X[1,0])<1e-3: continue
    hs=np.linspace(-1e4,1e4,200001)
    # det sym(X M(rho,rho,h)) = d (h - rho^2) - (c - g h)^2/4
    vals=[]
    A=lambda h: X@np.array([[h,rho],[rho,1.0]])
    def detsym(h):
        S=A(h); S=(S+S.T)/2; return np.linalg.det(S)
    # maximize concave quadratic exactly via vertex
    g=X[1,0]; c=X[0,0]*rho-X[1,1]*rho+X[0,1]
    hstar=(c+2*d/g)/g
    psi=rho*X[1,0]*(X[0,0]-X[1,1])+X[0,0]*X[1,1]-rho**2*X[1,0]**2
    pred=d/g**2*psi
    mx=max(mx,abs(detsym(hstar)-pred)/(1+abs(pred)))
    # check hstar is the max
    assert detsym(hstar)>=detsym(hstar+0.1)-1e-9 and detsym(hstar)>=detsym(hstar-0.1)-1e-9
print('max rel err of max_h det formula',mx)
