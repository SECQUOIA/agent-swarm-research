"""Independent dense checks of the locality manuscript; no historical imports.

Rational identities/PSD checks are exact. Random dense checks are floating-point
diagnostics, not proofs. Run from any directory with the research Python env.
"""
from pathlib import Path
import itertools
import json
import math
import platform
import numpy as np
import sympy as sp

OUT = Path(__file__).resolve().parents[1]/'results'
report = {"python": platform.python_version(), "numpy": np.__version__,
          "sympy": sp.__version__, "seed": 2026091302, "counts": {}}
rng = np.random.default_rng(report["seed"])


def count(key, amount=1):
    report["counts"][key] = report["counts"].get(key, 0) + amount


def tail(x, L):
    return x ** (L + 1) / (1 - x)


def near(x, L):
    return x ** (L + 2) * (1 - x ** L) * (1 - x ** (L + 1)) / ((1 - x) * (1 - x * x))


def local(R, sizes, selected, L, exact=False):
    bounds = np.cumsum([0] + sizes)
    ids = [j for t in selected for j in range(bounds[t], bounds[t + 1])]
    pick = lambda M, a, b: M.extract(a, b) if exact else M[np.ix_(a, b)]
    eye = sp.eye if exact else np.eye
    zero = sp.zeros if exact else lambda n: np.zeros((n, n))
    RR = pick(R, ids, ids)
    A, D = eye(len(ids)), zero(len(ids))
    chosen_bounds = np.cumsum([0] + [sizes[t] for t in selected])
    blocks = []
    for i, t in enumerate(selected):
        target = list(range(chosen_bounds[i], chosen_bounds[i + 1]))
        hist = [j for a, s in enumerate(selected[:i]) if t - s <= L
                for j in range(chosen_bounds[a], chosen_bounds[a + 1])]
        dd = pick(RR, target, target)
        if hist:
            cross, hh = pick(RR, target, hist), pick(RR, hist, hist)
            beta = cross * hh.inv() if exact else np.linalg.solve(hh, cross.T).T
            dd = dd - (beta * cross.T if exact else beta @ cross.T)
            for a, u in enumerate(target):
                for b, v in enumerate(hist):
                    A[u, v] = -beta[a, b]
        for a, u in enumerate(target):
            for b, v in enumerate(target):
                D[u, v] = dd[a, b]
        blocks.append(target)
    Z = A * RR * A.T if exact else A @ RR @ A.T
    return RR, A, D, Z, blocks


def exact_psd(M):
    # Every matrix passed here is symmetric; all principal minors characterize PSD.
    for k in range(1, M.rows + 1):
        for ids in itertools.combinations(range(M.rows), k):
            assert M.extract(ids, ids).det() >= 0


# Exact finite geometric identity and rational theta smallness.
for L in range(9):
    for x in [sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(3, 4)]:
        total = sum(x ** (h + 2 * d) for h in range(1, L + 1)
                    for d in range(L + 1 - h, L + 1))
        assert total == near(x, L)
        count("exact_geometric")
for C, m, r in [(sp.Rational(1), sp.Rational(1), sp.Rational(2, 5)),
                 (sp.Rational(3), sp.Rational(2), sp.Rational(1, 2))]:
    theta = (4*C*r + m*r*(1-r))/(4*C*r + m*(1-r))
    assert 2*C*(r/(theta-r)-r/(1-r)) == m/2
    count("exact_theta")

# Exact scalar witnesses, KL determinant ratios, and sharp stationary limits.
R = sp.Matrix([[2, sp.Rational(1, 2), sp.Rational(1, 4)],
               [sp.Rational(1, 2), sp.Rational(5, 4), sp.Rational(1, 8)],
               [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(17, 16)]])
_, _, _, Z, _ = local(R, [1]*3, list(range(3)), 1, exact=True)
assert Z[2, 1] == -sp.Rational(1, 20)
R = sp.Matrix([[1, 0, sp.Rational(3, 5)], [0, 1, sp.Rational(3, 5)],
               [sp.Rational(3, 5), sp.Rational(3, 5), 1]])
ratios = []
for pivots in [[], [0], [1], [0, 1]]:
    A, D = sp.eye(3), sp.eye(3)
    for t in range(3):
        hist = [j for j in pivots if j < t]
        if hist:
            b = R.extract([t], hist) * R.extract(hist, hist).inv()
            D[t,t] = R[t,t] - (b * R.extract(hist,[t]))[0]
            for j, v in enumerate(hist): A[t,v] = -b[j]
    Q = A.T * D.inv() * A
    assert sp.trace(Q*R) == 3
    ratios.append(1/(Q.det()*R.det()))
assert ratios == [sp.Rational(25,7),sp.Rational(16,7),sp.Rational(16,7),1]
assert ratios[0]*ratios[3]/(ratios[1]*ratios[2]) == sp.Rational(175,256)
report["exact_pivot_ratios"] = list(map(str, ratios))
count("exact_counterexamples", 2)

