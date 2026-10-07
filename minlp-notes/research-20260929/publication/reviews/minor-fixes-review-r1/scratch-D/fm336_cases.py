"""Group D: sanity check of the fm336 / tiny2 exact-optimum case arguments.
Exact part: the case inequalities with Fractions. Float part: grid brute force per binary
assignment of fm336 (q_i set to their largest allowed values, w_i to their smallest)."""
from fractions import Fraction as Q
import itertools, numpy as np
opt = Q(187, 270)
print('b1=1 bound 0.2+0.614125 =', Q('0.2') + Q('0.614125'), '>', opt, Q('0.2') + Q('0.614125') > opt)
print('b0=1 bound 5*0.343 =', 5 * Q('0.343'), '>', opt, 5 * Q('0.343') > opt)
print('b0=b1=0: q0 <= 3*0.7-2.1 =', 3 * Q('0.7') - Q('2.1'), '; q1 <= 2*0.85-1.7 =', 2 * Q('0.85') - Q('1.7'),
      '; b2=0: q2 <= 3*0.6-1.8 =', 3 * Q('0.6') - Q('1.8'))
s2 = (Q('0.5') + Q('1.8') - Q('0.3')) / 3
print('b2=1: s2 >= (0.5+1.8-0.3)/3 =', s2, '; cost >= 0.1 + 2*s2^3 =', Q('0.1') + 2 * s2**3, '== opt', Q('0.1') + 2 * s2**3 == opt)
print('p1 fixed 0.614125 = 0.85^3:', Q('0.85')**3 == Q('0.614125'))
# tiny2: b=1, min over s in [0.7,1] of 0.2-2.4s+s^3 is at s=sqrt(0.8); value 0.2-1.6 sqrt(0.8) > -1.337 iff 0.8 < (1.537/1.6)^2
print('tiny2: 0.8 < (1.537/1.6)^2:', Q('0.8') < (Q('1.537') / Q('1.6'))**2, '; float value', 0.2 - 1.6 * 0.8**0.5,
      '; b=0 forces s=0.7: obj', -Q('2.4') * Q('0.7') + Q('0.343'))
# float brute force fm336
best = {}
g0 = np.linspace(0.7, 1.0, 3001); g2 = np.linspace(0.6, 1.0, 4001)
for b0, b1, b2 in itertools.product([0, 1], repeat=3):
    s0 = g0[g0 <= 0.7 + 0.3 * b0 + 1e-12]; s2v = g2[g2 <= 0.6 + 0.4 * b2 + 1e-12]
    s1 = 0.85  # p1 fixed at 0.614125 = 0.85^3
    if s1 > 0.85 + 0.15 * b1 + 1e-12: continue
    q1 = max(0.0, min(1.0, 2 * s1 + 0.3 * b1 - 1.7)) if 2 * s1 + 0.3 * b1 - 1.7 > -1e-9 else -1.0
    S0, S2 = np.meshgrid(s0, s2v, indexing='ij')
    q0 = np.minimum(1.0, 3 * S0 + 0.3 * b0 - 2.1); q2 = np.minimum(0.5, 3 * S2 + 0.3 * b2 - 1.8)
    feas = (q0 >= -1e-9) & (q2 >= -1e-9) & (q1 >= -1e-9) & (np.maximum(q0,0) + q1 + np.maximum(q2,0) >= 0.5 - 1e-12)
    cost = 0.2 * b1 + 0.1 * b2 + 5 * np.maximum(0, S0**3 + b0 - 1) + 1 * max(0, s1**3 + b1 - 1) + 2 * np.maximum(0, S2**3 + b2 - 1)
    best[(b0, b1, b2)] = float(cost[feas].min()) if feas.any() else None
print('fm336 float grid min per (b0,b1,b2):', best)
print('overall', min(v for v in best.values() if v is not None), 'vs 187/270 =', float(opt))
