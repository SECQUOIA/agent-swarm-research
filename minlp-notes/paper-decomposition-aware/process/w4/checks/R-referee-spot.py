"""R-referee spot checks (exact where possible, short runtime)."""
from fractions import Fraction as Fr
import math, random

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond

# 1. Lemma states constants
s = math.sqrt(17/15)
c = 3 + 2*s + (2+s)/math.sqrt(2)
check("lem:states radius constant %.4f < 7.3" % c, c < 7.3)
phi = lambda m: 0.75 + 8*math.log(1.25 + 4*math.sqrt(2*m))
check("phi(1)=%.3f<=20, phi(2)=%.3f<=20" % (phi(1), phi(2)), phi(1) <= 20 and phi(2) <= 20)
check("phi(m) <= 10 ceil(log2(m+2)) for m<=10^6 sample",
      all(phi(m) <= 10*math.ceil(math.log2(m+2)) for m in list(range(1, 2000)) + [10**k for k in range(3, 7)]))
psi = lambda m: 0.75 + 8*math.log(1.25 + 3*math.sqrt(m))
check("commonmesh psi(m) <= 8 ceil(log2(m+2))",
      all(psi(m) <= 8*math.ceil(math.log2(m+2)) for m in list(range(1, 2000)) + [10**k for k in range(3, 7)]))
c2 = (2+s)*(1+1/math.sqrt(8))
check("commonmesh (G4) constant %.4f < 4.15" % c2, c2 < 4.15)

# 2. Prop twocenters bound beta <= -max(theta^2 M^2/379, h^2/20) on random graded grids (exact)
def graded(lo, hi, c, h, th):
    nodes = {c}
    t = Fr(0)
    while c + t < hi:
        t = min(t + h + th*t, hi - c); nodes.add(c + t)
    t = Fr(0)
    while c - t > lo:
        t = min(t + h + th*t, c - lo); nodes.add(c - t)
    return sorted(nodes)
def wmax(G):
    w = {}
    for a, b in zip(G, G[1:]):
        w[a] = max(w.get(a, 0), b - a); w[b] = max(w.get(b, 0), b - a)
    if len(G) == 1: w[G[0]] = 0
    return w
random.seed(1)
bad = 0
for trial in range(300):
    M = Fr(random.randint(1, 40))
    th = Fr(1, random.choice([4, 8, 16, 32]))
    h = M*Fr(random.randint(1, 64), 64)
    cx = M*Fr(random.randint(0, 50), 50)
    Gx = graded(Fr(0), M, cx, h, th)
    Gz = sorted({Fr(0), M} | {M*Fr(random.randint(0, 10), 10) for _ in range(3)})
    wx = wmax(Gx)
    beta = min(x*x - 2*x*z + M*z - Fr(2, 8)*wx[x]**2 for x in Gx for z in Gz)  # L_x = 2, d_z = 0
    bound = -max(th*th*M*M/379, h*h/20)
    if beta > bound: bad += 1
check("prop:twocenters bound on 300 random graded grids", bad == 0)
check("0.23^2/20 > 1/379", Fr(23, 100)**2/20 > Fr(1, 379))

# 3. Prop cv-limit: numeric lower bound check of L_K/g_K for K={x,y} and K={x},{y} (float grid)
def cvlimit(M, N=401):
    F = lambda x, y: M*(x-y)**2 - (x+y-2)**2/8 + 2*(y-1)
    xs = [2*i/(N-1) for i in range(N)]; ys = [1 + 2*i/(N-1) for i in range(N)]
    # K={x,y}: g = min F/dist^2
    g = min(F(x, y)/((x-1)**2+(y-1)**2) for x in xs for y in ys if (x, y) != (1.0, 1.0))
    r_xy = (2*M - 0.25)/g
    # K={x}: V(x)=min_y F, L via max second difference, g via min V/(x-1)^2
    Vx = [min(F(x, y) for y in ys) for x in xs]
    hstep = xs[1]-xs[0]
    Lx = max((Vx[i-1]-2*Vx[i]+Vx[i+1])/hstep**2 for i in range(1, N-1))
    gx = min(Vx[i]/(xs[i]-1)**2 for i in range(N) if abs(xs[i]-1) > 1e-12)
    Vy = [min(F(x, y) for x in xs) for y in ys]
    Ly = max((Vy[i-1]-2*Vy[i]+Vy[i+1])/hstep**2 for i in range(1, N-1))
    gy = min(Vy[i]/(ys[i]-1)**2 for i in range(N) if abs(ys[i]-1) > 1e-12)
    return r_xy, Lx/gx, Ly/gy
for M in [1, 4, 16]:
    r = cvlimit(M, 201)
    target = (4*M - 0.5)/3
    check("prop:cv-limit M=%d ratios %s >= %.3f (grid estimate)" % (M, tuple(round(v, 2) for v in r), target),
          min(r) >= target*0.98)
print("ALL PASS" if ok else "SOME FAIL")
