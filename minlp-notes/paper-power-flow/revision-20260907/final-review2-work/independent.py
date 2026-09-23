"""Final reviewer calculations; numerical falsification checks are not proofs."""
import math
import random
import numpy as np
import sympy as s

# Symbolic complex-power signs, independent of the supplied checker.
ei, fi, ej, fj, g, b, h, t = s.symbols('ei fi ej fj g b h t', real=True)
ui, uj = ei+s.I*fi, ej+s.I*fj
power = s.expand(ui*s.conjugate((h+s.I*t)*ui+(g+s.I*b)*(ui-uj)))
hij, dij, r2 = ei*ej+fi*fj, fi*ej-ei*fj, ei**2+fi**2
assert s.expand(s.re(power)-(h*r2+g*(r2-hij)-b*dij)) == 0
assert s.expand(s.im(power)-(-t*r2-b*(r2-hij)-g*dij)) == 0

# Three-valued crossing identity against atan2, using integer phasors.
rng = random.Random(2026090802)
pairs = 0
for _ in range(10000):
    start = [rng.randint(-100,100) for _ in range(2)]
    end = [rng.randint(-100,100) for _ in range(2)]
    if start == [0,0] or end == [0,0]: continue
    det = start[0]*end[1]-start[1]*end[0]
    dot = start[0]*end[0]+start[1]*end[1]
    if det == 0 and dot < 0: continue
    k = (1 if start[1]<0<=end[1] and det>0 else
        -1 if end[1]<0<=start[1] and det<0 else 0)
    a = math.atan2(end[1],end[0]) % (2*math.pi)
    z = math.atan2(start[1],start[0]) % (2*math.pi)
    assert abs(math.atan2(det,dot)-(a-z+2*math.pi*k)) < 3e-15
    pairs += 1

# Evaluate the actual complex power on weighted graphs with real lifts.
# Path ramps allow total angle span >2pi while each edge remains short.
profiles = 0
for n in range(2,22):
    for trial in range(20):
        theta = (np.arange(n)*1.4 if trial == 0 else
                 np.array([rng.uniform(-.7,.7) for _ in range(n)]))
        theta -= theta.mean()
        edges = [(j,rng.randrange(j)) for j in range(1,n)] if trial else [(j-1,j) for j in range(1,n)]
        v = np.array([rng.uniform(.5,4) for _ in range(n)])
        lap = np.zeros((n,n))
        for i,j in edges:
            conductance = rng.uniform(.1,3)
            lap[i,i] += conductance; lap[j,j] += conductance
            lap[i,j] -= conductance; lap[j,i] -= conductance
        u = v*np.exp(1j*theta)
        pq = u*np.conj(lap @ u)
        q = pq.imag
        delta = pq.real-v*(lap @ v)
        lam = np.linalg.eigvalsh(lap)[1]
        ell,U = min(v),max(v)
        assert np.linalg.norm(theta) <= math.pi*np.linalg.norm(q)/(2*ell**2*lam)+1e-10
        assert min(delta) >= -1e-10
        assert max(delta) <= math.pi**2*U**2*np.linalg.norm(q)**2/(8*ell**4*lam)+1e-10
        energy = theta @ lap @ theta
        assert abs(-theta@q-sum((-lap[i,j])*v[i]*v[j]*(theta[i]-theta[j])*math.sin(theta[i]-theta[j]) for i,j in edges)) < 1e-9
        profiles += 1
print('PASS: symbolic rectangular signs;', pairs, 'integer-phasor crossing comparisons;', profiles, 'independent complex-power/stability profiles, including long real-angle path ramps.')