# Exact rational full-block checks of the newly strengthened far-pair bound.
n, d = 4, 2
r = sp.Rational(1,2)
transitions = [None, sp.Matrix([[0,r],[-r,0]]),
               sp.Matrix([[r,0],[0,-r]]), sp.Matrix([[r/2,r/2],[0,0]])]
R = sp.zeros(n*d)
for t in range(n):
    R[t*d:(t+1)*d,t*d:(t+1)*d] = 2*sp.eye(d)
    product = sp.eye(d)
    for s in range(t-1,-1,-1):
        product = product*transitions[s+1]
        R[t*d:(t+1)*d,s*d:(s+1)*d] = product
        R[s*d:(s+1)*d,t*d:(t+1)*d] = product.T
for k in range(1,n+1):
    for selected in itertools.combinations(range(n),k):
        for L in range(n):
            RR, A, D, Z, blocks = local(R,[d]*n,list(selected),L,True)
            delta = 0 if L >= n-1 else 2*(tail(r,L)+sp.Rational(1,2)*near(r,L))
            # Congruent exact PSD checks avoid square roots and eigenvalues.
            exact_psd(delta*D+(Z-D))
            exact_psd(delta*D-(Z-D))
            for i,t in enumerate(selected):
                for j,s in enumerate(selected[:i]):
                    if t-s > L:
                        pair = Z.extract(blocks[i],blocks[j])
                        exact_psd(r**(2*(t-s))*sp.eye(d)-pair*pair.T)
                        count("exact_block_far_pairs")
            count("exact_block_spectral_models")

# Removing the observation-noise identity recovers an exact fully observed
# Markov chain with a singular transition. Check every information path and
# both innovation directions against an independent principal inverse.
latent_R=R-sp.eye(n*d)
F=sp.Matrix([[sp.Rational(i+1,7),sp.Rational((i*i+2)%5,3)] for i in range(n*d)])
for k in range(1,n+1):
    for selected in itertools.combinations(range(n),k):
        ids=[j for t in selected for j in range(t*d,(t+1)*d)]
        fs=F.extract(ids,[0,1]); rs=latent_R.extract(ids,ids)
        true=fs.T*rs.inv()*fs
        first=list(range(selected[0]*d,(selected[0]+1)*d))
        ffirst=F.extract(first,[0,1])
        forward=ffirst.T*latent_R.extract(first,first).inv()*ffirst
        last=list(range(selected[-1]*d,(selected[-1]+1)*d))
        flast=F.extract(last,[0,1])
        reverse=flast.T*latent_R.extract(last,last).inv()*flast
        for i,j in zip(selected,selected[1:]):
            ii=list(range(i*d,(i+1)*d)); jj=list(range(j*d,(j+1)*d))
            fi=F.extract(ii,[0,1]); fj=F.extract(jj,[0,1])
            pi=latent_R.extract(ii,ii); pj=latent_R.extract(jj,jj)
            cross=latent_R.extract(ii,jj)
            phi=cross.T*pi.inv(); omega=pj-phi*cross
            ff=fj-phi*fi
            forward+=ff.T*omega.inv()*ff
            gain=cross*pj.inv(); innovation=pi-gain*cross.T
            fr=fi-gain*fj
            reverse+=fr.T*innovation.inv()*fr
        assert true==forward==reverse
        count("exact_markov_paths_both_directions")


def check_float(R,sizes,delta_fun, name):
    n = len(sizes)
    max_ratio = 0.
    for k in range(1,n+1):
        for sel in itertools.combinations(range(n),k):
            for L in range(n):
                RR,A,D,Z,blocks = local(R,sizes,list(sel),L)
                val,vec=np.linalg.eigh(D)
                Di=(vec*(1/np.sqrt(val)))@vec.T
                err=np.linalg.norm(Di@Z@Di-np.eye(len(D)),2)
                delta=0. if L >= n-1 else float(delta_fun(L))
                assert err <= delta+2e-8, (name,sel,L,err,delta)
                Q=A.T@np.linalg.solve(D,A)
                inv=np.linalg.inv(RR)
                assert np.linalg.eigvalsh(Q-(1-delta)*inv)[0] > -2e-8
                assert np.linalg.eigvalsh((1+delta)*inv-Q)[0] > -2e-8
                max_ratio=max(max_ratio,err/delta if delta else 0.)
                count(name)
    report[name+"_max_error_to_bound"] = max_ratio


# Variable packet dimensions, large diagonal eigenvalues, arbitrary block metrics.
sizes=[1,2,3,1,2]
ix=np.cumsum([0]+sizes); N=ix[-1]; r=.4; C=.3; m=1.
R=np.zeros((N,N))
for t,dt in enumerate(sizes):
    U=rng.normal(size=(dt,dt))
    R[ix[t]:ix[t+1],ix[t]:ix[t+1]]=2*np.eye(dt)+(10.**(t))*U@U.T
    for s in range(t):
        block=rng.normal(size=(dt,sizes[s])); block/=max(1,np.linalg.norm(block,2))
        block*=C*r**(t-s)
        R[ix[t]:ix[t+1],ix[s]:ix[s+1]]=block
        R[ix[s]:ix[s+1],ix[t]:ix[t+1]]=block.T
