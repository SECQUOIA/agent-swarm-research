"""Exact checks for core-only noise, with no residual perturbation.

The fixture oracle solves convex scalar recourse after eliminating one
residual coordinate. It tests the new growth/interiority interface.
"""
from fractions import Fraction as Q


def pd(A):
    A=[list(row) for row in A]
    for i in range(len(A)):
        assert A[i][i]>0
        for j in range(i+1,len(A)):
            for l in range(j,len(A)):
                A[j][l]-=A[i][j]*A[i][l]/A[i][i]
                A[l][j]=A[j][l]


total_bisections=0
total_slabs=0
clipped=0
for offset,coupling,linear in ((Q(1,4),Q(1,4),Q(1,100)),
                               (Q(1,2**400),Q(1,2**400),Q(0))):
    for noise in (Q(-1,10),Q(1,10)):
        def objective(v,z,w):
            t=v-Q(1,2); u=z-offset-coupling*v
            return t*t-t**4+u*u+u**4+(w-Q(1,4)-z/3)**2+linear*z+noise*v
        def recourse(v,bounds,eta):
            global total_bisections
            (lo,hi),(wl,wh)=bounds
            def point(z):
                return z,min(wh,max(wl,Q(1,4)+z/3))
            def derivative(z):
                u=z-offset-coupling*v; w=point(z)[1]
                return 2*u+4*u**3-Q(2,3)*(w-Q(1,4)-z/3)+linear
            if derivative(lo)>=0:
                p=point(lo); value=objective(v,*p)
                return value,value,p
            if derivative(hi)<=0:
                p=point(hi); value=objective(v,*p)
                return value,value,p
            while True:
                mid=(lo+hi)/2; p=point(mid); upper=objective(v,*p)
                slope=derivative(mid)
                lower=upper+min(slope*(lo-mid),slope*(hi-mid))
                if upper-lower<=eta:
                    return lower,upper,p
                if slope<0:
                    lo=mid
                else:
                    hi=mid
                total_bisections+=1

        # The residual root is interior for every core value. These simple
        # rational inequalities certify a coupled stationary solution.
        ulo,uhi=(-linear,Q(0)) if linear else (Q(0),Q(0))
        assert 2*ulo+4*ulo**3+linear<=0<=2*uhi+4*uhi**3+linear
        assert 0<offset+ulo and offset+coupling+uhi<1
        assert 0<Q(1,4)+(offset+ulo)/3<Q(1,4)+(offset+coupling+uhi)/3<1
        # Squared residuals form an invertible triangular linear map, so
        # H_RR >= 8/9 I; the quartic only increases this Hessian.
        mu=Q(1,2)
        pd([[Q(20,9)-mu,Q(-2,3)],[Q(-2,3),Q(2)-mu]])

        # Core value is t²-t⁴+(noise+linear*coupling)*v+constant.
        # Its unique stationary root is in |t|<.1; the exact Taylor
        # remainder gives projected growth at least .62, hence gV=.25.
        effective=noise+linear*coupling
        lo,hi=Q(-1,10),Q(1,10)
        assert 2*lo-4*lo**3+effective<0<2*hi-4*hi**3+effective
        assert 1-Q(1,4)-Q(1,10)-3*Q(1,100)>Q(1,4)
        for _ in range(180):
            mid=(lo+hi)/2
            if 2*mid-4*mid**3+effective<0:
                lo=mid
            else:
                hi=mid
        core_interval=(lo+Q(1,2),hi+Q(1,2))

        M1,T,G,L=Q(32),Q(64),Q(4),Q(23,8)
        sensitivity=M1/mu
        gV=Q(1,4)
        g=min(gV/(1+2*sensitivity**2),mu/4)
        tau=Q(1,2)
        radius=min(Q(1,8),tau/(16*M1),g/(4*T))
        amp=2+(L+8)/g
        mesh=Q(1); stage=0
        while mesh>min(radius/(4*amp),g*radius**2/(16*G*amp)):
            mesh/=2; stage+=1
        midcore=sum(core_interval)/2
        index=(midcore/mesh+Q(1,2)).numerator//(midcore/mesh+Q(1,2)).denominator
        core=index*mesh
        D=(core-mesh,core+mesh)
        assert D[0]<core_interval[0]<core_interval[1]<D[1]
        e=L*mesh**2/8
        original=[(Q(0),Q(1))]*2
        lower,upper,witness=recourse(core,original,e)
        assert upper-lower<=e
        patch=[(max(Q(0),z-radius),min(Q(1),z+radius)) for z in witness]
        exclusions=[]
        for i in range(2):
            for sign in (-1,1):
                threshold=witness[i]+sign*radius
                if 0<threshold<1:
                    bounds=list(original)
                    bounds[i]=(Q(0),threshold) if sign<0 else (threshold,Q(1))
                    ell,u,p=recourse(core,bounds,g*radius**2/16)
                    assert u-ell<=g*radius**2/16
                    exclusions.append(ell); total_slabs+=1
        assert min(exclusions)-upper>2*G*(D[1]-D[0])
        fullpatch=[D]+patch
        midpoint=[(a+b)/2 for a,b in fullpatch]
        rQ=max((b-a)/2 for a,b in fullpatch)
        v,z,w=midpoint
        qcurv=2+12*(z-offset-coupling*v)**2
        Hess=[[2-12*(v-Q(1,2))**2+coupling**2*qcurv,-coupling*qcurv,Q(0)],
              [-coupling*qcurv,qcurv+Q(2,9),Q(-2,3)],
              [Q(0),Q(-2,3),Q(2)]]
        pd([[Hess[i][j]-(T*rQ+g if i==j else 0) for j in range(3)] for i in range(3)])
        if offset<Q(1,2**200):
            assert patch[0][0]==0
            assert mesh>offset and stage<400
            clipped+=1

# Growth-lift inequalities with independent positive scales.
lift_cases=0
for gv in (Q(1,2**30),Q(1,3),Q(2**20)):
    for mu in (Q(1,2**20),Q(1),Q(2**15)):
        for H in (Q(1,100),Q(1),Q(2**30)):
            g=min(gv/(1+2*H*H),mu/4)
            assert g*(1+2*H*H)<=gv and 2*g<=mu/2
            lift_cases+=1
print(f"PASS: 4 core-only nonlinear closure fixtures; {total_slabs} excluded slabs; {total_bisections} rational recourse bisections; {clipped} patches clipping a 400-bit interior residual coordinate; {lift_cases} growth-lift cases")
