"""Exact gaps of the successive waterno2_06 certificates and ratios to the listed duals (dossier check)."""
from fractions import Fraction as F
import math
P6 = F('282888037386904807969455615812871') / 10**30
D = {'wave2': F(148469661946242564611253309, 562949953421312000000000),
     'cert2': F(38164240025509421, 140737488355328), 'cert3': F(19181443079783745, 70368744177664),
     'certA': F(2437338627747397, 8796093022208), 'certB': F(39157472136693483, 140737488355328)}
up = lambda x, d: math.ceil(x * 10**d) / 10**d
dn = lambda x, d: math.floor(x * 10**d) / 10**d
for k, d in D.items():
    g = (P6 - d) / d * 100
    print(f'06 {k}: dual (truncated) {dn(d, 9):.9f}  gap/dual {float(g):.5f}% (<= {up(g, 2):.2f}%)  abs gap {float(P6 - d):.6f}')
L = F('165.1902989'); W = D['wave2']; B = D['certB']
print('certB closes this share of (primal - best listed dual):', float((B - L) / (P6 - L)))
print('certB closes this share of the wave-2 gap:', float((B - W) / (P6 - W)))
listed = {6: ('165.1902989', '282.8880374'), 9: ('273.8958303', '922.5952898'), 12: ('479.5051427', '2263.358374'),
          18: ('770.7361733', '5269.638815'), 24: ('1095.126488', '7332.721691')}
ours = {6: B, 9: F(3627661341387654598825371, 4398046511104000000000), 12: F(9190837775594918144252281, 4398046511104000000000),
        18: F(5267563083146225483626937, 1099511627776000000000), 24: F(115688878681251187594323079, 17592186044416000000000)}
for T, (ld, lp) in listed.items():
    ld, lp = F(ld), F(lp)
    print(f'T={T}: ratio ours/listed dual {float(ours[T] / ld):.4f}; listed gap/dual {float((lp - ld) / ld * 100):.2f}%')
