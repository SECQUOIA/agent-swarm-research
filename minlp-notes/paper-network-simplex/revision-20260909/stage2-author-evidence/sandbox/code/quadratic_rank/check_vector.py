"""Exact algebra checks for quadratic-system covariance and cross products."""
import random
import sympy as sp

rng = random.Random(20260905)
z = sp.symbols('x1 x2 x3 y1 y2 y3')
x1, x2, x3, y1, y2, y3 = z
outputs = [x2*y3-x3*y2, x3*y1-x1*y3, x1*y2-x2*y1]
hessians = [sp.hessian(f, z) for f in outputs]
assert sum((h*h for h in hessians), sp.zeros(6)) == 2*sp.eye(6)
a = sp.Matrix(sp.symbols('a1 a2 a3'))
A = sp.Matrix([[0,a[2],-a[1]],[-a[2],0,a[0]],[a[1],-a[0],0]])
assert A.T*A == (a.dot(a))*sp.eye(3)-a*a.T
symbolic = sum((a[j]*hessians[j] for j in range(3)), sp.zeros(6))
assert symbolic == sp.BlockMatrix([[sp.zeros(3),A],[-A,sp.zeros(3)]]).as_explicit()
for coeffs in [(1,0,0),(0,1,0),(0,0,1),(1,2,3),(-2,4,1),(7,-3,-2)]:
    assert sum((coeffs[j]*hessians[j] for j in range(3)), sp.zeros(6)).rank() == 4
print('PASS: exact cross-product Hessians, sum of squares, and skew-rank identity')

for trial in range(15):
    transform = sp.Matrix(6, 6, lambda i,j: rng.randint(-3,3))
    covariance = transform*transform.T+sp.eye(6)
    energy = sum(sp.trace(h*covariance*h*covariance) for h in hessians)
    assert energy**3 >= 12**3*covariance.det()
print('PASS: covariance energy determinant inequality on 15 exact SPD matrices')

# A centered finite distribution tests the fourth-moment identity independently.
points = [sp.Matrix([rng.randint(-2,2) for _ in range(6)]) for _ in range(8)]
mean = sum(points,sp.zeros(6,1))/len(points)
points = [v-mean for v in points]
covariance = sum((v*v.T for v in points),sp.zeros(6))/len(points)
for h in hessians:
    vals = [(v.T*h*v)[0] for v in points]
    moment = sum(((u-v).T*h*(u-v))[0]**2/4 for u in points for v in points)/len(points)**2
    rhs = sum(v*v for v in vals)/(2*len(points)) + (sum(vals)/len(points))**2/2 + sp.trace(h*covariance*h*covariance)
    assert moment == rhs
print('PASS: exact centered fourth-moment expansion for all three outputs')