assert np.linalg.eigvalsh(R)[0]>m
theta=(4*C*r+m*r*(1-r))/(4*C*r+m*(1-r))
B=2*C/m*r/(theta-r); old=C*(1+B*r/(theta-r))
df=lambda L:2*old/m*tail(theta,L)*(1+B*theta*(1-theta**L)/(1-theta))
check_float(R,sizes,df,"float_general_decay")
M=np.diag(np.exp(np.linspace(-3,3,N)))
check_float(M@R@M.T,sizes,df,"float_supplied_metric")

# Intrinsic partial observations with moving singular latent support and noncommuting
# coordinates. P_t has rank 2 in dimension 4, so no state inverse is available.
n,latent=5,4; sizes=[1,2,1,3,2]; ix=np.cumsum([0]+sizes)
rho=.55; gamma=.6; s_bound=2.
U=[np.linalg.qr(rng.normal(size=(latent,latent)))[0] for _ in range(n)]
P=[u@np.diag([1.,.4,0.,0.])@u.T for u in U]
trans=[None]+[rho*U[t]@U[t-1].T for t in range(1,n)]
H=[]; noise=[]
for dt in sizes:
    h=rng.normal(size=(dt,latent)); h/=max(1,np.linalg.norm(h,2))
    H.append(h); noise.append(.5*np.eye(dt))
R=np.zeros((ix[-1],ix[-1]))
for t in range(n):
    R[ix[t]:ix[t+1],ix[t]:ix[t+1]]=H[t]@P[t]@H[t].T+noise[t]
    product=np.eye(latent)
    for j in range(t-1,-1,-1):
        product=product@trans[j+1]
        cross=H[t]@product@P[j]@H[j].T
        R[ix[t]:ix[t+1],ix[j]:ix[j+1]]=cross
        R[ix[j]:ix[j+1],ix[t]:ix[t+1]]=cross.T
kappa=s_bound/(1+s_bound)
check_float(R,sizes,lambda L:2*kappa*(tail(gamma,L)+math.sqrt(kappa*s_bound)*near(gamma,L)),
            "float_partial_singular")

# Spacing floor, row support recurrence, separated-mask count, all edge cases.
for n in range(1,9):
    for g in range(1,n+2):
        for L in range(n):
            b=.5; P=r=1.; kap=.5
            floor=P
            for _ in range(L//g):floor=P*(1-b**(2*g))+b**(2*g)*r*floor/(r+floor)
            floor+=r
            phi=lambda h: P*b**h if h>L else P*kap*(1-kap)*b**h*sum(
                b**(2*d) for d in range(max(g,L+1-h),L+1,g))
            scores=[0.]*n
            for M in range(g,n):scores[M]=max(scores[M-1],phi(M)+scores[M-g])
            delta=max(scores[t]+scores[n-1-t] for t in range(n))/floor
            for M in range(n):
                best=0.
                for mask in range(1<<max(0,M-g+1)):
                    inds=[g+j for j in range(max(0,M-g+1)) if mask>>j&1]
                    if all(v-u>=g for u,v in zip(inds,inds[1:])):
                        best=max(best,sum(phi(h) for h in inds))
                assert abs(best-scores[M])<1e-12
                count("float_row_dp_exhaustions")
            valid=sum(all(v-u>=g for u,v in zip(inds,inds[1:]))
                      for mask in range(1<<L)
                      for inds in [[j for j in range(L) if mask>>j&1]])
            formula=1+sum(math.comb(L-(g-1)*(q-1),q)
                          for q in range(1,math.ceil(L/g)+1))
            assert valid==formula
            count("exact_mask_counts")
            # Sample all feasible schedules for n<=6 to check normalized bound/floor.
            if n<=6:
                R=np.array([[P*b**abs(t-s)+r*(t==s) for s in range(n)] for t in range(n)])
                for mask in range(1,1<<n):
                    sel=[t for t in range(n) if mask>>t&1]
                    if any(v-u<g for u,v in zip(sel,sel[1:])):continue
                    _,_,D,Z,_=local(R,[1]*n,sel,L)
                    assert np.diag(D).min()>=floor-1e-12
                    invd=1/np.sqrt(np.diag(D))
                    err=np.linalg.norm((Z-D)*invd[:,None]*invd[None,:],2)
                    assert err<=delta+1e-12
                    count("float_spacing_spectral_models")

# Reproduce the generic-constant windows printed in the manuscript.
C=m=1.;rho=.4
theta=(4*C*rho+m*rho*(1-rho))/(4*C*rho+m*(1-rho))
B=2*C/m*rho/(theta-rho);old=C*(1+B*rho/(theta-rho))
thresholds={}
for target in [.05,.01]:
    thresholds[str(target)]=next(L for L in range(500)
        if 2*old/m*tail(theta,L)*(1+B*theta*(1-theta**L)/(1-theta))<=target)
assert thresholds=={"0.05":49,"0.01":58}
report["generic_thresholds"]=thresholds
report["result"]="all checks passed; floating checks are diagnostics, not certificates"
(OUT/"stage02-checks.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
