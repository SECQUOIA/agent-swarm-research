"""R1-math: checks of Theorem 6.2 (via measure LP and exact appendix certificates),
Theorem 6.3 (alternation vs moment-matching LP), Prop 6.4, Cor 6.5 example."""
from fractions import Fraction as Fr
import random, itertools
import numpy as np
from scipy.optimize import linprog
random.seed(3)

def dist2(y, S): return min((y-s)**2 for s in S)

def glued_min(A, C, l, u, N=600):
    ys = np.linspace(float(l), float(u), N+1)
    ys = np.unique(np.concatenate([ys, [float(a) for a in A], [float(c) for c in C]]))
    n = len(ys)
    cA = np.array([dist2(y, [float(a) for a in A]) for y in ys])
    cC = np.array([dist2(y, [float(c) for c in C]) for y in ys])
    c = np.concatenate([cA, cC])
    Aeq = np.zeros((4, 2*n)); beq = np.zeros(4)
    Aeq[0, :n] = 1; beq[0] = 1
    Aeq[1, n:] = 1; beq[1] = 1
    Aeq[2, :n] = ys; Aeq[2, n:] = -ys
    Aeq[3, :n] = ys**2; Aeq[3, n:] = -ys**2
    res = linprog(c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs')
    return res.fun

def classify(A, C):
    a1, a2 = sorted(A); c1, c2 = sorted(C)
    if set(A) & set(C): return 'touch'
    pts = sorted([(a,'A') for a in A] + [(c,'C') for c in C])
    labs = [p[1] for p in pts]
    if labs in (['A','C','A','C'], ['C','A','C','A']): return 'interleave'
    if labs in (['A','A','C','C'], ['C','C','A','A']): return 'separated'
    return 'nested'

maxerr = 0
for trial in range(150):
    A = random.sample(range(0, 13), 2); C = random.sample(range(0, 13), 2)
    A = [Fr(a, 4) for a in A]; C = [Fr(c, 4) for c in C]
    l, u = Fr(0), Fr(3)
    delta = min(abs(s-t) for s in A for t in C)
    cls = classify(A, C)
    val = glued_min(A, C, l, u)
    expect = 0 if cls in ('touch', 'interleave') else float(delta**2/2)
    maxerr = max(maxerr, abs(val - expect))
    if abs(val-expect) > 1e-6: print("MISMATCH", A, C, cls, val, expect)
print("Theorem 6.2(ii) LP check max error:", maxerr)

# exact appendix certificates
def inf_quad(alpha, beta, s, m):  # inf_y alpha(y-s)^2 + beta(y-m)^2
    assert alpha + beta > 0
    return alpha*beta*(s-m)**2/(alpha+beta)

bad = 0
for trial in range(2000):
    vals = random.sample(range(-20, 21), 4)
    A = [Fr(v, random.randint(1,5)) for v in vals[:2]]; C = [Fr(v, random.randint(1,5)) for v in vals[2:]]
    if set(A) & set(C) or A[0]==A[1] or C[0]==C[1]: continue
    cls = classify(A, C)
    delta = min(abs(s-t) for s in A for t in C)
    if cls == 'separated':
        if max(A) > min(C): A, C, sgn = C, A, -1
        a0, g0 = max(A), min(C); d = g0 - a0; m0 = (a0+g0)/2
        assert d == delta
        # (y-s)^2 - d(y-m0): min at y = s + d/2
        kA = min(((s + d/2) - s)**2 - d*((s + d/2) - m0) for s in A)
        kC = min(((t - d/2) - t)**2 + d*((t - d/2) - m0) for t in C)
        if kA < d*d/4 or kC < d*d/4: bad += 1
    elif cls == 'nested':
        if not (min(A) < min(C) and max(C) < max(A)): A, C = C, A
        m = (min(C)+max(C))/2; R0 = (max(C)-min(C))/2; r = delta + R0
        assert all(abs(s-m) >= r for s in A) and all(abs(t-m) <= R0 for t in C)
        g = (r-R0)/(r+R0)
        kA = min(inf_quad(1, g, s, m) for s in A)
        kC = min(inf_quad(1, -g, t, m) for t in C)
        if kA + kC < delta**2/2: bad += 1
        if g*r*r/(1+g) - g*R0*R0/(1-g) != delta**2/2: bad += 1
print("appendix A.2 certificate failures:", bad)

# Theorem 6.3 random check: alt(A,C) >= k+1  <=>  measures with equal moments 1..k exist
def alt(A, C):
    pts = sorted([(a, 0) for a in A] + [(c, 1) for c in C])
    runs = 1
    for i in range(1, len(pts)):
        if pts[i][1] != pts[i-1][1]: runs += 1
    return runs - 1

def moment_feasible(A, C, k):
    A = [float(a) for a in A]; C = [float(c) for c in C]
    nA, nC = len(A), len(C)
    rows = []; rhs = []
    rows.append([1]*nA + [0]*nC); rhs.append(1)
    rows.append([0]*nA + [1]*nC); rhs.append(1)
    for p in range(1, k+1):
        rows.append([a**p for a in A] + [-c**p for c in C]); rhs.append(0)
    # maximize min weight slack to detect feasibility robustly: just feasibility
    res = linprog(np.zeros(nA+nC), A_eq=np.array(rows), b_eq=np.array(rhs), bounds=(0, None), method='highs')
    return res.status == 0

mism = 0; cnt = 0
for trial in range(1500):
    tot = random.randint(2, 7)
    pts = random.sample(range(-6, 7), tot)
    na = random.randint(1, tot-1)
    A, C = pts[:na], pts[na:]
    for k in range(1, 6):
        cnt += 1
        if (alt(A, C) >= k+1) != moment_feasible(A, C, k):
            mism += 1; print("alt mismatch", A, C, k, alt(A, C))
print("Theorem 6.3 checks:", cnt, "mismatches:", mism)

# Prop 6.4
for r in (1, 2, 3):
    A = sorted(set(sum(2**j for j in J) for n in range(r+1) for J in itertools.combinations(range(1, r+1), n)))
    C = [a+1 for a in A]
    assert A == list(range(0, 2**(r+1)-1, 2)), A
    # min over y in [0, 2^{r+1}-1] of dist^2(y,A)+dist^2(y,C) is 1/2
    from math import comb
    mn = min(min((y-s)**2 + (y-t)**2 for s in A for t in C) for y in [Fr(i, 4) for i in range(0, 4*(2**(r+1)-1)+1)])
    for k in range(1, 2**(r+1)-1):
        w = [Fr(comb(k+1, i), 2**k) for i in range(k+2)]
        ev = sum(w[i] for i in range(0, k+2, 2)); od = sum(w[i] for i in range(1, k+2, 2))
        assert ev == 1 and od == 1
        for p in range(0, k+1):
            assert sum(w[i]*i**p for i in range(0, k+2, 2)) == sum(w[i]*i**p for i in range(1, k+2, 2))
        # order k+1 should differ
        assert sum(w[i]*i**(k+1) for i in range(0, k+2, 2)) != sum(w[i]*i**(k+1) for i in range(1, k+2, 2))
    print("Prop 6.4 r=%d: A=%s, min=%s, binomial weights ok up to k=%d" % (r, A[:6], mn, 2**(r+1)-2))

# Prop 6.4 multilinearity check symbolic r=2
import sympy as sp
y = sp.symbols('y'); xs = sp.symbols('x1 x2')
DL = (y - sum(2**(j+1)*xs[j] for j in range(2)))**2 + sum(4**(j+1)*xs[j]*(1-xs[j]) for j in range(2))
print("D_L x_j^2 coefficients:", [sp.Poly(sp.expand(DL), *xs).coeff_monomial(xs[j]**2) for j in range(2)])

# Cor 6.5 example A={0,3}, C={1,2} on [0,3]
A, C = [0, 3], [1, 2]
print("nested example glued min:", glued_min(A, C, 0, 3), " Delta (beta* - 0):",
      min(min((yy-s)**2 + (yy-t)**2 for s in A for t in C) for yy in [Fr(i, 8) for i in range(25)]))
