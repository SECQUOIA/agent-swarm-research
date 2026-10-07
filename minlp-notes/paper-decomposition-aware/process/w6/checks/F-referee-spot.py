# F-referee spot checks (targeted, numeric/exact). Run: python3 F-referee-spot.py
import math
from fractions import Fraction as Fr

ok = True
# 1. Lemma lem:states radius constant and cap K(theta,n_P)=10/theta*ceil(log2(n_P+2))
c = 3 + 2*math.sqrt(17/15) + (2+math.sqrt(17/15))/math.sqrt(2)
print("radius constant", c, c < 7.3); ok &= c < 7.3
worst = 0.0
for mu in range(2, 31):
    th = 2.0**-mu
    for nP in list(range(1, 2000)) + [10**k for k in range(4, 13)]:
        need = 1 + 2*math.ceil((4/th)*math.log(1.25 + 4*math.sqrt(2*nP)))
        cap = 10/th*math.ceil(math.log2(nP+2))
        worst = max(worst, need/cap)
print("max need/cap over grid", worst); ok &= worst <= 1
# 2. Theorem thm:approx(b): 2^{mu*} <= 6 sqrt(kbar), mu*=max{2,ceil(log4(8 kbar))}
w = 0
for i in range(1, 200001):
    kb = 1 + i/1000.0
    mu = max(2, math.ceil(math.log(8*kb, 4) - 1e-12))
    w = max(w, 2**mu/math.sqrt(kb))
print("max 2^mu*/sqrt(kbar)", w); ok &= w <= 6
# 3. eq:logabsorb ceil(log2(n+2))^p <= 2 p^p (n+2)
bad = [(n, p) for n in range(1, 3000) for p in range(1, 25)
       if math.ceil(math.log2(n+2))**p > 2*p**p*(n+2)]
print("logabsorb violations", bad[:5]); ok &= not bad
# 4. Lemma tu-uniform: (sqrt(2(n-2))+1)^p >= n^{p/2} for even n>=4
bad = [n for n in range(4, 10**5, 2) if math.sqrt(2*(n-2))+1 < math.sqrt(n)]
print("tu-uniform violations", bad[:5]); ok &= not bad
# 5. Section 3 example F=(x1-x2)^2+2^{-k}x1^2: kappa>=2^{k+2}, kbar>2^{k+2}
for k in range(1, 30):
    L1, L2 = 2 + Fr(2, 2**k), Fr(2)
    g = Fr(1, 2**(k+1)); gam = Fr(1, 2**k)/(L1+L2)
    ok &= (L2/g >= 2**(k+2)) and (1/gam > 2**(k+2))
print("setting example ok", ok)
# 6. Remark rem:cf: snapping weaker iff R^2 >= 2 n^2  (g/(64 n^2 R^2) >= g/(32 R^4))
for n in range(1, 50):
    for R in range(1, 200):
        a = Fr(1, 64*n*n*R*R) >= Fr(1, 32*R**4)
        ok &= (a == (R*R >= 2*n*n))
print("rem:cf ok", ok)
# 7. Thm tu-exact J_ex: E_j <= g tau^2/(4 n_c) follows from 2^j >= eta n_c sqrt(kappa_c)/tau
import random
random.seed(1)
for _ in range(20000):
    nc = random.randint(1, 50); Lb = Fr(random.randint(1, 100), random.randint(1, 100))
    gS = Fr(random.randint(1, 100), random.randint(1, 1000)); eta = Fr(1, random.randint(1, 8))
    tau = Fr(1, random.randint(1, 10**6)); kc = max(Fr(1), Lb/gS)
    # least j with 2^j >= eta*nc*sqrt(kc)/tau  (use sqrt upper bound via float then verify exactly)
    j = 0
    while Fr(4**j)*tau*tau < eta*eta*nc*nc*kc: j += 1
    Ej = nc*Lb*(eta/2**j)**2/8
    ok &= Ej <= gS*tau*tau/(4*nc)
print("tu-exact J_ex ok", ok)
print("ALL OK" if ok else "FAILURE")
