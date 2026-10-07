"""Exact nonlinear approximate-recourse / excluded-region diagnostics.

The oracle below uses one-dimensional convex bisection after analytically
minimizing one residual coordinate. It is a fixture oracle, not GLS.
"""
from fractions import Fraction as Q


def clip(x, bounds):
    return min(bounds[1], max(bounds[0], x))


def objective(x,z,w,t):
    s=x-Q(1,2); u=z-x/4
    return s*s-s**4+u*u+u**4+(w-z/3)**2+t**4+t-x/400+z/100


iterations=0
def recourse(x, bounds, eta):
    """Return certified lower, feasible value, and rational completion."""
    global iterations
    (lo,hi),wb,tb=bounds
    t=tb[0]  # t^4+t is strictly increasing on the unit interval.
    def point(z):
        return (z,clip(z/3,wb),t)
    def derivative(z):
        u=z-x/4; w=point(z)[1]
        return 2*u+4*u**3-Q(2,3)*(w-z/3)+Q(1,100)
    if derivative(lo)>=0:
        p=point(lo); val=objective(x,*p)
        return val,val,p
    if derivative(hi)<=0:
        p=point(hi); val=objective(x,*p)
        return val,val,p
    while True:
        mid=(lo+hi)/2; p=point(mid); upper=objective(x,*p)
        slope=derivative(mid)
        lower=upper+min(slope*(lo-mid),slope*(hi-mid))
        assert lower<=upper
        if upper-lower<=eta:
            return lower,upper,p
        if slope<0:
            lo=mid
        else:
            hi=mid
        iterations+=1


def pd(A):
    A=[list(row) for row in A]
    for i in range(len(A)):
        assert A[i][i]>0
        for j in range(i+1,len(A)):
            for k in range(j,len(A)):
                A[j][k]-=A[i][j]*A[i][k]/A[i][i]
                A[k][j]=A[j][k]


def hessian_free(x,z):
    curvature=2+12*(z-x/4)**2
    return [[2-12*(x-Q(1,2))**2+curvature/16,-curvature/4,Q(0)],
            [-curvature/4,curvature+Q(2,9),Q(-2,3)],
            [Q(0),Q(-2,3),Q(2)]]


L,g0,tau,M1,T,G=Q(23,8),Q(1,16),Q(1,2),Q(32),Q(64),Q(4)
r=min(Q(1,8),tau/(16*M1),g0/(4*T))
amplification=2+(L+8)/g0
h=Q(1); stages=0
while h>min(r/(4*amplification),g0*r*r/(16*G*amplification)):
    h/=2; stages+=1
e=L*h*h/8
outside_accuracy=g0*r*r/16
original=[(Q(0),Q(1))]*3
lower,upper,witness=recourse(Q(1,2),original,e)
assert upper-lower<=e and upper==objective(Q(1,2),*witness)

# The exact optimizer has core x=1/2; u=z-x/4 is the unique real root
# of 4u^3+2u+1/100. Isolate it independently to certify containment.
# Its primitive integer cubic is irreducible modulo 3, hence over Q.
assert all((400*j**3+200*j+1)%3 for j in range(3))
lo,hi=Q(-1,100),Q(0)
for _ in range(200):
    mid=(lo+hi)/2
    if 4*mid**3+2*mid+Q(1,100)<0:
        lo=mid
    else:
        hi=mid
zrange=(Q(1,8)+lo,Q(1,8)+hi)
wrange=(zrange[0]/3,zrange[1]/3)
patch=[(max(Q(0),v-r),min(Q(1),v+r)) for v in witness]
assert patch[0][0]<zrange[0]<zrange[1]<patch[0][1]
assert patch[1][0]<wrange[0]<wrange[1]<patch[1][1]
assert patch[2][0]==0
assert upper>=lower

# Nonconvex full objective: a diagonal Hessian entry is negative elsewhere.
assert hessian_free(Q(0),Q(0))[0][0]<0
# The residual Hessian is PSD everywhere, as a sum of convex powers of
# affine forms and squares; check the explicit positive 2x2 block.
for z in (Q(0),Q(1,8),Q(1)):
    H=hessian_free(Q(1,2),z)
    pd([[H[1][1],H[1][2]],[H[2][1],H[2][2]]])

excluded=[]; calls=0
for i in range(3):
    for sign in (-1,1):
        threshold=witness[i]+sign*r
        if 0<threshold<1:
            box=list(original)
            box[i]=(Q(0),threshold) if sign==-1 else (threshold,Q(1))
            ell,u,p=recourse(Q(1,2),box,outside_accuracy)
            assert u-ell<=outside_accuracy
            assert all(a<=v<=b for v,(a,b) in zip(p,box))
            excluded.append(ell); calls+=1
assert min(excluded)-upper>2*G*(2*h)

# Uniform midpoint-gradient sign fixes t=0; the free nonlinear Hessian
# then has an exact rational positive-definiteness certificate.
fullpatch=[(Q(1,2)-h,Q(1,2)+h)]+patch
mid=[(a+b)/2 for a,b in fullpatch]
radius=max((b-a)/2 for a,b in fullpatch)
assert 1+4*mid[3]**3-M1*radius>0
H=hessian_free(mid[0],mid[1])
pd([[H[i][j]-(T*radius+g0 if i==j else 0) for j in range(3)] for i in range(3)])

# A feasible excluded upper value is not a valid replacement for its lower
# bound: F(z,w)=w^2 has flat optimizer z, including outside any small patch.
flat_lower=Q(0); flat_upper=Q(1,64); incumbent=Q(0)
assert flat_upper-incumbent>0 and not flat_lower-incumbent>0

# Classical compact certificates: sufficiently accurate feasible points
# have a small directly checkable full-box tangent gap, without a modulus.
for eta in (Q(1,16),Q(1,256),Q(16),Q(256)):
    Kf=Q(64)  # bounds residual Hessian norm times squared box diameter
    delta=min(eta/2,eta*eta/(8*Kf))
    _,u,p=recourse(Q(1,2),original,delta)
    z,w,t=p; offset=z-Q(1,8)
    gradient=[2*offset+4*offset**3-Q(2,3)*(w-z/3)+Q(1,100),
              2*(w-z/3),4*t**3+1]
    tangent_lower=u+sum(gi*((Q(0) if gi>=0 else Q(1))-yi)
                          for gi,yi in zip(gradient,p))
    assert 0<=u-tangent_lower<=eta

# Empty-core convention: A covers witness accuracy and makes the same
# base-only radius conditions sufficient.
for growth in (Q(1,2**30),Q(1),Q(2**30)):
    amp=2+8/growth
    assert 2/growth<=amp*amp
    mesh=min(Q(1),r/(4*amp),growth*r*r/(16*G*amp))
    assert 2*mesh*mesh<=growth*r*r/16

print(f"PASS: nonlinear approximate recourse at stage {stages}; {calls} certified excluded slabs; {iterations} exact convex bisections; 4 full-box tangent certificates; irrational optimum enclosure; nonconvex/full versus convex/residual Hessians; empty-core and lower-bound guards")
