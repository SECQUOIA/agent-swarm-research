"""R1-math: exact checks of algebraic claims in Sections 4-6 and Appendix A."""
import sympy as sp
from sympy import Rational as Q
import itertools

x, y, z, t, u = sp.symbols('x y z t u', real=True)

print("== Example 4.5 ==")
# tangent point of -x^3 for line through (1,-1)
x0 = sp.symbols('x0')
sol = sp.solve(sp.Eq(-x0**3 + (-3*x0**2)*(1-x0), -1), x0)
print("tangent roots", sol)
line = -1 - Q(3,4)*(x-1)
print("env at 0:", line.subs(x, 0))
# check the envelope is below -x^3 on [-1,1] and convex: piecewise -x^3 on [-1,-1/2], line on [-1/2,1]
print("min u^2-u^3 on [-1,1]:", min([(uu**2-uu**3) for uu in [Q(-1),Q(0),Q(1),Q(2,3)]]))
# verify the cut coefficients: rows x^2 - v1 <= 0, -x^3 + v2 <= 0; lambda=(1,1)
print("violation at (0,0,1/4): v1 - v2 =", 0 - Q(1,4))

print("== Example 4.7 second part ==")
# D=[0,2], rows z <= (x-2)^2/2, z <= x^2/2; point (1,1); measure 1/2 at 0, 1/2 at 2
for (mx, mz) in [(1,1)]:
    Eg1 = Q(1,2)*((0-2)**2/Q(2)) + Q(1,2)*((2-2)**2/Q(2))
    Eg2 = Q(1,2)*(0/Q(2)) + Q(1,2)*(4/Q(2))
    print("E[(u-2)^2/2] =", Eg1, " E[u^2/2] =", Eg2, " need >= z=1")
print("max_x min((x-2)^2/2, x^2/2) on [0,2] =", sp.Max(*[min((xx-2)**2/Q(2), xx**2/Q(2)) for xx in [Q(i,100) for i in range(201)]]))

print("== Triangle example (Sec 5.2) ==")
X, Y, Z = [Q(1,2)]*3
print("X+2Z+Y =", X+2*Z+Y, " x+y =", 1)
print("RLT sum:", sp.expand((1-x-y)*x + (1-x-y)*y - (x+y - x**2-2*x*y-y**2)))

print("== Prop 6.1 ==")
vbar = dict(mx=Q(1,2), my=Q(1,2), mz=Q(4,5), sx=Q(1,2), sy=Q(5,16), sz=Q(4,5), pxy=Q(3,8), pyz=Q(1,2))
# measure 1
m1 = [(Q(1,2), (0, Q(1,4))), (Q(1,2), (1, Q(3,4)))]
mom1 = dict(mx=sum(w*a for w,(a,b) in m1), my=sum(w*b for w,(a,b) in m1), sx=sum(w*a*a for w,(a,b) in m1),
            sy=sum(w*b*b for w,(a,b) in m1), pxy=sum(w*a*b for w,(a,b) in m1))
m2 = [(Q(1,5), (0, 0)), (Q(4,5), (Q(5,8), 1))]
mom2 = dict(my=sum(w*a for w,(a,b) in m2), mz=sum(w*b for w,(a,b) in m2), sy=sum(w*a*a for w,(a,b) in m2),
            sz=sum(w*b*b for w,(a,b) in m2), pyz=sum(w*a*b for w,(a,b) in m2))
print("mom1", mom1); print("mom2", mom2)
assert all(vbar[k]==v for k,v in mom1.items()) and all(vbar[k]==v for k,v in mom2.items())
D = (y - Q(1,4) - x/2)**2 + (y - 5*z/8)**2 + x*(1-x) + z*(1-z)
Dp = sp.Poly(sp.expand(D), x, y, z)
print("D expanded:", sp.expand(D))
# linearization
lin_map = {x**2:'sx', y**2:'sy', z**2:'sz', x*y:'pxy', y*z:'pyz', x:'mx', y:'my', z:'mz'}
def linearize(expr, point):
    expr = sp.expand(expr)
    val = 0
    for term in sp.Add.make_args(expr):
        c, mon = term.as_coeff_Mul()
        if mon == 1:
            val += c
        else:
            val += c*point[lin_map[mon]]
    return val
print("lin D at vbar:", linearize(D, vbar))
# min of D over box: by theorem, min over binary x,z of min_y
best = None
for xx in [0,1]:
    for zz in [0,1]:
        f = D.subs({x:xx, z:zz})
        ys = sp.solve(sp.diff(f,y), y)
        for yy in ys + [0, 1]:
            if 0 <= yy <= 1:
                val = f.subs(y, yy)
                if best is None or val < best[0]:
                    best = (val, (xx,yy,zz))
