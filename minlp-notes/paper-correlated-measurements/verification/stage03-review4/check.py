"""Independent exact checks of the scalar predecessor reduction (review 4)."""
from itertools import combinations
import json
from pathlib import Path
import sympy as s

R = s.Rational

def psd(M):
    return all(M.extract(ii, ii).det() >= 0
               for k in range(1, M.rows + 1)
               for ii in combinations(range(M.rows), k))

def dyadic_floor(x):
    d = s.Integer(1)
    while d*d > x:
        d /= 2
    while 4*d*d <= x:
        d *= 2
    return d

records = []
fixtures = [
    ([R(0), R(0), R(0)], [R(1, 2), R(-1, 2)], [R(1, 16), R(4), R(1, 4)], [R(2), R(-3), R(1, 8)]),
    ([R(1, 32), R(1, 64), R(0)], [R(-1, 2), R(1, 4)], [R(1, 16), R(16), R(1, 4)], [R(-8), R(1, 128), R(2)]),
]
for idx, (innov, trans, noise, sens) in enumerate(fixtures):
    n = len(noise)
    rmin = min(noise)
    rho = R(1, 2)
    B0 = R(1)
    eps = R(1, 7)
    scale = dyadic_floor(rmin)
    ds = [dyadic_floor(v) for v in noise]
    shift = s.zeros(n)
    for t, a in enumerate(trans, 1):
        shift[t, t-1] = a
    T = (s.eye(n)-shift).inv()
    K_orig = T*s.diag(*innov)*T.T
    assert all(K_orig[i,i] <= B0*rmin for i in range(n))
    K = K_orig/scale**2
    C = s.diag(*[scale/d for d in ds])
    D = s.diag(*[v/d**2 for v,d in zip(noise,ds)])
    h = max(abs(v/d) for v,d in zip(sens,ds))
    g = s.Matrix([v/(d*h) for v,d in zip(sens,ds)])
    tau = eps/4
    zeta = tau*(1-rho)**2/4
    E = zeta*T*T.T
    Kplus = K+E
    Rp = D+C*K*C.T
    Rplus = D+C*Kplus*C.T
    assert psd(E-zeta/(1+rho)**2*s.eye(n))
    assert psd(zeta/(1-rho)**2*s.eye(n)-E)
    assert psd(Rplus-Rp) and psd((1+tau)*Rp-Rplus)
    shear = s.eye(2*n+1)
    shear[n+1:,0] = g
    shear[n+1:,1:n+1] = C
    cov = shear*s.diag(s.eye(1),Kplus,D)*shear.T
    precision = cov.inv()
    bags = [{0,t+1,t+2,n+t+1} for t in range(n-1)] + [{0,n,2*n}]
    allowed = {tuple(sorted((i,j))) for bag in bags for i in bag for j in bag}
    for i in range(2*n+1):
        for j in range(i+1,2*n+1):
            assert precision[i,j] == 0 or (i,j) in allowed
    checked=0
    for k in range(n+1):
        for S in combinations(range(n),k):
            if not S:
                I=Ip=0
                variance=cov[0,0]
            else:
                gs=g.extract(S,[0])
                I=(gs.T*Rp.extract(S,S).inv()*gs)[0]
                Ip=(gs.T*Rplus.extract(S,S).inv()*gs)[0]
                obs=[n+1+t for t in S]
                variance=(cov.extract([0],[0])-cov.extract([0],obs)*cov.extract(obs,obs).inv()*cov.extract(obs,[0]))[0]
            assert I/(1+tau) <= Ip <= I
            assert s.cancel(variance-1/(1+Ip)) == 0
            checked += 1
    D0=4+16*B0+4*zeta/(1-rho**2)
    alpha=eps/(4*(D0+1))
    assert (1-alpha*D0)/(1+alpha) >= 1-eps/4
    records.append({'fixture':idx,'selected_sets':checked,'joint_vertices':cov.rows,'graph_width_bound':3})

assert s.Matrix([[2,1],[1,3]]).inv()[0,0] == R(3,5)
assert (s.Matrix([[2,1],[1,3]])[0,0])**-1 == R(1,2)
out={'status':'pass','checks':records,'private_block_witness':['3/5','1/2']}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