print("min D over box (binary x,z):", best)
# Check concavity of D in x and z
print("d2D/dx2 =", sp.diff(D, x, 2), " d2D/dz2 =", sp.diff(D, z, 2))
cut = 2*vbar['sy'] - Q(1,2)*vbar['my'] - vbar['pxy'] - Q(5,4)*vbar['pyz'] + Q(5,4)*vbar['mx'] - Q(3,4)*vbar['sx'] + vbar['mz'] - Q(39,64)*vbar['sz']
print("cut LHS at vbar:", cut, " rhs -7/128 =", Q(-7,128), " violation", Q(-7,128)-cut)
# check cut == D - 1/128 expanded
cut_expr = 2*y**2 - Q(1,2)*y - x*y - Q(5,4)*y*z + Q(5,4)*x - Q(3,4)*x**2 + z - Q(39,64)*z**2
print("D - cut_expr:", sp.simplify(sp.expand(D) - cut_expr), " (should be 1/16)")
# reduced objective
red = 2*y**2 - Q(1,2)*y - x*y - Q(5,4)*y*z + Q(1,16) + Q(1,2)*x + Q(25,64)*z
for xx in [0,1]:
    for zz in [0,1]:
        assert sp.expand(red.subs({x:xx,z:zz}) - D.subs({x:xx,z:zz})) == 0
print("reduced lin at vbar:", linearize(red, vbar))
print("reduced - D =", sp.factor(sp.expand(red - D)))

print("== sdp-identity ==")
a1, a2, c1, c2, wA, wC, dl = sp.symbols('a1 a2 c1 c2 omegaA omegaC delta', real=True)
U = y - a1 - (a2-a1)*x
V = y - c1 - (c2-c1)*z
Dfam = U**2 + wA*x*(1-x) + V**2 + wC*z*(1-z)
ell = {(0,0):(1-x)*(1-z), (1,0):x*(1-z), (0,1):(1-x)*z, (1,1):x*z}
A_ = [a1, a2]; C_ = [c1, c2]
F = {(i,j): Q(1,2)*((C_[j]-A_[i])**2 - dl**2) for i in (0,1) for j in (0,1)}
rhs = (U+V)**2/2 + sum(F[ij]*ell[ij] for ij in ell) + (wA - (a2-a1)**2/2)*x*(1-x) + (wC-(c2-c1)**2/2)*z*(1-z)
print("identity residual:", sp.expand(Dfam - dl**2/2 - rhs))

print("== Prop A.1 formula ==")
# p_xz formula; take an interleaving example and check PSD of unique completion
def propA1(a1v,a2v,c1v,c2v):
    # chord intersection: weights mx on a2, mz on c2 with equal mean and second moment
    lam, mu = sp.symbols('lam mu')
    sol = sp.solve([ (1-lam)*a1v + lam*a2v - ((1-mu)*c1v + mu*c2v),
                     (1-lam)*a1v**2 + lam*a2v**2 - ((1-mu)*c1v**2 + mu*c2v**2)], [lam, mu], dict=True)
    return sol
for (a1v,a2v,c1v,c2v) in [(Q(1,4),Q(3,4),Q(0),Q(5,8)), (Q(0),Q(2),Q(1),Q(3)), (Q(1),Q(3),Q(0),Q(2))]:
    sols = propA1(a1v,a2v,c1v,c2v)
    for s in sols:
        lam, mu = list(s.values())
        mx, mz = s[sp.Symbol('lam')], s[sp.Symbol('mu')]
        my = (1-mx)*a1v + mx*a2v; sy = (1-mx)*a1v**2 + mx*a2v**2
        pxy = mx*a2v; sx = mx
        pyz = mz*c2v; sz = mz
        pxz1 = (sy - (a1v+c1v)*my + a1v*c1v)/((a2v-a1v)*(c2v-c1v))
        pxz2 = mx*(a2v-c1v)/(c2v-c1v); pxz3 = mz*(c2v-a1v)/(a2v-a1v)
        M = sp.Matrix([[1,mx,my,mz],[mx,sx,pxy,pxz1],[my,pxy,sy,pyz],[mz,pxz1,pyz,sz]])
        ev = [sp.nsimplify(e) for e in M.eigenvals().keys()]
        print((a1v,a2v,c1v,c2v), "mx,mz=",mx,mz," pxz:",pxz1,pxz2,pxz3, " min(mx,mz)=",min(mx,mz),
              " eig>=0:", all(sp.N(e) > -1e-12 for e in M.eigenvals().keys()), " det", sp.simplify(M.det()))
